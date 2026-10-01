# AUDIT — Mini (minidregg) against Faré's foundations of OO and Houyhnhnm computing

Lane FAREOO, 2026-10-01. Companion to `FAREOO.md` (the principles, with citations into
`sources/`). This file holds Mini up to them: where it agrees (cite the file), where it
contradicts or falls short (cite the file and the exact mechanism), and what the
Houyhnhnm-shaped alternative is **in Mini's own terms** — cells, laws, capabilities,
turns, documents, rooms, the registry, the semantics digest. Findings are ranked by how
much they change what friends can do; each carries an honest cost (what re-emits, which
theorems move) and a falsifier.

What I read (nothing was built or run; I wrote nothing outside `~/dev/fareoo`):

- Mac: `/Users/ember/dev/claudesplosion/planning/{DATAMODEL,PLACE,SURPASS,EVAL,COMPUTE,DEOS,PRIVACY,MUD,CHANNELS}.md`,
  `SESSION-STATE.md` (head), `planning/place/p-templates.md`, `planning/privacy/k-narrow-hide.md`.
- persvati (read-only, over ssh), `P/` = `/home/ember/build/mini-datamodel-20260930/final-warm-b/src`
  at `7961b345` (UMBRELLA-SPLIT): `README.md`, `PROJECT.md`, `ATLAS.md`, `docs/DURABLE-STORE.md`,
  `docs/DISTRIBUTED-DESIGN.md`, `Kernel/World.lean`, `Kernel/ResourceTransaction.lean`,
  `Pred/Core.lean`, `Theory/TypedAuthorization.lean`, `Theory/PolicyInstall.lean`,
  `Theory/CanonicalReactiveView.lean`, `Theory/ViewMerge.lean`, `Compiler/CanonicalCellRegistry.lean`,
  `Compiler/CanonicalRuntimeProfile.lean`, `Kernel/NativeObservationController.lean`; listings of
  `Theory/`, `Kernel/`, `Compiler/`, `Pred/`; greps for `migrat`, `upgrade`, `policyAddress`,
  `semantics`.
- Faré: everything in `FAREOO.md`; citations below use its keys (`ltuo`, `eoomi`, `poof`,
  `chNN`, `persist`, `fci`, `rc25`, `lil`).

Tags: **READ** (cited), **ASSUMED** (mine, listed in §6), **PROPOSED**. Verdicts:
**AGREES** · **AGREES, UNBUILT** (the design says it, the tree does not yet) · **FALLS
SHORT** (the mechanism is weaker than the principle) · **CONTRADICTS** (the design chose
against the principle) · **FORK** (two defensible designs; the choice is taste or custody).

---

## 0. The verdict in one paragraph, and the table

Mini is Houyhnhnm where Faré's principles are about *the world*: persistence is the
Store's property and no friend ever saves; history is a fold of signed, deterministic
turns with checkpoints and an audit; authority is attenuation ("only connectivity begets
connectivity") with revocation as a theorem; every activity carries its own law; the
Lean admit function is the implementation, not a model beside one; sources are open; and
the decision to referee compute by re-execution rather than by a proof system is the one
Faré's Urbit chapter argues for a world of friends. Mini is *not* Houyhnhnm where Faré's
principles are about *specification* — the half that is actually OO. In his own
vocabulary (after Wegner): "I concur with Wegner (1987) in calling 'object-based' those
languages and systems that provide internal modularity (first- or second-class) without
internal modular extensibility, while reserving 'object-oriented' for languages that do
also offer inheritance" (`ltuo` §3.2.3) — **Mini today is object-based**: cells with
laws are first-class modules; nothing in the world extends anything else in the world. A law is one closed
first-order `Pred` installed on one cell by replacement; it has no `self`, no `super`, no
parents, and the only way for B to "extend A's law" is to copy A's JSON — a fork. Cell
kinds, verbs, factory templates and evaluators are closed inductives and pinned profile
constants compiled into the Host, so every new kind of thing a friend might want is a
rebuild, a semantics-digest bump and a re-genesis — and re-genesis, which Faré calls the
degenerate "drop it" upgrade, is Mini's *only* upgrade, by doctrine. Templates (the
closest thing to a prototype) are files rendered by a Python script with a Nat→name map
that the kernel never sees: fourth-class in his taxonomy. The three things to do first
are the three that turn "extend together" from a slogan into a mechanism: laws that
inherit along the room tree and from named parent laws (linearized, conjunction-combined,
refusals naming the ancestor clause); kinds and templates as prototype cells in the world
(a birth says `from`), so a friend can mint a kind without the operator rebuilding the
Host; and the flag day as a Lean-checked, linear *carry* from the old Store to the new,
so re-genesis keeps what it claims to keep by theorem rather than by shell script.

