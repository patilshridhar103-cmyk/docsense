"""
DocSense — ask plain-English questions about compliance documents.

Pipeline (RAG):
  1. Retrieve — find the most relevant document for the question.
  2. Augment  — build a prompt containing that document + strict guardrails.
  3. Generate — an LLM (Claude) answers using ONLY that document.
  4. Cite     — the answer reports which document it came from.

Run:
    python docsense.py "how long do we keep backups?"

For AI-generated answers, set your Anthropic API key first:
    pip install anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."

Without a key, DocSense still runs and shows the most relevant document
(retrieval only), so the tool works for anyone who clones the repo.
"""

import argparse
import os
from pathlib import Path

DOCS_FOLDER = "sample_docs"

# Common filler words that shouldn't count toward relevance.
STOPWORDS = {
    "how", "long", "do", "we", "the", "a", "an", "is", "are", "of",
    "to", "in", "for", "on", "must", "when", "what", "where", "our", "have",
}


def load_docs(folder):
    """Read every .md file in `folder` into a dict: {filename: text}."""
    docs = {}
    for file in Path(folder).glob("*.md"):
        docs[file.name] = file.read_text(encoding="utf-8")
    return docs


def retrieve(question, docs):
    """Return the name of the document most relevant to `question`.

    Scores each document by how many meaningful words it shares with the
    question (ignoring stopwords). Returns None if nothing matches.

    NOTE: this is simple keyword retrieval. It is brittle (e.g. "backup" vs
    "backups"). The natural upgrade is semantic search with embeddings.
    """
    q_words = set(question.lower().split()) - STOPWORDS
    best_name, best_score = None, 0
    for name, text in docs.items():
        score = len(q_words & set(text.lower().split()))
        if score > best_score:
            best_score, best_name = score, name
    return best_name


def build_prompt(question, name, text):
    """Augment: wrap the retrieved document + guardrails around the question."""
    return f"""Answer the question using ONLY the document below.
If the document does not contain the answer, say "Not found in the documents."

DOCUMENT ({name}):
{text}

QUESTION: {question}"""


def ask_claude(prompt):
    """Generate: send the prompt to Claude and return its answer text.

    Returns None if the Anthropic library or API key isn't available, so the
    caller can fall back to retrieval-only mode.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        from anthropic import Anthropic
    except ImportError:
        return None

    client = Anthropic()
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def answer(question, docs):
    """Run the full pipeline: retrieve -> augment -> generate -> cite."""
    name = retrieve(question, docs)
    if name is None:
        return "Not found in the documents."

    prompt = build_prompt(question, name, docs[name])
    reply = ask_claude(prompt)

    if reply is None:
        # No API key: fall back to showing the most relevant document.
        return (
            f"(No API key set — showing the most relevant document instead of an "
            f"AI answer.)\n\nMost relevant: {name}\n\n{docs[name]}"
        )

    return f"{reply}\n\n(source: {name})"


def main():
    parser = argparse.ArgumentParser(description="Ask questions about compliance documents")
    parser.add_argument("question", help="your question, in plain English")
    args = parser.parse_args()

    docs = load_docs(DOCS_FOLDER)
    print(answer(args.question, docs))


if __name__ == "__main__":
    main()
