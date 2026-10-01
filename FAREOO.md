# Faré's foundations of OO — a connected account

François-René Rideau (Faré, @Ngnghm): what an object is, what inheritance is, what
"Houyhnhnm computing" demands of a system people live in. Written 2026-10-01 from the
sources in `sources/` (every citation names a file there; section numbers are the
author's own). Each claim is tagged **READ** (I read it, citation follows) or
**INFERRED** (my connection, not his sentence). Where he gives a definition or an
equation it is quoted, not paraphrased.

Citation key: `poof` = `sources/poof-paper.md` (Scheme Workshop 2021); `eoomi` =
`sources/eoomi2024.md`; `ltuo` = `sources/ltuo-book.md` (book draft, 2026); `rc25` =
`sources/poof-slides-2025-racketcon-src.md`; `fci` = `sources/fci2017.md`; `climb` =
`sources/climbing.md`; `thesis` = `sources/thesis.md`; `persist` =
`sources/persist-model.md` (March 2024 reframing); `pslides` =
`sources/persist-slides-2025.md`; `lil` = `sources/lil-ilc2012.md`; `snapl` =
`sources/snapl2015.md`; `chN` = `sources/houyhnhnm-chNN.md`; `todo` =
`sources/poof-todo.md`; `gpoo` = `sources/gerbil-poo-prototypes.md`; `els26` =
`sources/poof-slides-2026-els-src.md`. Tweets: `sources/tweets-oo.md` (see §0).

---

## 0. One paragraph, in his words

**READ.** "What is the essence of object-oriented programming? *Incremental composition
of code and data fragments with late binding.*" (`gpoo` Abstract). Formally: "the
essence of Object-Orientation (OO) is a mechanism for reified (in-language) Incremental
Modularity" (`eoomi` Abstract); in the book's final wording, "Object Orientation ('OO')
is a technique that enables the specification of programs through extensible and
modular partial specifications, embodied as entities within a programming language"
(`ltuo` §2.1). The whole thing fits in two lines of Scheme:

```scheme
(define (fix p b) (define f (p (lambda i (apply f i)) b)) f)
(define (mix c p) (lambda (f b) (c f (p f b))))
```

"We will make the case that the above two definitions summarize the essence of
Object-Oriented Programming (OOP), and that all the usual OOP concepts can be easily
recovered from them—all while staying within the framework of pure Functional
Programming (FP)." (`poof` §1.1.1). The purpose that justifies the mechanism is social:
"supporting fine-grained division of labor in software development" (`ltuo` §4 intro).

The rest of this file unfolds that paragraph, then widens to the Houyhnhnm material
(persistence, live upgrade, kernels, platforms, points of view), which is the same
doctrine — *internalize the process of change, so people can cooperate without
coordinating* — applied to whole computing systems rather than to programs.

**Tweets.** The scry drip of @Ngnghm (`raw/ngnghm.jsonl`) had delivered **0** tweets
when this file was first written (the first page lands after a 429 sleep, ~20:14
local). `sources/tweets-oo.md` is appended as pages arrive; anything from the tweets
that changes a section below is flagged there with the section number.

---

## 1. What an object IS: a fixed point over a prototype; `self`, `super`, open recursion

**READ.** The primitive is not the object. "In general, we will call *prototype* such a
computation increment." A prototype (initially, a *prototype wrapper*) is "a function of
two arguments, self and super (or, above, f and b, for fixed-point and base value)"
(`poof` §1.1.4). The types, in his notation:

```
(deftype (Proto Self Super) (Fun Self Super -> Self st: (<: Self Super)))
fix : (Fun (Proto Self Super) Super -> Self st: (<: Self Super))
mix : (Fun (Proto Self Super) (Proto Super Sup2) -> (Proto Self Sup2))
```
(`poof` §1.1.4). What the two arguments mean:

- `self` "will hold the instance resulting as a fixed point from the entire
  computation. When composing multiple prototypes, every prototype will receive the
  same value as their self argument: the complete instance that results from applying
  each prototype in order. This allows prototypes to 'cooperate' with each other on
  different aspects of the computation ... accessed through the self argument in what
  is called 'late binding'." (`poof` §1.1.4)
- `super` "holds the partial result of the fixed-point computation after applying only
  the 'next' prototypes ... children prototypes can accumulate, modify or override the
  method values inherited from the parent prototypes." (`poof` §1.1.4)

**READ.** The instance/prototype distinction is load-bearing: "Instances are the
non-composable complete outputs of instantiation, whereas prototypes are the
composable partial inputs of instantiation." (`poof` §1.3.1). In the 2024 and 2026
wording the two sides are renamed **specification** and **target**: "more than
prototype, class, object, or method, the fundamental notions of OO are specification
and target: target computations are being specified by extensible and modular, partial
specifications" (`ltuo` §2.3.1).

**READ.** Open recursion is the mechanism of modularity, `super` the mechanism of
incrementality: "a prototype specifying one aspect of a computation should be able to
make (forward) references to the complete computation being specified itself ... the
prototype should be or contain a function with the computation self as input for
self-reference, and returns as output a computation ... that uses self in an open
recursion" (`eoomi` §3.1 Embodying Modularity); "Each prototype should be able to refer
not only to the complete computation with all available information, but also to the
partial computation with only the information specified so far" (`eoomi` §3.1
Embodying Incrementality). The 2025 slides compress it: "Modularity: dev needs little
knowledge in / Extensibility: dev needs little knowledge out / ... Intralinguistically"
(`rc25`), and give the set-of-bindings form: "Open modular spec: ∏M → ∏X ... Close
modular spec: ∏M → ∏M ... Extract record ∏M from spec ∏M → ∏M? Close open loops, tie
knots… fixed-point operator Y" (`rc25` "Minimal (First-Class) Modularity").

**READ.** Partiality is the point, not a defect: "the entire point of incremental
programming is that you want to define and manipulate fragments that are not complete
specifications" (`poof` §3.2); "not every prototype can be successfully instantiated,
which is actually an essential feature of prototypes" (`eoomi` §3.3.5); "Typesystems and
semantic frameworks incapable of dealing with such incomplete information are thereby
incapable of apprehending OO." (`ltuo` §2.1.1).

**READ.** There is no object in the minimal model: "we have been doing 'Object-Oriented
Programming' without any actual object!" (`poof` §4.2.1); "Maybe the field should be
named after Inheritance, or Prototypes, or Incremental Modularity, and banish the word
'Object' forevermore from its name." (`eoomi` §5.2 OO without Objects). What *is* an
object, when there is one, is §5 below (conflation).

**READ.** Generality: the instance need not be a record. "Prototypes are not just for
records as functions from symbol to value: they can be used to incrementally specify
any kind of functions!" (`poof` §3) — the examples are numeric functions and thunks;
records are merely "a better suited target for general-purpose incremental modular
specification, since they allow the indefinite further specification of new aspects"
(`eoomi` §5.2).

---

## 2. Inheritance = composition of partial specifications (a monoid)

