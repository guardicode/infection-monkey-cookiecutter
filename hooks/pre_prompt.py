import json
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console


def prompt_for_generic_or_plugin():
    console = Console()
    console.print("  [dim][0/0][/] What type of project do you want to create?")
    console.print("    [bold magenta]1[/bold magenta] - [bold]Generic[/bold]")
    console.print("    [bold magenta]2[/bold magenta] - [bold]Plugin[/bold]")
    choice = Prompt.ask(
        "    Choose from ",
        choices=["1", "2"],
        default="1",
    )
    return choice


def extend_default_cookiecutter(data):
    project_type = prompt_for_generic_or_plugin()

    if project_type == "2":
        data["__project_type"] = "plugin"
        cookiecutter_plugin_config_path = Path("cookiecutter_plugin.json")
        if cookiecutter_plugin_config_path.exists():
            plugin_config = json.loads(cookiecutter_plugin_config_path.read_text())
            plugin_config.update(data)

            data.clear()
            data.update(plugin_config)


def main():
    cookiecutter_config_path = Path("cookiecutter.json")
    if not cookiecutter_config_path.exists():
        return

    data = json.loads(cookiecutter_config_path.read_text())
    try:
        extend_default_cookiecutter(data)
    except KeyboardInterrupt:
        return
    cookiecutter_config_path.write_text(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
