
"""
Scorer for evaluating answers against expected responses. The criterion checking functions check
1 question at a time, and return True if the criterion is met and False if not.
'Correct' is defined as any document containing the answer rather than one specific document.
"""

import config
from store import Result


def _normalize(text: str) -> str:
    """Normalize text for comparison."""
    return text.strip().lower()

def _contains(search_string: str, search_item: str) -> bool:
    """Check if the normalized needle is in the normalized haystack."""
    if not search_string or not search_item:
        return False
    return _normalize(search_item) in _normalize(search_string)

def criterion_1_retrieval(expects: str, results: list[Result]) -> bool:
    #for each result in results, check if expects is in at least one of the result.text
    for result in results:
        if _contains(result.text, expects):
            return True
    return False

def criterion_2_source(answer: str, results: list[Result]) -> bool:
    #for each result in results, check if has a source
    sources = [result.source for result in results]
    for source in sources:
        if _contains(answer, source):
            return True

    return False
    
    

#we don't need to check that the relevance gate stops out of scope questions since judge isn't 
#called if the question is out of scope(run_eval.py checks that before calling judge)

def _max_chunk_length() -> int:
    global _MAX_CHUNK_LEN
    #we want to minimimize the number of times we read over the documents and chunk them, so once we do it once,
    #it gets stored in a global variable and we skip doing it again
    if _MAX_CHUNK_LEN is None:
        from ingest import load_documents
        from chunker import split_documents
        chunks = split_documents(load_documents())
        _MAX_CHUNK_LEN = max(len(chunk.text) for chunk in chunks) if chunks else 0
    return _MAX_CHUNK_LEN

CRITERION_4_MAX = 350   # the number criteria.md commits to — deliberately NOT config.CHUNK_SIZE

#although chunk size is already handled, this returns a boolean result for the scorer.py for the k results
def criterion_4_chunk_size() -> bool:
    return _max_chunk_length() <= CRITERION_4_MAX

def criterion_5_source_check(expects: str, answer: str, results: list[Result]) -> bool:
    #for each result in results, check if the source is in the answer and the 
    # expects is in the result.text
    correct_sources = {r.source for r in results if _contains(r.text, expects)}
    if not correct_sources:
        return False
    for source in correct_sources:
        stem = source.removesuffix(".md")
        if _contains(answer, source) or _contains(answer, stem):
            return True
    return False

DETAIL = []
_MAX_CHUNK_LEN = None

def judge(question: str, expects: str, answer: str, results: list[Result]) -> bool:
    """Return True if the answer is correct and False if not"""

    c1 = criterion_1_retrieval(expects, results)
    c2 = criterion_2_source(answer, results)
    c4 = criterion_4_chunk_size()
    c5 = criterion_5_source_check(expects, answer, results)

    DETAIL.append({
        "question": question,
        "c1": c1,
        "c2": c2,
        "c4": c4,
        "c5": c5,
    })

    return bool(c1 and c2 and c4 and c5)