"""Pygments lexer for Lambda Discipline, mirroring src/syntax/token.rs."""

from collections.abc import Iterable, Iterator
from typing import Any

from pygments.lexer import RegexLexer
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Whitespace,
)

IDENT = r"[A-Za-z_][A-Za-z0-9_']*"


class LbdLexer(RegexLexer):
    name = "Lambda Discipline"
    aliases = ["lbd"]  # noqa: RUF012
    filenames = ["*.lbd"]  # noqa: RUF012

    def __init__(self, builtins: Iterable[str] = (), **options: Any) -> None:
        super().__init__(**options)  # type: ignore
        self.builtins = set(builtins)

    tokens = {  # noqa: RUF012
        "root": [
            (r"\s+", Whitespace),
            (r"--.*?$", Comment.Single),
            (r'"([^"\\]|\\.)*"', String),
            (r"-?[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?", Number),
            (r"(use|let|in)\b", Keyword),
            (r"\\|λ", Keyword.Declaration),
            # A definition: a name at the start of a line followed by `:` or `=`.
            (rf"^{IDENT}(?=\s*[:=])", Name.Function),
            (r"(Number|String|Bool|Unit|List)\b", Keyword.Type),
            (IDENT, Name),
            (r"->|=|:", Operator),
            (r"[()\[\],.<>]", Punctuation),
            (r".", Text),
        ]
    }

    def get_tokens_unprocessed(
        self, text: str, stack: Iterable[str] = ("root",)
    ) -> Iterator[tuple[int, Any, str]]:
        for index, token, value in super().get_tokens_unprocessed(text, stack):
            if token is Name and value in self.builtins:
                token = Name.Builtin
            yield index, token, value
