# Formalizing the Notion of Implementation, as Illustrated with Concurrent Garbage Collection

- URL: https://fare.tunes.org/files/cs/implement1.pdf
- Date: undated (thesis-era chapter)
- Fetched: 2026-10-01T22:09Z (pdftotext -layout)
- Author: François-René Rideau (Faré)

---

                             Formalizing the Notion of Implementation,
                         as Illustrated with Concurrent Garbage Collection
                                          François-René Rideau -D ă.ng-Vũ Bân

                                          CNET DTL ASR (France Télécom)
                                              38–40 rue du general Leclerc
                                       92794 Issy Moulineaux Cedex 9, FRANCE
                                               http://fare.tunes.org/


Abstract                                                           of concurrent implementations. Lamport has developed no-
                                                                   tions of atomicity and implementation for concurrent sys-
We study the notion of implementation in a generic frame-          tems [16, 19], but his single-universe formalism isn’t im-
work for computational semantics. This paper, the first            mediately suitable to specify generic notions of metapro-
in a series, gives the detailed formal presentation of a no-       gramming or of compiling. Goerigk and Hoffmann [10] give
tion of implementation. We introduce the notion pointing           a formal definition for compiler correctness that is essen-
out the issues raised in presence of concurrency, and illus-       tially the same as we use, but do not systematically develop
trate our ideas with Concurrent Garbage Collection. We             their meta-logic or study additional properties of implemen-
then give a definition for the notion of implementation in a       tations.
generic meta-level framework for the semantics of comput-              This paper aims at providing as generic a meta-level
ing systems. We formalize usual properties expected from           framework as possible to internally express the notion of
implementations, and particularly find an original notion of       an implementation of a higher-level “abstract” computing
“soundness”. We show how this notion can be used to solve          system by means of a lower-level “concrete” computing sys-
such problems as modular implementation of synchronized            tem. Yet, we try to provide a framework that allows to ob-
concurrent systems. We relate this formal notion of sound-         tain in a reusable and composable way results that be useful
ness to many hacker tricks that were naturally used during         to people specifying, implementing, and verifying compilers,
actual implementation of various systems.                          especially in presence of concurrency. We do not use a par-
                                                                   ticular logical meta-formalism (computerized or not), but
1   Introduction                                                   think the presented framework should pose no problem be-
                                                                   ing expressed in any existing formalism.
As computing systems get more complex, especially due to               In section 2, we informally study the difficulty of speci-
concurrency and distribution, and as they get more used in         fying concurrent implementations, and examine as a sample
mission-critical devices, it becomes increasingly important        problem the concurrent garbage collected implementation
to understand how the high-level services they render may          of a high-level language. In section 3, we propose a generic
be correctly implemented in terms of low-level software and        notion of implementation, in a generic framework for com-
hardware.                                                          putational semantics. In section 4, we study various desir-
     Formalizing the notion of implementation may help spec-       able properties of implementations, and their composability
ify, verify and debug the correct behavior of implementations      we particularly introduce an original notion of “soundness”
(open or not), or of metaprogramming tools that produce            that generalizes many stronger ad-hoc notions found in other
and/or analyze implementations (most notably static or dy-         works on implementation. In section 5, we show how this
namic compilers). It is thus of interest to people designing       notion is a useful tool to establish in a modular way the cor-
or developing such metaprogramming tools, and to everyone          rectness of the implementation of concurrent systems, such
wondering how much they can trust the tools they use.              as in the previously considered garbage collector case. We
     There have been many works on the formal specification        discuss implementation techniques for soundness. We con-
and verification of interpreters and compilers [11, 25, 13, 6].    clude in section 6, suggesting possible applications to the
However, these works are restricted to single-threaded cen-        present work.
tralized programming models and do not generalize obvi-
ously to specification of arbitrary parallel or distributed pro-   2     An Informal Approach
grams. Araujo [2] discusses correctness of a parallel imple-
mentation of Prolog, but in a setting where he needs not           2.1    Specifying Concurrent Implementations
bother with atomicity, which is precisely the main problem
                                                                   An implementation is a correspondance between two com-
                                                                   puting systems, one being a higher-level “abstract” com-
                                                                   puting system and the other being a lower-level “concrete”
                                                                   computing system. This correspondance ought to preserve
                                                                   the semantics of the abstract system; this means that com-
                                                                   putations done with the concrete computing system lead
                                                                   to observations that are consistent with computations that
                                                                   would have been done in the abstract system.
    Typically, abstract systems of interest are modern high-          whereby they eliminate sets of objects that are smaller than
level programming languages such as dialects of the LISP              the set of unreachable objects. On the other hand they may
or ML family of languages, or more recently, the Java lan-            not collect any reachable object; that would be unsafe, and
guage. Less general cases include programs that are written           would likely lead to horrible death of implemented programs
in such languages. Concrete systems of interest are modern            when they try to access an object that has been collected.
microprocessor-based computers, or pools thereof, as pro-                 Garbage collection is a relatively high-level transforma-
grammed in assembly language. Often, an implementation                tion on object graphs; however, computer memory hardware
is split into layers, factoring the correspondance through in-        typically doesn’t provide dynamically reconfigurable graphs
termediate computing systems such as virtual machines or              as such, but statically configured arrays of dynamic data
widely available low-level programming languages such as              cells according to the Von Neumann architecture. Object
C.                                                                    graphs may be represented by mapping every node of the
    The semantics of such computing systems and their im-             graph to chunks of consecutive data cells in memory, and
plementation is very well understood in the single-threaded           with arcs of the graph being represented as a number in
case; there have even been proven-correct implementations             corresponding data cell of the father node, pointing to the
of high-level languages with proven-correct microprocessors           first data cell of the son node. A same object graph may
[6]. Sequential monoprocessor implementations of sequen-              have multiple representations as a memory state, depending
tial or concurrent languages may be even extracted from               on the mapping of graph nodes to memory chunks; a GC
formal specifications of their abstract semantics [?]. That           may safely modify the mapping as long as it preserves the
is, when the implementation is serialized at the low-level,           graph. A same object graph may also lack any representa-
serial synchronization of concurrent high-level activities is a       tion as a memory state, if it contains more nodes that can
marginal benefit.                                                     be fit into the finite memory size. On the other hand, not all
    But formalizing the implementation of a sequential or             memory states are valid graph representation; the encoding
concurrent high-level system with a concurrent low-level sys-         of graphs may rely on complex invariants to be respected
tem is still a research topic. Concurrent low-level system can        by well-formed memory states so that GC may happen. For
be a multiprocessor system, a distributed system, or any              instance, many GC techniques require that the GC algo-
computer with multiprogramming operating environment.                 rithm should be able to precisely differentiate pointers from
The difficulty is that implementating high-level computing            other numbers, so that it may update, swizzle, marshall, or
systems involves system services such as automatic mem-               otherwise specially process pointers when moving, mapping,
ory management (garbage-collection) checkpointing, persis-            or migrating objects around the implementation-controlled
tence, transactions, dynamic compilation, code migration,             world. Lastly, a given memory state must represent only
support for source-level debugging, and that every such ser-          one valid object graph, or else we would be unable to use
vice depends on global invariants that must be preserved              the concrete computations to unambiguously implement the
despite the concurrency of the low-level system.                      abstract computations. The correspondance between ab-
    A satisfying theory of implementation must thus be ap-            straction and concrete computation states is thus a partial
plicable to concurrent computing systems, and include the             one-to-many relation in the general case, although in some
study the good properties of an implementation relative to            cases, it might be useful to have the implementation be total,
the preservation of high-level invariants.                            or to refine its exact behavior until it be one-to-one.
                                                                          Now, GCs are not usually run alone for the sake of it;
2.2   Concurrent Garbage Collection                                   rather, they run as a system support service, concurrently
                                                                      with actual implementation of the abstract activities that
We’ll try to illustrate the properties we want to study about         modify the graph, “mutators”. And for architectural rea-
implementations using the more specific but typical case of           sons, it may be plainly impossible, or extremely inefficient
the implementing garbage collection in concurrent program-            for the underlying computing architecture to preserve the
ming language.                                                        GC invariants at all moments; so that mutator operations
    Garbage collection [5, 28], or “GC”, is a technique used          that are conceptually atomic when manipulating abstract
for automatic memory management when implementing                     graphs may involve many instructions when concretely im-
typed high-level languages whose programming model in-                plemented. The concurrent mutators may introduce lots of
volves a dynamically evolving graph of objects. It consists           transient states, that do not correspond to any valid ab-
in having a special system activity, named the garbage col-           stract graph representation; but the GC activity must only
lector or also “GC”, track down objects in the graph that             be able to observe the mutated memory when it is in a “sta-
are “dead”, that is, unreachable from any currently user-             ble” state that respects invariants. We say that the mutator
accessible object, and collect them, that is, eliminate them          implementation is sound if it is always possible for the GC
from the graph, saving representation space for future new            to observe it in a stable state when needed. Soundness thus
objects.                                                              appears as an essential property of implementations so as to
    Eliminating dead objects is a safe transformation of pro-         safely combine multiple concurrent activities.
gram state in as much as it preserves the semantics of the                We may also study more classical properties of garbage
language: that is, it allows no abstract user observation that        collected implementations of high-level languages. A GC’ed
would distinguish the transformed program from the origi-             implementation will be complete, if it enables the represen-
nal one. A garbage collector needs not eliminate all unreach-         tation of all possible object graphs that may happen as valid
able objects; if actual computations run concurrently with            states during the abstract computation; this is only possible
the garbage collector, determining the exact set of objects           if we can give a bound on the total amount of live nodes at
that are reachable at a given moment would require stopping           any moment in the computation state, so that they may all
all other activities for the duration of the GC, which can be         be encoded within the finite amount of available concrete
more expensive than is worth. So garbage collectors, concur-          memory. A GC’ed implementation will be live if it never
rent or not, may have various degree of “conservativeness”            stops or hangs, if progress of concrete computations corre-


                                                                  2
spond to observable progress of abstract computations; this               that constitute a program in context, and of the (step) re-
means that GC activity will always give the hand back to                  lation as one of (atomic) reduction from one expression to
mutator activities after a (hopefully short) while. A GC’ed               another. The elements that are ≤ to a given expression are
implementation will be real-time if there can be a bound                  refined expressions into which it may be rewritten, that have
on the “while” involved in making abstract computations                   more specialized denotational semantics than the considered
progress; in presence of concurrent activities, this affects              expression. The computing system can thus be viewed as a
not only liveness of the implementation, but also soundness,              term rewrite system.
since the mutator activities must “stabilize” fast enough so                  Finally, category theorists [20] will consider a preorder
that the GC can do its job and yield back execution to other              as just a category whose objects are the elements of the
mutators fast enough.                                                     set, and whose arrows are couples of objects that satisfy
    Without going into the details of garbage collection, we              the binary relation (i.e. a category where you decide not to
have already isolated properties that we require from im-                 distinguish arrows that have same domain and codomain).
plementation of garbage-collected languages. There now re-                The objects of the category are the semantic interpretations
mains to formalize this intuition.                                        of the programs of a language, endowed with a preorder
                                                                          structure.
3     A Simple Model for Implementation                                       This same model seems to be a common root to most
                                                                          widely-used formal frameworks for defining and analyzing
3.1    Modelling Computing Systems                                        the semantics of computing systems: denotational seman-
                                                                          tics, operational semantics, rewrite logic, abstract state ma-
Before we can express the notion of implementing a comput-                chines. It may thus be used to model implementations of a
ing system with another, we must first formalize the notion               system whose semantics is described in one of these frame-
of a computing system. By “computing systems”, we mean                    works with another lower-level system whose semantics is
just anything, from the most universal computing system                   described in another of these frameworks. Note that this
(such as a full-fledged installation of GNU/Linux) down to                model conspicuously takes into account only internal be-
the most special-purpose finite device (that may itself be                havior of computing systems, the spontaneous intrinsic re-
given by a description within a universal system). Turing-                lations, transitions, reductions or morphisms that exist be-
machines (universal or not) or variants of λ- or π- calculi               tween elements, states, expressions or objects of the system.
1
   are eligible, as are systems constituted by the states of              This model could be extended with more structure, but this
execution of general- or special-purpose programming lan-                 is not essential to the current study.
guages, or by just the reachable states of execution of a given               In the rest of this paper, we will indifferently use the
program in some language.                                                 vocabulary of a set theorist, a model theorist, a logician, a
    We’ll choose the simplest model we can think of that has              semantician, a category theorist, in an attempt to raise uni-
some characteristic significant structure, so as to get the               versal mutual understanding. In diagrams, we’ll also draw
intuition of what we mean without having to overcome too
many details. We feel that the essence of computation is                                                 ∗
                                                                                                     x       x′
that an operator sets some initial state in a system, and lets
the system evolve in a sequence of state transitions; at times,           the fact that x ≤ x′ and
the operator will observe the current state of computations,
so as to see possible progress or success of the system.                                                 +
    To formalize such a model, we will consider what set the-                                        x       x′
orists call a preorder: a set with a internal binary relation
                                                                          the fact that x ≤ x′ and x 6= x′ . Assuming that ≤ is indeed
≤ that is both reflexive and transitive. ≤ is sometimes ob-
                                                                          defined from a step relation −→, we’ll also draw
tained as the reflexive transitive closure −→∗ of a “step”
relation −→; however, it needs not be, and it is often con-
                                                                                                     x       x′
fusing to try to express everything in terms of atomic steps.
    Model theorists who think in terms of stateful abstract               the fact that x is rewritten in x′ in one step.
machines will like to understand an element of the set as a
possible state of the machine, and of the (step) relation as
one of (atomic) transition from one state to another. The                 3.2   Implementation
elements that are ≤ to a given state constitute the possible              Informally, we want an implementation to be a correspon-
future states into which it may naturally evolve. The com-                dance between two computing systems, an “abstract” sys-
puting system can thus be viewed as a transition system.                  tem A and a “concrete” system C, whereby states in a (hope-
    Logicians may rather consider the states as states of rel-            fully large enough) fragment of A are each “implemented” by
evant knowledge about the system [12], and the relation as                a choice of one or more states in C. Implementation means
a monotonous refinement or non-monotonous evolution of                    that an implementing concrete state should somehow have
this knowledge. The elements that are ≤ to a given state                  the “same” observable behavior as the implemented abstract
are possible future states of knowledge about the system in               state, although it may do as it pleases when abstract behav-
presence of internal though process only. The computing                   ior is only partially specified. An implementation may be
system can thus be viewed as a logical reasoning system.                  partial: sometimes, not all of the abstract system is im-
    Semanticians who study programming languages, will                    plemented (particularly if said abstract system is infinite,
like to understand an element of the set as the expression                while the concrete system is finite); we will be satisfied with
   1
     There must be some relation between the notion of implemen-
                                                                          a fragment of the abstract system that be big enough to
tation and that of (bi)simulation, as known in asynchronous process       successfully complete considered computations.
calculi, but cannot say which at the time being.                              To formalize the notion, consider systems A and C en-
                                                                          dowed with preorders as above. An implementation will be


                                                                      3
some kind of partially-defined non-deterministic but injec-               the rest of this section, we’ll consider as defined above an im-
tive function from A to C; its inverse function, a partial                plementation Φ−1 of an abstract computing system A with a
deterministic function from C to A will be a “partial inter-              concrete system C through the intermediate system O, given
pretation” of C in A.                                                     by the canonical injection j : O ֒→ C, and an interpretation
    Partial and non-deterministic functions have not been as              function φ : O −→ A.
widely used for formal reasoning as have been their total de-
terministic counterparts, but have nonetheless been studied               4.1   Safety
and formalized in logical, mathematical or computational
frameworks [8, 22, 27]. Set theorists might just consider                 The most essential property, that we will require from just
them as just binary relations; applicative functional pro-                every implementation so it be considered correct, is that of
grammers may take them as a primitive concept; but cate-                  safety: any observable result that be yielded by concrete
gory theorists as well as many people will prefer to express              evaluation must correspond to a valid abstract result that
them in terms of total deterministic functions.                           could legally have been obtained by evaluation in the ab-
    A partial function f from a set X to a set Y can be easily            stract system.
macro-expressed from within common frameworks of total                        Formally, for any diagram
deterministic functions, as the data of an intermediate set
Z of individual associations, and two (total deterministic)                                             a       a′
functions anf : Z → X and imf : Z → Y respectively giving
the antecedent and image of every individual association.                                           Φ           Φ
Thus, y is a possible value of f (x), which we write y ✁                                                    ∗
f (x), iff there is a z such that anf (z) = x and imf (z) = y.                                          c        c′
                                                                                                            C
f is deterministic iff anf is injective; it is total iff anf is
surjective; it is surjective iff imf is surjective; it is injective       we must be able to complete the diagram into
iff imf is injective. In particular f is total deterministic iff
anf is bijective.                                                                                           ∗
    To stay within a framework of total deterministic func-                                             a       a′
                                                                                                            A
tions, we’ll thus have an implementation be the data of an
                                                                                                    Φ           Φ
intermediate set O of “observable abstract states” (or equiv-
alently of “stable concrete states”), with an injection j from                                              ∗
                                                                                                        c        c′
O into C (equivalently, we will consider O as a subset of                                                   C
C), and a function φ from O to A. We can then say that a
concrete state c is stable and corresponds to observable ab-              That is, if by computing from an implementation c of a, we
                          φ        j                                      can observe an (intermediate or final) concrete state c′ that
stract state a iff a           o        c which we’ll also write          can be interpretable as abstract state a′ , then a′ must be
                       Φ                                                  a correct result that could have been found by doing com-
more simply as a            c . We will use the following dia-            putations purely within the abstract system. Any abstract
gram                                                                      observation made by observing and interpreting the concrete
                                Φ                                         system must be valid in the abstract system.
                           A         C
                                                                              In other words, the basic reduction structure of the com-
to denote the fact that Φ = j ◦ φ−1 be an implementation
                           −1                                             puting systems must be preserved by φ. Set theorists will
of A with C. Note that we privilege the inverse Φ = φ ◦ j −1              say that φ is a non-decreasing function; category theorists
of the implementation Φ−1 ; in fact, as we’ll see later, it is            will say that φ is a (covariant) functor2 . Note that by the
the “interpretation” Φ, not the implementation Φ−1 , that                 very construction of the structure on O as induced from C,
preserves structure and deserves to be an arrow.                          it is given that j be structure-preserving.
    There remains to give a computing system (preorder)                       Safety is a composable property: if Φ−1 is a safe imple-
structure on O. Since O is conceptually a subset of C                     mentation of A with C, and Ψ−1 is a safe implementation
(through embedding j), we may quite naturally define ≤ in                 of C with D, then Ψ−1 ◦ Φ−1 is a safe implementation of A
O such that o ≤ o′ in O iff j(o) ≤ j(o′ ) in C. Set theorists             with D.
say that we consider on O the preorder structure induced                      To illustrate the difference between safe and unsafe, con-
by C, or the reciprocal image through j of C’s structure.                 sider computations on natural numbers, where the states we
Category theorists say that O is a full subcategory of C, or              observe are those when the system yields results. An imple-
that j is an embedding of O in C.                                         mentation with fixed-precision integers will be safe if it traps
    To sum up, when we have such a partial function Φ =                   on overflow; any result it will yield will be correct. An im-
φ ◦ j −1 with φ : O −→ A and j : O ֒→ C, then we say that                 plementation with fixed-precision integers that silent wraps
Φ−1 is an implementation of A with C through O.                           computations that overflow is not safe, and may yield wrong
                                                                          results when initial conditions imply too large numbers dur-
                                                                          ing computation. Note that safety does not mandate termi-
4   Properties of an Implementation
                                                                          nation. It only mandates that in case of termination or legal
Now that we have laid out the basic framework for study-                      2
                                                                                Let us remark the fact that structure preservation happens in
ing the notion of an implementation, we can formalize good                a way contravariant to that of Φ−1 : the “interpretation function” φ
properties that we expect from an implementation so it be                 that preserves structure goes in a direction opposite to that of the
                                                                          implementation Φ−1 . In categorical words, the theory of implemen-
considered useful. Of course, depending on our (informal)                 tation is inherently decompositional, rather than compositional. We
intent for a given implementation, we’ll require a different              may argue that it explains the utter failure of so many attempts to
set of properties to be fulfilled by this implementation. In              build compositional meta-objects framework. This justifies our priv-
                                                                          ileging Φ as the object of logical interest.



                                                                      4
observation, the implementation yield a correct result. It is               Φ−1 is an implementation of A with C through O, and Ψ−1
always safe to not answer; of course, answers are desirable                 is a sound implementation of C with E such that all image
when possible, but misleading incorrect answers are worse                   values of Ψ in C are also in O, then Ψ−1 ◦ Φ−1 is sound.
than no answer. When designing mission-critical systems, it                     Variant: We can have various notions of “real-time”
is safe not to come with a design, but unsafe to come with                  and/or bounded-resource soundness, assuming we have a
a design that might erroneously kill people under intended                  notion of “duration” or “size” of transition paths between
use conditions.                                                             two states, by requiring that can be exhibited transition
    This notion of safety is the same as found in works by                  path from c′ to c′′ be of duration or size less than some
Lamport [17]. It is what Goerigk calls partial correctness [9],             maximum admissible response time or more generally than
“partial” corresponding to the fact that Φ be a partial func-               some maximum pre-allocated amount of resources.
tion rather than a total function.
    Since safety is such an essential property, from now on,                4.3   Completeness
we’ll only consider safe implementations. Besides, the cat-
egorical formalism we chose to be equally used as others                    An interesting property that we may require from an imple-
demands structure-preservation from every considered func-                  mentation, is that of completeness, whereby all transitions
tion, anyway.                                                               from a given implemented abstract state are themselves im-
                                                                            plemented.
4.2   Soundness                                                                Formally, from diagram

Another important property of implementations is that of                                                   ∗
                                                                                                       a       a′
soundness: an implementation is sound iff any possible con-                                                A
crete transition path is somehow “meaningful”, and corre-                                          Φ
sponds to part of an abstract transition path3 .
   This can be formalized by requiring that any diagram                                                c

                                 a                                          deduce diagram
                                                                                                           ∗
                             Φ                                                                         a       a′
                                                                                                           A
                                     ∗                                                             Φ           Φ
                                 c        c′
                                     C
                                                                                                           ∗
                                                                                                       c       c′
may be completed into a diagram                                                                            C
                                                                                Note that we do not require every abstract state to be
                                     ∗                                      implemented, which is a property that we call totality (from
                         a                     a′′
                                     A                                       a deduce a          c ). An implementation that has both
                     Φ                         Φ                                            Φ
                             ∗            ∗                                 completeness and totality will be said to be faithful. Com-
                         c           c′        c′′                          pleteness and totality are composable properties. Complete-
                             C            C                                 ness and soundness combined yield a composable property,
                                                                            too. If we look at temporal logic statements on transitions,
That is, if concrete computations starting from a stable state
                                                                            completeness ensures preservation of increasing “may” state-
c have led to intermediate state c′ , then they must lead from
                                                                            ments by Φ.
c′ to a further stable state c′′ .
                                                                                Variant: Sometimes, we don’t require that all possible
    In other words, the concrete system mustn’t have mean-
                                                                            transitions be implemented, but only that there be at least
ingless transitions, whereby it spontaneously go wild or enter
                                                                            one implemented transition whenever there is a transition
a deadlock; instead, starting from a stable state, it must al-
                                                                            possible from a given observable abstract state. Formally,
ways keep the possibility of evolving into a stable state, of
                                                                            from same diagram as for completeness above, deduce dia-
“stabilizing”.
                                                                            gram
    Soundness as such is not a composable property, since
                                                                                                          ∗
given sound implementations Φ−1 of A with C and Ψ−1 of                                                 a      a′′
C with E, we cannot know for sure without an additional                                                   A
hypothesis that the observable state in C that we obtain                                             Φ       Φ
from invoking the soundness of Ψ−1 is itself a stable state                                               ∗
with respect to Φ−1 . However, there are several ways to                                               c      c′′
                                                                                                          C
obtain some degree of composability for soundness results,
by invoking additional properties. For instance, composition                with a′′ not a priori related to a′ . We call this property
of a sound implementation of A with C with a sound and                      advance-preservation. Advance-preservation is not compos-
complete implementation of C with E (see below). Also, if                   able.
   3
      It so happens that logicians tend to call “soundness” the prop-
erty that we above called “safety” [13]. To avoid confusion, it might       4.4   Liveness
be better to use another name for the present property. The name
“metastability”, albeit long and hard-sounding, has been proposed,          A useful property to require from an implementation is that
since the property ensures that an external monitoring “meta-object”        of liveness: any concrete evaluation must spontaneously ad-
may stabilize the state of the system so that concurrent internal ac-
tivities will only make safe observations; We are not otherwise aware
of this property having been given a name before.



                                                                        5
vance. Formally, given a diagram                                           but requires in its conclusion that

          a                                                                                             a         a′
                                                                                                             A
      Φ
              +         +            +       ...   +        +   ...        instead of merely that
        c0         c1           c2                     cn
              C         C            C             C        C
                                                                                                             +
                                                                                                        a         a′
with c0 . . . cn . . . an infinite sequence of strict transitions in                                         A
C we deduce
                               +                                           which means that you can retrieve individual abstract steps
                          a          a′
                               A                                           of computation from a concrete trace of execution; i.e. stable
                        Φ          Φ                                       states are never optimized away as could otherwise be done.
                               +         ∗
                          c0         c′      ck                            5     Synchronizing Concurrent Implementations
                               C         C
That is, there is an integer k such that abstract computation              5.1    Concurrent Implementations
has strictly advanced before concrete computation reaches                  A concurrent computation system is a system made of
k-th transition.                                                           mostly independent components. Most of the time, compo-
    Liveness is a composable property. If we look at temporal              nents behave like independent computing systems of their
logic statements on transitions, liveness ensures preservation             own, with local transitions that do not affect other compo-
of increasing “must” statements by Φ.                                      nents, and may happen in parallel. Sometimes, the compo-
    Variant:     For “real-time” or otherwise bounded re-                  nents interact with each other, and the global system state
source variants of liveness, we strengthen the property by                 is modified in a non-local synchronized way.
weakening the hypothesis that the sequence (cn ) be infi-                      To formalize that, consider a system S such that the set
nite, and introducing instead some weaker criterion of be-                 of states of S is the product Πi∈I Si of the set of states of var-
ing “long enough” for sequence (cn ) (for instance being of                ious subsystems (Si )i∈I . Each subsystem Si is called a com-
length greater than N , for a given integer N ). Such vari-                ponent of the system, and the each projection pi : S −→ Si
ants may compose or not, depending on expected criteria on                 is called a partial view on the system. Each Si is also en-
the length of transition paths for the implementations being               dowed with a “local” computational structure −→Si . The
composed and for their result.                                             global system S has a computational structure −→ such that
    Variant: With strong liveness, we consider individual                  the product structure Πi∈I −→Si is fully included in the
steps instead of just strict transition, and we demand that                structure −→; that is, any tuple (ti )i∈I of (possibly null)
c′ = ck . Hence, from                                                      local transitions is a valid global transition, so that local
                                                                           transitions may happen “in parallel”. S may also have ad-
          a                                                                ditional “synchronized” transitions, that are no products of
      Φ                                                                    local transitions, and represent coherent communication or
                                                                           interaction between two or more components of S 4 .
        c0         c1           c2           ...       cn       ...            A concurrent implementation is simply an implementa-
              C         C            C             C        C              tion the concrete system of which is a concurrent system.
                                                                           When implementing a concurrent abstract system with a
with c0 . . . cn . . . an infinite sequence of steps in C, we deduce       concurrent concrete system we often want to establish a
                                                                           correspondance between components of the concrete system
                                     +                                     and components of the abstract system. This can be for-
                                a        a′
                                     A                                     malized as having partial views of each system that make
                            Φ            Φ                                    4
                                                                                 Note that with the above definition, just any system could be
                                     +                                     considered concurrent by butchering it into components, trying to de-
                            c0           ck                                fine proper sets of local transitions, and falling back to having only
                                     C
                                                                           null transitions on every component, with every transition not ex-
                                                                           pressed as a product of local transitions being considered a “synchro-
    Strong liveness combines both weak liveness and sound-                 nized” transition. Concurrency is not an intrinsic property of a com-
ness simultaneously in the same property, and is compos-                   puting system, but a property of its formalization; a same computing
able, all of which make it a very pleasing property. It is                 system may have several distinct concurrent or sequential formaliza-
                                                                           tions, whose interest depend on the problem the user is trying to solve
a useful property for a single-threaded monoprocessor im-                  when studying the system. For instance, in the case of GC as consid-
plementation of a computing system, and allows for design                  ered before, most monoprocessor GC’ed implementations statically
of straightforward such implementations. However, it is                    interleave GC with mutator threads at allocation points; there is no
so strong that it costs too much to achieve in a concur-                   explicit GC thread visible from the system thread scheduler, only a
                                                                           special system mode for GC; conceptually though, we can still con-
rent or distributed implementation, since it requires sponta-              sider GC to happen as a concurrent service, one important enough
neous and simultaneously synchronization of all the concur-                that it has a specific scheduler, optimized for cheap synchronization
rent or distributed processes. Strong liveness like the previ-             and inlined around the whole program. As says Lamport, processes
ous, “weak”, liveness, has “real-time” and bounded-resource                are in the eye of the beholder [18].
variants, with similar remarks as in the above cases.
    An even stronger (and still composable) variant, strong
step preservation has same hypotheses as strong liveness,



                                                                       6
the following diagram commute:                                        be optimized and inlined all around “user” code to achieve
                                                                      better efficiency, rather than having a kernel. Finding an
                              p A′                                    optimized version of a monitor for the implementation of a
                          A           A′
                                                                      given abstract system with a given concrete system is left as
                                                                      an exercise to the reader.
                        Φ            Φ′
                                                                          The above implementation technique thus allows to mo-
                              pC ′                                    dularly achieve a safe and sound concurrent implementation
                          C           C′
                                                                      of a concurrent system from safe and sound implementations
Note that the concrete system will typically have more com-           of each of its components, as combined with a suitable mon-
ponents than the abstract system, with additional compo-              itor; the monitor ensures that interactions between concur-
nents representing system services such as message-passing            rent activities may only happen when all relevant activities
kernels, schedulers, garbage collectors, etc.                         are synchronously in a suitably stable state. What remains
    Assuming we know how to separately implement each of              to be acknowledged about it is that the key to this modular
the components of a given abstract system (as considered              design is in the notions of stable states and of sound imple-
with its local structure), as well as how to implement the            mentation. And the key has to match the lock: the latter
“synchronized” transitions (possibly in a sequential way),            notion depends on the former, and the former depends di-
the question is how to achieve a “reasonably concurrent”              rectly on the abstract system being implemented, its concur-
implementation of the whole system, that would allow lo-              rency and atomicity model; when implementing a different
cal transitions to happen concurrently while still performing         application, the abstract system changes, and so does the
global synchronized transitions. That is, we want a tech-             notion of stable state, so does the concurrency and atomic-
nique to correctly combine concurrent implementations.                ity model. This means that a monitor for a given low-level
                                                                      notion of stability isn’t immediately suitable as a monitor for
5.2   Soundness as a Synchronization Primitive                        a higher-level notion of stability that would have additional
                                                                      invariants; given such a notion, it requires the rework of a
The solution we formalize is to require each component’s im-          complete new layer of a monitor and of wrappers around user
plementation to be not just safe but also sound (and possibly         processes so as to implement the abstract system, and then,
complete, live, etc), and to use one or several additional sys-       wrapped user processes cannot interact seamlessly with un-
tem components to monitor synchronization of “user” com-              wrapped user processes. This gives a theoretical account of
ponents. Actually, this solution is being used universally, in        the abstraction gap that prevents seamless mixing of com-
a large variety of special cases.                                     ponents written in high-level languages such as Java with
    Consider an abstract system A with components Ai , such           components written in low-level languages such as C, least
that we have a safe and sound implementation of each Ai               the low-level component follows stringent conventions such
with Ci . Then we can construct a safe and sound imple-               as JNI.
mentation C of A with “user” components Ci′ and “system”                  All in all, it appears that it is useful to define several
components Cs , defined as follows: the states of Ci′ are the         notions of state stability, depending on the kind of synchro-
product of those of Ci with the state space of additional             nization needed, on the invariants that the system is able to
control flags and data that will be shared with the monitor           express. Unability for a high-level programming language
and mostly controlled by the monitor, but accessible to no            to directly express the user application’s arbitrary invari-
other Cj′ . When control flags indicate Ci′ is running, then          ants leads to expensive cost in terms or program complexity
Ci′ has local transitions corresponding to each of Ci ’s tran-        and inefficiency due to abstraction inversions [3] involved in
sitions. When control flags indicate Ci′ must stop, it will           reimplementing the application’s conceptually low-level in-
by soundness converge to a stable state, set a control flag           variants in terms of the programming language’s high-level
indicating stability, and stop (i.e. have no more transition).        primitives.
When a synchronized transition is to happen, because a user               Use of various mechanisms to achieve transparent preser-
component wants to communicate, or because some system                vation by the system of a non-trivial notion of stability can
service (clock, GC, I/O driver, etc) triggers one, the mon-           be traced back at least to ITS [7], in the late 1960’s, with
itor will set “stop” flags on all relevant components, wait           its PCLSRing feature [4], whereby interrupted system calls
for their all being stabilized, and execute a sequential im-          would always leave a process in valid user mode state. “Re-
plementation of the abstract synchronized transitions from            flective” systems attempt to provide a way for the program-
stable abstract component states; it may reactivate the com-          mer to define monitors within his usual application program-
ponents when done, or begin another abstract synchronized             ming language, using “metaobjects” that run concurrently
transition.                                                           with normal objects and are able to control them [21, 14].
    Particular instances of this technique have been in use           However, the only language we know that allows the pro-
for decades, and informally constitute the very core of op-           grammer to directly define his own notion of stability is
erating system and language implementation design. Op-                C--, with its notion of safe-points, and with soundness be-
erating systems for time-sharing systems are thus typically           ing specified in terms of an ExecuteToNextSafePoint prim-
implemented with a “kernel” serves the role of monitor for            itive [24]. Not surprisingly, the need for such notion was a
the implementation of a collection of “user processes” and            direct consequence of designing the C-- language as a generic
“system services” that constitute the abstract computing              portable back-end to arbitrary high-level languages, each
system. Note that the monitor may itself be split into con-           with its own abstract notion of stable state. Our study sug-
current components, each corresponding to special kinds of            gests that all languages, even high-level languages, should
synchronized transitions that may be implemented without              have the capability of defining one or several notions of sta-
global synchronization; this is all the truer since the con-          ble states, for they are always used to implement applica-
current system can be distributed rather than centralized.            tions that are higher-level computing systems than they are.
On the other hand, as with GC, part of the monitor may


                                                                  7
5.3    Techniques to Achieve Soundness                                    This formal notion of implementation could be used to
                                                                      specify failsafe implementations, by considering various “en-
We have formalized soundness and seen how to use it, but              richments” of the concrete system of an implementation with
haven’t yet explained how it could be implemented. Herein,            additional state transitions for every kind of failure, and
we’ll try to give a general view of well-known techniques             studying properties that are preserved in presence of fail-
that have already been used in the past to achieve soundness          ures (in increasing order of preference, liveness, soundness,
whenever it has been needed. Mosberger et al. [23] propose            safety).
use of various stabilization techniques for achieving atomic              A further research area we intend to explore, is to use
operations in presence of interrupts.                                 this formal notion of an implementation, together with a for-
    The general idea behind implementing soundness is that            mal notion of metaprogramming [26] to better understand
the state of an interrupted process to be stabilized must be          and specify the semantics of reflective systems. Reflective
rolled back or rolled forward to some previous or next sta-           systems are an attempt to allow direct expression (as op-
ble state. Roll-back is implemented by making reversible              posed to mere manual implementation) of user-defined do-
all operations effected since last stable state, which may            main specific languages, by dynamically interning an im-
mean storing all modified components of the stable state,             plementation of these languages; formalizing the notion of
or logging reversal information for every modification. It            implementation is thus necessary to specify the correctness
isn’t always possible to roll-back, since some operations are         of reflective programs.
intrinsically irreversible; for instance, you can’t usually un-           We may even try to deduce “meta-object protocols” from
print data that was sent to a line-printer. Roll-forward is           the above-mentionned formalized logical properties: stabi-
typically implemented by reentering the interrupted activ-            lization primitives can be considered a computational coun-
ity in a special mode that will stop at next safe point. Safe         terpart to the logical property of soundness, and we may try
points may detect the necessity of stopping by polling a par-         to similarly find computational counterparts to other logical
ticular system flag, by releasing and reacquiring locks at the        properties.
end of atomic blocks, which are ways to manually achieve                  A related research topic is Aspect Oriented Program-
strong liveness as previously suggested. A more complicated           ming [15], whereby a program is defined by multiple dis-
but more efficient efficient technique is to temporarily mod-         tinct aspects that an implementation of the program should
ify user code so its jump out into the monitor instead of             simultaneously implemenent. For instance, from our analy-
continueing execution; Ogesen used such technique for GC              sis of the notion of implementation, we may interpret cross-
in the EVM implementation of Java [1].                                cutting problems in AOP as the expression of implementa-
    Now, whatever nifty mechanisms the system uses to                 tion being a decompositional notion rather than a compo-
achieve soundness with respect to its own invariants, lack of         sitional one. A particular class of systems that must thus
user-accessibility of such mechanisms forces the user to pay          simultaneously implement multiple aspects are systems de-
a high cost when enforcing the high-level invariants he cares         scribed with the ODP models, used in the industry and
about. In absence of efficient system support for soundness           telecommunications.
with respect to user-defined invariants, the user must indeed
fall back to the extremely costly methods of manually ac-
quiring locks or polling, or invest in unportable reimplemen-         References
tation of system mechanisms. User definability of varieties
of stability invariants and corresponding safe points can thus         [1] Ole Agesen. GC Points in a Threaded Environment.
be viewed as a declarative dual to manually acquiring and                  Technical report, Sun Microsystems, 1998. http://
releasing locks around critical sections; like all declarative             www.sunlabs.com/research/java-topics/.
approaches, it requires an additional bit of support from              [2] Lourdes Araujo. Correctness proof of a Distributed
metaprogramming tools (compilers), but in exchange allows                  Implementation of Prolog by means of Abstract State
the latter to do all kinds of system-dependent optimizations               Machines. Journal of Universal Computer Science,
that the programmer couldn’t otherwise achieve in a way at                 3(5):416–442, 1997.    http://www.eecs.umich.edu/
the same time a simple, portable, and efficient.                           gasm/verif.html.

6     Conclusion                                                       [3] Henry G. Baker. Critique of DIN Kernel Lisp Definition
                                                                           Version 1.2. Lisp and Symbolic Computation, 4, 4:371–
We have defined a generic notion of implementation, appli-                 398, March 1992.
cable to a wide variety of existing systems and formalisms.
We have formalized various desirable properties of imple-              [4] Alan Bawden. PCLSRing: Keeping Process State Mod-
mentations, and identified one, soundness, that we think                   ular. Technical report, MIT, 1989. http://fare.
lacked deserved recognition. We have shown how to use our                  tunes.org/tmp/emergent/pclsr.htm.
formalized concept of soundness to achieve concurrent im-              [5] David Chase and al. Garbage Collection FAQ, 1996.
plementations of concurrent systems in a modular way. We                   http://www.iecc.com/gclist/GC-faq.html.
have stressed the fact that at the center of all the proper-
ties we studied lies the intrinsically application-dependent           [6] Paul Curzon. A verified Vista implementation. Tech-
notion of a stable system state. We have accordingly sug-                  nical Report 311, University of Cambridge, Computer
gested that language design should include an explicit user-               Laboratory, September 1993. http://www.cl.cam.ac.
definable notion of stable system state.                                   uk/users/pc/fintr93.html.
    We think that the above contribution is of interest to
