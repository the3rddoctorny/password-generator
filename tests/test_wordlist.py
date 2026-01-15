import json
import math
from pathlib import Path

WORDS_PATH = Path(__file__).resolve().parents[1] / "assets" / "words_v1.json"
BAD = set("lio")  # ambiguous chars you banned


def load_words():
    assert WORDS_PATH.exists(), f"Missing word list: {WORDS_PATH}"
    words = json.loads(WORDS_PATH.read_text(encoding="utf-8"))
    assert isinstance(words, list), "words_v1.json must be a JSON array"
    return words


def test_wordlist_size_is_at_least_1024():
    words = load_words()
    assert len(words) >= 1024, f"Word list too small: {len(words)}"


def test_wordlist_words_are_clean():
    words = load_words()

    for w in words:
        assert w.isalpha() and w.islower(), f"Bad word (not lowercase a-z): {w}"
        assert set(w).isdisjoint(BAD), f"Ambiguous char in word: {w}"
        assert 4 <= len(w) <= 7, f"Word length out of range (4-7): {w}"


def test_entropy_floor_from_wordlist_size():
    # Your generator choice-space: 2 words + 1 digit (1-9) + 1 of 8 symbols
    words = load_words()
    n = len(words)

    bits = 2 * math.log2(n) + math.log2(9) + math.log2(8)
    assert bits >= 26, f"Entropy floor too low: {bits:.2f} bits (wordlist size {n})"
