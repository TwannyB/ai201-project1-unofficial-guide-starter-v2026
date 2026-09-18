#!/usr/bin/env python3
"""
Read the chunks retrieval actually returns, in full.

Milestone 4 asks you to run test questions through retrieval and *read* what
comes back — on topic, or just sharing a few words with the question?
`app.py retrieve` cuts each chunk to 52 characters, which is enough to compare
distances and not enough to judge that. This prints the whole chunk.

Like `app.py retrieve`, this spends no model call. Retrieval and embedding both
run on your machine, so run it as often as you like.

    python inspect_retrieval.py                 # first three questions
    python inspect_retrieval.py --all           # all five
    python inspect_retrieval.py "your question" # one of your own
    python inspect_retrieval.py --top-k 10      # look further down the list
"""

import argparse

import config
import gate
from questions import answered
from store import search


def show(question: str, expects: str | None, top_k: int, corpus: str) -> None:
    results = search(question, top_k=top_k, corpus=corpus, variant="default")

    print("=" * 78)
    print(f"Q: {question}")
    if expects:
        print(f"   a correct answer should contain: {expects!r}")
    print("=" * 78)

    if not results:
        print("Nothing came back. Have you run `python app.py index`?")
        return

    found_at = None
    for rank, r in enumerate(results, 1):
        hit = expects and expects.lower() in r.text.lower()
        if hit and found_at is None:
            found_at = rank

        print(f"\n[{rank}] distance {r.distance:.4f}  |  {r.label}"
              f"{'  <-- contains the answer' if hit else ''}")
        print("-" * 78)
        print(r.text)

    decision = gate.check(results)
    print(f"\nGate: {decision.explanation}")

    if expects:
        if found_at is None:
            print(f"VERDICT: the answer is NOT in the top {len(results)}. "
                  f"The model cannot answer this question.")
        elif found_at == 1:
            print("VERDICT: the answer is the closest chunk.")
        else:
            print(f"VERDICT: the answer is at rank {found_at} of {len(results)} — "
                  f"{found_at - 1} less relevant chunk(s) rank above it.")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", help="one question of your own")
    parser.add_argument("--all", action="store_true",
                        help="all five questions, not just the first three")
    parser.add_argument("--top-k", type=int, help=f"default {config.TOP_K}")
    parser.add_argument("--corpus", help=f"default {config.CORPUS}")
    args = parser.parse_args()

    top_k = args.top_k or config.TOP_K
    corpus = args.corpus or config.CORPUS

    if args.question:
        show(args.question, None, top_k, corpus)
        return

    questions = answered()
    if not args.all:
        questions = questions[:3]

    print(f"corpus: {corpus}   top_k: {top_k}   threshold: {config.THRESHOLD}")
    print(f"chunking: CHUNK_SIZE={config.CHUNK_SIZE} "
          f"CHUNK_OVERLAP={config.CHUNK_OVERLAP}\n")

    for q in questions:
        show(q["question"], q.get("expects"), top_k, corpus)


if __name__ == "__main__":
    main()
