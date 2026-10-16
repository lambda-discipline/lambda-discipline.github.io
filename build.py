#!/usr/bin/env python3
"""Builds the Lambda Discipline website into _site/.

The builtin reference and the examples come from the language repository:
the builtins from `lbd docs --json`, the examples from its `.lbd` files, run
through `lbd` so each page shows the program's real output.

    python build.py                      clone or update the repo in .cache/, build lbd
    python build.py --repo ../lambda-discipline-rust   use an existing checkout as is
    python build.py --lbd path/to/lbd    skip `cargo build` and use this binary
"""

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TypedDict

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from lbd_lexer import LbdLexer

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache" / "lambda-discipline"


class BuiltinDoc(TypedDict):
    """One builtin, as `lbd docs --json` describes it."""

    name: str
    signature: str
    arity: int
    variadic: bool
    doc: str


class ModuleDoc(TypedDict):
    name: str
    title: str
    builtins: list[BuiltinDoc]


class Reference(TypedDict):
    version: str
    modules: list[ModuleDoc]


class Example(TypedDict):
    title: str
    url: str
    path: str
    source_url: str
    summary: str
    source: str
    output: str


def main() -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument(
        "--repo", type=Path, help="use this checkout instead of cloning"
    )
    parser.add_argument(
        "--no-update", action="store_true", help="don't pull the cached clone"
    )
    parser.add_argument(
        "--lbd", type=Path, help="lbd binary to use instead of building one"
    )
    parser.add_argument(
        "--out", type=Path, default=ROOT / "_site", help="output directory"
    )
    args = parser.parse_args()

    config: dict[str, Any] = tomllib.loads(
        (ROOT / "site.toml").read_text(encoding="utf-8")
    )
    repo = (
        args.repo.resolve()
        if args.repo
        else fetch_repo(config["upstream"], update=not args.no_update)
    )
    lbd: Path = args.lbd.resolve() if args.lbd else build_lbd(repo)

    Site(config, repo, lbd, args.out.resolve()).build()


# --- The language repository -------------------------------------------------


def run(
    command: list[str | Path], cwd: Path | None = None, check: bool = True
) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(str(part) for part in command), file=sys.stderr)
    return subprocess.run(
        command, cwd=cwd, check=check, capture_output=True, text=True, encoding="utf-8"
    )


def fetch_repo(upstream: dict[str, str], update: bool) -> Path:
    """Clones the repository into .cache/, or fast-forwards an existing clone."""
    if not (CACHE / ".git").exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                upstream["branch"],
                upstream["repo"],
                CACHE,
            ]
        )
    elif update:
        run(["git", "fetch", "--depth", "1", "origin", upstream["branch"]], cwd=CACHE)
        run(["git", "reset", "--hard", "FETCH_HEAD"], cwd=CACHE)
    return CACHE


def build_lbd(repo: Path) -> Path:
    run(["cargo", "build", "--release", "--locked"], cwd=repo)
    name = "lbd.exe" if sys.platform == "win32" else "lbd"
    return repo / "target" / "release" / name


