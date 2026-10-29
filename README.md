# infection-monkey-cookiecutter
A cookiecutter template used for Infection Monkey-related projects

## Commit message hooks (`hook_gitlint`)

`hook_gitlint` adds gitlint checks for the commit message rules at
https://cbea.ms/git-commit that a linter can enforce: a blank line after the subject, a subject of
at most 50 characters that is capitalized, imperative and doesn't end with a period, and a body
wrapped at 72 characters.
Merge commits are not checked. It is on by default.

Two optional checks build on it, both off by default:

- `require_jira_prefix`: the subject must start with a Jira key, e.g. `OCPSG-123: `.
- `require_pr_number_on_merge`: merges into `master`, `main`, `dev` or `develop` must contain a PR number
  (`#123`). Fast-forward merges create no commit, so they can't be checked.

To turn any of them on in an existing project:

```bash
cruft update --variables-to-update '{"hook_gitlint": true, "require_jira_prefix": true}'
```

cruft doesn't update `README.md`, so copy the "Development setup" and "Commit messages" sections
from a newly generated project into the project's README. Each developer then runs
`pre-commit install` once in each clone.

## Testing

The tests cover the `hook_gitlint` commit hooks. Run them from the repo root:

```bash
pip install cookiecutter gitlint pydocstyle pytest
pytest tests
```
