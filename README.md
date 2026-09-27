# The Unofficial Guide

<!-- City Guides Corpus -->

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

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->
     
     For my project, I selected the City Guides corpus. The system answers questions about specific cities and locations,
     especially questions that tourists or visitors might have about the city. These questions might include
     when the city is a busy place to book a stay in, what sights there are to see in the city, or when trains in the city run. 

## Chunking Strategy

**Chunk size: 350**
**Overlap: 105**

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

I selected 350 characters to be the chunk size. I selected 350 because most of the questions I have to test the RAG require the subtitle within the city guide, and then usually about 2-4 sentences. In the sections that answer my five test questions, all five sections are between 260 and 332 characters in length, so 350 would keep all 5 answers, and hopefully
the answers to other potential questions as well, intact. At 300, two of the five answers would be cut. As far as the actual chunking strategy, started with one method, then Claude helped me improve the method twice. The first method, which I typed by hand, split the text of each document by "\n\n##" characters, which inside of each city guide seperates the guide's subsections. I chose those as the split becuase answers to questions tend to be condensed into subsections. I then realized that I didn't actually utilize the set chunk size and chunk overlap variables I set in config.py and had trouble implementing it myself, so Claude implemented a new chunking strategy for me. After testing Claude's method, I then realized that the system was still only giving slightly relevant answers, which Claude suggested was becuase each chunk didn't always explicitly reference the exact city in sentences where answers would be found. Claude then implemented a strategy that attached the title of each document to each chunk(which was the name of the city the chunk's information referred to.)

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: guide_accessibility.md#0 `` — produced by: `` chunker.py::split_documents

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: guide_corry_vale.md#4 `` — produced by: `` chunker.py::split_documents

```
Corry Vale
## Eat and drink

One pub in the largest village serves food seven days a week. A second, in the third village, opens Thursday to Sunday. There is afarm shop at the valley mouth that sells bread, cheese and little else, and it closes at 4pm. Bring supplies; this is not a place with options.
```

**Chunk 3** — source: guide_givens_mill.md#2 `` — produced by: `` chunker.py::split_documents

```
Elder Ness
## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

**Chunk 4** — source: guide_marchwood.md#2 `` — produced by: `` chunker.py::split_documents

```
Kestrelford
## Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

**Chunk 5** — source: guide_seasons.md#0`` — produced by: `` chunker.py::split_documents

```
Getting around the region
## Driving

Parking is the constraint rather than driving. Both Halden Bay lots fill by
10am on summer weekends. Kestrelford's lower car park is free and involves a
steep walk up.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
How long is the seafront in Pellow Sands? Answer using only the information in the documents below. If they don't cover it, say you don't have enough information.


**Answer:**

```
The seafront in Pellew Sands is two miles long (guide_accessibility.md and guide_pellew_sands.md).

Sources retrieved: guide_accessibility.md, guide_pellew_sands.md
```

**My relevance cutoff:**

The group of distances for the correct answers ranged from 0.191 to 0.598, while the group for out of scope answers ranged from 0.754 to 0.899. I selected my relevance cutoff to be 0.676. I selected this number because it was right in the middle of the farthest correctly answered question(0.598) and the closest incorrectly answered question(0.754). Taking the average of these numbers returns a relevance cutoff that would be equally weigh and hopefully avoid refusing to answer a question the system successfully found the answer to, and confidently giving an incorrect answer.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|When is accomodation in Brightwater expensive?|yes|0.353|
|When should I visit Cory Vale|yes|0.598|
|What time do the boats come in in Halden Bay|yes|0.232|
|In Marchwood, what time do trains to Brightwater stop?|yes|0.191|
|Since what year has the covered market been operating in Marchwood?|yes|0.404|
|What is the capital of Mongolia?|no|0.754|
|How do I change the oil of a diesel engine?|no|0.882|
|Who won the 1994 World Cup?|no|0.899|
|What is the recommended dosage of ibuprofen for a headache?|no|0.818|
|How do I write a for loop in Rust?|no|0.814|


## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->


**1.**
(UNIT 2)I wrote scorer.py by hand on purpose so that I would understand it, and used Claude to review each version instead of writing it for me. It caught three things I had wrong. My judge function returned (bool, DETAIL) as a tuple, which would have crashed run_eval.py on the first question after already spending an API call. My criterion_2_source checked whether the Result objects had a .source attribute rather than whether the answer text named one, so it could never return False. And my criterion_4_chunk_size compared the chunker's output against config.CHUNK_SIZE, the same value the chunker uses to build the chunks, which made it a check that could never fail — I changed it to compare against a literal 350 so it fails if the config drifts away from what criteria.md promises. I also turned down Claude's suggestion to add an atexit handler that dumps per-criterion results, because the assignment only asks for a function that returns a bool and it was more machinery than I needed.

**2.**
I hand-coded the first chunking function myself, splitting each document wherever the pattern "\n\n##" appeared, because that's where the subsection breaks are in these guides. I then realized I had set CHUNK_SIZE and CHUNK_OVERLAP in config.py and never actually used either one, and I couldn't work out how to add them without losing the section-based split, so I asked Claude to do it. Before writing anything it measured my corpus and reported that the median section was 282 characters and the longest was 708, which confirmed 350 was a reasonable cap rather than a guess.

What came back had a problem I only saw because we looked at the real output: the first version carried overlap across paragraph breaks, so a sentence about Thornby Wells ended up glued onto the front of Marchwood's chunk in guide_accessibility.md. I had it suppress overlap at paragraph breaks and only apply overlap inside a paragraph that was too long on its own.

Later I asked why the answers were still only loosely relevant. Claude found that chunks carried the section heading but not the city name — "## What to see" is a heading ten of my guides share, so the chunk holding "the harbour at 6am when the boats come in" never said "Halden Bay" anywhere in it. Attaching the document title to every chunk moved the answer chunk for my five questions from ranks #16, not-in-top-20, #11, #5 and #1 to rank 1 for all five. I told Claude to hold that change at first because I thought it belonged to a later unit, then decided it was in scope and had it applied.



**3.**
I didn't intend for Claude to do this one. I asked why the built-in retrieve command didn't show the full chunk text, and rather than just answering, Claude wrote inspect_retrieval.py — which prints the full chunk, its distance, and whether it contains the expected answer. I kept it and used it for my criterion 1 evidence, but I hadn't asked for a new file, and it is one more thing in the repo that I have to be able to explain.


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
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. None of the chunks are more than 350 characters |max <= 350| 5/5 | 5/5 | 5/5 | MET |
| 5. The source named in the answer contains the answer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

Criterion 1(Retrieved chunk contains the answer):

### When is accomodation in Brightwater expensive? — run 1

```
Accommodation is thin and expensive during graduation week and in early September. Outside those windows there is more supply than demand. The two hotels on the riverside are the obvious choice and the guesthouses on Corry Lane are better value.
```

File(s) and Function(s): inspect_retrieval.py, store.py::search, chunker.py::split_documents

Criterion 2(Answer names a source):

```
Accommodation in Brightwater is expensive during graduation week and in early September (guide_brightwater.md).
```

File(s) and Function(s): run_eval.py::main

Criterion 3(Gate stops out-of-corpus):

Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.754)  What is the capital of Mongolia?
  refused  (best distance 0.882)  How do I change the oil in a diesel engine?
  refused  (best distance 0.899)  Who won the 1994 World Cup?
  refused  (best distance 0.818)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.814)  How do I write a for loop in Rust?
  -> gate refused 5 of 5

File(s) and Function(s): run_eval.py::check_out_of_scope

Criterion 4(No chunk over 350):
124 chunks, 256 characters on average (shortest 23, longest 350), produced by chunker.py::split_documents

From: python chunker.py
File(s) and Function(s): chunker.py::split_documents, summary line by chunker.py::describe

Criterion 5(Source named is correct):
### When is accomodation in Brightwater expensive? — run 1

- Best distance: 0.3529 (passed the gate)
- Sources retrieved: guide_brightwater.md, guide_regional_transport.md

```
Accommodation in Brightwater is expensive during graduation week and in early September (guide_brightwater.md).
```

chunk from guide_brightwater.md#7 that contains it:

Accommodation is thin and expensive during graduation week and in early September. Outside those windows there is more supply than demand. The two hotels on the riverside are the obvious choice and the guesthouses on Corry Lane are better value.

File(s) and Function(s): run_2026-09-26_1329_before.md, scorer.py::judge


## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | `scorer.py::criterion_1_retrieval` checks whether the `expects` phrase appears in the text of any retrieved chunk. All 5 questions passed on all 3 runs, against a target of 4. Retrieval is deterministic, so the same 5/5 goes in all three run columns. |
| 2 | Every answer names a source | MET | `scorer.py::criterion_2_source` checks whether any retrieved source filename appears in the answer text. It passed on all 15 runs, so every answer named at least one document. |
| 3 | Gate stops out-of-corpus questions | MET | `run_eval.py::check_out_of_scope` put all 5 OUT_OF_SCOPE questions through the gate in one deterministic pass. All 5 were refused, with best distances from 0.754 to 0.899 — all well above my 0.676 cutoff. |
| 4 | None of the chunks are more than 350 characters | MET | `python chunker.py` reports 124 chunks with the longest at 350, which covers every chunk rather than only the 5 retrieved per question. I tested with `<=` because the criterion says no more than 350, and my longest chunk is exactly 350. |
| 5 | The source named in the answer contains the answer | MET | `scorer.py::criterion_5_source_check` finds which retrieved documents actually contain the `expects` phrase, then checks that the answer named one of them. It passed on all 15 runs. For the 1863 question two documents contain the answer, and I counted naming either one as correct. |

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

All five of the criterion were met for my system. All 15 runs passed, and the gate refused 5 of 5. 

I wouldn't consider the first criterion, that the retrieved chunks contain the answer, to be safe because before I made large changes to the system in Unit one, it failed the criterion badly. I originally had the document splitting function make chunks by dividing on the pattern "\n\n##", which chunked without labeling the chunks by their document title. The chunk that contained the answer was ranked at #16 before the change to the chunking mechanism was made. This made a lot the chunks received only slightly relevant or completely irrelevant to the question asked.

The second criterion(Answer names a source) can be considered safe because generate.py's GROUNDING_INSTRUCTION explicitly has the model name the document the answer came from.

The third criterion(Gate stops out of corpus) wasn't safe since the closest out of scope question was 0.754, which is close to the set relevance cutoff of 0.676.

The fourth criterion(No chunk over the size 350 chars) can now be considered safe since the chunker enforces it when chunking the documents.

The fifth criterion(Source named is correct) wasn't too safe because there wasn't anything coded into the project that forced the model to cite the file that actually held the answer it retrieved.

If I was to tighten a criterion,  I'd tighten criterion 3 from "the gate refuses at least 4 of 5" to "the gate refuses all 5, and every out-of-scope question's best distance is at least 0.1 above the cutoff." My closest out-of-scope question is 0.754 against a 0.676 cutoff — only 0.078 of headroom — so the tightened version would fail, which is the point: the original target passed without testing how close the system actually came.

## The Improvement

**What I changed:** I'm changing the TOP_K value from 5 to 3 




**Why I picked it:**
I picked it because all five answers are at rank 1, so 4 of every 5 chunks in the prompt are noise. 
<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. None of the chunks are more than 350 characters | max <= 350 | 350 | 350 | 350 | MET |
| 5. The source named in the answer contains the answer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

No, it didn't help since the verdict s stayed the same. However, we retrieved less chunks and still got the correct answer, so the additional 2 chunks were likely noise. 

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

Corry Vale is still 0.078 from being refused. It passes, but barely. It could be because I mispelled Corry Vale in the questions.py file, so I'll fix the spelling. 

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
I'd write criterion 4 differently. "None of the chunks are more than 350 characters" is a property the chunker enforces by construction, so maybe it'd be better to replace it with a criterion about the quality of the chunks. An example of a better criterion might be to make sure that at least 4 of the 5 chunks read as a complete thought without cutting off sentences on either end. 