import argparse
from pathlib import Path

# 1. set up the tool to expect one word from the terminal
parser = argparse.ArgumentParser(description="Search compliance documents")
parser.add_argument("word", help="the word to search for")
args = parser.parse_args()

# 2. args.word now holds whatever the user typed
question_word = args.word

# 3. the DocSense logic you already wrote
docs = {}
for file in Path("sample_docs").glob("*.md"):
    docs[file.name] = file.read_text(encoding="utf-8")

print(f"Searching for '{question_word}'...\n")
for name, text in docs.items():
    if question_word.lower() in text.lower():
        print(f"Found in: {name}")
    else:
        print(f"Not in: {name}")