| # | principle (FAREOO §) | Mini today | verdict | alternative in Mini's terms | rank |
|---|---|---|---|---|---|
| 1 | laws as partial specs with `super`; inheritance = composition (§1–3) | one `Pred` per cell, installed by replacement; `PolicyInstall.Source.previous` is a version chain, not a parent | **CONTRADICTS** | `LawRef` parents + the `parent` tree as implicit ancestry; C3-linearized conjunction; `super/…` leaf reporting | **1** |
| 2 | classes = prototypes for type descriptors; first-class kinds (§6) | `CanonicalCellRegistry.Kind` closed inductive; `Verb` closed inductive; `FactoryTemplate` pinned in the runtime identity | **CONTRADICTS** | a `kind` cell (layout descriptor + default law + name map + init); births `from`; verbs as data over a fixed small core | **2** |
| 3 | non-stop change; upgrade functions; forks (§7, §11) | re-genesis, "no migration", old bytes refuse to load; GENESIS-CARRY is a shell script | **CONTRADICTS** (by doctrine) | `Compiler/Carry.lean`: linear `World_v → World_{v+1}` with named drops, applied to a cloned Store, audited; the semantics-digest chain as the effective history | **3** |
| 4 | orthogonal protocols; extend things you do not own (§6, §9) | a law is attached to one cell; cross-cell reference by `joint/target/{cellId}`; room laws govern management only | **FALLS SHORT** | room-scoped laws over `under R` (= inheritance from the room, finding 1); role-named references through the room index | 4 (folds into 1) |
| 5 | points of view as lenses; same data, many interfaces (§13) | `Scope.fields` narrowing; hiding root; `view at`; observation ships whole cells; name maps live in template files | **FALLS SHORT** | name maps as cells (an "interface" cell); per-address openings (planned K-FIELDS/D1); a cell may be read under any interface whose addresses it holds | **5** |
| 6 | conflation: the named thing is both value and spec (§5) | a cell id names a value; extending means re-lawing or re-birthing from a file | **FALLS SHORT** | follows from 1+2: a cell's law and kind are references to prototype cells; `create --from CELL` | (in 2) |
| 7 | orthogonal persistence; no save; publish = tag + capability (§10) | Store = checkpoint + MAC-chained log of turns; `audit`; `view at`; signed observation under a capability | **AGREES** | — (per-document tagging as a capability on a version: PLACE/DEOS already) | — |
| 8 | transactions vs atomic sections (§10) | a turn is a global atomic unit | **FORK**, Mini right | — (see §7.7) | — |
| 9 | persistence of processes/continuations (§10) | cells persist; runners (Hermes, grains) are transient outside the kernel; Nock doors persist their state as a cell | **FALLS SHORT**, deliberately | doors as the model for every runner; no change proposed now | 7 |
| 10 | kernel is as kernel does; no monopoly on invariants (§12) | one Host, one admit; laws decentralize enforcement; `installPolicy` is a verb; overrides are turns | **AGREES** mostly; **FORK** on the fixed bottom | the admit function as a turtle (a meta-world) — named, not scheduled | 8 |
| 11 | platforms not applications; using is programming (§12) | one client; shell verbs are compositions; grains are instances; laws have a shell grammar | **AGREES**; templates are third-class | templates → prototype cells (finding 2) | — |
| 12 | four roles never conflated; the integrator's choice binds no one else (§14) | the operator's re-genesis and pinned profile bind every friend | **FALLS SHORT** | finding 3 + kinds as cells; the operator becomes an integrator of a *carry*, not the author of everyone's loss | (in 3) |
| 13 | names are meeting points, not hashes (§9) | cell ids are Nats; policies are content-addressed; names are private client hints; the room index as namespace is designed | **AGREES, UNBUILT** | the room index document as the room's namespace, resolved by the client | 6 |
| 14 | semantic tower; first-class implementations; no "jets" sham (§8) | compute = Nock in Lean, re-executed; nockvm is an untrusted oracle; no proof system in admission | **AGREES** (Faré's own prescription) | — | — |
| 15 | laziness for initialization (§4) | births hand-sequence create → init → law | **FALLS SHORT**, minor | prototype init as lazy formulas over `self` (with finding 2) | 9 |

---

## 1. Finding 1 — laws cannot inherit; they can only be replaced or copied

### What Faré requires

**READ.** "Inheritance is the mechanism by which partial modular specifications are
incrementally extended into larger modular specifications" (`ltuo` §2.4.1); the criterion
for extensibility is "the ability to extend, refine or modify a software entity without
having to read, rewrite, or modify any of the previous functionality ... only having to
write the additions" (`ltuo` §4.2.2); copying is a fork and "propagating bug fixes and
other changes to all the forks becomes all the harder as the number of copies increases"
(`ltuo` §4.2.6). With multiple parents the system must linearize: "programmers only need
declare the dependencies between objects and their direct super objects: the object
system will automatically compute a suitable precedence list" (`poof` §4.3.2), and
concurrent contributions to one aspect must *combine*, not conflict (`ltuo` §7.3.4.2).

### What Mini has

**READ.** A law is a `Pred`: a closed first-order AST with leaves `eq | le | memberOf |
writeOnce | monotone | eqSlots | leSlots | leSlotsOff | witnessed | hashEq | ran | not |
allL | anyL` over string slot names and `Int` literals, "no `→ Bool` / `→ Prop` function
anywhere" (`P/Pred/Core.lean:1-60`, the inductive at `:126-170`). There is no leaf that
names another law. Evaluation is over one `(old, new)` pair of projected slots
(`:214-260`). A cell has **one** law "judging EVERY verb" (`MUD.md` §2 preamble, citing
P-TEMPLATES finding 4). The law of a cell is resolved from the authority cell's
`policyAddress : PolicyId → PolicyRevision → Digest` (`P/Theory/TypedAuthorization.lean`,
`AuthState`), i.e. a content address; installing a new one is the `installPolicy` verb,
"Replacing a program resource's acceptance policy" (`P/Theory/TypedAuthorization.lean:86-88`).
A policy source carries `previous : Option Digest` and `Successor` demands
`version = head.version + 1 ∧ previous = some head.address` (`P/Theory/PolicyInstall.lean:30-52`).
That is a *version chain*: the new body is whole; nothing in it refers to the old body.
Rooms: the room cell's law "governs *management*: who may add to the roster, who may
delegate `under R`, whether the room may be re-lawed" (`PLACE.md` §2.1) — it does not
reach the cells under the room; "the honest rostered law is *structural*" because "`Pred`
cannot say 'request/subject ∈ roster fields' (no variable indexing)" (`PLACE.md` §2.1).

**READ.** The only composition available is syntactic: `Pred.all [p, q]` written by whoever
holds both texts. P-TEMPLATES' laws are assembled exactly so — "the installed law
`management ; law.player`" — by a Python renderer substituting placeholders into JSON
files (`planning/place/p-templates.md`, "The grammar and the JSON agree").

### The scenario a friend hits

A founds `lab` with a management law and installs `field state monotone; field state in
{0,1,2}` on `lab/board` (PLACE J13). B, a member, creates `lab/board2` and wants "the
board rules, plus: only I may close a task". B's options: (i) copy A's JSON and append a
clause — a fork; when A fixes a bug in the board rules, `board2` keeps the bug; (ii) ask A
to install B's variant — coordination, the cost Faré books "in the column of costs"
(`ltuo` §4.1.3 fn). Neither is "cooperate without coordinating". A second scenario: A
wants "every cell under `lab` is append-only after height H" — there is no place to say
it once; it is a law per cell, installed by whoever holds `installPolicy` on each.

### The Houyhnhnm alternative, in Mini's terms (PROPOSED)

**K-LAW-INHERIT.** A policy source gains `parents : List PolicyRef` (a `PolicyRef` =
`(policyId, revision)` or the distinguished `room`), and the system cell's `parent` tree
(`P/Kernel/World.lean:94-110`, `World.parent`) supplies an *implicit* parent: the law of
the cell's room, recursively to the realm. The effective law of a cell is the C3
linearization of that DAG (the tree part is trivially linear; explicit parents give the
diamonds), and the **combination is conjunction**: every ancestor's clauses apply once, in
precedence order; a child may only add. This is the "standard method combination" of a
law language whose values are verdicts — and it is *attenuation*, the same shape as
`Scope.Narrows` ("fewer targets, fewer verbs, and no larger budget",
`P/Theory/TypedAuthorization.lean:626-634`): a child law never widens a parent. `super`
is not an override (that would be amplification) but a *name*: the refusal leaf
(`firstFailingLeaf`, K-LAW-LEAF) reports which ancestor's clause refused — "refused:
law-denied: lab (room law) clause 2: field state monotone" — and a law may use `super`
slots to *read* the ancestors' verdict on the same step (`super/verdict`, `super/leaf`)
when it wants to say "if the room allows it, additionally require X". Overriding a parent
is what it is today: re-lawing the parent under its own management law, by its owner.

What this gives, concretely: "every cell under `lab` is append-only" is one clause in
`lab`'s law; `board2` inherits `board`'s rules by naming `board`'s policy as a parent and
follows A's revisions (a `PolicyRef` may pin a revision or follow `head`; following is
the Houyhnhnm default — "a name, which denotes a fixed intent, may refer to varying
content", `ch09` Global Namespace); a library of laws (a `policySource` cell, which
already exists as a kind, `P/Compiler/CanonicalCellRegistry.lean:57-75`) becomes
inheritable. Faré's own TODO describes the resulting shape: "a configuration DAG of
classes ... Keeping all your code in a vast open recursion until the very last moment"
(`todo`).

