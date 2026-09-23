from rapidfuzz import fuzz

FUZZY_MATCH_THRESHOLD = 80


def judge(question, expects, answer, results) -> bool:
    """
    A correct answer doesn't have to quote `expects` verbatim — the model can
    paraphrase, reorder words, or change punctuation and still be right. An
    exact substring check (`expects in answer`) fails all of those. Instead,
    score how well `expects` matches *some* part of `answer` and accept it
    above a threshold.

    `fuzz.partial_ratio` finds the best-aligned substring of `answer` for
    `expects`, so a short expected phrase isn't penalized for `answer` being a
    full paragraph around it.
    """
    expects = expects.strip().lower()
    answer = answer.strip().lower()

    if not expects:
        return False

    return fuzz.partial_ratio(expects, answer) >= FUZZY_MATCH_THRESHOLD


def retrieval_hits(expected, results) -> bool:
    return any(expected.strip().lower() in chunk.lower() for chunk in results)
