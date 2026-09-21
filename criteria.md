# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

One of my question's answer sits in a chunk's second paragraph so I expect to miss that sometimes.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

Naming a source is instruction-following the generation prompt controls directly, not something that gets harder on a harder question, so there's no reason to expect less than 5 of 5.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**

These questions are about topics that don't overlap with campus_life at all, so I expect the gate to catch nearly all of them, but since I haven't set the actual distance cutoff yet, I'd rather leave room for one surprise than claim a perfect score before I've measured anything.

---

## 4. Chunks have the rigtht size

When a post has more than one paragraph, splitting it must not cut a sentence in half. In at least 9 out of 10 chunks with multi-paragraph posts, they should begin and end on a sentence boundary rather than mid-word or mid-sentence.

**Why this target:**

Some documents pack distinct sub-topics into separate paragraphs, so a paragraph-based split risks a paragraph break that doesn't line up with a sentence break. 9 out of 10 leaves room for one document I haven't read closely enough yet.

---

## 5. Every answer names the correct source

For at least 4 of my 5 test questions where two documents cover similar-sounding topics, the source the answer names is the correct one, not just any document that was retrieved.

**Why this target:**

Citing a source is easy but citing the right one actually tests retrieval. 4 out of 5 accounts for the corpus having several such close pairs.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
