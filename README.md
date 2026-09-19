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
I asked Claude to write the chunking function for me twice. The first time, I'd already handcoded a chunking method that split the documents into chunks wherever there was the pattern "\n\n##", which I observed was where subsection separations were. I then realized that I didn't include the set chunk size and chunk overlap, so I had Claude implement a strategy that followed both of those preset config variables. I then had Claude investigate why the answers I was getting from the system still seeemed to only be slightly relevant to the questions that I was asking, and Claude suggested that the chunking process currently removes the exact city the chunk's information was referring to. I then had Claude implement a new strategy that built off of the old strategy by appending the title(city) of the chunk to the beginning of each chunk. This improved answers drastically, and I didn't make any changes to new strategy Claude wrote for me. 

**2.**
I didn't intend for Claude to do this, but I asked Claude a question about the "retrieve" command in the terminal written for the project and why it didn't return the full chunk with it, and Claude created a "inspect_retrieval.py" for me to see the embedding distance from the query, along with the full chunk. I didn't make any changes to what Claude created.


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