**READ.** "Inheritance is the mechanism by which partial modular specifications are
incrementally extended into larger modular specifications, until the point where a
complete specification is obtained from which the specified target computation can be
extracted." (`ltuo` §2.4.1). The algebra: "mix is associative" (`poof` §1.2.3); "the
identity prototype ... is a neutral element for mix ... Thus prototypes form a monoid"
(`poof` §1.3.2). In the 2024 notation:

```
Mixin self super = self ⊂ super ⇒ self → super → self
fix = λ mixin top ↦ Y (λ self ↦ mixin self top)
mix = λ child parent self duper ↦ child self (parent self duper)
```
(`eoomi` §4.1 Mixin Semantics). The claimed contribution is "promoting composition of
wrappers rather than their application to a generator as the algebraic structure of
interest" (`poof` §1.1.2 (b)).

**READ.** Modularity and incrementality are distinct and both needed: "merging disjoint
commuting mixins embodies modularity, but not incrementality ... to achieve it
intralinguistic, you need a way to operate on existing modules, which by definition is
not commutative" (`eoomi` §3.3.5). So inheritance is *non-commutative* by design;
order is meaning.

**READ.** Single inheritance is the degenerate case: "'Single inheritance' consists in
prototypes being second-class entities that you can only apply to generators
immediately after having defined them, with a fixed base instance for all generators"
(`poof` §1.3.4); "single inheritance is strictly less expressive (Felleisen 1991) and
less modular than mixin and multiple inheritance" (`eoomi` §4.2). Semantics of single
inheritance: `Gen self = self → self`, `extend = λ mixin parent self ↦ mixin self
(parent self)` (`eoomi` §4.2).

**READ.** The 1990 equations were consequences, not axioms: "The equations of Bracha and
Cook (1990) were not arbitrary axioms, but necessary consequences of more primitive
principles" (`ltuo` §11.1.1). The design is a "fixed point in design space": GCL (Google,
~2004), Jsonnet (2014), Nix extensions (2015) and T (1981) all reinvented it (`poof`
§7.2.2; `eoomi` §3.2.5 "Minimal Design, Maximal Outreach").

**INFERRED.** Because inheritance is a monoid on partial specifications, "a law that
extends another's law" has an exact meaning in his terms: `mix mine theirs`, where
`mine` may read `super` (what theirs decided) and `self` (what the whole decides). A
system that only lets you *replace* a specification has single inheritance at best,
usually none. That is the test I apply to Mini in `AUDIT.md`.

---

## 3. Mixins, multiple inheritance, linearization — and why multiple beats mixin

**READ.** Mixins are the simplest to formalize ("The Last Shall Be First", `eoomi`
§4.1) but *less modular* than multiple inheritance, because with mixins the dependency
order is extra-linguistic: "With mixin inheritance, developers would have to manually
curate the order in which they mix prototypes, extra-linguistically ... Their dependency
DAG will not be a hidden implementation detail, but part of the interface. And when
some upstream module modifies the dependency DAG of a prototype, all the prototypes in
all the modules that transitively depend on it will have to be updated by their
respective maintainers" (`eoomi` §4.3 More Modular). The failure mode is spelled out
with a worked DAG (Z ← K1,K2,K3 ← A..E ← O): a naive pre-mix "Z K1 A B C O K2 D B E O K3 D
A O would be incorrect, with unwanted repetitions of A, B, D, O redoing their effects
too many times and possibly undoing overrides" (`poof` §4.3.1); "manual maintenance of
precedence lists is a modularity nightmare" (`poof` §4.3.1).

**READ.** Multiple inheritance fixes this by making the DAG an in-language entity and
*linearizing*: "programmers only need declare the dependencies between objects and
their direct super objects: the object system will automatically compute a suitable
precedence list ... The algorithm that computes this precedence list is called a
linearization: It considers the dependencies as defining a directed acyclic graph
(DAG) ... and it completes this partial order into a total (or linear) order" (`poof`
§4.3.2); C3 is the settled algorithm (`poof` App. A.1). A prototype under multiple
inheritance is therefore "a tuple of: (a) a mixin function ... (b) an ordered list of
direct super prototypes ... (c) a unique name" (`eoomi` §4.3 Prototypes as a DAG).

**READ.** The diamond: "there is no general way to combine multiple modular definitions
into one, except to keep one and drop the others" (`ltuo` §7.3.4.1), so the
"conflict" semantics of C++/Smalltalk/Self is "the single least useful among all
possible consistent behaviors" (`ltuo` §7.3.4.1); users who want better would have to
"implement their own variant of a CRDT for the values of their methods" on top of a
broken system (`ltuo` §7.3.4.1 fn). The flavorful answer is "Cooperation not Conflict"
(`ltuo` §7.3.4.2): "The older (1976) 'flavorless' viewpoint sees it as a conflict to
resolve between methods that override each other. The newer (1979) 'flavorful'
viewpoint sees it as a cooperation to harmonize between methods that combine with each
other." (`ltuo` §2.4.3). In the TODO's blunt form: "wrappers must be CRDTs (which
[Cook] fails to notice) ... which comes for free if you linearize your ancestors and
apply a plain old wrapper" (`todo`).

**READ.** The strict ordering of modularity: "(1) flavorful multiple inheritance with
local order and monotonicity, (2) less consistent flavorful multiple inheritance, (3)
mixin inheritance, (4) flavorless 'conflict' multiple inheritance, (5) single
inheritance, and (6) no inheritance" (`ltuo` §11.1.8).

**READ.** Single and multiple together — the *suffix property* and C4 (2024): "what
enables the optimizations of single inheritance is ... the suffix property: the
precedence list of a struct is a suffix of that of every descendant of it" (`ltuo`
§7.4.2); "It is not exactly single inheritance as such that mattered, rather it was the
suffix property implicit in single inheritance" (`ltuo` §7.4.3). C4 "in addition to the
constraints of C3, also respects the suffix property for specifications that are
declared as suffixes" (`ltuo` §7.4.4); shipped in Gerbil Scheme 2024 and as
header-only C++20 (`sources/c4-mixins-readme.md`: "every ancestor's behavior takes
effect once and only once, in a consistent order. Inconsistent inheritance graphs are
rejected at compile time").

**READ.** Method combinations and generalized prototypes: a generalized prototype
"would involve: (a) a lens ... that can extract or update the method from the current
partial computation of the raw prototype fixed-point; (b) an object-setter that 'cooks'
the raw prototype fixed-point into a referenceable self object; (c) a method-wrapper"
— `($lens-gen setter getter wrapper method)` (`poof` App. B.2.2). The book makes this
the central move: "focused specifications ... enriching it ... with two access paths: a
path from the top of the program state to the module context being referenced, and a
path from the top of the program state to the method being extended ... formalize[d] as
functional lenses" (`ltuo` §9.1.2). Payoff: "open method specifications can now be
considered individually, then grouped incrementally into larger algebraically coherent
chunks; at each step, every specification can be parsed, defined, typed, analyzed,
proved correct, algebraically combined" (`ltuo` §9.1.2).

**INFERRED.** The two tests this gives a system: (i) can a third party *declare a
dependency* between two specifications and have the system order them, or must it
hand-write the order (mixin at best)? (ii) when two independent extensions touch the
same aspect, does the system *combine* them (flavorful) or *refuse* (conflict)?

---

## 4. The role of laziness

**READ.** "Lazy makes OO Easy" (`eoomi` §5.1). Two reasons. Performance/sharing: in an
eager language "applicative order evaluation may cause an explosion in redundant
recomputations of methods, and sometimes infinite loops ... computations needed
multiple times will lead to an exponential duplication of efforts" (`eoomi` §5.1);
`δfix`/`δmix` with `delay` fix this (`poof` §3.2). Semantics: "prototypes incrementally
specify computations rather than values" (Call-By-Push-Value) and "laziness
(call-by-need) is the best good way to reify a computation as a value, bridging between
the universes of computations and values" (`eoomi` §5.1 Computations vs Values).

**READ.** Laziness is what dissolves initialization order: "lazy evaluation enables
modular initialization of prototype slots: Slots are bound to lazy formulas to compute
their values ... The slot initialization order needs not be the same across an entire
prototype hierarchy ... There are no null values that become ticking bombs at runtime"
(`eoomi` §5.1 Method Initialization Order); "circularities are the general case in the
presence of modularity—and only more so with OO ... the simplest, most natural and
safest usable setting for OO is: lazy evaluation" (`ltuo` §4.1.6.1); "The more
programmers must agree on a protocol to follow, the less modular the approach." (`ltuo`
§4.1.6.1).

