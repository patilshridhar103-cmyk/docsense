# DocSense

A command-line tool that answers plain-English questions about compliance documents,
grounding every answer in your actual documents and citing its source.

> *Portfolio / learning project — built while learning Python. Uses fictional sample
> compliance policies, not real proprietary data.*

## The problem
Regulated-industry teams lose hours verifying requirements against long policy and
standards documents. A keyword search ("Ctrl+F") finds *where a word appears* but can't
*answer a question* — and a general chatbot will confidently make up answers, which is
unacceptable in compliance work.

## What DocSense does
Ask a question in plain English; DocSense finds the relevant policy, sends it to an LLM
with strict "answer only from this document" instructions, and returns a grounded answer
**with a citation** to the source document.

## How it works (RAG)
1. **Retrieve** — search the documents for the most relevant one.
2. **Augment** — build a prompt containing that document + guardrails ("answer ONLY from
   this; if it's not here, say so").
3. **Generate** — an LLM (Claude) writes the answer from that source.
4. **Cite** — the answer includes which document it came from.

## Run it
```bash
# 1. install dependencies
pip install anthropic

# 2. set your API key (never commit this)
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. search the documents
python docsense.py "password"
```

## Product decisions
- **Problem:** engineers lose hours verifying requirements against long standards.
- **User:** a compliance / functional-safety engineer.
- **Job-to-be-done:** "When I review a requirement, confirm which clause applies and where
  it's stated, so I don't fail an audit."
- **Why RAG (not a raw chatbot):** answers must be grounded in *these* documents and cite
  the source — hallucination is unacceptable in compliance-critical work.
- **Success metric:** time-to-answer and citation accuracy.
- **Scope of v1 (cut on purpose):** single-doc retrieve-and-cite loop only. No multi-user,
  no UI, no write-back — proven the core loop first.

## What I learned
- Building a full **RAG pipeline** end to end (retrieve → augment → generate → cite).
- That the hard part of RAG is **retrieval quality**, not the LLM call — naive keyword
  search is brittle (misses "backup" vs "backups").
- Python fundamentals: files, `pathlib`, dictionaries, classes, `pytest`, `argparse`, git,
  and calling an API safely (keys in the environment, never in code).

## Future work
- Semantic retrieval with **embeddings** (match meaning, not exact words).
- Wrap it in a web API (FastAPI) so other apps can use it.

---
*Built as a hands-on learning project.*