**Cost (honest).** Re-emits: the `Pred` codec does not change (no new leaf); the policy
*source* codec gains `parents`; `CanonicalPolicyAdmission` compiles the linearized
conjunction (its two-way lowering theorems, cited in `SURPASS.md` row 4, are restated over
`Pred.all (precedenceList.map body)` — mechanically, since `all` is already in the
algebra); the authority wire bumps; the semantics digest changes; one re-genesis. New
theorems: `effective_law_eval : eval (effective c) = (lin c).all (fun p => eval p.body)`;
`inherited_never_widens : effective c ⊢ refuses ⊇ parent refuses` (a two-liner from
`List.all`); `c3_tree_is_chain` (the parent tree linearizes to the chain); `leaf_names_ancestor`.
Theorems that move: `firstFailingLeaf_none_iff_eval` becomes a corollary over the
linearized list. What stays: `room_confidentiality`, `step_narrows_stable` (the parent
tree is append-only, so a cell's ancestry never changes under it — exactly the
"inheritance hierarchies are being set up before they are used" regime `eoomi` §7.1
asks for). Lanes: ~3 (theory; admission compile; shell grammar `law lab/board2 "parents
lab/board; …"` + K-LAW-LEAF rendering). Cost estimate is not a constraint (CLAUDE.md).