**READ.** Laziness is also what makes conflation possible (next section): "Lazy is
essential: most specifications are partial" (`rc25` "Conflation"); "thanks to lazy
evaluation, you don't have to care about whether [the fixed point converges] to refer to
the two together" (`eoomi` §5.3).

**READ.** The counter-intuitive conclusion: "contrary to what many may assume ... OO is
more easily expressed in a pure lazy functional setting. Indeed, we could argue that OO
as such is almost never practiced in a mutable setting, but rather as a pure functional
static metaprogramming technique" (`eoomi` §5.1 "If it's so good..."); "the natural
paradigm for OO is Pure Lazy Functional Programming" (`ltuo` §11.1.5).

---

## 5. Conflation: specification × target; the "object" is a hidden product

**READ.** The missing concept in sixty years of literature: "Jsonnet and Nix both
confront and elegantly solve the above issue, and in the very same way, with one small
trick: they bundle and conflate together instance and prototype in a same single
entity, the 'object'. Indeed, in a pure context, and given the base super value for the
given prototype representation, there is one and only one instance associated to a
prototype up to any testable equality, and so we may usefully cache the computation of
this instance together with the prototype." (`poof` §4.2.2). Nix's `__unfix__` is the
visible trace (`poof` §4.2.2). Formally "a conflation can be seen as a Cartesian product
with implicit casts to either component factor depending on context" (`ltuo` §2.3.2);
"Prototype = Spec × Target ... Want to compute a method? Use the target / Want to
inherit? Use the spec" (`rc25`).

**READ.** Why it is *modularity*, not sugar: "developers of reusable libraries are
forced to decide in advance and in utter ignorance which parts of a system they or
someone else may want to either extend or query in the future. Having to choose between
specification and target at every potential extension point leads to an exponential
explosion of bad decisions ... By sparing programmers a decision they lack information
to make, the conflation of specification and target is an essential usability feature
of Prototype OO: it increases intertemporal cooperation between programmers and their
future collaborators (most usually including their future selves) without the need for
communication between the two (which would require time-travel). Thus, in first-class
OO, Conflation Increases Modularity." (`ltuo` §2.3.3). "The conflation of prototype and
instance into an object enables future phasing and extensions without the original
programmers having to anticipate how their code will be used" (`eoomi` §5.3).

**READ.** The rule that goes with it: "Conflation without Distinction is Confusion."
(`eoomi` §5.3; `ltuo` §2.3.4) — the subtyping/subclassing confusion of decades is
exactly "confusing target (subtyping) and specification (subclassing)" (`ltuo` §2.3.4);
"Spec Inheritance: before fix-point / Target Subtyping: after fix-point / DOES NOT
COMMUTE!" (`rc25` "What about Types?").

**READ.** Conflation generalizes: records conflated with functions (T's "closures are a
poor man's objects") are "an implicit product of several things ... We will call this
implicit product a conflation" (`eoomi` §5.2 Conflating Records and Functions);
defaults, type restrictions, visibility, docs, examples, tests, generators are added "as
additional conflated aspects of a prototype" (`eoomi` §5.3 Conflating More Features).
Abstract vs concrete classes, Flavors' mixins vs instantiable flavors, were the
practitioners' implicit recognition (`ltuo` §6.1.8).

**INFERRED.** For a system of named resources, conflation says: the thing a friend
names should be usable *both* as a value to query and as a specification to extend,
without the author having pre-decided which. If "extending X" requires a different kind
of handle than "using X", the design has refused conflation and will pay the
exponential-decision cost.

---

## 6. "A class is a prototype for a type"; classes are second-class; all OO is prototype OO

**READ.** "A Class is a Prototype for a Type." (`eoomi` §6.1); "a class is 'just' a
prototype for a type descriptor" (`poof` §5.1.2); "A class is a compile-time prototype
for a type descriptor: a record of a type and accompanying type-specific methods"
(`ltuo` §2.2.2). Consequence: "class-based languages only have second-class classes
whereas only prototype-based languages have first-class classes" (`poof` §5.1.2); "Class
OO makes classes Second-Class" (`eoomi` §6.1); "Class OO is a lie. There is no such
thing. All OO is Prototype OO. Some of it is used to metaprogram types and procedures
on those types." (`todo`). C++ templates are "a full-fledged Pure Functional Lazy
Dynamically-Typed Prototype OO language at compile-time" (`ltuo` §2.2.3).

**READ.** Type descriptors are richer than static types: "additional constraints on
values beside principal type membership; methods to encode and decode values, to print
and parse them ... default values ... pseudo-random value generators ... algebraic
operations whereby this type implements an interface" (`poof` §5.2.1); "The type
descriptor system can describe itself as well as all pieces of the system, generating
routines for all kinds of automation or user interaction" (`poof` §5.2.4). Typeclass
dictionaries and vtables are the same thing: "Runtime type descriptors correspond to the
'dictionaries' passed around at runtime in implementations of typeclasses ... They also
correspond to the 'vtable'" (`poof` §5.2.5), and the correspondence "can be made
formal, with automated transformations between the two styles (Rideau 2012)" — i.e.
Interface-Passing Style, `lil`.

**READ.** Interface-Passing Style (2012) is the detached-class view: "an interface as
'detached' class information, as the part of an object that doesn't include its state,
and by viewing an object as a 'subjective' interface, one where some state has been
moved into the interface" (`lil` §4.3.1); "Interface-Passing Style separates [behavior
and state], with the interface carrying only the behavior. Object-oriented Style
conflates them" (`lil` §4.3.1). Its sharpest gift is *punning*: "an object can be in the
target type of several interfaces ... simply change the interface, and the same data can
be punned into meaning usefully different things ... Just look through the lens of a
different interface." (`lil` §3.2.3). And a two-way bridge pure ⇄ stateful via a linear
effect model: "From a pure interface, a stateful interface may be deduced by putting the
persistent values in a mutating box ... From a stateful interface, a pure interface may
be deduced by putting ephemeral values in a linearized box that ensures any value is
only modified once" (`lil` §4.2.1); same in `poof` §6.1.1: "a mutable object can be
viewed as a monadic thread of pure object state references, with an enforced linearity
constraint".

**READ.** Typeclasses/traits are "modular but not extensible / Contra Cook:
extensibility matters!" (`rc25` "What about Typeclasses or Modules?"). The remedy is the
*orthogonal protocol*: "requiring specifications (and prototypes and classes) to inherit
from a common ancestor to be able to define a method, means that you cannot add new
methods to specifications after the fact ... This design is terrible, because it
requires omniscience from a class author about all the interfaces that the users of the
class may ever want to satisfy, including, impossibly, about interfaces that do not
exist yet" (`ltuo` §9.2.9); "CLOS generic functions and Clojure protocols enable
programmers to define methods for a class (or typeclass) after the fact ... I will call
this design orthogonal protocol" (`ltuo` §9.2.9). Methods then live on a *pair*: "the gf
on the one hand, and the specification, prototype or class on the other ... This is the
essence of any real solution to the 'expression problem'" (`ltuo` §9.2.10).

**READ — the ecosystem view.** "Programmers don't extend just one class, yielding an
extended class—they extend one class hierarchy ... or even one ecosystem, yielding an
extended ecosystem." (`ltuo` §9.3.7); "The impossible extension ownership conflicts
dissolve, when one realizes the unit of coherent extension was never the individual
class or object or function, but the entire program or library being modified." (`ltuo`
§9.3.7); "Keeping all your code in a vast open recursion until the very last moment ...
instead of a single global context that you side-effect, you can have many lexical
variants of context that you update non-destructively" (`todo`); "Global fixed-point of
entire namespace (nixpkgs…)" (`rc25`). And the line most relevant to any
content-addressed design: **"a name path or location properly identifies an extensible
'intention' rather than an immutable 'extension', a meeting point rather than fixed
code ... If users wanted the latter, they would be using cryptographic hashes, not
names."** (`ltuo` §9.3.7).

