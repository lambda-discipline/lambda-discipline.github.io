# Contributing to the Lambda Discipline website

Thanks for helping! Fixes to wording, new pages, better examples and design
improvements are all welcome. By taking part you agree to follow the
[Code of Conduct](CODE_OF_CONDUCT.md).

This repository is the website only. Bugs in the language or the `lbd`
interpreter belong in the
[language repository](https://github.com/lambda-discipline/lambda-discipline/issues).
Some of the site comes from there, too:

* the [builtin reference](https://lambda-discipline.github.io/builtins/) is
  generated from `lbd docs --json`, so builtin descriptions are fixed in the
  `builtins!` table in the language's `src/builtins.rs`;
* the [examples](https://lambda-discipline.github.io/examples/) are `.lbd`
  files from the language repository, so a new example goes there first and
  is then listed in `site.toml` here.

## Reporting issues

Open an issue with the matching template: a broken page or link, a mistake in
the docs, or an idea for the site. Include the page URL. For security
problems, see [SECURITY.md](SECURITY.md) instead.

## Development setup

You need Python 3.11 or newer, Git, and Rust 1.85 or newer to build `lbd`.

```bash
python -m venv .venv
```

```bash
.venv/bin/pip install -r requirements-dev.txt
```

On Windows the scripts are in `.venv\Scripts\` instead of `.venv/bin/`.

Build the site and preview it:

```bash
python build.py
```

```bash
python -m http.server -d _site
```

`build.py` clones the language repository into `.cache/`, builds `lbd` and
writes `_site/`. If you already have a checkout of the language, use it as is
with `--repo ../lambda-discipline`, and skip the Cargo build with
`--lbd path/to/lbd`. See [README.md](README.md) for every option and for how
the repository is laid out.

Optional but recommended: install the [pre-commit](https://pre-commit.com)
hooks, which format and check your changes before each commit.

```bash
pre-commit install
```

## Writing pages

* Pages are Markdown in `content/`, with `title` and `description` front
  matter. Mark Lambda Discipline code blocks with `lbd` so they are
  highlighted.
* Keep the tone plain and precise. Every code sample should run, and its
  comments should show what it really prints: check them with `lbd run`.
* Link to other pages with root-relative paths such as `/reference/#types`.
  The link checker verifies them, including the `#fragment`.

## Before you open a pull request

Everything CI checks can be run locally:

```bash
black --check .
```

```bash
ruff check .
```

```bash
mypy
```

```bash
python build.py
```

```bash
lychee --offline --root-dir "$PWD/_site" _site
```

Drop `--offline` to check external links too. Look at the pages you changed
in a browser, in both light and dark mode and at phone width.

## Commit messages

Use `prefix: summary`, with the summary in lowercase and the imperative mood,
for example `docs: explain let-polymorphism`. Common prefixes are `feat`,
`fix`, `docs`, `style`, `refactor`, `ci`, `deps` and `chore`. Explain why in
the body when it isn't obvious.
