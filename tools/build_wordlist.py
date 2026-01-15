import re
import json

BAD_CHARS = set("lio")     # visually ambiguous
MIN_LEN = 4
MAX_LEN = 7

words = []

with open("diceware.wordlist.asc") as f:
    for line in f:
        parts = line.strip().split()
        if not parts:
            continue

        word = parts[-1].lower()

        if (
            MIN_LEN <= len(word) <= MAX_LEN and
            set(word).isdisjoint(BAD_CHARS) and
            re.fullmatch(r"[a-z]+", word)
        ):
            words.append(word)

# deterministic order
words = sorted(set(words))

# take exactly 1024
final = words[:1024]

print(f"Final word count: {len(final)}")

with open("words_v1.json", "w") as out:
    json.dump(final, out, indent=2)