**Falsifier.** Build: A revises `lab/board`'s policy; with no turn on `board2`, B's next
write to `board2` is refused by the *new* clause and the leaf names `lab/board`. If that
cannot be exhibited, the inheritance is not live. Refutable pole: a child whose law would
*admit* what an ancestor refuses must be unconstructible (`inherited_never_widens`), and
a parent DAG with a cycle or an inconsistent order must refuse at install with a name
(C3's error, `poof` App. A.1).

---

## 2. Finding 2 — kinds, verbs and templates are second-class: every new kind of thing is a flag day

### What Faré requires

**READ.** "A class is 'just' a prototype for a type descriptor" (`poof` §5.1.2); "class-based
languages only have second-class classes whereas only prototype-based languages have
first-class classes" (`poof` §5.1.2); type descriptors carry "methods to encode and decode
values, to print and parse them ... default values ... pseudo-random value generators"
(`poof` §5.2.1). "The system of course can recognize privacy and performance annotations
about authorized programs" but "a new picture compression format is automatically usable
by each and every function that uses pictures throughout the system" (`ch07`). Internal
extensibility means not having to "read, rewrite, or modify any of the previous
functionality" (`ltuo` §4.2.2); "Fourth-class entities include design patterns, as
translated into code using editors, copy-paste" (`ltuo` §4.1.2).

### What Mini has

**READ.** `inductive Kind | content | eventHistory | authority | declaredObject |
resourceBook | accountMetadata | declaredProgram | policySource | pay | stream |
nockProgram | clock` with hand-assigned registry tags (`P/Compiler/CanonicalCellRegistry.lean:57-105`).
`inductive Verb : ResourceKind → Type` with fifteen constructors
(`P/Theory/TypedAuthorization.lean:76-100`); `ResourceKind` is `object | account | program`.
The factory template is a pinned constant of the runtime identity: "The runtime identity
therefore commits ... the full factory grant template. Each receiver consumes the same
`Profile`; a request cannot choose a template, field, order width or compiler"
(`P/Compiler/CanonicalRuntimeProfile.lean:1-13`, `FactoryTemplate :35-40`). The
evaluator registry is "compiled into the Host in ZK.md's carrier pattern" (`EVAL.md` §0).
Story and Hermes "templates" are files under `deploy/shell/templates/` rendered by
`p-templates-render.py`, and "Fields are Nat-numbered with a name map in the template"
(`MUD.md` §2 preamble; `planning/place/p-templates.md`). The flag-day record for one day
alone: K-BIRTH-WINDOW "Flag day: semantics digest + birth projection v3 → re-genesis";
BRAID-PROOF "flag days store encoding v2, resource view v5, at-height view v2, stream
schema v2"; `tickClock` "verb tag renumbered 7/13 → 11/17 because appendObject holds
7/13" (`SESSION-STATE.md`, 10-01 entries).

**READ.** The asymmetry in one sentence of his: "Anyone's second-class entities are
someone else's first-class entities" (`ltuo` §4.4.5). Kinds, verbs and templates are
first-class for whoever edits the Lean and rebuilds the Host, and second-class (kinds,
verbs) or fourth-class (templates, name maps) for a friend at the shell. The finding is
not that Mini lacks the entities; it is *who* holds them first-class.

### The scenario a friend hits

C wants a "poll" in `commons`: a cell with options, one vote per member, closes at a
height. Nothing in C's power makes a *kind* of poll: C can birth a `declaredObject`, write
a law by hand, keep a private name map, and tell friends which Nat is which. A second
poll is a copy. If the shape needs a verb that is not in the fifteen (say `vote`, which
should be `appendObject`-like but one-per-subject), it is a Lean change, a tag, a
rebuild, a semantics-digest bump and a re-genesis announced in `commons` — the operator's
act, not the friend's. Faré: "to Houyhnhnms, there is no difference between using and
programming" (`ch07`); here the difference is exactly "which things need ember to rebuild
the Host".

### The Houyhnhnm alternative, in Mini's terms (PROPOSED)

**K-KIND-CELL.** A new registry kind `kind` (the last one that needs a rebuild): a cell
whose store is a *type descriptor as first-order data* — a layout descriptor (namespaces,
key and value codecs chosen from a fixed menu of codec codes, disciplines rom/ram/
appendOnly), the default law (a `PolicyRef`, finding 1), the name map (`Nat ↦ String`,
and back), initial values and formulas (finding 15), and the verbs it answers (a subset
of a small fixed verb core: observe, mutate, append, delegate, installPolicy, revoke).
`create --from K` births a cell whose `kind` row in the system cell names `K` (the same
shape as `parent`), whose layout is K's descriptor, whose effective law has K's default
law as an ancestor, and whose name map any client reads from K. A kind cell is itself a
cell: it has a law (who may revise it), a room, a history, and it may inherit from another
kind cell (a prototype for a prototype — Faré's "we will instead make the prototype itself
an object", `poof` §4.3.3). The compiled `Kind` inductive shrinks to the roles that *are*
kernel semantics (authority, resourceBook, policySource, kind) plus one `declared` role
whose layout is read from the kind cell.

This is the move ATLAS already named and did not take: "apps are factory-minted cells
whose contracts are *inherited* kernel theorems" (`P/ATLAS.md` §2) — with the factory
a cell, not a profile constant. It also dissolves the "a request cannot choose a
template" rule into an authority question: a kind cell is chosen by capability, like any
cell.

**Cost (honest).** This is the largest change here: the layout becomes data, so
`StoreCodec` must be generic over a descriptor (DATAMODEL §3.9's `Layout` is already a
structure of codecs; the step is a *decoder* from descriptor bytes to `Layout` with a
proof that the canonical codec round-trips for every decodable descriptor — the K4 exit
theorem `∀ n, ∃ s, …` restated per descriptor). The projection into `Pred.State`
(`resource/field/{n}/…`) is already name-agnostic (Nats), so laws do not move. What
re-emits: the registry tags (one new), the birth frame (`from`), the system layout (a
`kind` namespace beside `parent`), the semantics digest, one re-genesis. New theorems:
`kind_recorded`/`kind_exists`/`kind_stable` (clones of `step_parent_*`,
`P/Kernel/World.lean:1025-1062`); `layout_of_descriptor_roundtrip`;
`default_law_is_ancestor`. Verbs: keep the inductive but *name* the verbs in the kind
cell; a friend-defined verb is a (core verb, kind) pair until there is evidence a new
core verb is needed — this is finding 2's deliberate under-reach, see falsifier. Lanes:
~6–8. It should land *after* finding 1 (the default law is an ancestor) and *with*
finding 3 (the first re-genesis that carries kinds).

**Falsifier.** C mints `poll` without any Host rebuild, D births two polls `from` it, a
law revision on `poll` refuses a stale vote on both, and `mini show` prints field names
from the kind cell on a client that never saw C's files. Negative pole: a descriptor that
decodes to no layout (bad codec code, duplicate namespace) refuses at the kind cell's
birth with a name, and a `from` naming a retired or non-kind cell refuses (`missingKind`,
beside `missingParent`). If after a month the verb core has had to grow for ordinary
friend-made kinds, the "verbs stay compiled" half was wrong and verbs become data too.

---

## 3. Finding 3 — re-genesis is the only upgrade; the carry is a shell script

### What Faré requires

**READ.** The degenerate case is allowed: "just don't upgrade the data, and instead drop
it, as you modify the code" (`ch05`). But "To program is to change programs, and to change
programs is to program" (`ch05`); "Persistence doesn't require anyone to agree with other
people on a low-level protocol; it only requires each person to maintain compatibility
with their own previous data ... what they need is to remember the old code and data, and
to be able to express the new code (generator) in terms of the old one (to upgrade the
code) and able to interpret the old data schema in terms of the new data schema (to
upgrade the data)" (`ch10`). The mechanism: "require every type modification to be
accompanied by a well-typed upgrade function, taking an object in the old type and
returning an object in the new type"; "linear logic to ensure that when writing an
upgrade operator, you must explicitly drop any data that you don't care about anymore";
"each change is always run in its own virtual fork of the system"; "effective history"
vs "actual history" (`ch05`). "Schema Upgrade is a regular part of the development
activity ... regression tests include data migration tests" (`persist` Schema Upgrade).
And the verdict on systems that decline: "Languages that assume 'purity' or absence of
code upgrade thereby deny these issues, and leave their users helpless" (`ltuo` §6.3.2).

### What Mini has

**READ.** The doctrine is explicit and deliberate: "A 'flag day' here means a rebuild, not
a migration ... make the old shape **refuse to load** rather than reinterpret"
(`/Users/ember/dev/breadstuffs/CLAUDE.md`, the project doctrine this session runs under;
Mini's own `CLAUDE.md` does not restate it, but the Store and the planning docs apply it).
The Store says so in its refusal table: "store holds a retired whole-image record; re-genesis (no migration)"
(`P/docs/DURABLE-STORE.md`, "What refuses to load"). No module in `Theory/`, `Kernel/` or
`Compiler/` migrates world state across a semantics digest (grep `migrat`/`upgrade`: hits
are the application-grain package lifecycle and prose). The planned carry is a script:
F6 GENESIS-CARRY, "`native/resource-client/genesis.sh`; new `mini export-genesis` ...
after a re-genesis from the export: every key present, every Book balance equal, the
room tree equal; resources are not carried, and the tool says so" (`SURPASS.md` §5.1 F6).
The social protocol: "after Oct 13 a re-genesis is announced in `commons` by ember and the
friends re-enroll — that is the price and it is said here" (`PLACE.md` §4.10, §6.5), "the
old Store is kept read-only as `history/` for `doc at`" (`PLACE.md` §6.5). Measured
frequency, one day: at least four flag days queued (`SESSION-STATE.md` 10-01 18:15, 18:55).

### Where Faré and Mini agree, first

The *refuse-to-load* half is right and Houyhnhnm: a stale shape must not be
reinterpreted ("the old shape refuses to load" is his "all sources of non-determinism are
either eliminated or recorded" applied to schemas). The *keep the old Store as
`history/`* half is his "fork the old data together with the correct version of the code
that knows how to create and manipulate it" (`ch05`). What is missing is only the middle:
the typed, checked function between the two, and the discipline that it names what it
drops.

### The scenario a friend hits

B has a document, a law, three grants and a balance. Flag day. B is told in `commons` to
re-enroll. Keys and balances come back (F6); the document does not ("resources are not
carried"); the grants do not; the law does not. B's week of work is in `history/`,
readable at a height, and not *theirs* any more. Faré's test — "one author's or
integrator's choice ... does not and cannot bind anyone else's" (`ch09`) — fails: the
integrator's (operator's) flag day decided what every author keeps.

### The Houyhnhnm alternative, in Mini's terms (PROPOSED)

**K-CARRY.** Every flag day ships `Compiler/Carry/<digest_old>-to-<digest_new>.lean`: a
function `carry : World_old → Except CarryRefusal World_new` over the *old* and *new*
Lean types (both are in the tree at the cut — the old module is kept under a versioned
namespace exactly long enough to be the domain of `carry`), with:

- **linearity by construction**: `carry` is written against a `Linear` wrapper — every
  cell of the old world must be either mapped (`keep c f`) or explicitly dropped
  (`drop c reason`); a theorem `carry_total : ∀ c ∈ old.cells, mapped c ∨ dropped c` is
  the "you must explicitly drop" rule of `ch05` as a type;
- **the carried claims as theorems**, not a tool's prose: `carry_keys`, `carry_balances`
  (Σ per asset preserved, from `Theory/Conservation.lean`), `carry_parentage`
  (`World.parent` preserved up to the id map), `carry_grants` (every non-revoked
  capability has an image whose scope `Narrows` the original's image — never wider),
  `carry_laws` (every policy source has an image in the new `Pred` codec, or is dropped
  by name);
- **applied in a fork**: the carry runs on a *cloned* Store producing the new Store's
  genesis; the old Store is untouched and becomes `history/` (PLACE §6.5); the new
  genesis seed records `(digest_old, carryDigest, headRoot_old)` so the chain of
  semantics digests with carries between them is the **effective history** (`ch05`) —
  readable by `mini audit --lineage`;
- **a migration test in the journey**: the whole journey runs on the carried Store, not
  only on a fresh one (SURPASS S3's growth row has a cousin: "G at 1000, then carry, then
  J0–J8 again").

Re-genesis-as-wipe remains available (a carry that drops everything is a valid carry, and
the cheapest); what changes is that *dropping B's document is a named decision in a Lean
file*, not a sentence in a planning doc.

**Cost (honest).** This is process as much as code: the old types must be retained one
cut deep (a `V_old` namespace; the twin-deletion doctrine is unhurt because the old
module is the *domain* of a function, not a parallel implementation, and it is deleted at
the next cut). The first carry (FD-1, the Turn cutover, `SURPASS.md` §2(b)) is the
expensive one because the old record shape carries whole post images; later carries are
mostly identity on cells plus codec lifts. The journey grows by one leg. What re-emits:
the genesis seed frame (lineage fields). Theorems: the five `carry_*` above per flag
day, generated from one `Carry` structure with proof fields (ATLAS's "obligations as
proof fields" pattern, `P/ATLAS.md` §4). Lanes: 2 for the structure + the FD-1 carry;
then ~1 per flag day, folded into the flag-day lane.

**Falsifier.** After a flag day, B's document, law and grants are present on the new
Store with the same ids (or the mapped ids), and `mini audit --lineage` replays old
genesis → old head → carry → new head to the served root. Negative: a carry that silently
omits a cell must fail to *compile* (`carry_total`); a carry that widens a grant must
fail `carry_grants`. If, after three flag days, every carry is "drop all", the mechanism
was theater and this finding was wrong about what friends keep.

---

## 4. Finding 4 — extending what you do not own: laws attach to one cell only

**READ.** Faré's "orthogonal protocol": "requiring specifications ... to inherit from a
common ancestor to be able to define a method, means that you cannot add new methods to
specifications after the fact ... it requires omniscience from a class author about all
the interfaces that the users of the class may ever want to satisfy" (`ltuo` §9.2.9);
"the unit of coherent extension was never the individual class or object or function,
but the entire program or library" (`ltuo` §9.3.7).

**READ.** Mini: a cell's law is chosen by its owner (`installPolicy` on the `.program`
projection, `P/Theory/TypedAuthorization.lean:86-88`); a law on *my* cell may read
*your* cell's slots in the same command only through `joint/target/{cellId}/…`, "keyed by
the target's **cell id**" (`MUD.md` §2 preamble), i.e. explicit communication in Faré's
sense ("a process specifically names another process ... requires tight coupling",
`ch08`). A room cannot impose a law on its cells (finding 1). Views over other people's
cells exist only as observation under a capability.

**Verdict: FALLS SHORT; folds into finding 1.** With K-LAW-INHERIT, the room's law *is*
the after-the-fact protocol over every cell under it, including cells born before the
clause was added (ancestry is stable, the clause is not frozen); and a library policy
cell is a protocol anyone may inherit. The remaining gap — a third party attaching a
*view* or an *index* to a cell it does not own — is finding 5 and K-DOC-INDEX
(`DEOS.md` §0.1, "a cached, coverage-filtered fold"), which is the right shape: the index
is a fold the kernel maintains, not a law the owner must have anticipated.

**Scenario.** The referee runner (MUD §2.5) wants "every sheet under `W` records `ref` as
last writer" without editing each sheet's law: today impossible; with finding 1, one
clause on `W`. **Falsifier:** as finding 1's.

---

## 5. Finding 5 — points of view: narrowing exists, lenses do not; name maps live in files

**READ.** Faré: "an object can be in the target type of several interfaces ... simply
change the interface, and the same data can be punned into meaning usefully different
things ... Just look through the lens of a different interface" (`lil` §3.2.3); focused
specifications carry "a path from the top of the program state to the module context"
(`ltuo` §9.1.2); a view is never a copy.

**READ.** Mini: `Scope.fields : Option (Finset CellField)` narrows what a capability may
read and write (`P/Theory/TypedAuthorization.lean:607-616`, K-FIELDS merged per
`SURPASS.md` row 2); the hiding root blinds leaves so a narrowed reader learns nothing
about the rest (`planning/privacy/k-narrow-hide.md` §1); `view at` reads the world at a
height (`DEOS.md` §0.1, k-index); `ObserverLens` with exact dependency sets and
"dirty views are reprojected from the sole canonical post-cell"
(`P/Theory/CanonicalReactiveView.lean:1-20`) is theory with no Host caller; observation
"returns that cell's packed store bytes" (`P/Kernel/NativeObservationController.lean:9-11`;
per-address openings are planned D1). The name map that makes `resource/field/3` mean
`state` lives in the template folder (`planning/place/p-templates.md`), so two friends
reading the same cell through two clients can disagree on what field 3 is called, and the
kernel has no opinion.

**Verdict: FALLS SHORT, modestly.** Narrowing is a lens (a restriction), and the
dependency-set view is exactly Faré's "projections are pure typed programs returning their
exact dependency set" (`P/PROJECT.md`, reactive lifecycle item 1) — this part he would
praise. What is missing is the *interface as a thing in the world*: a name map, a
rendering, a set of derived fields over a cell's addresses, that a friend can publish and
another can read a cell *through*.

**Alternative (PROPOSED), folded into K-KIND-CELL.** The kind cell carries the name map;
an **interface cell** is a kind cell with no layout of its own — a name map plus derived
slots (`Pred`-style formulas over addresses, read-only) — and a reader may ask for a cell
*under* any interface whose addresses the cell holds (`mini show CELL --as poll-summary`).
Two interfaces on one cell is LIL's pun; the kernel checks only that the addresses exist.
Cost: client-side at first (the client resolves the interface cell and renders); kernel
only if derived slots should be law-visible. **Falsifier:** two clients with no shared
files print the same field names for the same cell; a cell read under an interface whose
addresses it lacks is refused by name.

---

## 6. Finding 6 — names: Mini chose hashes and ids; the room index is the Houyhnhnm namespace, unbuilt

**READ.** Faré: "a name path or location properly identifies an extensible 'intention'
rather than an immutable 'extension', a meeting point rather than fixed code ... If users
wanted the latter, they would be using cryptographic hashes, not names" (`ltuo` §9.3.7);
"persistence ... means you can give a stable name to a stable activity" (`ch08`).

**READ.** Mini: cell ids are `Nat`s (`P/Kernel/World.lean:47`); policies are addressed
by `(policyId, revision) → Digest`; "Names are hints the client keeps privately ... There
is no directory of people; there are keys and grants" (`PLACE.md` §1). And the answer is
already designed: "a room's index is a hyperdocument whose links are the room's map, and
anyone with `mutateObject` on the index can redraw it" (`PLACE.md` §1 item 2).

**Verdict: AGREES, UNBUILT.** Keys-and-grants with no admin table is the biscuit shape
and is right (Faré: "mutually agreeable contracts between equally free parties",
`ch06`). But a world friends *share* needs shared meeting points, and the design has
them: the room index document. The gap is that the client's `lab/board` resolves through
a private address book, not through `lab`'s index. **Alternative:** resolve `ROOM/NAME`
through the room index cell by default (a link named `board` → cell id), private hints
as the fallback; the index is a document under the room's law, so naming is governed like
everything else. **Falsifier:** B's `lab/board` resolves on a fresh client with only the
room capability; renaming in the index moves it for everyone; two links with one name
refuse at the index's law. Cost: client + one index-law template; no kernel change.

---

## 7. Where Mini is right and Faré would agree — said plainly

### 7.1 Orthogonal persistence — AGREES

**READ.** No friend saves: a turn is accepted and appended; the Store is "checkpoint +
MAC-chained log, re-admitted by `audit`" (`DEOS.md` §1.1); "No signed ingress is
re-admitted" on open, "every check refuses" (`P/docs/DURABLE-STORE.md`, Open); the world
root is a function of the logical map and "one write rehashes one path per written slot".
History is a fold with `fold_append` (`P/Kernel/World.lean:409`) — Faré's "monotonic
storage that never loses data by construction, so that all programs get in(de)finite undo
by default" (`snapl` §4.3) and his log of "events with their proper timestamp" from a
"well-determined state" (`ch03`). Publishing is a capability on a version (`view at`
checks the grant at that height, `SURPASS.md` row 9) — his "tagging a version ... and
granting select others a capability to access the tagged version" (`persist`
Publishing). Rooms are his domains: "Origin Domain Validates Copy Out / Share Out"
(`pslides`) is `room_confidentiality` + `Narrows`.

### 7.2 Authority — AGREES

**READ.** `Capability` with `root`, `parent`, `ancestors`, `holder`, `scope`, a height
window (`P/Theory/TypedAuthorization.lean:741-756`); `attenuation_admits_subset`,
`ancestor_revocation_rejected` (`PLACE.md` §1); "Overriding invariants, while possible,
requires special privileges and will be logged" (`ch06`) is exactly `installPolicy` as a
verb whose exercise is a turn in the journal. "Flag whoever reaches for forbidden
capabilities as hostile" (`pslides`) is the uniform `undisclosed` refusal
(`PRIVACY.md` §0). ATLAS §2's "authority = constructive knowledge ... To hold a capability
is to be able to exhibit a witness that verifies" is Faré's verify/find seam one level
down.

### 7.3 Decentralized enforcement — AGREES

**READ.** "the invariants that ultimately matter ... are always those of the overall
system, the 'final' applications" (`ch06`): in Mini every cell carries its own law and
the kernel checks *that* law, not a fixed set (`P/Pred/Core.lean`; `PLACE.md` §2.6 "a
transition table, a budget, a two-signature rule, a write-once register ... are all one
`Pred`"). Conservation is a theorem of the Book, not a kernel bitmask
(`P/Theory/Conservation.lean` via `SURPASS.md` row 5). Linear value as "some variant of
what we call linear logic" (`ch06`) is `δ ∈ ker Σ`.

### 7.4 Compute by re-execution, no proof system in admission — AGREES, and it is Faré's own argument

**READ.** Faré on jets: "you must implement things twice ... And how do you ensure the
equivalence ... You can fail to, or lie"; the remedy is "an advanced metaprogramming
infrastructure capable of manipulating arbitrary program semantics in a formally correct
way" so the two are "confident[ly] ... equivalent" (`ch10`). Mini: the Lean `Nock.exec`
is the referee, nockvm is an untrusted oracle differential-tested on 11,050 rows, and the
kernel "re-executes a claimed run and admits only on exact match"
(`no_accepted_of_output_mismatch`, `SURPASS.md` row 14; `EVAL.md` §0). And on *why* no
proof system: "A global consensus on deterministic computation semantics only matters if
you want to replay and verify other random people's computations ... If you only want to
replay your own computations (or those of friends), you don't need a global consensus on
a deterministic function; you only need to know what you're talking about, and write it
down" (`ch10`) — which is `MEM/project-no-proof-system-in-mini-admission.md` said by
Faré in 2016. (He would add that the *semantics digest* is "what you're talking about,
written down" — and that it must therefore be *carried*, finding 3.)

### 7.5 Lean is the implementation — AGREES

**READ.** "Compiled Lean decides every admission" (`SURPASS.md` row 7); "Rust has no
semantics or refinement theorem in this repository" (`P/PROJECT.md` Hard invariants 2).
This is Faré's "Lean authors the artifacts" in his own words: "A hand-written model 'of'
an implementation is a twin, and twins drift" (`P/README.md`) is `eoomi`'s and
`ch10`'s argument. The *one* remaining twin the planning names — `DurableDataIntent.execute`
vs `World.step` (`SURPASS.md` row 7) — is the kind of thing he calls "the pretense of
having fully formalized the state of the system and its state function" (`ch10`); the
cutover (FD-1) is the right fix and is scheduled.

### 7.6 Platforms, not applications — AGREES

**READ.** "application grains ... are instances of the platform, not its organizing
architecture" (ember, `PLACE.md` header); one client with shell verbs that are
"compositions of `invoke … write at`, `read`, and K-STREAM's `say`" (`MUD.md` §2.1); the
law grammar is an internal DSL rendering to the one algebra (`PLACE.md` §2.6) — "refine
their 'normal' programming languages ... not ... a new minilanguage" (`ch09`); Hermes
uses "MCP tools = the client contract" (`DEOS.md` §0.1). Faré: "the difference between a
programmer and a user, is that the programmer knows there is no difference" (`ch07`).

### 7.7 Transactions — a FORK where Mini is right

**READ.** Faré: "Transactions are Bad: Require Global Knowledge, Don't Compose ...
Necessary because processes don't persist" (`pslides`); his alternative is atomic sections
+ memory barriers inside a persistent process (`persist` Atomicity, Synchronization).
Mini's turn is a global atomic unit (`World.admit`, `P/Kernel/World.lean:351-367`).

**Why Mini is right here.** Faré's target is the *database* transaction: a transient client
cutting its own computation at a server's convenience. Mini's turn is not that; it is the
unit of *admission and receipt* across parties who do not trust each other's processes —
the thing a signature is over and a nullifier consumes. His own carve-out applies:
determinism and global cuts matter "if you want to replay and verify other random
people's computations" (`ch10`), and a world of friends with receipts is exactly a
(small) version of that. Inside one friend's runner (a Nock door, Hermes), his atomic
sections are the right model, and that is where Mini already puts the division: "the
kernel does not execute the program; it admits the program's *writes*" (`PLACE.md` §1
item 3). What would make him object is if a *runner's* local work had to be a kernel
turn to persist — which is finding 9.

---

## 8. The remaining findings, briefly

### 8.1 Finding 7 — persistence of processes (runners) — FALLS SHORT, deliberately

**READ.** "Persisting Continuations simplifies everything else" (`pslides`); the persistence
domain persists "Running Processes, too" (`pslides`). Mini: the kernel persists cells; a
runner is "a subject with an account, a program document, and grants" whose process runs
outside — hosted Hermes "with restart" (M5), a grain in a jail (M6). Nock doors are the
exception that shows the shape: "instance = declared object, `door.state` = jam atom,
`door.event`; poke/peek" (`EVAL.md` §0.1 table) — a persistent actor whose continuation
*is* a cell. **Scenario:** a Hermes librarian mid-task when the box restarts loses its
plan; a door would not. **Alternative:** no kernel change now; the design rule "every
long-lived runner is a door or has a door-shaped checkpoint cell" belongs in PLACE §2.7's
ladder. **Falsifier:** restart the Host mid-task; the door resumes its plan from its cell;
Hermes does not. Rank 7.

### 8.2 Finding 8 — the fixed bottom: `admit` is not a turtle — FORK

**READ.** Faré: "Every turtle is unique, but no turtle is special" (`ch04`); "there is no
more fixed bottom for software" (`fci` §5.3); and the sharpest line, "the invariants that
ultimately matter ... a kernel that possesses a monopoly on invariant enforcement, is
absurd on its face" (`ch06`). Mini, in its own words: "A kernel that is a cell is a kernel
whose law can be rewritten by a turn; Mini's whole value is that `admit` is not in the
world it admits ... The Host binary and its Lean are not cells" (`DEOS.md` §1.1).

**Both are right about different things.** Faré's "no monopoly" is satisfied by per-cell
laws (§7.3). His "no fixed bottom" is about *migration*: being able to change the
implementation below a running thing. Mini's refusal is about *authority*: the admit
function must not be reachable by the authority it judges. His architecture reconciles
them with the tower: "the topmost computation ... is fixed, specifies the desired
semantics of the tower, and limits the access rights of all implementations" (`fci`
§5.1) — the semantics digest is Mini's topmost computation; the Host binary is one
implementation of it; a flag day is a change of implementation *plus* a change of top.
Finding 3 (the carry) is the honest cheap version of "every computation has its
controller" (`fci` §5.1): the controller is the operator with a Lean-checked carry. The
full version — a meta-world whose turns are flag days of this world — is a research fork,
not a lane. **Falsifier for the fork:** if finding 3's carries turn out to be the *same*
Lean each time (a generic `Carry` over descriptors), the meta-world exists in all but
name and should be named. Rank 8.

### 8.3 Finding 9 — initialization order — FALLS SHORT, minor

**READ.** "lazy evaluation enables modular initialization ... The slot initialization
order needs not be the same across an entire prototype hierarchy" (`eoomi` §5.1). Mini:
births "in the order P-TEMPLATES fixed for stories (create under management, init
fields, install the law)" (`MUD.md` §2.1) — a protocol, hand-kept, in a script; and a
birth is "pinned to the ADMISSION height" so an intervening admission refuses it
(`SESSION-STATE.md` 16:58; fixed by a slack window). With K-KIND-CELL the init is data on
the kind cell (initial values, or formulas over `self` addresses evaluated at birth), so
the order is derived, not scripted. Rank 9; rides finding 2.

### 8.4 Finding 10 — the four roles — FALLS SHORT, and finding 3 repairs it

**READ.** `ch09`'s rule: "if it ... requires a person having a role to specify
information that only people with other roles may know, then it is a deeply
dysfunctional design". Mini's operator is author (of the Host), integrator (of `final`),
and the party whose flag day decides every author's loss; the pinned `FactoryTemplate`
"a request cannot choose a template" makes the integrator the author of every birth's
shape. Findings 2 and 3 move both decisions into the world (kind cells chosen by
capability; carries that keep by theorem). The `friends/` roster and tariffs
(`PLACE.md` §6.4) are rightly the operator's — custody.

### 8.5 Things Faré would not change

Keys and grants with no admin table; the uniform refusal; `Pred` as a closed first-order
algebra *for the policy path* (his N3 argument is in `P/Pred/Core.lean`'s header and he
makes the same one against opaque payloads: "interactions between automated processes
should happen using the highest level but least expressive language possible", `ch04`);
the hiding root as the owner's custody; the Book as the one owner of money; `maxDelta`
as bounded linear logic (EVAL §2b(b) is a reading he would sign); the audit as an
operator command, never the request path (his monitor, `ch03`).

---

## 9. Ranking, and the three to do first

Ranked by how much they change what friends can do, with cost:

1. **K-LAW-INHERIT** (finding 1, absorbs 4). *Changes:* laws compose along the room tree
   and by named parents; a room governs its cells; a law library is inheritable;
   refusals name the ancestor. *Cost:* policy-source codec + admission compile + shell
   grammar; semantics digest; one re-genesis; ~3 lanes; the lowering theorems restate
   over a list. *Theorems move:* `firstFailingLeaf_*` (corollary); new
   `effective_law_eval`, `inherited_never_widens`, `c3_tree_is_chain`.
2. **K-KIND-CELL** (finding 2, absorbs 5, 6-in-part, 9). *Changes:* friends mint kinds;
   births say `from`; name maps and interfaces are in the world; no rebuild per kind.
   *Cost:* descriptor-generic `StoreCodec`, a `kind` system namespace, birth frame,
   registry tag; semantics digest; one re-genesis; ~6–8 lanes. *Theorems:*
   `kind_recorded/exists/stable`, `layout_of_descriptor_roundtrip`,
   `default_law_is_ancestor`.
3. **K-CARRY** (finding 3, absorbs 10). *Changes:* a flag day keeps documents, laws,
   grants by theorem; the semantics-digest lineage is auditable; the operator stops
   deciding every author's loss. *Cost:* a `Carry` structure with proof fields; the
   FD-1 carry (expensive once); a journey leg; ~2 lanes then ~1 per flag day.
4. **K-INDEX-NAMES** (finding 6). *Changes:* `ROOM/NAME` is a shared meeting point.
   *Cost:* client + an index-law template; 1 lane; no kernel change.
5. **K-INTERFACE** (finding 5's second half). *Changes:* one cell, many readings.
   *Cost:* client first; 1 lane; kernel only for law-visible derived slots.
6. Doors as the runner model (finding 7) — a design rule, no lane.
7. The meta-world (finding 8) — research; named, not scheduled.

**The three to do first: 1, 3, 2 — in that order.** Finding 1 first because it is the
cheapest, it is the one that makes "extend together" true in the kernel rather than in
JSON files, and it reuses the parent tree that K-ROOM already proved stable
(`step_narrows_stable`) — the inheritance hierarchy is already append-only, which is the
precondition Faré sets for stateful OO. Finding 3 second because the next flag day is
already queued (FD-1) and it is the one whose carry is hardest; doing K-CARRY *on* FD-1
means the most expensive carry is written while the old types are freshest, and every
later flag day inherits the structure. Finding 2 third because it is the largest and it
wants both: its default laws are ancestors (1) and its first re-genesis must carry kinds
(3). Doing 2 before 1 would mint kinds whose laws still cannot be shared; doing 2 before
3 would mint kinds that the next flag day drops.

What *not* to do: do not build the meta-world (finding 8) to satisfy "no fixed bottom";
do not replace turns with atomic sections (§7.7); do not add a proof system to admission
to satisfy "semantic tower" (§7.4 — Faré's argument runs the other way for friends); do
not make `Pred` higher-order (his N3 argument and Mini's are the same).

---

## 10. ASSUMED (mine) and what I did not read

- **ASSUMED** that the breadstuffs flag-day doctrine is Mini's: Mini's `CLAUDE.md` (57
  lines, read) does not say it; `docs/DURABLE-STORE.md` ("re-genesis (no migration)"),
  `PLACE.md` §4.10 and `SURPASS.md` §2(b) enact it.
- **ASSUMED** that `final`'s laws and kinds are as at `7961b345`; the braids landing
  today (`SESSION-STATE.md` 18:40, 18:55) do not, by their reports, add law inheritance,
  world-resident kinds, or a carry.
- **ASSUMED** that no shell verb today composes two existing policies by reference; I
  read the grammar (`PLACE.md` §2.6, `p-templates.md`) and `Pred/Core.lean`'s AST; I did
  not read `shell.rs`.
- **ASSUMED** that `FactoryTemplate` being in the runtime identity means a friend cannot
  select a different birth shape without a profile change; I read the header
  (`CanonicalRuntimeProfile.lean:1-13`) and the structure, not the birth controller.
- **NOT READ:** `Compiler/CanonicalPolicyAdmission.lean` body (the compile of `Pred` to
  the circuit — finding 1's restatement cost is estimated from the header and the
  SURPASS citation); `Kernel/NockDoor.lean`; `Kernel/ResourceBirthPolicyController.lean`;
  any `Host/*.lean`; `shell.rs`; the k-room branch sources (cited through PLACE and
  SURPASS).
- **NOT READ at source:** the C3 code in `poof` App. A.1 beyond its statement; the
  `coop.rkt` library.
- Tweets: see `sources/tweets-oo.md` for what arrived and whether any finding moved.
