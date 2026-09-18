"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+")


def _sentences(text: str) -> list[str]:
    """Split on sentence-ending punctuation. Good enough for prose like this."""
    return [s.strip() for s in _SENTENCE_BREAK.split(text.strip()) if s.strip()]


def _overlap_tail(text: str, overlap: int) -> str:
    """
    The last whole sentences of `text`, up to `overlap` characters.

    Whole sentences, so the overlap is approximate — at most `overlap`
    characters, rarely exactly that. Cutting mid-sentence to hit the number
    exactly would defeat the point of having overlap at all.
    """
    tail: list[str] = []
    total = 0
    for sentence in reversed(_sentences(text)):
        if total + len(sentence) > overlap:
            break
        tail.insert(0, sentence)
        total += len(sentence)
    return " ".join(tail)


def _pack(units: list[str], budget: int, joiner: str, overlap: int) -> list[str]:
    """
    Greedily fill windows of at most `budget` characters from `units`.

    `overlap` of 0 means no carry-over between windows. Pass 0 wherever the
    boundary is already a change of subject: a paragraph break is one, and
    carrying a sentence across it drops the previous paragraph's subject into
    this paragraph's chunk, which is worse than no overlap at all.
    """
    windows: list[str] = []
    current = ""

    for unit in units:
        if not current:
            current = unit
        elif len(current) + len(joiner) + len(unit) <= budget:
            current += joiner + unit
        else:
            windows.append(current)
            tail = _overlap_tail(current, overlap) if overlap else ""
            current = f"{tail} {unit}".strip() if tail else unit
            if len(current) > budget:
                current = unit          # the overlap didn't fit; drop it

    if current:
        windows.append(current)
    return windows


def _hard_cut(text: str, budget: int) -> list[str]:
    """
    Last resort, for a single sentence longer than the whole budget.

    Nothing in city_guides triggers this, but it is what makes the chunk size
    a guarantee rather than a hope.
    """
    if len(text) <= budget:
        return [text]
    pieces = (text[i : i + budget].strip() for i in range(0, len(text), budget))
    return [p for p in pieces if p]


def _split_section(section: str, chunk_size: int, overlap: int) -> list[str]:
    """
    One `##` section as one chunk where it fits, or several where it doesn't.

    Every piece keeps the section heading, so a chunk taken from the middle of
    a long section still says what it is about. The heading counts against
    `chunk_size` — the cap is the cap.
    """
    section = section.strip()
    if not section:
        return []
    if len(section) <= chunk_size:
        return [section]

    heading, _, body = section.partition("\n")
    prefix = f"{heading.strip()}\n\n"
    budget = chunk_size - len(prefix)

    windows: list[str] = []
    pending: list[str] = []     # paragraphs still small enough to share a chunk

    for paragraph in (p.strip() for p in body.split("\n\n")):
        if not paragraph:
            continue
        if len(paragraph) <= budget:
            pending.append(paragraph)
            continue

        # This paragraph alone is over budget, so it has to be cut internally.
        # Flush what came before it first, to keep the chunks in reading order.
        windows.extend(_pack(pending, budget, "\n\n", 0))
        pending = []
        for window in _pack(_sentences(paragraph), budget, " ", overlap):
            windows.extend(_hard_cut(window, budget))

    windows.extend(_pack(pending, budget, "\n\n", 0))

    if not windows:
        return [section]
    return [prefix + window for window in windows]


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents on their `##` section headings.

    The city_guides documents are sectioned guides, not running prose: every
    `##` heading starts a new subject, and the answer to a question about one
    subject is almost always inside one section. So sections are the unit, and
    a section that already fits inside CHUNK_SIZE is left alone — 79 of the 98
    sections in this corpus are.

    The rest divide, in this order:
      1. on paragraph breaks, with no overlap (the break is the topic change);
      2. on sentence boundaries inside an over-long paragraph, carrying up to
         CHUNK_OVERLAP characters of whole sentences forward;
      3. on a character count, only if one sentence is longer than the budget.

    Dividing long sections is a gain, not a loss. `guide_accessibility.md`'s
    "Straightforward" section is 708 characters of three unrelated towns; split,
    each town gets its own chunk and still carries the "Straightforward"
    heading, which is the actual answer to whether that town is easy to get
    around. Left whole, a question about Brightwater would pull back a chunk
    two thirds about somewhere else.
    """

    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []

    for doc in documents:
        # Splitting on the heading consumes the "##", so put it back. The first
        # piece is the document's own "# Title" block and already has its own.
        pieces = doc.text.split("\n\n##")
        sections = pieces[:1] + [f"##{piece}" for piece in pieces[1:]]

        index = 0
        for section in sections:
            for text in _split_section(section, chunk_size, overlap):
                chunks.append(
                    Chunk(
                        text=text,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
