---
title: Tooling
description: Editor support, the Jupyter kernel and the lbd command line.
---

# Tooling

## Editors

| Editor | Package | What you get |
| --- | --- | --- |
| VS Code | [lbd-vscode](https://github.com/lambda-discipline/lbd-vscode) | Syntax highlighting, file icons, and running the current file with `lbd run`. |
| GNU Emacs | [lbd-emacs-major-mode](https://github.com/lambda-discipline/lbd-emacs-major-mode) | A major mode for `.lbd` files. |
| GNU Emacs | [lbd-emacs-inf-repl-mode](https://github.com/lambda-discipline/lbd-emacs-inf-repl-mode) | Run the REPL in a buffer and send code to it. |
| Any TextMate-compatible editor | [lbd-tm-grammar](https://github.com/lambda-discipline/lbd-tm-grammar) | The grammar behind the VS Code highlighting. |

## Jupyter

[lbd-jupyter-kernel](https://github.com/lambda-discipline/lbd-jupyter-kernel)
runs Lambda Discipline in Jupyter notebooks. It drives `lbd repl` over a pipe,
so definitions carry over from cell to cell.

## The command line

| Command | What it does |
| --- | --- |
| `lbd run <file>` | Type-check and run a program. The exit code is 1 on any error. |
| `lbd check <file>` | Type-check without running. |
| `lbd check <file> --emit tokens` | The token stream. |
| `lbd check <file> --emit ast` | The syntax tree. |
| `lbd check <file> --emit types` | The inferred type of every definition. |
| `lbd check <file> --emit core` | The Core IR the backend runs. |
| `lbd repl`, or just `lbd` | The [REPL](/reference/#the-repl). |
| `lbd docs [name]` | The [builtin reference](/builtins/). |
| `lbd docs --json [name]` | The same reference as JSON, for tools. |

## Using Lambda Discipline as a library

The interpreter is also a Rust library. The compiler stages are public
modules, and `Session::compile` hands you the Core IR, ready for a backend of
your own. Implement `backend::Backend` to emit whatever you like; the
repository's `tests/pipeline.rs` contains a minimal example.
