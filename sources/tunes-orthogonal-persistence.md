# TUNES wiki: Orthogonal Persistence (Faré's old article)

- URL: http://tunes.org/wiki/orthogonal_20persistence.html
- Date: undated (TUNES era, ~2000s)
- Fetched: 2026-10-01T22:21Z (pandoc)
- Author: François-René Rideau (Faré), TUNES

---

CTO CLiki for the TUNES project

Home About CLiki Text Formatting

Orthogonal Persistence

The term for a system's property in which objects persist until they are no more needed, neither before, which would make the system fail, nor after, which would waste (eventually all) the system's limited resources.

Here are two short stories to illustrate the idea. When my mother first used a computer, she spent the whole night entering in a database the references of books in her library. Then, she shut the computer down, and went to sleep. The next day, she turned her computer back on, and the data had disappeared! She didn't "know" she had to explicitly "save" the data before to quit the application. Well, persistence of data means that the data would have been still there; orthogonal persistence of data means that she wouldn't have had to care about it. At about the same time, I had a wonderful battery-backed programmable pocket calculator, that never lost its data during normal operation; actually it would lose its whole patiently typed programs when the battery die or if doing really buggy operations (particularly when programming in assembler), with no means to backup on tape or disk. So that my calculator's memory was orthogonally persistent, but unsatisfyingly, not in a resilient, fail-proof way.

Orthogonal persistence is quite a natural concept, because this is exactly what people need when manipulating objects, as what counts to serious people is not (just) the fun they have during a computer session, but the work they accumulate during successive sessions. Untrained people, like my mother was, expect data to be orthogonally persistent; progress in computer systems like elsewhere is in not having to care. If you're not convinced in orthogonal persistence being natural, imagine that there would be two kinds of papers, one that would persist, the other that would self-destroy after it's no more on the top of your desk; you could use the latter for short-lived drafts, but you'd use the former for anything that has any worth; and even when you're not writing things that ought to last, you might be using the persistent paper, just because it might unexpectedly turn up as more valuable than initially expected, and you don't want to waste your precious mind resources at assessing the real shortlivedness of your information, nor at making a copy: your time is much more precious than the paper. So the only time you use short-lived paper would be in specific, scheduled events, as part of streamlined business use. The same should eventually happen with computers: only as part of developing optimized applications would people ever care about using memory that isn't orthogonally persistent.

Now, no single traditional "industry standard" operating system supports orthogonal persistence. This is most ridiculous, very error-prone, completely insecure, and is a major source of overhead to both programmers (IBM evaluated overhead of explicit fetching and storing of data to 30% of total program code, not taking into account check, conversion, and recovery of data), and users, who must constantly worry about saving their data, and are subject to horrible failures after some bug or accidental shutdown prevented the completion of explicit data save.

One alleged reason why orthogonal persistence was not accepted is because it is said to be too expensive to implement. It is not, as some systems like Eumel or Lisp systems showed. A tradition developed to have non-persistent systems, and require users/programmers to explicitly save and restore the state of the objects they use from low-level persistent media.

Such an unbearable state of fact is a proof of either the complete stupidity of corporate system software designers, or their utter despise of the computer users, or more likely, both of them. As usual, the only justification they give for that is a blind following of an obsolete tradition, that they impose by force, because with it they racket the whole world, whereas good software would free the world from them.

Actually, as the discrepancy of speed between of memory components and computing units grows everyday larger, it becomes everyday more obvious that DRAM is really another cache between the CPU and persistent storage, just like (zero to two levels of) SRAM and CPU registers before it. There is no reason why normal users should still have to explicitly fill and empty this cache, when all these things could much more reliably be done automatically by the computer itself. The fact that flushing be done by system software or system hardware is utterly irrelevant to the user, who considers these two as a whole when using them.

Of course, by reserving one computer per user, letting it continuously turned on, with the same session running, persistence can theoretically be achieved, but at the first bug or power-failure, everything will be lost, whereas the traditional policy is to allow plenty of bugs to exist, and to propose rebooting as a usual technique to get around them. The problem with Orthogonal Persistence is thus one of reliability and performance.