def commit_of(repo: Path) -> str | None:
    result = run(["git", "rev-parse", "HEAD"], cwd=repo, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


# --- Rendering ---------------------------------------------------------------


class Site:
    def __init__(self, config: dict[str, Any], repo: Path, lbd: Path, out: Path):
        self.config = config
        self.repo = repo
        self.lbd = lbd
        self.out = out
        self.reference: Reference = json.loads(run([lbd, "docs", "--json"]).stdout)
        self.builtin_names = {
            b["name"] for m in self.reference["modules"] for b in m["builtins"]
        }
        self.formatter: HtmlFormatter[str] = HtmlFormatter(nowrap=True)
        self.commit = commit_of(repo)
        self.urls: list[str] = []
        self.env = Environment(
            loader=FileSystemLoader(ROOT / "templates"),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["lbd"] = self.highlight_lbd  # type: ignore
        self.env.filters["inline_md"] = self.inline_markdown  # type: ignore
        self.env.globals.update(  # type: ignore
            site=config,
            upstream=config["upstream"]["repo"],
            commit=self.commit,
            version=self.reference["version"],
            year=datetime.now(UTC).year,
        )

    def build(self) -> None:
        # Empty the output directory rather than deleting it, so a preview
        # server running in it (which locks it on Windows) doesn't stop a build.
        for child in self.out.glob("*") if self.out.exists() else []:  # type: ignore
            shutil.rmtree(child) if child.is_dir() else child.unlink()  # type: ignore
        shutil.copytree(ROOT / "static", self.out, dirs_exist_ok=True)
        (self.out / ".nojekyll").write_text("")

        for path in sorted((ROOT / "content").glob("*.md")):
            self.render_markdown_page(path)
        self.render_builtins()
        self.render_examples()
        self.render_not_found()
        self.render_sitemap()

        # The deploy workflow compares this commit with upstream to decide
        # whether a scheduled run has anything new to publish.
        build_info: dict[str, Any] = {
            "commit": self.commit,
            "version": self.reference["version"],
            "built": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        self.write("build.json", json.dumps(build_info, indent=2) + "\n")
        print(f"built {self.out}", file=sys.stderr)

    def write(self, relative: str, text: str) -> None:
        path = self.out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def page(self, url: str, template: str, **context: Any) -> None:
        """Renders a template to the pretty URL `url` (`/` or `/name/`)."""
        html_text = self.env.get_template(template).render(current=url, **context)
        self.write(
            url.strip("/") + "/index.html" if url != "/" else "index.html", html_text
        )
        self.urls.append(url)

    def render_not_found(self) -> None:
        """GitHub Pages serves /404.html for any path that doesn't exist."""
        html_text = self.env.get_template("404.html").render(
            current="/404.html", title="Page not found"
        )
        self.write("404.html", html_text)

    def render_sitemap(self) -> None:
        base = self.config["url"]
        entries = "".join(
            f"  <url><loc>{html.escape(base + url)}</loc></url>\n" for url in self.urls
        )
        self.write(
            "sitemap.xml",
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{entries}</urlset>\n",
        )
        self.write(
            "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n"
        )

    # Highlighting and Markdown.

    def highlight_lbd(self, code: str) -> str:
        lexer = LbdLexer(builtins=self.builtin_names)
        return highlight(code, lexer, self.formatter).rstrip("\n")

    def highlight_block(self, code: str, language: str) -> str:
        if language == "lbd":
            body = self.highlight_lbd(code)
        else:
            try:
                body = highlight(
                    code, get_lexer_by_name(language), self.formatter
                ).rstrip("\n")
            except ClassNotFound:
                body = html.escape(code.rstrip("\n"))
        label = f' data-lang="{html.escape(language)}"' if language else ""
        return f'<pre class="code"{label}><code>{body}</code></pre>'

    def markdown(self, text: str) -> str:
        """Markdown with fenced code blocks highlighted by Pygments."""
        blocks: list[str] = []

        def stash(match: re.Match[str]) -> str:
            blocks.append(
                self.highlight_block(match.group("code"), match.group("lang") or "")
            )
            return f"\n\nCODEBLOCK{len(blocks) - 1}\n\n"

        text = re.sub(
            r"^```(?P<lang>[\w+-]*)[ \t]*\n(?P<code>.*?)^```[ \t]*$",
            stash,
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        rendered = markdown.markdown(
            text,
            extensions=["tables", "toc", "smarty"],
            extension_configs={"toc": {"permalink": "#", "toc_depth": "2-3"}},
        )
        return re.sub(
            r"<p>CODEBLOCK(\d+)</p>", lambda m: blocks[int(m.group(1))], rendered
        )

    def inline_markdown(self, text: str) -> str:
        rendered = markdown.markdown(text, extensions=["smarty"])
        return rendered.removeprefix("<p>").removesuffix("</p>")

    # Pages.

    def render_markdown_page(self, path: Path) -> None:
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        url = "/" if path.stem == "index" else f"/{path.stem}/"
        template = meta.get("template", "page.html")
        self.page(
            url,
            template,
            title=meta.get("title"),
            description=meta.get("description"),
            content=self.markdown(body),
        )

    def render_builtins(self) -> None:
        self.page(
            "/builtins/",
            "builtins.html",
            title="Builtins",
            description="Every builtin function, with its type and what it does.",
            modules=self.reference["modules"],
        )

    def render_examples(self) -> None:
        examples = [self.example(path) for path in self.example_paths()]
        for example in examples:
            self.page(
                example["url"],
                "example.html",
                title=example["title"],
                description=example["summary"],
                example=example,
            )
        self.page(
            "/examples/",
            "examples.html",
            title="Examples",
            description="Programs from the Lambda Discipline repository, with their output.",
            examples=examples,
        )

    def example_paths(self) -> list[Path]:
        settings = self.config["examples"]
        first = [self.repo / p for p in settings["first"]]
        rest = sorted(
            p for p in (self.repo / "examples").rglob("*.lbd") if p not in first
        )
        paths = first + rest + [self.repo / p for p in settings["extra"]]
        missing = [str(p) for p in paths if not p.exists()]
        if missing:
            sys.exit("missing examples (update site.toml): " + ", ".join(missing))
        return paths

    def example(self, path: Path) -> Example:
        relative = path.relative_to(self.repo).as_posix()
        source = path.read_text(encoding="utf-8")
        summary: str = self.config["examples"].get("summaries", {}).get(
            relative
        ) or first_sentence(leading_comment(source))
        # Examples read files relative to the repository root, the way the
        # repository's own tests run them.
        result = run([self.lbd, "run", relative], cwd=self.repo, check=False)
        if result.returncode != 0:
            sys.exit(f"{relative} failed:\n{result.stderr}")
        slug = re.sub(
            r"[^a-z0-9]+",
            "-",
            Path(relative)
            .with_suffix("")
            .as_posix()
            .removeprefix("examples/")
            .removeprefix("tests/golden/programs/")
            .lower(),
        ).strip("-")
        title: str = self.config["examples"].get("titles", {}).get(
            relative
        ) or humanize(path.stem)
        return {
            "title": title,
            "url": f"/examples/{slug}/",
            "path": relative,
            "source_url": f"{self.config['upstream']['repo']}/blob/{self.config['upstream']['branch']}/{relative}",
            "summary": summary,
            "source": source,
            "output": result.stdout,
        }


# --- Helpers -----------------------------------------------------------------


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    """`---`-delimited `key: value` lines at the top of a content file."""
    meta: dict[str, str] = {}
    if text.startswith("---\n"):
        header, _, text = text[4:].partition("\n---\n")
        for line in header.splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, text


def leading_comment(source: str) -> str:
    """The first line of the `--` comment a file starts with, if any."""
    first = source.lstrip().split("\n", 1)[0]
    return first[2:].strip() if first.startswith("--") else ""


def first_sentence(text: str) -> str:
    return re.split(r"(?<=\.)\s", text, maxsplit=1)[0]


def humanize(stem: str) -> str:
    words = stem.replace("_", " ").replace("-", " ").strip()
    return words[:1].upper() + words[1:]


if __name__ == "__main__":
    main()
