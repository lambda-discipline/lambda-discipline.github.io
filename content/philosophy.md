---
title: Philosophy
description: The ideas behind Lambda Discipline, and why the language looks the way it does.
---

# Philosophy

> A language should be small enough to hold in your head, and strict enough
> that what you hold there is true.

Lambda Discipline begins with the lambda calculus, the smallest language that
can express any computation: variables, functions of one argument, and
application. Everything else is there to make that core pleasant to write and
safe to run. Where convenience and coherence disagree, coherence wins.

## The lambda is the unit of thought

There are no statements, no loops and no special forms. A program is
definitions and applications of `\x. body` functions, and each application is
an S-expression whose shape *is* its meaning: `(f x y)` applies `f` to `x`,
then to `y`. A grammar this small has no corners to memorize. You learn it once
and then think only about your problem.

Functions take one argument at a time, so partial application is free. The
builtins are designed for it: the data a function works on always comes last,
which makes `(map (add 1))`, `(filter (lt 0))` and `(split ",")` complete,
meaningful functions on their own.

## Discipline means types

The *discipline* is the type system. Every program is checked with
Hindley-Milner inference before a single expression runs, and a program that
doesn't type-check doesn't run. There are no warnings to ignore.

Inference keeps the discipline from becoming bureaucracy. You write
annotations where they say something useful to a reader, and the checker works
out the rest, always finding the most general type. When you do write an
annotation, it is a contract: its type variables are rigid, so a function
can't quietly claim to be more general than it is.

## Laziness is the honest default

Arguments are evaluated when they are needed, and only once. With laziness,
`if`, `and` and `or` need no special treatment: they are ordinary functions
that simply don't touch the branch they don't take. Control flow is just
another thing you can define, pass around and partially apply.

Laziness asks for a runtime that respects it, so tail calls run in constant
space, deep recursion is bounded by memory rather than a fixed stack, and a
value that depends on itself is reported instead of hanging.

## Values don't change

Lists are immutable persistent vectors. Adding, removing or reading an element
returns a new list in logarithmic time and leaves the original exactly as it
was. A name means one thing for its whole life, which is what makes laziness,
sharing and equational reasoning safe.

## Errors are part of the interface

A language is used mostly while it is telling you that you're wrong. Lambda
Discipline reports every independent error it finds in one run, points at the
exact code responsible, and suggests the name you probably meant. Runtime
errors point at the call that failed. Nothing crashes with a stack trace from
the implementation.

## Built like a compiler

Under the interpreter is a conventional compiler pipeline, the shape of rustc
or GHC: a lexer and parser, name resolution, type inference, and a Core IR that
is closure-converted and uncurried. Today that IR feeds a lazy abstract
machine. Tomorrow it can feed a transpiler, a virtual machine or native code
without the front end changing. Builtins are declared once, with their type and
documentation, and every stage reads that one declaration. The
[builtin reference](/builtins/) on this site is generated from it.

## Free to improve

Lambda Discipline is young, and it isn't bound by compatibility with its own
past. Its current implementation is a ground-up rewrite that renamed builtins,
tightened the type system and changed the syntax wherever doing so made the
language more coherent. It will keep doing that while it's young.
