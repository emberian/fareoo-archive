# Slides: RacketCon 2025

- URL: https://fare.tunes.org/files/cs/poof/slides-2025-racketcon.html
- Date: 2025
- Fetched: 2026-10-01T22:09Z (pandoc)
- Author: François-René Rideau (Faré)

---

[MuKn.com]

Compositional
Object-Oriented
Prototypes

 

(define (instantiate s) (Y (λ (m i) (s m i ⊤))))

(define (inherit c p m i) (compose (c m i) (p m i)))

 

François-René Rideau <fare@mukn.com>

http://github.com/metareflection/poof

 

(fifteenth RacketCon) 2025-10-04

 

PgDn: next

PgUp: previous

↑ ↓ ← → ESC ⏎

Touchscreen: swipe down until you must swipe right

Compositional Object-Oriented Prototypes

Plan of the Talk

- Introduction: OO, Informally
- Minimal OO, Formally
- Wait, what?
- What about my favorite OO feature?
- Inheritance: Mixin, Single, Multiple
- Conclusion: Making sense of OO

Introduction: OO, Informally

Claims

OO is Internal Modular Extensibility
We rebuild OO atop pure FP from these first principles

Classes, mutation, objects(!) are not fundamental
Key ignored semantic notion: Conflation

Mixin Inheritance: most fundamental, not most modular
Best Inheritance: combine Single and Multiple

Introduction: OO, Informally

What OO is not about

C++ (or even Java, etc.)

Classes

“Encapsulation”, “Information Hiding”

Opposite of FP, Inheritance vs Composition

Mutable records everywhere

Asynchronous Message Passing everywhere

UML / Co-Algebras / Relational Modeling

Introduction: OO, Informally

What OO is about

Modularity: dev needs little knowledge in

Extensibility: dev needs little knowledge out

Language-internal: first-class or second-class

 

Support for Division of Labor

 

Mechanism: Inheritance

Introduction: OO, Informally

Internal vs External

First class: internal, runtime (values, some via reflection)

Second class: internal, compile-time (types, macros)

 

Third class: external, software (tooling)

Fourth class: external, wetware (design patterns)

Compositional Object-Oriented Prototypes

Plan of the Talk

- Introduction: OO, Informally
- Minimal OO, Formally
- Wait, what?
- What about my favorite OO feature?
- Inheritance: Mixin, Single, Multiple
- Conclusion: Making sense of OO

Minimal OO, Formally

Minimal First-Class Semantics

You only really understand it if you can program it

Second-class is just first-class at compile-time
Any semantics is necessarily first-class for someone

A non-minimal model means you’re still confused

Minimal OO, Formally

Minimal First-Class Extensibility: What

Values: V
Extensions: V → V

e.g. for type V = Record
(define point-p (record (x 2) (y 4)))
(define (paint-blue p)
  (extend-record p 'color 'blue))

Minimal OO, Formally

Minimal First-Class Extensibility: How

Good: Apply extensions
  (ext value)

Better: Compose extensions
  (compose ext1 ext2)

... important if restricted extension language

Minimal OO, Formally

Minimal First-Class Extensibility: Top

To get V from V → V, apply to top value ⊤

Typical choices:
   V = Record, ⊤ = (record)
   V = Number, ⊤ = 0
   V = Pointer, ⊤ = null
In pure partial lazy FP, ⊤ = (lazy ⊥)

Bad: use fixpoint combinator Y : (V → V) → V

Minimal OO, Formally

Minimal First-Class Modularity: Records

Values: V, W, X...
Identifiers: I, J.
Set of bindings, a.k.a. record, a.k.a. indexed product:
   ∏R = i:I → Rᵢ

