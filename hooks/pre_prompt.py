from typing import Any, Dict, Optional
import json
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console


def main():
    cookiecutter_config_path = Path("cookiecutter.json")
    if not cookiecutter_config_path.exists():
        return

    cookiecutter_json = json.loads(cookiecutter_config_path.read_text())
    try:
        extended_cookiecutter_json = extend_default_cookiecutter(cookiecutter_json)
    except KeyboardInterrupt:
        return

    if extended_cookiecutter_json:
        cookiecutter_config_path.write_text(
            json.dumps(extended_cookiecutter_json, indent=4)
        )


def extend_default_cookiecutter(
    cookiecutter_json: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Extend the default cookiecutter.json with additional plugin configuration.

    :param cookiecutter_json: The default cookiecutter.json
    :return: The extended cookiecutter.json with plugin configuration
    """
    context = """{{ cookiecutter | jsonify }}"""
    if "__project_type" in context:
        project_type = context["__project_type"]
    else:
        project_type = prompt_for_generic_or_plugin()

    cookiecutter_json["__project_type"] = project_type
    if project_type == "generic":
        return cookiecutter_json
    elif project_type == "agent_plugin":
        cookiecutter_plugin_config_path = Path("cookiecutter_plugin.json")
        if cookiecutter_plugin_config_path.exists():
            plugin_config = json.loads(cookiecutter_plugin_config_path.read_text())

            # We change the order of the prompts to ask for the plugin configuration first
            # after we choose the project type
            return {**plugin_config, **cookiecutter_json}


def prompt_for_generic_or_plugin() -> str:
    """
    Prompt the user to select the project type.
    :return: The selected project type. "1" for generic, "2" for agent plugin
    """
    console = Console()
    console.print("  [dim][0/0][/] What type of project do you want to create?")
    console.print("    [bold magenta]1[/bold magenta] - [bold]Generic[/bold]")
    console.print("    [bold magenta]2[/bold magenta] - [bold]Agent plugin[/bold]")
    choice = Prompt.ask(
        "    Choose from ",
        choices=["1", "2"],
        default="1",
    )
    return parse_choice(choice)


def parse_choice(choice: str) -> str:
    if choice == "1":
        return "generic"
    elif choice == "2":
        return "agent_plugin"
    return "unknown"


if __name__ == "__main__":
    main()
