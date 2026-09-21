# The Unofficial Guide

Mayra Vazquez-Sanchez
Corpora picked: campus_life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a retrieval-augmented Q&A system over `campus_life`, a corpus of about 90 short posts covering housing, dining, courses, admin deadlines, money, and transit at one college. It answers specific questions a student might actually have — "what's the add/drop deadline," "how many hours a week does BIOL 160 take," "does financial aid travel with you on study abroad" — by retrieving the post that covers the topic and citing it by name in the answer. If a question isn't something campus_life covers, a relevance gate refuses it instead of guessing.

## Chunking Strategy

**Chunk size:** Split by paragraph
**Overlap:** None, paragraphs stay whole

I split on blank-line paragraph breaks instead of a character count because most of my posts are one short paragraph and stay a single chunk either way, but a few (like course_biol_160.txt's Format/Workload/Advice) pack distinct sub-topics into separate paragraphs that a fixed-size window would have lumped into one chunk or cut arbitrarily. I dropped overlap because paragraphs here already read as complete, self-contained thoughts, so there's nothing mid-sentence to protect against.

## Sample Chunks

**Chunk 1** — source: `source: admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `source: course_cs_340_exams.txt#1` — produced by: `chunker.py::split_documents`

```
Start the term project in week three, not week eight; everyone learns this the hard way.
```

**Chunk 3** — source: `source: course_stat_150.txt#0` — produced by: `chunker.py::split_documents`

```
STAT 150 Applied Statistics

Transferred in last year, so take this with a grain of salt. Format is flipped: watch the recordings, class time is problem sets. Assessment: three equally weighted midterms, no final. No curve, but the lowest midterm is dropped.
```

**Chunk 4** — source: ` source: health_center.txt#1` — produced by: `chunker.py::split_documents`

```
Counselling is separate, in the same building, and has its own intake process with a shorter wait than people expect — usually three or four days for a first session.
```

**Chunk 5** — source: `source: housing_morrow_house.txt#3` — produced by: `chunker.py::split_documents`

```
Laundry costs $1.50 wash, $1.25 dry, coin or card. On noise: loud until about 1am on weekends, no enforced quiet hours.
```

## Sample Answer

**Question:**

How is financial aid handled for study abroad programs?

**Answer:**

```
The financial aid package travels with you when you study abroad. 

Source: admin_study_abroad.txt

Sources retrieved: admin_add_drop_deadline.txt, admin_campus_jobs_and_financial_aid.txt, admin_graduation_requirements.txt, admin_study_abroad.txt, admin_transcript_requests.txt
```

**My relevance cutoff:** 0.65
 
 My worst in-corpus distance (0.513, laundry) and best out-of-scope distance (0.825, Mongolia) leave a 0.31 gap with nothing in it, so I set the cutoff in the middle rather than hugging either group.

| Question | In corpus? | Best distance |
|---|---|---|
| What kind of discounts are available for textbooks? | yes | 0.299 |
| How is financial aid handled for study abroad programs? | yes | 0.346 |
| What do students say about laundry wait times? | yes | 0.513 |
| What do students say is the difference between a work-study job and a non-work-study job? | yes | 0.442 |
| What is one graduation requirement that catches students off-guard? | yes | 0.484 |
| What is the capital of Mongolia? | no | 0.825 |
| How do I change the oil in a diesel engine? | no | 0.934 |
| Who won the 1994 World Cup? | no | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| How do I write a for loop in Rust? | no | 0.896 |

## How I Used AI

**1.** I'd selected the character-window loop in `fallback_split` and asked Claude to change it to split by paragraph instead. It pointed out that was the wrong function — the file's own comments say to keep `fallback_split` as the baseline to compare against — and that I'd already accidentally pasted that loop into `split_documents`, leaving `chunk_size` and `overlap` undefined. It rewrote `split_documents` to split on blank-line paragraphs there instead, and added a rule I hadn't asked for: folding any paragraph under 60 characters into the one after it, since a bare title line would otherwise become its own chunk with no content.

**2.** I gave Claude my measured best-distance table from Milestone 4 — five in-corpus questions, five `OUT_OF_SCOPE` ones — and asked where to set the cutoff. It recommended 0.65, roughly the midpoint between my worst in-corpus distance (0.513) and my best out-of-scope distance (0.825), and when I asked what I'd get wrong at that number, it said the table only covers ten questions, so the real risk is a future question that overlaps more than these do — not anything visible in this data. I used 0.65 in `config.py` since the gap was wide enough that the exact number inside it mattered less than picking one.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