**READ.** Subjective dispatch — a *point of view* as a dispatch argument: "'subjective
dispatch' ... wherein some context provides an implicit extra argument to a method
call ... Slate allows for a dynamically bound subject"; it only has teeth in first
position: "Subjective dispatch in first position can then enable context-dependent
methods to completely override the meaning of programs in arbitrary ways" (`ltuo`
§9.3.6).

---

## 7. Mutation, identity, and code upgrade — the honest list of questions

**READ.** "mutability of object fields ... is completely orthogonal to the essence of
OO" (`ltuo` §6.3.1); "mutation or lack thereof are not an intrinsic property of
computations, but only of some representations ... an attribute of the map, not of the
territory" (`ltuo` §6.3.4). The usable rule for stateful OO: "inheritance hierarchies
are being set up before they are used, but don't change while being used though they
might change before, after and between uses" (`eoomi` §7.1 Mutation).

**READ.** But *changing the specification of a live system is code upgrade*, and he
refuses to pretend it away: "updates to the inheritance structure of OO specifications
can be seen as a special case of code upgrade in a dynamic system ... The only popular
programming language that fully addresses all these code upgrade issues in its defined
semantics is Erlang" (`ltuo` §6.3.2); upgrades should "only happen when the system is
'quiescent'" (`ltuo` §6.3.2, citing PCLSRing). The questions he says a designer *must*
answer: "what to do with previously computed targets when a specification is updated:
Should a target once computed be left forever unchanged ...? Should a target be wholly
invalidated, losing any local state ...? Should some 'indirect' properties be cached,
and if so how is this cache invalidated ...? Should a protocol such as
update-instance-for-redefined-class be invoked ... eager or lazy ...? Should a class
maintain at all times and at great cost a collection of all its instances ...?" (`ltuo`
§6.3.2). And the verdict on systems that dodge: **"Languages that assume 'purity' or
absence of code upgrade thereby deny these issues, and leave their users helpless,
forced to reinvent entire frameworks of identity and update so they may then live in
systems they build on top of these frameworks, rather than directly in the language
that denies the issues."** (`ltuo` §6.3.2).

**READ.** Cache invalidation has three honest regimes: never cache (T, JavaScript);
"purity-by-default and cache all the computations it can ... up to users to explicitly
create cells"; or track mutations pervasively, "at which point the language is more in
the style of higher-order reactive or incremental programming" (`poof` §6.2).

---

## 8. The semantic tower; first-class implementations; reflection without a fixed bottom

**READ.** Computations as categories: "a computation as a category in which nodes are
the potential states of the computation and arrows are the transitions between those
states" (`fci` §2.1). "An interpretation of a concrete computation C as an abstract
computation A is a partial functor Φ from C to A. Its inverse is called an
implementation of A with C" (`fci` §2.1). Properties: soundness, totality,
completeness, bounded liveness, and "our biggest contribution is the notion of
observability, that allows to retrieve an abstract computation state from an arbitrary
concrete computation state, by first synchronizing to an observable state ...
Observability generalizes PCLSRing" (`fci` §2.2). Safe points: "a generalized notion of
safe points that enable observing a computation at a higher-level than that at which it
runs, and therefore to climb up the semantic tower, when at runtime most existing
systems only ever allow but to go further down" (`climb` abstract; arXiv 2606.04034,
June 2026).

**READ.** Migration is the universal operation: "a given abstract computation A can be
implemented with a computation C with an interpretation Φ; and if Φ is observable, then
C can be interrupted, an abstract state can be retrieved from its concrete state, and
that state can be re-implemented with another computation K" (`fci` §4.1); "JIT
compilation, software upgrade (including database schema upgrade), dynamic refactoring,
can be viewed as migration" (`fci` §4.1); "migration consists in interacting with
software by changing semantic layers below" (`fci` §4.1). Tooling becomes natural
transformations: "Code instrumentation, tracing, logging, profiling, single-stepping,
omniscient (time-travel) debugging, code and data coverage, access control, concurrency
control, optimistic evaluation, orthogonal persistence, virtualization,
macro-expansion ... all these techniques can be seen as natural transformations of
implementations" (`fci` §4.2).

