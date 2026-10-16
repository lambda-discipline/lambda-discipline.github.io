---
title: Language reference
description: Syntax, types and evaluation of Lambda Discipline, plus the REPL and diagnostics.
---

# Language reference

Lambda Discipline is a lazy, statically typed functional language. A program
is a list of definitions and expressions; every computation is the
application of a function to arguments, written as an S-expression.

[TOC]

## A program

A file contains three kinds of item, in any order:

```lbd
use "std.lbd"                               -- include another file

square : Number -> Number = \x. (mul x x)   -- a definition, with a type
cube = \x. (mul x (square x))               -- the type is optional

(println (cube 3))                          -- an expression, run when the program runs
```

Definitions are order independent and may be mutually recursive. Expressions
at the top level are evaluated in the order they appear.

`use` paths are relative to the file that contains them, and each file is
included at most once however many times it is used.

## Lexical structure

| Element | Form |
| --- | --- |
| Comment | `--` to the end of the line |
| Identifier | a letter or `_`, then letters, digits, `_` and `'`: `x`, `foldl`, `go'` |
| Number | `42`, `-5`, `3.14`, `6.02e23`: all numbers are 64-bit floats |
| String | `"..."` with the escapes `\n \t \r \0 \\ \" \' \u{3bb}` |
| Keywords | `use`, `let`, `in` |
| Lambda | `\` or `λ` |

Numbers print the way most languages print them: `42`, `3.14`,
`0.30000000000000004`, `Infinity`.

## Syntax

```text
item  = "use" STRING                         include another file
      | IDENT [":" type] "=" expr            definition; the annotation is optional
      | expr                                 evaluated in order when the program runs

expr  = "\" IDENT [":" type] "." expr        lambda (also `λ`)
      | "let" IDENT [":" type] "=" expr "in" expr
      | "(" expr expr+ ")"                   application; any expression can be called
      | "(" expr ")" | "(" ")"               grouping, unit
      | "[" expr, ... "]"                    list
      | NUMBER | STRING | IDENT

type  = Number | String | Bool | Unit | List<type>
      | lowercase-variable | type -> type | (type)
```

### Lambdas

A lambda takes exactly one parameter. Functions of several arguments are
lambdas that return lambdas, and calling one with fewer arguments gives back a
function waiting for the rest:

```lbd
add3 = \a. \b. \c. (add (add a b) c)

(println (add3 1 2 3))       -- 6
addTen = (add3 4 6)          -- a function of one more argument
(println (addTen 5))         -- 15
```

A parameter can carry a type: `\x: Number. (mul x x)`.

### Application

`(f a b c)` applies `f` to `a`, then the result to `b`, then to `c`. Anything
can be in function position, including another application or a lambda:

```lbd
(println ((\x. (mul x 2)) 21))   -- 42
```

### `let`

`let name = value in body` names a value inside an expression. A `let` is
recursive, so it can define local loops, and it is generalized, so a local
function can be used at several types:

```lbd
collatz = \start.
    let go = \n. \steps.
        (if (eq n 1) steps
            (go (if (eq (mod n 2) 0) (div n 2) (add (mul 3 n) 1)) (add steps 1)))
    in (go start 0)

(println (collatz 27))   -- 111
```

### Lists

`[1, 2, 3]` is a list. All elements have the same type, and `[]` is the empty
list. Lists are immutable: `push`, `remove`, `cons` and the rest return a new
list and leave their argument unchanged. See the [list builtins](/builtins/#list).

## Types

| Type | Values |
| --- | --- |
| `Number` | 64-bit floating-point numbers |
| `String` | Unicode text |
| `Bool` | `true` and `false` |
| `Unit` | `()`, the result of `print` and `println` |
| `List<a>` | lists whose elements have type `a` |
| `a -> b` | functions from `a` to `b`; the arrow associates to the right |
| `a`, `b`, ... | type variables: any type at all |

### Inference

Lambda Discipline uses Hindley-Milner type inference with let-polymorphism,
so annotations are never required:

* An unannotated definition gets its most general type: `id = \x. x` is
  `a -> a`, and can be used on numbers and strings alike.
* Mutually recursive definitions are inferred together, then generalized.
* A program with a type error does not run at all.

### Annotations

An annotation is a promise the checker holds you to. Its type variables are
rigid, so a definition can't claim to be more general than it is:

```lbd
f : a -> b = \x. x   -- error: the body has type a -> a
```

Type variables in an annotation scope over the whole definition, so the
lambdas inside can refer to them:

```lbd
apply : (a -> b) -> a -> b = \f: (a -> b). \x: a. (f x)
```

`print` and `println` are the one exception to ordinary typing: they take any
number of arguments of any types, and must be called directly rather than
passed around as values.

## Evaluation

Evaluation is **call-by-need**: an argument is evaluated only when the function
uses it, and at most once. That is why `if`, `and` and `or` are ordinary
builtins rather than special forms. `if` only evaluates the branch it picks,
so this is safe:

```lbd
safeDivide = \a. \b. (if (eq b 0) 0 (div a b))
```

and so is this:

```lbd
const = \x. \unused. x
(println (const 1 (error "never evaluated")))   -- 1
```

* **Tail calls** run in constant space, so loops written as recursion don't
  grow memory.
* **Deep recursion** is limited only by memory: a million nested calls take
  about half a gigabyte. Runaway recursion stops with a "recursion is too
  deep" error rather than a crash.
* **Self-dependent values** such as `x = (add x 1)` are reported as errors
  instead of looping forever.
* **Comparison** is structural, like OCaml: numbers, strings, booleans and
  lists can be compared with `eq`, `lt` and friends. Comparing functions is a
  runtime error.

## The REPL

Run `lbd` with no arguments, or `lbd repl`. Enter definitions and
expressions; definitions stay for the rest of the session. Commands start
with `:`, and any unambiguous prefix works, so `:t` is `:type` and `:l` is
`:load`. Tab completes names, commands and file paths.

| Command | What it does |
| --- | --- |
| `:help` (`:?`) | List the commands. |
| `:quit` (`:exit`, Ctrl-D) | Leave. |
| `:type <expr>` | The type of an expression, without evaluating it. |
| `:info <name>` | The type and definition site of a name, or a builtin's docs. |
| `:load <file>` / `:reload` | Load and run a file, or load the last one again. |
| `:env` (`:browse`) | Your definitions and their types. |
| `:docs [name]` | The builtin reference. |
| `:reset` | Forget every definition. |

Without a terminal (a pipe, Jupyter, an editor mode) the REPL reads standard
input without printing prompts.

## Diagnostics

Errors point at the code that caused them, and one run reports as many
independent errors as it can find:

```text
Error: mismatched types
   ╭─[ examples/demo.lbd:1:13 ]
   │
 1 │ (print (add "hello" 5))
   │             ───┬───
   │                ╰───── expected `Number`, found `String`
   │
   │ Note: in argument 1 of `add`
───╯
```

Misspelled names come with suggestions, and `lbd check <file> --emit
tokens|ast|types|core` prints each stage of the compiler for when you want to
see what it sees.
