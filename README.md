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

---

# Unit 2

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks have the right size | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Every answer names the correct source | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Criterion 1 — retrieved chunk contains the answer** (produced by `store.py::search`, chunks from `chunker.py::split_documents`)

Question: How is financial aid handled for study abroad programs?

- Sources retrieved: admin_add_drop_deadline.txt, admin_campus_jobs_and_financial_aid.txt, admin_graduation_requirements.txt, admin_study_abroad.txt, admin_transcript_requests.txt

```
Your financial aid package travels with you when you study abroad. 

Source: admin_study_abroad.txt
```
> The chunk from admin_study_abroad.txt containing "the financial aid package travels with you when you study abroad" was in the top 5.

**Criterion 2 — every answer names a source** (produced by `generate.py::answer_from_chunks`)

Question: What do students say is the difference between a work-study job and a non-work-study job?

```
The difference is that work-study earnings do not count against your financial aid the way ordinary income does, whereas non-work-study campus jobs do count against your financial aid. 

Source: `admin_campus_jobs_and_financial_aid.txt`
```

Question: What is one graduation requirement that catches students off-guard? 

```
The writing-intensive requirement (taking two courses in different departments) is the one that catches people off-guard (admin_graduation_requirements.txt).
```

> Whether explicitly labeled as "source" or inline, every answer names a source.

**Criterion 3 — gate stops out-of-corpus questions** (produced by `run_eval.py::check_out_of_scope` calling `gate.py::check`, cutoff 0.65)

```
Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.825)  What is the capital of Mongolia?
  refused  (best distance 0.934)  How do I change the oil in a diesel engine?
  refused  (best distance 0.886)  Who won the 1994 World Cup?
  refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.896)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

**Criterion 4 — chunks have the right size** (produced by `chunker.py::split_documents`)

Question: What kind of discounts are available for textbooks?
Source: money_textbooks.txt

```
Textbooks without paying full price

The library holds one copy of most required texts on two-hour reserve. For courses where the text is used constantly that isn't enough, but for the reading-light courses it's genuinely all you need.

The campus store price-matches, which is not advertised anywhere and you have to ask at the counter with the other listing on your phone.
```

> Chunks containing the answer begin and end on a sentence boundary and aren't cut off mid-word or mid-sentence.

**Criterion 5 — every answer names the correct source** (produced by `generate.py::answer_from_chunks`)

Question: What do students say about laundry wait times? 

- Sources retrieved: dining_halden_hall_followup.txt, dining_kestrel_commons_followup.txt, dining_north_kitchen_followup.txt, housing_old_brewhouse_laundry.txt, housing_tamsin_court_laundry.txt

```
Students state that the dryers back up on Sunday evenings and that you will wait on Sunday after 6pm. 

Sources: `housing_tamsin_court_laundry.txt` and `housing_old_brewhouse_laundry.txt`
```

> Even when two sources are correct, they are both named. 

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Target was 4 of 5; all three runs came back 5/5, retrieval is deterministic, so the same questions return the same chunks every run. |
| 2 | Every answer names a source | MET | Target was 5 of 5; the strictest bar possible and every run landed exactly on it, so this is the closest call of the five. |
| 3 | Gate stops out-of-corpus questions | MET | Target was 4 of 5; the gate refused all 5 out-of-scope questions in every run, and even the nearest miss (Mongolia at distance 0.825) sat 0.175 past the 0.65 cutoff, so there was real distance, not just a lucky count. |
| 4 | Chunks have the right size | MET | Target (revised) was 4 of 5; all three runs scored 5/5, and since paragraph splitting is deterministic for the same documents, I didn't expect this to vary run to run the way retrieval or generation might. |
| 5 | Every answer names the correct source | MET | Target was 4 of 5; all three runs hit 5/5, including the laundry pair where the answer correctly named both housing_tamsin_court_laundry.txt and housing_old_brewhouse_laundry.txt instead of just one. |

## Diagnoses

Nothing missed. All five criteria passed in all three runs. That said, three of them (1, 4, and 5) depend on chunking and retrieval, and since I'm asking the same five questions every time, those stages give the same answer every run. There's nothing that could actually make them fail on a second or third try. So getting 5/5 three times over doesn't really prove much beyond what one run already showed. Criteria 2 and 3 are the ones where something could genuinely go wrong each run, and both still passed comfortably. If I were tightening anything, I'd raise criterion 1's target from "4 of 5" to "5 of 5," since there's no good reason to allow for a miss that can't happen. What would actually tell me more is testing on a bigger, more varied set of questions instead of just rerunning the same five.

## The Improvement

**What I changed:**

Added keyword search (BM25) alongside the existing semantic search in `store.py::search`, and combined the two rankings so a chunk can surface either by meaning or by exact word match.

**Why I picked it:**

My diagnosis pointed out that the same five questions never stress-tested retrieval, and a broader set would likely include exact terms — course codes, dollar amounts — that semantic search alone tends to miss.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks have the right size | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Every answer names the correct source | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

Yes: on the laundry question, retrieval used to pull in three unrelated dining chunks alongside the two real laundry sources, but after adding keyword search it retrieves five genuine laundry posts (from five different dorms) and the answer correctly names all of them instead of just two.

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