**READ.** The architecture: for every computation "(1) the topmost computation that is
being computed, that is fixed, specifies the desired semantics of the tower, and limits
the access rights of all implementations, (2) and the bottommost computation that
currently implements the above, that can be arbitrarily changed within those access
rights" (`fci` §5.1); "every computation has its controller" and "there is a tower of
controllers" (`fci` §5.1; `thesis` §8.3: "it's puppeteers all the way back, with no
ultimate back wall"). "From the point of view of the application, I/O effects are system
calls into an outside program, the controller ... (in categorical terms, effects are a
free monad)" (`fci` §5.2). "With reflection, there is no more fixed bottom for software.
All software by construction runs virtualized, just not at the CPU level, but instead at
the level of whatever language it is written in" (`fci` §5.3).

**READ.** Full abstraction is the precondition: "computations must all have a clear
opaque bottom: (1) it must be perfectly clear what the bottom is; and (2) the bottom
must be totally opaque, such programs above cannot see below" (`thesis` §8.5.1); "A
fully abstracted value may only be used according to the interface specified by the
abstract variable type" (`ch06` Abstraction); "There is no supported way for code to
distinguish between 'normal' and 'virtualized' machines" (`ch08` Activity Sandboxing).

**READ.** Turtles: "Houyhnhnm computer systems ... can dynamically add new layers below a
running program ... Every turtle is unique, but no turtle is special." (`ch04` Building
up vs building down); "if you wrote a program in abstract language A, and specified a
given implementation I of language A generating code in concrete language C, then you
actually specified a program in language C. And as long as you don't proceed to make
modifications at the lower level of language C that invalidate the abstraction to
language A, then you can remove the constraint, go back to the level of program A, and
later choose a different implementation I'" (`ch04` Meta-level Strategies). Reflection
is the *pointing*: "the magic was in the pointing all along: in the ability to translate
semantics into those elegant LAMBDAs, rather than in the elegant but ubiquitous LAMBDAs
themselves" (`els26` "My Answer (2)"); and today's languages fail "below the line":
"Lisp makes it exceptionally easy to extend the language 'from above', but doesn't help
extend it 'from below'" (`els26` "Not Below the Line").

**READ.** The MOP sketch: "Add serialization, persistence, to a meta-object, NOT to the
object. Different capabilities for objects and their meta-objects => more security."
(`ltuo` §10.7); and he already lists a ZK layer as one slice of a tower: "(d) the
execution is interpreted as pure transitions of a low-level virtual machine so a
zero-knowledge proof of faithful execution can be produced" (`ltuo` §10.7.1).

**READ.** Against fixed VMs (Urbit): a frozen semantics "doesn't actually make for
robust persistence ... it prevents future improvements and fixes while encouraging bad
practice" (`ch10` Future-proofing the wrong thing). "A global consensus on deterministic
computation semantics only matters if you want to replay and verify other random
people's computations, i.e. for crypto-currencies with 'smart contracts' like
Ethereum ... If you only want to replay your own computations (or those of friends),
you don't need a global consensus on a deterministic function; you only need to know
what you're talking about, and write it down." (`ch10`). Jets: "you must implement
things twice ... And how do you ensure the equivalence ... You can fail to, or lie"
(`ch10` Impedance Mismatch), and the fix he names: "if only you had an advanced
metaprogramming infrastructure capable of manipulating arbitrary program semantics in a
formally correct way! You might then automatically generate both the Nock code ... and
the supporting u3 code ... and be confident they are equivalent" (`ch10`).

---

## 9. Modularity and extensibility: the criteria, the four classes, open vs closed

**READ.** The criteria (his italics removed):
- "A design is modular if it enables developers to cooperate without having to
  coordinate, compared to alternative designs that enable less cooperation or require
  more coordination" (`eoomi` §2.1); "coordination counts negatively, in the column of
  costs" (`ltuo` §4.1.3 fn).
- "A design is incremental if it enables developers to enact change through small local
  modifications compared to alternative designs that require larger (costlier) rewrites
  or more global modifications (or prohibit change, same as making its cost infinite)."
  (`eoomi` §2.2); later renamed extensibility: "A design is more extensible if it
  enables developers to enact more kinds of change through smaller, more local
  modifications" (`ltuo` §4.2.3).
- Together: "Modularity means you only need to know a small amount of old information
  to make software progress. Incrementality means you only need to contribute a small
  amount of new information to make software progress." (`eoomi` §2.3).

**READ.** Modularity "is the organization of software source code in order to support
division of labor" (`eoomi` §2.1) and is "first and foremost meta-linguistic" (`ch09`
The Elusive Formalization); "Modules do not solve a problem of information to show or
hide, but of responsibilities to negotiate, of incentives to align. The problem they
solve is not logical, but social." (`ch09`). The four classes: "Entities are
first-class if they can be manipulated as values at runtime ... second-class if they
exist at compile-time ... third-class if they are automated by tools outside the
language ... fourth-class if they are notions in the programmer's head" (`ltuo` §4.1.2);
"Fourth-class entities include design patterns" (`ltuo` §4.1.2); "(Design) patterns
mean 'I have run out of language.'" (`ch04`, quoting Hickey). OO is the *internal*,
first-class embodiment: "We dub prototype such an embodiment of incremental modularity
within a language." (`eoomi` §3.1).

**READ.** Internal extensibility defined: "the ability to extend, refine or modify a
software entity without having to read, rewrite, or modify any of the previous
functionality, indeed without having to know how it works or have access to its source
code, only having to write the additions, refinements and modifications" (`ltuo`
§4.2.2). Forking is the external alternative and its cost: "external extensibility
through editing ... means that these entities are 'forked', which in turn reintroduces
complexity in the maintenance process, as propagating bug fixes and other changes to
all the forks becomes all the harder as the number of copies increases" (`ltuo` §4.2.6).
Patches are "maximum extensibility, minimum modularity" (`ltuo` §4.2.5).

**READ.** Open vs closed, precisely: ML modules "cannot inside the language define an
extension in a modular way: definitions from one module cannot implicitly refer to
definitions supplied later by independent extensions into their eventual combination"
(`ltuo` §4.3.1); UML/coalgebras/relational models "fail to model OO precisely because
the 'classes' they specify are mere types: they lack the module context that enables
self-reference" (`ltuo` §4.2.5). "Two Mindsets: Compositionality for reducible problems
/ Extensibility for irreducible problems" (`rc25`).

**READ.** "Runtime Processes Make Bad Compile-Time Modules": microkernels/microservices
"add low-level runtime barriers that do not improve safety compared to language
barriers" and "Modularity is a matter of semantics, as manipulated by programmers at
programming-time, and by compilers at compile-time; the runtime barrier crossings of
these myopic designs cannot conceivably do anything to help with that, only hinder"
(`ltuo` §4.1.5.1); the valid reason to split is socioeconomic (Conway) (`ltuo`
§4.1.5.1). "The programming language types are the communication types" (`ch07`).

**READ.** Names: "Names allow to express fixed intent in an ontology where the extent
will change" (`ch08` What's in a Name?); a module name is "a Schelling point where the
plans of sentient beings meet with the fewest coordination issues" (`ch09` Global
Namespace); "a name, which denotes a fixed intent, may refer to varying content" (`ch09`).

---

## 10. Orthogonal persistence: a friend never "saves"