To have fast and reliable Orthogonal Persistence would be easy if only computers or disks were equipped with battery backed up memory, or "TRAM" (TRAM -- transactional RAM) as they have been dubbed. Power failures would thus be gracefully handled without sacrificing speed by requiring changes to be committed to slow disk before continuing. Unhappily hardware is not available, and we're forced to compromise otherwise. The compromise is that either you use a much more expensive uninterrupted power supply (UPS) for your whole system (rather than just the TRAM), and/or you allow for some latency before buffers are committed to disk. The user may then control the latency of committing, in a document-dependent way, depending on the available system capabilities. He may also insert explicit synchronization points, to wait for data to be committed to persistent storage (just like fsync() under Unix). Also, if your hardware is not equipped with TRAM, there is still a need to track down commitment of data to disk before to publish that the transaction was actually committed. But this is no particular disadvantage of orthogonal persistence as compared to other forms of explicit persistence, since all modern operating systems have just as much problem guaranteeing commitment of data in explicitly persistent databases, and require that a special procedure be called to ensure that buffers be flushed to disk during commits or shutdown.

One misunderstanding about Orthogonal Persistence is that by getting rid of filesystems, one would also throw away tree-like hierarchies of directories. Such tree-like hierarchies are indeed a simple and natural way to organize thoughts, although by far not the only one. Even with orthogonal persistence, there would still be a lot of nested "dictionaries", that bind objects to human-readable and typeable names. However, said objects won't be files anymore; instead of raw streams of contiguous bytes, they will be just any structured data that your computing system can manipulate. Also, not everything will have to be force-mapped into tree-like hierarchies or else built with altogether completely different tools from usual (SQL, etc.).

Another misunderstanding is that orthogonal persistence would (try to) remove the "save" button of document editors. That is not completely correct. With orthogonal persistence, there would be normally no need to save data (though in absence of TRAM, there might be a use for a command to force early commitment), but there is still a need to manage data. Indeed, even with orthogonal persistence, users will want some kind of explicit save/commit primitive to distinguish between well-established releases of his documents, just like they do with versioning software like CVS. Even the simplest document editor will likely have a way to distinguish between "stable", "development" and "backup" releases of the current document. Orthogonal persistence will change nothing about the advantages and intrinsic complexities of project management; what it will do is provide enhanced reliability through simpler and better factorized implementation, with system-side marshalling and error management.

An excellent read is Jochen Liedtke's A Persistent System in Real Use - Experiences of the First 13 Years (1993)

See Claus Reinke's bibliography about persistence.

Systems like Cedar, Eumel, Grasshopper, Mungi, and Texas have successfully implemented orthogonal persistence.

For a variation on orthogonal persistence combined with atomicity through logging marshalled atomic requests, see Prevalence.

------------------------------------------------------------------------

I am a bit confused by L4, does it support Orthogonal Persistence by itself? I have the feeling it use to be, but now it is outside of it's scope. I have tried the fiasco-L4 demo floppy, and found it nice. But as I understand, fiasco is very different than pistachio L4 mikrokernel. And since Mungi is based on L4, I guess it adds stuff to write image to an IDE disk once in a while to L4. Of these systems, only Mungi seems to have open-sources. For L4-Intel64, I guess it would be possible to adapt for Intel32, but since the sources are from 1998, I would guess they use the old interface of L4. --Paul

L4 being a microkernel doesn't include any persistence layer, though you could probably build one atop. Mungi apparently does, but I don't know how it handles atomic commitment, or whether it even tries. -- Faré

------------------------------------------------------------------------

Perhaps an operating system's commitment latency could be auto-configurable? It seems there are exactly three options:

1.  This computer employs TRAM. (Very low latency)
2.  This computer employs a UPS. (Moderate latency, say 10% of UPS battery life, and code to handle battery-low warnings.)
3.  This computer employs no battery back-up. (Very high latency, code needed to recover from data loss.)

--datagrok

Yes, this is ideally auto-configured. And data-loss is still better avoided using journalling, despite the latency. That said, no system is perfect, and if you know how to build recovery tools, it's all the better. -- Faré

------------------------------------------------------------------------

Page in this topic: Texas  

------------------------------------------------------------------------

Also linked from: Argon   C Compiler dlopen VM   Charm   EROS   EUMEL   File System   Grasshopper   Marshalling   Max   Methods of Migration   Microkernel Debate   Napier88   Persistence   Persistence 101   Plurix   Prevalence   Torsion   Version-Aware  
