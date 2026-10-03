# LTUO canonical offline mirror — 2026-10-03

Canonical source: [Lambda: The Ultimate Object](https://fare.tunes.org/files/cs/poof/ltuo.html), François-René Rideau. Downloaded 2026-10-03; server reports last modification 2026-09-29 17:36:35 UTC. This is a work in progress, including an explicit editorial boundary in chapter 10; §10.6.1 is only a heading.

- [Open the offline book](../raw/mirrors/ltuo/2026-10-03/ltuo.html).
- [Exact fetch/asset manifest](../raw/mirrors/ltuo/2026-10-03/manifest.json), with URLs, retrieval timestamps, byte lengths and SHA-256 hashes.
- [Original HTTP headers](../raw/mirrors/ltuo/2026-10-03/ltuo.http-headers.txt).
- [Readable extraction](../raw/mirrors/ltuo/2026-10-03/ltuo-readable.txt) and [section/anchor index](../raw/mirrors/ltuo/2026-10-03/sections.json).
- Existing [October 1 book extraction](ltuo-book.md), [connected account](../FAREOO.md) and [historical Mini audit](../AUDIT.md) remain unchanged.

The canonical HTML is **4,266,596 bytes**, SHA-256:

```
0644ab39f5a08fef711abc5da19f3c703c2db260b10fda851ea512857377966c
```

It is byte-identical to the previously downloaded `raw/html/poof-ltuo.html`. Fresh Pandoc 3.11 extraction is also byte-identical to the earlier `raw/html/poof-ltuo.txt`; the old catalog header and all historical files were preserved. This retrieval establishes currency of that snapshot, not a newly revised edition.

The bounded mirror includes only the single-file book and its nine direct display assets. The canonical `scribble-common.js` URL returned HTTP 404. A supplemental script from the official Racket Scribble repository occupies that path in the offline mirror; its different source URL and exact hash are recorded. It is not represented as Faré's original script. The canonical HTML itself was not rewritten. The zero-byte `scribble-style.css` is the actual successful canonical response.

Validation resolved all 2,838 book-local anchor references against 1,474 anchor names, found no broken book-local anchors, and verified every direct asset is present. The four stylesheets reference no secondary assets. Bibliographic external links remain external; no linked-site crawl was performed. A local-browser check loaded the mirror, followed the §5.4.1 anchor, rendered text, formulas, code and side footnotes, and reported no console warnings or errors. The temporary browser and server were closed.

## Primary passages used for the Objective Bend construction review

Read these in the book itself, using the index above for all exact anchors. The following are navigation, not replacements for the text:

| Question | Sections and canonical links |
|---|---|
| Open versus closed modular extensions; context versus inherited/result target | [§5.4.1–4](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.M.E%29), [§8.2.1–4](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.T.N.M.Tf.M.E%29) |
| Deferral, sharing, and computational fixed points | [§5.3.2.3–5](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.Lazy_.Y%29), [§10.3.2](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.S.Ro.Ro.S%29) |
| Final self despite later overrides | [§5.5.4](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.Io.Ma.E%29) |
| Incomplete specifications; recursive specification/target conflation | [§6.1.2.3–6.1.4](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.First_.Issue__.Incomplete_.Specifications%29) |
| Linearization constraints, identities, C4 and suffix layout | [§7.3.3–7.4.6](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.R.Sa.D.N%29), [§10.4.2](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.Suffix_.Specifications%29) |
| Recursive self types, binary methods, existential type descriptors | [§8.3–8.4.4](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.N.N.O.O.T.T%29) |
| Independently varying context/focus and nested specifications | [§9.1.4–9.1.6](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.F.M.E%29) |
| After-the-fact protocol extension | [§9.2.9](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.Inherited_.Interfaces_vs_.Orthogonal_.Protocols%29) |
| Open policy questions for live code evolution | [§6.3.2](https://fare.tunes.org/files/cs/poof/ltuo.html#%28part._.Mo.Ia.C.U%29) |

Cross-checks read directly: [poof](poof-paper.md), §§1.1–1.2, 3, 4.1–4.3; [EOOMI](eoomi2024.md), §§3.1–3.2 and the lazy-initialization/§5.2 discussion; [First-Class Implementations](fci2017.md), §§2–5; [Climbing](climbing.md), §§2–5; [Persistence Model](persist-model.md), persistence domains, atomicity, synchronization, publishing, exhaustion, schema upgrade, execution context and domain composition; [C4-Mixins](c4-mixins-readme.md), semantics and suffix API.

The book's accompanying `pommette/pommette.scm` was also retrieved separately for a targeted read of `c4-linearize` and its tests, not as a display dependency of the book. In particular, the code updates ancestor counts when adding local-order candidate lists, a detail not explicit in the book's pseudocode. No claim of executing that Scheme suite is made.

Scholar: Codex primary-source lane, 2026-10-03. See the [primary-source construction synthesis](ltuo-objective-bend-20261003.txt) for consequential language decisions, proof obligations, independent source consumers, and the distinction between primary-source claims and proposed Objective Bend design. Full reading and council notes remain in the assigned scholar workbox; no completed implementation or refinement theorem is claimed by this catalog.
