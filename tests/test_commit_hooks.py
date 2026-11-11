from pathlib import Path

import pytest
import yaml
from cookiecutter.main import cookiecutter

TEMPLATE_DIR = Path(__file__).parent.parent
HOOK_REPO = "https://github.com/adamdelman/gitlint-commit-hook"


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


def gitlint_repos(project: Path) -> list[dict]:
    config = yaml.safe_load((project / ".pre-commit-config.yaml").read_text())
    return [repo for repo in config["repos"] if repo["repo"] == HOOK_REPO]


def test_hook_gitlint__on_by_default(tmp_path: Path) -> None:
    project = render(tmp_path)
    (repo,) = gitlint_repos(project)
    assert [hook["id"] for hook in repo["hooks"]] == ["gitlint"]
    assert "commit-msg" in (project / ".pre-commit-config.yaml").read_text().splitlines()[1]
    assert not (project / ".gitlint").exists()
    assert not (project / ".commit_hooks").exists()


@pytest.mark.parametrize(
    "context, args",
    [
        ({}, None),
        ({"require_jira_prefix": True}, ["--require-jira-prefix"]),
        ({"require_pr_number_on_merge": True}, ["--require-pr-number-on-merge"]),
        (
            {"require_jira_prefix": True, "require_pr_number_on_merge": True},
            ["--require-jira-prefix", "--require-pr-number-on-merge"],
        ),
    ],
    ids=["none", "jira", "pr-number", "both"],
)
def test_hook_gitlint__options_become_args(
    tmp_path: Path, context: dict[str, bool], args: list[str] | None
) -> None:
    (repo,) = gitlint_repos(render(tmp_path, **context))
    assert repo["hooks"][0].get("args") == args


def test_hook_gitlint__off(tmp_path: Path) -> None:
    project = render(tmp_path, hook_gitlint=False)
    assert gitlint_repos(project) == []
    assert "gitlint" not in (project / ".pre-commit-config.yaml").read_text()
    assert "gitlint" not in (project / "pyproject.toml").read_text()
