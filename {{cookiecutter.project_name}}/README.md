# {{ cookiecutter.project_name | replace('-', ' ') | replace('_', ' ') }}
{%- if cookiecutter.hook_gitlint %}

## Development setup

Install [pre-commit](https://pre-commit.com) once per machine, then enable the hooks in each clone:

```bash
pipx install pre-commit   # or: brew install pre-commit
pre-commit install        # installs the pre-commit, prepare-commit-msg and commit-msg hooks
```

If `pre-commit install` refuses because `core.hooksPath` is set (e.g. by the old commit-guard tool),
remove the global hook path first:

```bash
git config --global --unset core.hooksPath
```

## Commit messages

Commit messages follow [How to Write a Git Commit Message](https://cbea.ms/git-commit), as far as
a linter can check:

- Separate the subject from the body with a blank line.
- Keep the subject at most 72 characters long.
- Capitalize the subject.
- Don't end the subject with a period.
- Use the imperative mood in the subject (`Add`, not `Added` or `Adds`).
- Wrap the body at 72 characters.

```text
Add map writer

Explain what changed and why, not how.
```

{%- if cookiecutter.require_jira_prefix %}

The subject also starts with a Jira key, e.g. `OCPSG-123: Add map writer`.
{%- endif %}
{%- if cookiecutter.require_pr_number_on_merge %}

Merging a branch into `master`, `main`, `dev` or `develop` needs a PR number (`#123`) in the merge
message. GitHub's merge button adds it for you. Merges into other branches and `git pull` merges
don't need one. A fast-forward makes no commit, so it can't be checked; use `git merge --no-ff`.
{%- endif %}

Fixups, squashes, amends and `git revert` commits are not checked.
{%- if not cookiecutter.require_pr_number_on_merge %} Neither are merges.{% endif %} The rules come
from [gitlint-commit-hook](https://github.com/adamdelman/gitlint-commit-hook).
{%- endif %}
