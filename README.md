# lambda-discipline.github.io

[![CI](https://github.com/lambda-discipline/lambda-discipline.github.io/actions/workflows/ci.yml/badge.svg)](https://github.com/lambda-discipline/lambda-discipline.github.io/actions/workflows/ci.yml)
[![Deploy](https://github.com/lambda-discipline/lambda-discipline.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/lambda-discipline/lambda-discipline.github.io/actions/workflows/deploy.yml)

The website for [Lambda Discipline](https://github.com/lambda-discipline/lambda-discipline),
served at <https://lambda-discipline.github.io>.

`build.py` turns the pages in `content/` and the language repository into a
static site in `_site/`:

* the [builtin reference](https://lambda-discipline.github.io/builtins/) comes
  from `lbd docs --json`;
* every `.lbd` file under the repository's `examples/`, plus the golden test
  programs listed in `site.toml`, becomes an example page with the output the
  current `lbd` prints for it.

## Building

You need Python 3.11+ and, unless you pass `--lbd`, Rust to build `lbd`.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt   # .venv\Scripts\pip on Windows; requirements-dev.txt for the checks
```

```bash
python build.py
```

clones the language repository into `.cache/` (or fast-forwards it), builds
`lbd` with `cargo build --release`, and writes `_site/`. Options:

| Option | What it does |
| --- | --- |
| `--repo PATH` | Use an existing checkout as it is instead of `.cache/`. |
| `--no-update` | Don't pull the cached clone. |
| `--lbd PATH` | Use this `lbd` binary instead of building one. |
| `--out PATH` | Write the site somewhere other than `_site/`. |

Preview it with:

```bash
python -m http.server -d _site
```

## Layout

| Path | What it holds |
| --- | --- |
| `content/*.md` | Pages, with `title`, `description` and optional `template` front matter. `index.md` is the home page; every other file becomes `/<name>/`. |
| `templates/` | Jinja2 templates. `builtins.html`, `examples.html` and `example.html` render the generated pages. |
| `static/` | Copied to the site as is: the stylesheet and the λ logo. |
| `site.toml` | Navigation, the upstream repository, and which examples to show in what order. |
| `lbd_lexer.py` | The Pygments lexer used to highlight Lambda Discipline code. |

In Markdown pages, fenced code blocks marked `lbd` are highlighted with that
lexer, and `[TOC]` inserts a table of contents.

## Deployment

`.github/workflows/deploy.yml` builds the site and publishes it with GitHub
Pages (Settings → Pages → Source: GitHub Actions). It runs on every push to
`master`, on demand, and once a day. The daily run compares the language
repository's latest commit with the one recorded in the live site's
`/build.json`, and only rebuilds when they differ.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup and the
checks CI runs (black, ruff, mypy, and lychee for links). Please follow the
[Code of Conduct](CODE_OF_CONDUCT.md), and report vulnerabilities as described
in [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE.txt)