**READ.** The Sacred Motto: "I object to doing things that computers can do." (`ch02`;
attributed to Olin Shivers in `ltuo` §4.1.2). Persistence by default: "make data
persistence the default, at every level of abstraction ... the change you made will
remain in the system forever" (`ch02`). "The adjective 'orthogonal' means that the
persistence of data is a property of the domain you're working in, as managed by the
system; it is not an aspect of data that programmers have to deal with in most
ordinary programs" (`ch02`). The 2024 model: "Orthogonal Persistence essentially
reverses the burden of persistence: all state changes are safely written to persistent
storage by default, and escaping into transience is the edge case sometimes invoked
for performance" (`persist` Persistence by Default); "Houyhnhnms do not have any
library to manage persistence; instead, Houyhnhnms have a number of libraries to manage
transience." (`ch04`).

**READ.** What remains once persistence is automatic — six issues "reframed upside down
into not having been Persistence issues after all": "persistence domains, atomicity,
synchronization, publishing, resource exhaustion and schema upgrade" (`persist` intro).
- **Domains**: "logical entities having a persistent identity, and how they are
  dynamically mapped down to various underlying substrates" (`persist` Domains);
  "ordinary programs don't know and can't even possibly know which domain they will be
  running in, and letting them query those details would be a breach of abstraction ...
  only programs with adequate capabilities can manipulate the persistence and privacy
  levels of computing domains, except of course to deliberately spawn a subdomain with
  yet strictly fewer capabilities" (`ch02`). Nested like `(me (work ...) (home ...)
  (secret ...))`; "Origin Domain Validates Copy Out / Share Out; Destination Domain
  Validates Paste In / Share In" (`pslides`).
- **Atomicity = anti-transactions**: "atomicity is managed with explicit atomic
  sections: code that produces intermediate states that should not be persisted is
  wrapped in such sections ... Code that contains atomic sections can be freely
  composed with other code containing atomic sections" (`persist` Atomicity). Versus:
  "Transactions are Bad: Require Global Knowledge, Don't Compose, Always too small or
  too big ... Necessary because processes don't persist" (`pslides`); atomic sections
  "say 'don't cut the computation here' which only depends on local knowledge";
  transactions "say 'cut the computation exactly here' which requires global knowledge"
  (`persist` Modularity). "Database Transactions are the wrong Abstraction" (`pslides`).
- **Synchronization**: "explicit memory barriers: an instruction or procedure that
  pauses evaluation until after the changes so far are committed" (`persist`
  Synchronization); "every asynchronous message sent to a persistent process must (1)
  be idempotent, and (2) can only be sent after a memory barrier" (`persist`); "Don't
  Commit, Synchronize" (`pslides`).
- **Publishing**: "you never have to *save* a file, yet you still once in a while have
  to *name* or *tag* a version" (`persist` Publishing); "explicitly tagging a version of
  their data as suitable for sharing, and granting select others a capability to access
  the tagged version on a replica" (`persist`); "Never Save and Copy, Publish and Share"
  (`pslides`).
- **Resource exhaustion**: quotas per domain; "processes are stopped when they run out
  of space, and can be resumed after space issues are solved; space is reserved so
  special debugging processes can run inside the scope of a stopped process" (`persist`).
- **Schema upgrade**: §11 below.

**READ.** What the system logs: "the persistence log doesn't need to record anything else
but these events with their proper timestamp ... This however, requires that all sources
of non-determinism are either eliminated or recorded" (`ch03` Dealing with Bad
Memories); retention is the end-user's choice, not the programmer's (`ch03`). Data is
ADTs, not bytes: "all Houyhnhnm computing data is defined in terms of Algebraic Data
Types, independently from underlying encoding ... the very notion of file doesn't
apply"; access paths are "a list of accessors" (`ch03` Data at the Proper Level).
"the source is the semantic state of the system, on which change happens, and from
which the text is extracted if and when needed" (`ch03`).

**READ.** Versioning is system-wide and virtualization is branching: "In Houyhnhnm
computing systems, there are no applications and no 'save' buttons" (`ch03`); "infinite
undo comes for free on any kind of data" (`ch03`); "virtualization is merely the ability
to branch the history of changes in the system ... all destructive or catastrophic
experiments happen in branches that are never merged into the official reality";
"only merge into reality those transactions that pass all checks"; "It is also possible
to branch only part of the system while the rest of the system remains shared" (`ch03`
Virtualization as Branching). "you built the entire system on top of monotonic storage
that never loses data by construction, so that all programs get in(de)finite undo by
default. Extra performance, not correctness, is what requires additional work." (`snapl`
§4.3). Deletion is deliberate and leaves a trace (`ch02`).

**READ.** The monitor: "a simple but complete computing system ... it also specifically
understands enough of the semantics of the regular system to inspect it, fix it, and
restart it" (`ch03`); "Stop processes & escape to metasystem" (`pslides`).

**READ.** Persistence of *processes*, not just data: "Persisting Continuations
simplifies everything else" (`pslides` Thesis recap); the high-level route is
"Continuation-Passing Style will make stack frames into objects; lambda-lifting will
make lexical scope into objects; various explicit monads will make the context of as
many effects into objects" (`persist` Persisting Execution Context). Full abstraction
between roles: "App developer not allowed to see how data is persisted / Persistence
Implementer not allowed to see data / User or Admin can configure service and
providers" (`pslides`).

**READ.** What makes it *safe* is capabilities, and persistence raises the stakes:
"Orthogonal Persistence does make low-level errors extremely undesirable: memory
corruption, type mismatches, bad indexes, resource leaks, fork-bombs, security
breaches, etc., will persist and permanently corrupt the system state" (`thesis` §7.3.5);
"Reflection is necessary to inspect processes, modify them, salvage the runaway ones.
Yet some form of protection from unauthorized tampering is necessary. This calls for
some kind of capability-based architecture" (`persist` Long Range Issues); "Flag
whoever reaches for forbidden capabilities as hostile ... whether code is written by
humans or AI!" (`pslides`).

---

## 11. Non-stop change: live upgrade, schema migration as a first-class transaction

**READ.** "To program is to change programs, and to change programs is to program."
(`ch05` Change Comes from the Inside); "To Houyhnhnms, change happens inside the
computing system that changes, because everything relevant is ipso facto inside the
system, part of its ontology" (`ch05`); the issues of upgrade "all but disappeared if
you considered code change transactions as first-class objects" (`ch05` intro).

**READ.** The mechanisms, item by item (`ch05` Automating Live Upgrade):
- "a notion of transactions for code and data upgrade, that can be composed and
  applied atomically";
- "each change is always run in its own virtual fork of the system, where failure is
  quite acceptable";
- "type systems track how incoherent the system is, and maintain for the programmer a
  to-do list for those parts of the system that haven't been updated";
- "require every type modification to be accompanied by a well-typed upgrade function,
  taking an object in the old type and returning an object in the new type";
- "linear logic to ensure that when writing an upgrade operator, you must explicitly
  drop any data that you don't care about anymore, so you can't lose information by
  mistake or omission";
- "upgrade functions can be overridden at the granularity of individual variables";
- "tracks the difference between on the one hand renaming some variable, and on the
  other hand deleting some variable and adding another";
- "effective history ... made of coherent changes that describe how to upgrade from
  previous released versions to the latest one" vs "actual history ... often made of
  incoherent changes, of backing from blind alleys";
- "Histories themselves constitute a monotonic algebra where it is always possible to
  merge histories".

**READ.** The cheap cases are cheap: "the case that is easy in Human computer systems,
namely eschewing any upgrade and dropping the old data is just as easy ... just don't
upgrade the data, and instead drop it, as you modify the code" (`ch05`); and "you can
simply fork the old data together with the correct version of the code that knows how
to create and manipulate it ... computation itself is immortal" (`ch05`). A
representation-only change is "decompile and recompile" (`ch05`). In the 2024 model:
"Schema Upgrade is a regular part of the development activity. Variables and fields
being added include initial or default values or formulas; class redefinitions include
migration methods; regression tests include data migration tests" (`persist` Schema
Upgrade); "just by not forgetting the code history, and instead making schema evolution
a regular part of the programming language" (`persist`). "Never Migrate, Upgrade and
Reconfigure ... Normal operations, not million-dollar crises" (`pslides`).

**READ.** Persistence does not require agreement with anyone else: "Persistence doesn't
require anyone to agree with other people on a low-level protocol; it only requires each
person to maintain compatibility with their own previous data ... what they need is to
remember the old code and data, and to be able to express the new code (generator) in
terms of the old one (to upgrade the code) and able to interpret the old data schema in
terms of the new data schema (to upgrade the data)." (`ch10`). "allowing for divergence
creates an incentive towards convergence" (`ch10`).

**READ.** Hot-patching as a scaling necessity: "Hot-patching effectively decouples the
release cycle of multiple pieces of software—a necessity for large systems ...
Ecosystems without hot-patching just cannot scale" (`ch09` Code Instrumentation).
Relinking "without any interruption in the music, with an atomic code switch at a time
the buffers are in a stable state" (`ch06` Runtime and Compile-time Enforcement).

**INFERRED.** Put §7 and §11 together and his position on "re-genesis" is unambiguous:
wiping and re-creating is the *degenerate* upgrade ("drop it") and must be *available*,
but a system whose *only* upgrade is wipe has refused to internalize change and is
"den[ying] these issues" (`ltuo` §6.3.2). The Houyhnhnm bar is: an upgrade is a typed,
linear, composable transaction applied in a fork, with an upgrade function per changed
type, overridable per variable, and a to-do list of incoherence.

---

## 12. Kernel is as kernel does; platforms, not applications; IPC at the meta-level

**READ.** "What is it that a kernel does?" — resource management, access control,
abstraction, enforcement, bootstrapping — and none of these defines one (`ch06`).
Resource management is "an inherent aspect of most programs ... The simplest idiom for
that is to use a proxy, a handle ... More advanced idioms include using some variant of
what we call linear logic" (`ch06` Resource Management). Access control: "explicit
primitives in their programming language to let programmers define the access
abstractions that fit their purposes" (`ch06`). Enforcement: "the invariants that
ultimately matter in a computing system are never those that underlie any 'base'
system; instead, they are always those of the overall system, the 'final' applications,
as experienced by users ... a kernel that possesses a monopoly on invariant
enforcement, is absurd on its face" (`ch06` Enforced and Unenforced Abstractions); "each
activity is properly isolated and its invariants cannot be violated by any other
activity, except those that explicitly run at its meta-level" (`ch06`); "Most invariants
can be enforced statically by the high-level language's compiler" (`ch06`);
"Overriding invariants, while possible, requires special privileges and will be logged"
(`ch06` Polycentric Order). "as many 'kernels' as there are computing subsystems" (`ch06`).
Bootstrapping: "the time to restart a Houyhnhnm system is never more than the time to
page in the state of the working memory" (`ch06`). Enforcement is "achieved through
mutually agreeable contracts between equally free parties" (`ch06`).

**READ.** Platforms: "Houyhnhnms don't have a notion of application ... they think in
terms of platforms that they extend with new functionality" (`ch07`); "programmers do not
write standalone applications in non-autistic cases; instead, they write new modules
that extend the capabilities of the platform ... a new picture compression format is
automatically usable by each and every function that uses pictures throughout the
system" (`ch07`). The expression problem is acknowledged, not waved away: when one module
adds entities and another adds interfaces, "a further module may define how to handle
these new combinations; or a suitable generic fallback may have been provided with the
new interface; or lacking any of the above, the system will fail and drop to its
metasystem" (`ch07`). Extension languages: ad hoc ones "usually end up with a very
badly designed language"; the platform instead gives "domain-specific languages, type
systems, contracts" (`ch07`). "If you don't build DSLs, your general purpose language has
all the downsides of Turing-equivalence with none of the upsides." (`ch10`). Build
systems are the same lesson: "growing the system happens by enriching the normal
programming language with these features, not by building a new minilanguage" (`ch09`).

**READ.** Using is programming: "there is no difference between using and programming;
if anything, the difference between a programmer and a user, is that the programmer
knows there is no difference" (`ch07`; `snapl` §3.4: "a single, simpler interface, in
which a same language may be either spoken or written").

**READ.** IPC: "Implicit communication is controlled by the users of a program rather
than by the programmers who write it" (`ch08`); "presenting data to the end-user is the
job of a meta-program separate from the activity that displays the data" (`ch08`);
composition is "of programs of arbitrary types, with arbitrary numbers of inputs and
outputs all of them properly typed according to some high-level object schema" (`ch08`);
"Communication channel names become regular identifiers of the programming language;
the language lets programmers use dynamic binding to control these identifiers" (`ch08`);
servers move "completely to a separate meta-program that controls the process you
communicate with" (`ch08`). "persistence ... means you can give a stable name to a
stable activity" (`ch08`). "There can be no bugs in all the lines of code that the
programmers don't have to write anymore." (`ch08`). "metaprogramming requires free
availability of sources" (`ch08`).

---

## 13. Points of view

**READ.** The whole series opens on it: "The fundamental difference between Human
computer systems and Houyhnhnm computing systems is one of point of view." (`ch01`);
"Humans have computer systems, Houyhnhnms have computing systems" (`ch01`) — things vs
processes, "which always involves wetware first" (`ch01`). Simplicity is measured from
that view: "a short description when you take into account the entire software system,
including the compiler, interactive editor, formal verification tools, libraries,
operating system, drivers, hardware blueprints, etc., and including the informal
conventions" (`ch01`).

**READ.** Technical points of view he gives first-class standing: (a) *interfaces as
lenses* on the same data — "the same data can be punned into meaning usefully different
things ... Just look through the lens of a different interface" (`lil` §3.2.3); (b)
*focused specifications* — a specification carries "a path from the top of the program
state to the module context being referenced" (`ltuo` §9.1.2); (c) *subjective
dispatch* — a context as hidden first argument (`ltuo` §9.3.6); (d) *the semantic
tower* — "developers may focus on some aspects and ignore others depending on the level
of abstraction at which appear the issues they are battling with" (`fci` §3.2), and
*observability* lets one view a running concrete thing abstractly (`fci` §2.2); (e)
*domains* — the UI "makes it clear at all times which domain you're currently working
with" (`ch02`); (f) *purity vs state* — "Purity or statefulness is a matter of the
programmer's point of view, not intrinsic properties of the underlying computation"
(`ltuo` §10.7.1). Replay scope is a point of view too: "you can specify the scope and
context in which you replay some computation, within the resources that you control"
(`ch07`).

**INFERRED.** A "view" in his sense is never a copy and never a weaker object: it is the
same target seen through a different interface/lens/level, and the lens is itself a
first-class, composable thing. A narrowing that produces a *new* object the original
cannot be recovered from is a fork, with fork costs (`ltuo` §4.2.6).

---

## 14. Division of labor: the four roles, blame, time preference

**READ.** Four roles on any module: "1. Authors write and modify the code ... 2. Users
refer to the code by name while abstracting over its exact contents ... 3. Integrators
assemble a collection of modules into an overall application ... 4. End-Users use a
software assembly while remaining blissfully unaware" (`ch09` Social Roles). The design
law: "one author's or integrator's choice of which sets of which modules to use in which
specific version does not and cannot bind anyone else's"; "if it fails to serve one or
more of the roles, or requires a person having a role to specify information that only
people with other roles may know, then it is a deeply dysfunctional design" (`ch09`).
"Free software, by decoupling the roles of author and integrator, make it possible to
solve DLL hell" (`ch09`). Building "from source control", a network of branches
promoted by tests, "HEAD" as one node of it (`ch09` Out of DLL Hell).

**READ.** Economics of platforms: "Developer talent is stretched thin, as the same tasks
are done over and over, once per application"; "experts of any given domain can focus on
their domain of expertise ... need only do it once per platform" (`ch07` Programming
Incentives). Persistence shifts who answers to whom: "Admins answer to Users, not to App
Vendors" (`pslides`); administrators "whose interests are better aligned because they
will be liable in case of malpractice" (`ch03`).

**READ.** Responsibility: "When a casual user mistake causes a tool to fail
catastrophically, fools blame the user who operated the tool; wise men blame the
toolsmiths who built the tool." and one level up, "wise men blame the programming
language designer" (`ch11` Bad Tools); blame is *subadditive* (`ch11` The Blame Game).
Low time preference: "general principles ... largely independent from whatever
technology is 'at hand'" (`ch11`).

**READ.** AI agents as developers change the numbers, not the principles: "AIs too will
eventually hit complexity walls; factoring code in good ways that promote reuse across
agents will be essential for AIs to cooperate together" (`ltuo` §11.3.2); "A tight
virtual machine that is safe so users don't need to reboot or deal with corrupt state,
one that is easily extensible from the inside without having to go through long
compilation cycles—that's what a fast AI will want" (`ltuo` §11.3.3). "OO is for
programmers who are more ambitious than clever." (`ltuo` §11.3.2).

---

## 15. What Houyhnhnm computing demands of a system friends live in

Collected from the above, as checkable demands (each line cites where it comes from):

1. **Persistence is the domain's property, never the program's.** No save, no load; the
   log is the user's events plus recorded non-determinism (`ch02`, `ch03`, `persist`).
2. **Atomicity is local ("don't cut here"), synchronization is a barrier, messages out
   are idempotent and post-barrier.** Transactions as the global unit are "the wrong
   abstraction" (`persist`, `pslides`).
3. **Publishing is tagging + granting a capability to a replica**, not copying
   (`persist` Publishing).
4. **Everything is a partial specification that can be extended by someone who did not
   write it, in-language, without forking**; dependencies between specifications are
   declared and linearized, not hand-ordered; concurrent extensions of one aspect
   combine (`eoomi`, `ltuo` §7, §9.2.9, §9.3.7).
5. **The named thing is both a value and a spec (conflation)**, and names are meeting
   points for changing content, not hashes of fixed content (`ltuo` §2.3, §9.3.7).
6. **Change is inside the system**: typed, linear, composable upgrade transactions,
   applied in a fork, with a to-do list of incoherence; renames ≠ delete+add; effective
   history ≠ actual history (`ch05`, `persist`, `ltuo` §6.3.2).
7. **No single kernel with a monopoly on invariants**: each activity enforces its own
   invariants, statically where possible; overriding is privileged and logged (`ch06`).
8. **Platforms, not applications**: new kinds of entity become usable by every existing
   interface; new interfaces can be attached to existing entities after the fact
   (`ch07`, `ltuo` §9.2.9).
9. **Full abstraction with first-class implementations**: the top of each tower is fixed
   and limits rights; the bottom can be migrated while running; a controller per
   computation; observability/safe points so any live thing can be viewed abstractly
   (`fci`, `thesis` §8).
10. **Points of view are lenses**, first-class and composable, never copies (`lil`,
    `ltuo` §9.1).
11. **Four roles, never conflated**: authors, users, integrators, end-users; the
    integrator's HEAD is one branch among many (`ch09`).
12. **Using is programming**: one language, spoken or written, with a continuum of
    proficiency; DSLs are internal, not bolt-on (`ch07`, `snapl`, `ch10`).
13. **The monitor**: a small complete system that understands the big one well enough to
    stop, inspect, fix and restart it (`ch03`).
14. **Sources are available to the meta-level**; a black box is "crippled" and runs in a
    paranoid sandbox at the periphery (`ch08`).
15. **Low time preference**: general principles over the tool at hand (`ch11`).

---

## Appendix: sources I looked for and did not find, or could not confirm

- A standalone 2022–2026 *paper* on OO foundations beyond the 2024 EOOMI draft: none
  found. Everything later is the book draft (`ltuo`, text says "these days, in 2026")
  and talks (NJPLS 2023, LambdaConf 2024/2025, RacketCon 2025, SHU 2025, ELS/ELTE 2026).
  The README says "After giving up on getting a paper published on my broader ideas
  about OO, I (Faré) am instead preparing a book" (`sources/poof-readme.md`).
- "COOP 2023" in the slides ("'Specifications': COOP 2023 (by yours truly) / No
  classes, not even objects!") is the `coop.rkt` library inside `metareflection/poof`
  (`rc25` "This very Presentation!"), not a separate publication. Not fetched as code.
- The POOF paper is **not** on arXiv (arXiv author search for Rideau returns only
  "Climbing Up the Semantic Tower -- at Runtime", 2606.04034, 2026-06-01).
- The 2016 "theory of Modularity" he cites as "Rideau (2016)" / "sketched in Rideau
  (2016)" — not located under fare.tunes.org/files; probably a talk. Not read.
- "Who Controls Your Computer? (And How to make sure it's you)" speech, cited in
  `ch10`: not fetched.
- The tweets: 0 of 7,346 had arrived at the time of the first draft (see §0 and
  `sources/tweets-oo.md`).
