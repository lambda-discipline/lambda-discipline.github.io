---
title: Lambda Discipline
template: home.html
---

```lbd
-- Types are inferred; annotations are checked.
fibonacci : Number -> Number = \n.
    (if (lt n 2) n (add (fibonacci (sub n 1)) (fibonacci (sub n 2))))

compose = \f. \g. \x. (f (g x))          -- (a -> b) -> (c -> a) -> c -> b

(println (map fibonacci (range 0 10)))   -- [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
(println ((compose show (mul 2)) 21))   -- 42
```

<ul class="features">
  <li><strong>Lambdas, and little else</strong>Programs are applications of <code>\x. body</code> functions, written as S-expressions. The whole grammar fits on a postcard.</li>
  <li><strong>Inferred types</strong>Hindley-Milner inference with let-polymorphism. Write annotations when they help you; the checker holds them to their word.</li>
  <li><strong>Lazy by default</strong>Call-by-need evaluation: arguments are evaluated only when used, and at most once. Tail calls run in constant space.</li>
  <li><strong>Immutable data</strong>Lists are persistent vectors. Every operation returns a new list and leaves the old one exactly as it was.</li>
  <li><strong>Errors that help</strong>Several diagnostics per run, each pointing at the code that caused it, with "did you mean" suggestions.</li>
  <li><strong>A real compiler</strong>Parser, resolver, type checker and a Core IR in front of a lazy abstract machine, with room for more backends.</li>
</ul>

## A first program

Save this as `hello.lbd`:

```lbd
greet : String -> String = \name. (concat "Hello, " name)

(println (greet "World"))
```

and run it:

```text
$ lbd run hello.lbd
Hello, World
```

Or start `lbd` with no arguments for a REPL, where `:type` shows the type of
any expression:

```text
λ> :type (map (add 1))
(map (add 1)) : List<Number> -> List<Number>
```

## Where to next

* [Install](/install/) the interpreter.
* Read the [language reference](/reference/) and the [builtins](/builtins/).
* Browse the [examples](/examples/), from Hello World to Advent of Code.
* Find out [why the language looks the way it does](/philosophy/).
