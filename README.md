# infection-monkey-cookiecutter
A cookiecutter template used for Infection Monkey-related projects

## Commit message hooks (`hook_gitlint`)

`hook_gitlint` (on by default) adds the `gitlint` hook of
[gitlint-commit-hook](https://github.com/adamdelman/gitlint-commit-hook) to the generated
`.pre-commit-config.yaml`. The rules it enforces and their tests live in that repo.

Two optional checks build on it, both off by default, passed to the hook as `args`:

- `require_jira_prefix`: the subject must start with a Jira key, e.g. `OCPSG-123: `.
- `require_pr_number_on_merge`: merges into `master`, `main`, `dev` or `develop` must contain a PR
  number (`#123`). Fast-forward merges create no commit, so they can't be checked.

To turn any of them on in an existing project:

```bash
cruft update --variables-to-update '{"hook_gitlint": true, "require_jira_prefix": true}'
```

cruft doesn't update `README.md`, so copy the "Development setup" and "Commit messages" sections
from a newly generated project into the project's README. Each developer then runs
`pre-commit install` once in each clone.

## Testing

The tests check the rendered `hook_gitlint` output. Run them from the repo root:

```bash
pip install cookiecutter pytest pyyaml
pytest tests
```
