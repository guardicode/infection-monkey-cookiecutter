import subprocess
import tomllib
from pathlib import Path

import pytest
import yaml
from cookiecutter.main import cookiecutter

TEMPLATE_DIR = Path(__file__).parent.parent
RUFF_REPO = "https://github.com/astral-sh/ruff-pre-commit"
LEGACY_REPOS = {
    "https://github.com/psf/black",
    "https://github.com/PyCQA/flake8",
    "https://github.com/pycqa/isort",
}
LEGACY_TOOLS = {"black", "dlint", "flake8", "isort"}


def render(output_dir: Path, **context: object) -> Path:
    return Path(
        cookiecutter(
            str(TEMPLATE_DIR),
            no_input=True,
            accept_hooks=False,
            output_dir=str(output_dir),
            extra_context={"project_name": "demo", **context},
        )
    )


def repo_urls(project: Path) -> set[str]:
    config = yaml.safe_load((project / ".pre-commit-config.yaml").read_text())
    return {repo["repo"] for repo in config["repos"]}


def pyproject(project: Path) -> dict:
    return tomllib.loads((project / "pyproject.toml").read_text())


def dev_dependencies(project: Path) -> set[str]:
    return set(pyproject(project)["tool"]["poetry"]["group"]["dev"]["dependencies"])


def test_hook_ruff__off_by_default(tmp_path: Path) -> None:
    project = render(tmp_path)
    tool = pyproject(project)["tool"]

    assert LEGACY_REPOS <= repo_urls(project)
    assert RUFF_REPO not in repo_urls(project)
    assert (project / ".flake8").exists()
    assert {"black", "isort"} <= tool.keys()
    assert "ruff" not in tool
    assert LEGACY_TOOLS <= dev_dependencies(project)
    assert "ruff" not in dev_dependencies(project)


def test_hook_ruff__on(tmp_path: Path) -> None:
    project = render(tmp_path, hook_ruff=True)
    tool = pyproject(project)["tool"]

    assert RUFF_REPO in repo_urls(project)
    assert not LEGACY_REPOS & repo_urls(project)
    assert not (project / ".flake8").exists()
    assert not {"black", "isort"} & tool.keys()
    assert tool["ruff"]["force-exclude"] is True
    assert tool["ruff"]["lint"]["isort"]["known-first-party"] == ["demo"]
    assert "ruff" in dev_dependencies(project)
    assert not LEGACY_TOOLS & dev_dependencies(project)


def test_hook_ruff__versions(tmp_path: Path) -> None:
    project = render(tmp_path, hook_ruff=True, _ruff_version="1.2.3")
    config = yaml.safe_load((project / ".pre-commit-config.yaml").read_text())
    (repo,) = [repo for repo in config["repos"] if repo["repo"] == RUFF_REPO]

    assert repo["rev"] == "v1.2.3"
    assert pyproject(project)["tool"]["poetry"]["group"]["dev"]["dependencies"]["ruff"] == "1.2.3"


@pytest.mark.parametrize(
    "excluded, expected",
    [
        ("vulture_allowlist.py", ["vulture_allowlist.py"]),
        ("a.py, b/*.py", ["a.py", "b/*.py"]),
        ("", []),
    ],
    ids=["default", "multiple", "empty"],
)
def test_hook_ruff__excludes(tmp_path: Path, excluded: str, expected: list[str]) -> None:
    project = render(tmp_path, hook_ruff=True, exclude_these_file_in_flake8=excluded)
    assert pyproject(project)["tool"]["ruff"]["extend-exclude"] == expected


def test_flake8__excludes_unquoted(tmp_path: Path) -> None:
    project = render(tmp_path, exclude_these_file_in_flake8="a.py,b.py")
    assert "exclude = a.py,b.py\n" in (project / ".flake8").read_text()


def test_hook_ruff__generated_project_passes(tmp_path: Path) -> None:
    """Files are passed by name, as pre-commit does, so excluded files must stay excluded."""
    project = render(tmp_path, hook_ruff=True)
    (project / "vulture_allowlist.py").write_text("undefined_name\n")
    python_files = [str(path.relative_to(project)) for path in project.rglob("*.py")]

    for command in (["ruff", "check", *python_files], ["ruff", "format", "--check", *python_files]):
        result = subprocess.run(command, check=False, cwd=project, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr
