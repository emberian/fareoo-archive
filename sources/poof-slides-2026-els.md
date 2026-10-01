# Slides: ELS 2026

- URL: https://fare.tunes.org/files/cs/poof/slides-2026-els.html
- Date: 2026
- Fetched: 2026-10-01T22:09Z (pandoc)
- Author: François-René Rideau (Faré)

---

[Dan Edwards and Peter Samson playing Spacewar! on a PDP-1]

Lambda, the Ultimate Paradigm

 

François-René Rideau <fare@mukn.com>

https://github.com/metareflection/poof

 

European Lisp Symposium 2026-05-11

 

PgDn: next

PgUp: previous

↑ ↓ ← → ESC ⏎

Touchscreen: swipe down until you must swipe right

Lambda, the Ultimate Paradigm

Plan of the Talk

- 
- Introduction: The Lambda Nature
- Does Lisp have the Lambda Nature?
- Fractured Symmathesy
- The Bright AI Lisp Future
- A New AI-assisted Lisp Symmathesy

Introduction: The Lambda Nature

Lambdist Koans (1)

[Greenblatt and Tom Knight before the Lisp Machine]

Introduction: The Lambda Nature

Lambdist Koans (2)

[The Connection Machine]

Introduction: The Lambda Nature

Lambdist Koans (3)

[LAMBDA: the Ultimate Imperative]

Introduction: The Lambda Nature

The Question

[SICP]

Introduction: The Lambda Nature

My Answer (1)

[Turing Machine]

Introduction: The Lambda Nature

My Answer (2)

[Pointing to the Moon]

Lambda, the Ultimate Paradigm

Plan of the Talk

- 
- Introduction: The Lambda Nature
- Does Lisp have the Lambda Nature?
- Fractured Symmathesy
- The Bright AI Lisp Future
- A New AI-assisted Lisp Symmathesy

Does Lisp have the Lambda Nature?

So, Was Lisp Great?

Does Lisp have the Lambda Nature?

Was Lisp Great? (1950s)

“Artificial Intelligence”,
Conditional Expressions,
Metacircular Interpreters,
Recursion,
Functional Programming,
List Processing and Symbolic Processing,
Dynamic Typing,
Interactive Programming,
Code as Data...

Does Lisp have the Lambda Nature?

Was Lisp Great? (1960s)

Automatic Storage Management (Garbage Collection),
Macros,
REPLs (then READ-EVAL-PRINT cycle),
Error handling,
Bootstrapped Compilers, Portable Programming,
Dynamic Scoping and explicit environment capture,
Symbolic Differentiation, Knowledge Representation,
Dynamic Code Extension, Logo,
Structure Editing, Time-sharing...

Does Lisp have the Lambda Nature?

Was Lisp Great? (1970s)

Object-Orientation, Prototype, Method Combination,
First-Class Continuation, Backtracking, Non-local Exit,
Lexical scoping, proper tail-call,
Extensible Editors, GUIs, Programmable Syntax,
Interactive Source-Level Debugging,
Rule-based Programming, Expert Systems,
Pattern-Matching, Constraint Propagation,
Concurrency- / Process- / Actor- oriented Programming,
Tagged Microarchitectures (Lisp Machines),
Lazy Evaluation, Typesystems, Theorem Provers...

Does Lisp have the Lambda Nature?

Was Lisp Great? (1980s)

CLOS—the greatest Object System ever designed—,
Massively Parallel Programming,
Macro Hygiene,
Commercial Lisp Machines, Network Programming,
Hypertext, CAD, Movie CGI, Symbolic Algebra,
Incremental Compilation, Dynamic Code Upgrade,
Resumable Exceptions, Delimited Control,
Genetic Programming, Orthogonal Persistence...

Does Lisp have the Lambda Nature?

Was Lisp Great? (1990s)

Meta-Object Protocols,
Web programming—especially so with continuations—,
ANSI CL standard,
C3 Linearization (Dylan),
Partial Evaluation (Scheme)...

Does Lisp have the Lambda Nature?

Was Lisp Great? (2000s)

Module Systems with Phase Separation (Racket),
Language-Oriented Programming (Racket),
Mixing Static Types and Dynamic Contracts (Racket),
Popularizing Persistent Data Structures (Clojure)...

Does Lisp have the Lambda Nature?

Was Lisp Great? (2010s)

Solver-aided programming (Racket (Rosette)),
Gradual typing matured (Racket),
Higher-order software contracts (Racket)...

Does Lisp have the Lambda Nature?

Was Lisp Great? (2020s)

Rhombus (Racket) — more infix syntax with macros
...

Does Lisp have the Lambda Nature?

Now, wait a minute...

Does Lisp have the Lambda Nature?

COPIED !?

[Newell & Simon paper on IPL]

Does Lisp have the Lambda Nature?

The LAMBDA Story

[McCarthy 'Programming - You're Doing It Completely Wrong' Meme]

Does Lisp have the Lambda Nature?

Adopt Any Paradigm

[Wild Chameleon Reptile With Beautiful Colors]

Does Lisp have the Lambda Nature?

Lisp Makes Paradigms Friends

Objects are a poor man’s closures.

— Norman Adams      

Closures are a poor man’s objects.

— Christian Quéinnec

Does Lisp have the Lambda Nature?

The Serendipity of Parentheses (1)

1958 LISP, MEXP, manually compiled:
foo=cons[bar;foo]

 

(SETQ FOO (CONS BAR FOO)) ; 1960 LISP I, SEXP, interpreted

 

MACRO (( ; 1963 LISP 1.5
(STASH (LAMBDA (FORM) (LIST (QUOTE SETQ)(CADAR FORM) (LIST (CONS (CADR FORM)
(CADAR FORM))) )))
))

Does Lisp have the Lambda Nature?

The Serendipity of Parentheses (2)

(DEFPROP PUSH ; 1966 PDP-6 LISP
  (LAMBDA (FORM)
    (LIST (QUOTE SETQ) (CADDR FORM)
      (LIST (QUOTE CONS)
            (CADR FORM) (CADDR FORM))))
  MACRO)

Does Lisp have the Lambda Nature?

The Serendipity of Parentheses (3)

(DEFUN PUSH MACRO (FORM) ; 1969 MACLISP
  (LIST 'SETQ (CADDR FORM)
    (LIST 'CONS
       (CADR FORM) (CADDR FORM))))

Does Lisp have the Lambda Nature?

The Serendipity of Parentheses (4)

(defmacro push (item place)
  ;; 1979 Lisp Machine Lisp
  `(setq ,place (cons ,item ,place)))

Does Lisp have the Lambda Nature?

The Serendipity of Parentheses (5)

(defmacro push (item place &environment env) ; 1984 CLtL1
    (multiple-value-bind
                    (temps vals stores store-form access-form)
              (get-setf-method place env)
        (let ((item-var (gensym "ITEM-")))
              `(let* ((,item-var ,item)
                              ,@(mapcar #'list temps vals)
                              (,(car stores) (cons ,item-var ,access-form)))
                    ,store-form))))

Does Lisp have the Lambda Nature?

The Serendipity of Parentheses (6)

(defmacro push (item place &environment env) ; 1991 ANSI CL
    (multiple-value-bind
                    (temps vals stores store-form access-form)
              (get-setf-expansion place env)
        (let ((item-var (gensym "ITEM-")))
              `(let* ((,item-var ,item)
                              ,@(mapcar #'list temps vals)
                              (,(car stores) (cons ,item-var ,access-form)))
                    ,store-form))))

Does Lisp have the Lambda Nature?

The Serendipity of Parentheses (7)

(define-syntax push ; Scheme
  (syntax-rules ()
    ((push item place)
     (set! place (cons item place)))))

Does Lisp have the Lambda Nature?

A Machine for Thinking (1)

I object to doing things that computers can do.

— Olin Shivers

Patterns mean “I have run out of language.”

— Rich Hickey 

Does Lisp have the Lambda Nature?

A Machine for Thinking (2)

[Le penseur de Rodin]

Lambda, the Ultimate Paradigm

Plan of the Talk

- 
- Introduction: The Lambda Nature
- Does Lisp have the Lambda Nature?
- Fractured Symmathesy
- The Bright AI Lisp Future
- A New AI-assisted Lisp Symmathesy

Fractured Symmathesy

Why Did It Stop?

Fractured Symmathesy

Symmathesy (1)

[Bruce Lee, Enter the Dragon Finger pointing to the Moon]

Fractured Symmathesy

Symmathesy (2)

[ARPANET Geographic Map September 1973]

Fractured Symmathesy

Symmathesy (3)

[Raphael’s The School of Athens]

Fractured Symmathesy

The AI Winter (1)

[Symbolics keyboard]

Fractured Symmathesy

The AI Winter (2)

[Berlin Wall fall]

Fractured Symmathesy

Tower of Babel

[The Great 'Tower of Babel', by Pieter Bruegel 1563]

Fractured Symmathesy

The Lone Wolf Curse

If you give someone Fortran, he has Fortran.
If you give someone Lisp, he has any language he pleases.

— Guy L. Steele Jr.

However, he’ll have a hard time finding someone else speaking
that same language he pleases.

— Faré (me)     

Fractured Symmathesy

Not Below the Line

[Iceberg]

Lambda, the Ultimate Paradigm

Plan of the Talk

- 
- Introduction: The Lambda Nature
- Does Lisp have the Lambda Nature?
- Fractured Symmathesy
- The Bright AI Lisp Future
- A New AI-assisted Lisp Symmathesy

The Bright AI Lisp Future

Turning the Tide

[Empty School of Athens]

The Bright AI Lisp Future

A Thinking Machine for Thinking Machines

[Robot variant of Rodin’s Thinker]

The Bright AI Lisp Future

Objective Costs

[Are there 10x developers?]

The Bright AI Lisp Future

Impedance Matching

[Pont du Gard]

The Bright AI Lisp Future

Diving Assistance

[Submarine dives Antarctica 2018]

The Bright AI Lisp Future

The Amplifier Problem (1)

[Op-amp symbol]

The Bright AI Lisp Future

The Amplifier Problem (2)

[3 star Michelin Restaurants Paris]

The Bright AI Lisp Future

The Amplifier Problem (3)

[Ripley Power Loader]

Lambda, the Ultimate Paradigm

Plan of the Talk

- 
- Introduction: The Lambda Nature
- Does Lisp have the Lambda Nature?
- Fractured Symmathesy
- The Bright AI Lisp Future
- A New AI-assisted Lisp Symmathesy

A New AI-assisted Lisp Symmathesy

AI-assisted Lisp Symmathesy

[Robot School of Athens]

A New AI-assisted Lisp Symmathesy

Prophecy and Challenge (1)

An extreme optimist is a man who believes that humanity
will probably survive even if it doesn’t take his advice.

— John McCarthy

A New AI-assisted Lisp Symmathesy

Prophecy and Challenge (2)

[Philippe Caza: Le Robot qui rêvait]

A New AI-assisted Lisp Symmathesy

Thank You!

Slides:          github.com/metareflection/poof

Join me:       Gerbil Scheme https://cons.io

Blog: ngnghm.github.io     X: x.com/ngnghm

Hire me:       <fahree@gmail.com>
