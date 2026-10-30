"""Ask Harbor & Vale's internal documents a question and print the sections retrieved.

    uv run python scripts/ask_docs.py "How much discount may a retention agent give?"
"""
import sys
import textwrap

from churn_pipeline.rag import default_index


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    index = default_index()
    print(f"{len(index.chunks)} sections indexed\n")
    for hit in index.search(" ".join(argv)):
        print(f"[{hit['score']:.3f}] {hit['source']} > {hit['section']}")
        print(textwrap.indent(textwrap.shorten(hit["text"], 300), "    "), "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
