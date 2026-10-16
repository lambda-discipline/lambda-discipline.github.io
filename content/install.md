---
title: Install
description: Install the lbd interpreter with Cargo, or build it from source.
---

# Install

Lambda Discipline is a single binary, `lbd`, that runs programs, type-checks
them and hosts the REPL.

## With Cargo

You need [Rust](https://www.rust-lang.org/tools/install) 1.85 or newer.

```bash
cargo install --git https://github.com/lambda-discipline/lambda-discipline
```

This puts `lbd` in `~/.cargo/bin`, which `rustup` already added to your `PATH`.

## Prebuilt binaries

Tagged versions are published on the
[releases page](https://github.com/lambda-discipline/lambda-discipline/releases)
for Linux (x86-64), macOS (Apple silicon) and Windows (x86-64). Download the
archive for your platform, extract it, and put `lbd` somewhere on your `PATH`.

## From source

```bash
git clone https://github.com/lambda-discipline/lambda-discipline
cd lambda-discipline
cargo build --release
```

The binary is `target/release/lbd`. Run the test suite with `cargo test`.

## Check that it works

```bash
lbd --version
```

```bash
lbd run examples/hello_world.lbd
```

## Using it

| Command | What it does |
| --- | --- |
| `lbd run <file>` | Type-check and run a program. The exit code is 1 on any error. |
| `lbd check <file>` | Type-check without running. |
| `lbd check <file> --emit <stage>` | Print an intermediate representation: `tokens`, `ast`, `types` or `core`. |
| `lbd repl`, or just `lbd` | Start an interactive session. |
| `lbd docs [name] [--json]` | Show the [builtin reference](/builtins/). |

Next, set up your [editor](/tooling/) or start with the
[language reference](/reference/).