language designers as well as to people trying to formally             [7] D. Eastlake, R. Greenblatt, J. Holloway, T. Knight, and
establish the correctness of program implementations and                   S. Nelson. ITS 1.5 Reference Manual. Memo 161a, MIT
of implementing metaprograms.                                              AI Lab, July 1969.


                                                                  8
 [8] Solomon Feferman. Definedness. Erkenntnis, 43:295–            [22] Sigurd Meldal and Michal Antonin Walicki.
     320, 1995. http://math.stanford.edu/~feferman/.                    Nondeterministic Operators in Algebraic Frame-
                                                                        works. Technical report, Stanford CS Laboratory,
 [9] Wolfgang Goerigk. On the Correctness of Compilers                  1995.   http://elib.stanford.edu/Dienst/UI/2.0/
     and Compiler Implementations. Technical report, 1995.              Describe/stanford.cs/CSL-TR-95-664.
     http://i44s11.info.uni-karlsruhe.de/~verifix/.
                                                                   [23] David Mosberger, Peter Drushel, and Larry L. Peter-
[10] Wolfgang Goerigk and Ulrich Hoffmann. Rigorous com-                son. Implementing Atomic Sequences on Uniproces-
     piler implementation correctness: How to prove the real            sors Using Rollforward. Software – Practice and Expe-
     thing correct. In Proc. FMTrends’98. Springer, 1998.               riences, 26(1), January 1996.
     http://i44s11.info.uni-karlsruhe.de/~verifix/.
                                                                   [24] Simon Peyton-Jones and Norman Ramsey. Machine-
[11] Joshua D. Guttman and Mitchell Wand, editors.                      Independent Support for Garbage Collection, Debug-
     VLISP: A Verified Implementation of Scheme. Kluwer,                ging, Exception Handling, and Concurrency. Techni-
     Boston, 1995. Originally published as a special dou-               cal Report CS-98-19, Department of Computer Science,
     ble issue of the journal Lisp and Symbolic Computation             University of Virginia, August 1998. http://www.cs.
     (Volume 8, Issue 1/2). ftp://ftp.ccs.neu.edu/pub/                  virginia.edu/~nr/pubs/c--rti-abstract.html.
     people/wand/vlisp/lasc/.
                                                                   [25] Cornelia Pusch. Verification of Compiler Correct-
[12] J. Y. Halpern, R. Fagin, Y. Moses, and M. Y Vardi.                 ness for the WAM. In J. von Wright, J. Grundy,
     Reasoning About Knowledge. MIT Press, 1995.                        and J. Harrison, editors, Theorem Proving in Higher
[13] John Hannan and Frank Pfenning. Compiler verifi-                   Order Logics (TPHOLs’96), pages 347–362. Springer-
     cation in LF. In Proceedings, Seventh Annual IEEE                  Verlag, 1996. http://isabelle.in.tum.de/~pusch/
     Symposium on Logic in Computer Science, pages 407–                 pubs/Pusch_TPiH1996.html.
     418, Santa Cruz, California, 22–25 June 1992. IEEE            [26] François-René Rideau. Metaprogramming and free
     Computer Society Press. http://www.cs.cmu.edu/                     availability of sources, January 1999.    Translated
     ~fp/papers/.                                                       from the french article “Métaprogrammation et li-
[14] R. Kaer and Th. Mahler. Introducing and Model-                     bre disponibilité des sources” published in confer-
     ing Polycontextural Logics. Technical report, Insti-               ence “Autour du Libre 1999”. http://fare.tunes.
     tut für Kybernetik und Systemtheorie, 1998. http:                 org/articles/ll99/index.en.html.
     //www.techno.net/pcl/tm/plisp/.                               [27] François-René Rideau. Reflection, non-determinism,
[15] Gregor Kiczales, John Lamping, Anurag Mendhekar,                   and the lambda-calculus. Rapport de recherche non
     Chris Maeda, Cristina Videira Lopes, Jean-Marc Lo-                 publié, CNET, 1999. http://fare.tunes.org/tmp/
     ingtier, and John Irwin. Aspect-Oriented Program-                  rndlc/.
     ming. In proceedings of the European Conference on            [28] Paul R. Wilson. Uniprocessor Garbage Collection Tech-
     Object-Oriented Programming (ECOOP), number 1241                   niques. In Proceedings of the 1992 International Work-
     in LNCS. Springer-Verlag, June 1997. http://www.                   shop on Memory Management, 1992. http://www.cs.
     parc.xerox.com/spl/projects/aop/.                                  utexas.edu/users/oops/papers.html.
[16] Leslie Lamport.       On Interprocess Communi-
     cation.     Distributed Computing, 1(2):77–101,               A   Acknowledgements
     1986.    http://gatekeeper.dec.com/pub/DEC/SRC/
     research-reports/abstracts/src-rr-008.html.                   I would like to thank Elie Najm, my PhD advisor, for helping
                                                                   me to clarify some implementation concepts. I am particu-
[17] Leslie Lamport. A Simple Approach to Specifying               larly indebted to Fabien Delpiano, my fellow PhD student,
     Concurrent Systems. Technical Report SRC-015, Digi-           for his precious help while writing this paper. Also, I wish
     tal, 1988. http://gatekeeper.dec.com/pub/DEC/SRC/             to thank members of the Tunes project for their constant
     research-reports/abstracts/src-rr-015.html.                   help and support. Last but not least, I must express my
                                                                   gratitude to Jean-Bernard Stefani, head of the marvelous
[18] Leslie Lamport. Processes are in the Eye of the Be-           department DTL/ASR of CNET, who made this research
     holder. Technical report, Digital, 1994. http://www.          possible.
     research.compaq.com/SRC/personal/lamport/tla/.
[19] Leslie Lamport.   Refinement in State-Based For-
     malisms.   Technical Report SRC-1996-001, Digi-
     tal, 1996.  http://www.research.compaq.com/SRC/
     personal/lamport/tla/.
[20] Saunders Mac Lane. Categories for the Working Math-
     ematician, Second Edition. Springer, 1998.
[21] Satoshi Matsuoka, Takuo Watanabe, Yuuji Ichisugi,
     and Akinori Yonezawa. Object-oriented concurrent re-
     flective architectures. Lecture Notes in Computer Sci-
     ence, 612:211–??, 1992.



                                                               9