Example:
R = {x: Number, y: Number, color: Symbol}
(define point-q
  (record (x 3) (y 4) (color 'blue)))

Minimal OO, Formally

Minimal First-Class Modularity: Spec

Module context: ∏M = i:I → Mᵢ
Modular specification for X: ∏M → X

Example:
M = { ls: Str → List(Str),
      sort: List(Str) → List(Str) }
(define (ls-sorted m)
  (compose (m 'sort) (m 'ls)))

Minimal OO, Formally

Minimal First-Class Modularity: What

modular module specification:
Given a common module context ∏M,
for each identifier j, a value of type Xⱼ:
∏M → ∏X = ∏M → j:J → Xⱼ
∏M module context, record of identifiers referenced
∏X module body, record of identifiers defined.

Minimal OO, Formally

Minimal First-Class Modularity: Y

Close modular spec: ∏M → ∏M
every identifier referenced is defined

Extract target record ∏M from spec ∏M → ∏M ?
link references, close open loops, tie knots, …

fixpoint combinator Y     

Minimal OO, Formally

Digression: Scheme vs FP

Issue 1: pure applicative Y sucks
Solution: stateful Y, lazy Y, or second class Y

Issue 2: unary functions are syntax-heavy
Solution: cope, autocurry, or multiple arities with care

coop.rkt choices: stateful Y (letrec), autocurry

Minimal OO, Formally

Minimal First-Class Modular Extensibility

Extensions: X → X
Modularity context: ∏M
Open modular extensible spec: ∏M → ∏(X → X)

Close modular extensible spec: ∏M → ∏(M → M)
Resolve each binding — apply to top value ⊤
Target from reduced modular spec ∏M → ∏M — use Y

Minimal OO, Formally

Minimal “Object-Orientation”

(define (instantiate spec)
   (Y (λ (m i) (spec m i ⊤))))
(define (inherit child parent m i)
   (compose (child m i) (parent m i)))

That's mixin inheritance, all the OO you need!

(deftype spec (Fun M → I → X → X))
(define (my-spec self method-id super)
  ...value)

Minimal OO, Formally

Minimal Example

(define (coord-spec self i super)
  (case i ((x) 2) ((y) 4) (else super)))
(define (color-spec self i super)
  (case i ((color) 'blue) (else super)))

(define point-p (instantiate
   (inherit coord-spec color-spec)))
(point-p 'x) ⇒ 2
(point-p 'color) ⇒ blue

Minimal OO, Formally

Minimal Example, non-trivial inheritance

(define (add-x-spec dx self i super)
  (case i ((x) (+ dx super))
          (else super)))
(define (rho-spec self i super)
  (case i ((rho)
     (sqrt (+ (sqr (self 'x))
              (sqr (self 'y)))))
          (else super)))

Minimal OO, Formally

Minimal Example, non-trivial inheritance (test)

(define point-r (instantiate
   (inherit (add-x-spec 1)
     (inherit coord-spec
       rho-spec))))
(point-r 'x) ⇒ 3
(point-r 'rho) ⇒ 5

Compositional Object-Oriented Prototypes

Plan of the Talk

- Introduction: OO, Informally
- Minimal OO, Formally
- Wait, what?
- What about my favorite OO feature?
- Inheritance: Mixin, Single, Multiple
- Conclusion: Making sense of OO

Wait, what?

What did we just do?

Reconstructed recognizable OO from first principles

The first principles: first-class, modularity, extensibility

 

OO literally in two short definitions, in any FP language

 

No classes, no mutation, no objects!

 

How is it even possible???

Wait, what?

Precedents

Yale T Scheme 1982, YASOS 1992 (applicative, stateful)

Bracha & Cook 1990: theoretical “model” of inheritance

GCL 2004: Runs all Google (lazy, dynamic scope)

Jsonnet 2014: GCL cleanup (lexical scope, JS-y syntax)

Nix extensions 2015: isomorphic to above, OO in 2 funs

Wait, what?

OO without objects (as in Yale T Scheme)

“object” is any value, “instance” is just a regular record
No inheriting from an “instance”

“component” is a specification
No computing methods from a “component”

No equivalent to object (or class) in other OO languages!
... contrast with GCL, Jsonnet, Nix, that have objects(!?)

Wait, what?

Conflation: hidden product, implicit cast

Prototype = Spec × Target
Target = lazily resolved fixpoint from spec

Want to compute a method? Use the target
Want to inherit? Use the spec

Lazy is essential: most specifications are partial

Prototype OO: Ani 1976, ThingLab 1977, SELF 1986,
JavaScript 1995, GCL 2004, Jsonnet 2014, Nix 2015

Compositional Object-Oriented Prototypes

Plan of the Talk

- Introduction: OO, Informally
- Minimal OO, Formally
- Wait, what?
- What about my favorite OO feature?
- Inheritance: Mixin, Single, Multiple
- Conclusion: Making sense of OO

What about my favorite OO feature?

What about Classes?

Class = (Second-class) Prototype for Type (+ methods)
Object, Instance = element of the target type

static methods = methods of the target type
object methods = static methods applied to the element

abstract class = used only for its spec
concrete class = used only for its target

C++ templates: pure lazy FP Prototypes at compile-time

What about my favorite OO feature?

What about Objects?

T: "object" is any value, "instance" is target from spec
Prototype OO: "object / instance" is Spec × Target
Class OO: "object / instance" is Target type element

"object" and "instance" are very ambiguous words
"object" as a concept is not necessary for OO

Fields are named first, understood much later.

What about my favorite OO feature?

What about Types?

Spec Subtyping: before fixpoint
Target Subtyping: after fixpoint

SUBTYPING and FIXPOINT DO NOT COMMUTE!

Fortress 2011 Type checking modular multiple dispatch
     with parametric polymorphism and multiple inheritance
Scala 2012 Dependent Object Types

Prototype OO? Dunno, maybe dependent types?

What about my favorite OO feature?

What about Typeclasses or Modules?

Haskell Typeclass, Rust Trait, ML modules...
     modular but not extensible
Contra Cook: extensibility matters!

Interface Passing Style 2012: extensible typeclasses
Isomorphism via macros:
         class ≃ typeclass
         (linear) pure ≃ stateful

What about my favorite OO feature?

What about side-effects?

Classes: pure lazy Prototype OO at compile-time

Target types historically mutable, but don’t have to be

Plenty of pure object libraries in Lisp, Java, Scala…

Mutable inheritance: semantics is hard, like all mutation
CLOS update-instance-for-redefined-class
invalidate caches (atomically?)

What about my favorite OO feature?

Multiple dispatch? Method combination?

both: LOOPS 1986, CLOS 1991, Dylan 1992

multiple dispatch only: Cecil 1992, Fortress 2006, Julia 2012

“generic functions”, see CLOS for docs and experience
see Fortress for proper types

Pure FP vs orphan/friend/mutually-def'd (type)classes?
Global fixpoint of entire namespace (nixpkgs…)

What about my favorite OO feature?

What about single or multiple inheritance?

Worth a section of its own (see next)

Lowdown:
   mixin inheritance is simplest
   single inheritance is most efficient, least expressive
   multiple inheritance is most modular
   You can have the best of them together!

Compositional Object-Oriented Prototypes

Plan of the Talk

- Introduction: OO, Informally
- Minimal OO, Formally
- Wait, what?
- What about my favorite OO feature?
- Inheritance: Mixin, Single, Multiple
- Conclusion: Making sense of OO

Inheritance: Mixin, Single, Multiple

Single Inheritance

Hoare 1966 (sub)classes (handwaving)
SIMULA 1967 “Prefix classes” (first implementation)
Smalltalk 1976 “single inheritance” (compromise)
   C-with-classes 1979, Java 1996, C# 2000,
   COBOL 2002, JavaScript 2015...

Very efficient, simplest for 1960s before cheap lambdas
Least expressive, least modular

Inheritance: Mixin, Single, Multiple

Multiple Inheritance

KRL 1975 “inheritance of properties” Ani 76, ThingLab 77
Method conflict if in parallel superclasses:
   Mesa 1979, SELF 1986, C++ 1989, ADA 2003
Method combination after linearizing inheritance DAG:
   Flavors 1979, LOOPS 1986, CLOS 1991
Simple combination, can only call super method:
   Ruby 1992, Python 1994, Scala 2004

Most expressive, most modular
Most complex (~100 loc), somewhat inefficient in general

Inheritance: Mixin, Single, Multiple

Mixin Inheritance

Yale T Scheme 1982: implemented, not conceptualized
Bracha/Cook 1990: conceptualized, not implemented

PLT Scheme 1998, Strongtalk 2002, GCL 2004, Newspeak 2006, Jsonnet 2014, Nix 2015

Simplest in FP, more expressive & modular than Single
As inefficient as Multiple Inheritance, less modular

Inheritance: Mixin, Single, Multiple

Mixin more Expressive than Single

Second-class OOP: expressiveness issue.
Single only cons a spec, not append spec
Less sharing, more duplication, extra hoops
… maintenance nightmare.

First-class OOP: your own mixins on top (PLT 1998)
Still extra hoops, extra concepts, extra complexity

Inheritance: Mixin, Single, Multiple

Multiple More Modular than Mixin

Spec depends on others to avoid source duplication
Can’t “just” pre-append: runtime duplication, bad,
   exponential, non-commutative, non-idempotent

Mixin inheritance: manually manage linearization
A spec’s inheritance DAG becomes part of its interface
Nightmare on transitive dependency change

Multiple inheritance: just declare direct superspecs
No maintenance nightmare, just bliss.

Inheritance: Mixin, Single, Multiple

Single and Multiple Together

Two separate hierarchies (lame): CLOS (struct/class)
Same hierarchy (yay): Ruby (class/module),
   Scala (class/trait), Gerbil Scheme (struct/class)

“struct” can inherit from “class” and vice-versa
struct only in “single inheritance” wrt other structs

“tail property”: the property actually needed for efficiency
a struct’s class linearization is a suffix to its subclasses’s

Compositional Object-Oriented Prototypes

Plan of the Talk

- Introduction: OO, Informally
- Minimal OO, Formally
- Wait, what?
- What about my favorite OO feature?
- Inheritance: Mixin, Single, Multiple
- Conclusion: Making sense of OO

Conclusion: Making sense of OO

Claims (Redux)

OO is Internal Modular Extensibility
We rebuild OO atop pure FP from these first principles

Classes, mutation, objects(!) are not fundamental
Key ignored semantic notion: Conflation

Mixin Inheritance most fundamental Inheritance
Best: combine Single and Multiple Inheritance

Conclusion: Making sense of OO

This very Presentation!

scribble + coop.rkt spit HTML for reveal.js

No objects, just specs and targets, mixin inheritance
FP+OO system in 350 loc incl. autocurry, comments
Prototypes for slides w/ toc in ~125 loc

How can TOC appear purely before the end?
Fixpoint magic! Lazy avoids exponential recomputation

… Time for demo?

Conclusion: Making sense of OO

Why did I care?

Great Usenet Flamewars of 1990s:
Dysfunctional Programming vs
                   Objectionable Disorientation
Talking Past Each Other… for Decades

1970s Lisp had both OO and FP
2000s Fortress, Scala: with types

Opposition in Mind, not in Reality

Conclusion: Making sense of OO

Why So Much Blindness?

Industry doesn’t care enough about Correctness
Academia doesn’t grok Programming In The Large

Both ignore the Human Factor:
interchangeable cogs, transient students

All get stuck in their paradigms

Conclusion: Making sense of OO

Two Mindsets

Compositionality for reducible problems
Extensibility for irreducible problems

Brighter than ambitious vs more ambitious than bright

History: OO invented to model complex SIMULAtions
History: FP to formalize simple computations in logic

Conclusion: Making sense of OO

Meta-Thesis

Humility, not fanaticism

Incommensurable paradigms? Go wider!

Researcher: old paradigm’s low-hanging fruits harvested

Simplicity matters

Racket, Scheme: λ’s for Semantics, macros for Syntax

Conclusion: Making sense of OO

Thank You!

Theory:          https://github.com/metareflection/poof

Practice:       Gerbil Scheme https://cons.io

X: https://x.com/ngnghm Blog: https://ngnghm.github.io

Hire me — or be hired by me!       <fare@mukn.com>

Plenty more research ideas, code and papers to write…
