"""Retrieval over the internal documents, tested without the network.

A bag-of-words embedder stands in for OpenAI, so these tests check the
chunking, ranking and cache logic, not the quality of real embeddings.
"""
import re
import zlib
from pathlib import Path

import numpy as np
import pytest

from churn_pipeline.rag import DEFAULT_SOURCES, DocIndex, split_markdown

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = sorted((ROOT / "knowledge" / "harbor_vale").glob("*.md"))
DIM = 512


class WordEmbedder:
    """Hashes each word into one of DIM buckets; counts the texts it embedded."""

    def __init__(self):
        self.embedded = 0

    def __call__(self, texts):
        self.embedded += len(texts)
        out = np.zeros((len(texts), DIM))
        for i, t in enumerate(texts):
            for w in re.findall(r"[a-z]+", t.lower()):
                if len(w) > 3:
                    out[i, zlib.crc32(w.encode()) % DIM] += 1
        return out


def test_corpus_is_the_five_internal_documents_plus_crew_outputs():
    names = [p.name for p in KNOWLEDGE]
    assert names == ["competitor_offers.md", "discount_policy.md", "incident_postmortem.md",
                     "past_campaigns.md", "retention_playbook.md"]
    assert set(KNOWLEDGE) <= set(DEFAULT_SOURCES)
    assert any(p.name == "model_card.md" for p in DEFAULT_SOURCES)


def test_every_internal_document_says_it_is_synthetic():
    for p in KNOWLEDGE:
        assert "Synthetic internal document" in p.read_text(), p.name


def test_split_markdown_gives_one_chunk_per_section():
    chunks = split_markdown(ROOT / "knowledge" / "harbor_vale" / "discount_policy.md")
    assert [c.section for c in chunks] == ["Overview", "Monthly retention budget", "Limits per customer",
                                           "Approval levels", "Offers that need extra care"]
    assert chunks[3].text.startswith("Harbor & Vale Discount and Retention Budget Policy > Approval levels\n")
    assert chunks[0].source == "knowledge/harbor_vale/discount_policy.md"


@pytest.mark.parametrize("query, source, section", [
    ("approval levels team lead discount", "discount_policy.md", "Approval levels"),
    ("support agent closes the complaint first, resolve before you reward", "retention_playbook.md", "Customers who complained"),
    ("competitor phone laptop electronics", "competitor_offers.md", "CartNest"),
])
def test_search_ranks_the_matching_section_first(query, source, section):
    hit = DocIndex.build(KNOWLEDGE, WordEmbedder()).search(query)[0]
    assert hit["source"].endswith(source) and hit["section"] == section
    assert set(hit) == {"source", "section", "cite_as", "score", "text"}
    assert hit["cite_as"] == f"[{source} > {section}]"


def test_cache_embeds_only_new_or_changed_sections(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    for p in KNOWLEDGE:
        (docs / p.name).write_text(p.read_text())
    cache = tmp_path / "index.json"
    first = WordEmbedder()
    total = len(DocIndex.build(sorted(docs.glob("*.md")), first, cache).chunks)
    assert first.embedded == total

    again = WordEmbedder()
    DocIndex.build(sorted(docs.glob("*.md")), again, cache)
    assert again.embedded == 0

    policy = docs / "discount_policy.md"
    policy.write_text(policy.read_text().replace("INR 1,200,000", "INR 1,500,000"))
    changed = WordEmbedder()
    DocIndex.build(sorted(docs.glob("*.md")), changed, cache)
    assert changed.embedded == 1


def test_cache_from_another_embedding_model_is_ignored(tmp_path):
    cache = tmp_path / "index.json"
    DocIndex.build(KNOWLEDGE, WordEmbedder(), cache, model="old-model")
    fresh = WordEmbedder()
    index = DocIndex.build(KNOWLEDGE, fresh, cache)
    assert fresh.embedded == len(index.chunks)


def test_missing_sources_are_skipped(tmp_path):
    index = DocIndex.build([*KNOWLEDGE, tmp_path / "not_written_yet.md"], WordEmbedder())
    assert {c.source.split("/")[-1] for c in index.chunks} == {p.name for p in KNOWLEDGE}
