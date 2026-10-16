---
title: About
description: Where Lambda Discipline comes from, how it is built, and how to take part.
---

# About

Lambda Discipline is an open-source functional programming language: lazy,
statically typed and built directly on the lambda calculus. It is developed in
the open by the [lambda-discipline](https://github.com/lambda-discipline)
organization on GitHub.

## History

The language has been implemented more than once, and each version has
learned from the last:

* A first [Rust implementation](https://github.com/lambda-discipline/lambda-discipline-rust-legacy),
  now archived.
* A [C++ interpreter](https://github.com/lambda-discipline/lambda-discipline-cpp)
  with a REPL, also archived.
* The [current implementation](https://github.com/lambda-discipline/lambda-discipline),
  a rewrite in Rust with full Hindley-Milner inference, call-by-need
  evaluation, immutable lists, a redesigned set of builtins and a compiler
  pipeline built to grow new backends.

## Taking part

Bug reports, language proposals and pull requests are welcome. Start with the
[contributing guide](https://github.com/lambda-discipline/lambda-discipline/blob/master/CONTRIBUTING.md),
and please follow the
[code of conduct](https://github.com/lambda-discipline/lambda-discipline/blob/master/CODE_OF_CONDUCT.md).
Security issues should be reported as described in the
[security policy](https://github.com/lambda-discipline/lambda-discipline/blob/master/SECURITY.md).

## This website

The site is built by a small Python script from the
[lambda-discipline.github.io](https://github.com/lambda-discipline/lambda-discipline.github.io)
repository. Every day it checks the language repository for new commits, and
when there are any it rebuilds: the [builtin reference](/builtins/) comes from
`lbd docs --json`, and every [example](/examples/) is run by the current
interpreter so the output you see is the output you'll get.

## License

Lambda Discipline and this website are released under the
[MIT license](https://github.com/lambda-discipline/lambda-discipline/blob/master/LICENSE.txt).
