"""Retrieval over Harbor & Vale's internal documents (the RAG part of the project).

The corpus is the synthetic internal documents in knowledge/harbor_vale/ plus
the latest insights and model card the crews wrote. Markdown files are split
into one chunk per "## " section, embedded with OpenAI, and searched by cosine
similarity. Embeddings are cached in artifacts/rag/index.json by the text's
sha256, so only new or changed sections are embedded again.

Plain Python like the other tools: the agent decides what to ask and how to
use the answer; this module returns the sections with their source.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
from crewai.tools import tool

ROOT = Path(__file__).resolve().parents[2]
EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_SOURCES = [
    *sorted((ROOT / "knowledge" / "harbor_vale").glob("*.md")),
    ROOT / "artifacts" / "latest" / "crew1" / "insights.md",
    ROOT / "artifacts" / "latest" / "crew2" / "model_card.md",
]
CACHE_PATH = ROOT / "artifacts" / "rag" / "index.json"
TOP_K = 4

Embedder = Callable[[Sequence[str]], np.ndarray]


@dataclass(frozen=True)
class Chunk:
    source: str
    title: str
    section: str
    text: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()


def split_markdown(path: str | Path, root: Path = ROOT) -> list[Chunk]:
    """One chunk per "## " section; text before the first one is the "Overview" chunk.

    Each chunk starts with "<title> > <section>" so a section keeps its context
    when it is retrieved on its own.
    """
    path = Path(path)
    try:
        source = str(path.resolve().relative_to(root))
    except ValueError:
        source = path.name
    title, section, body, chunks = path.stem, "Overview", [], []

    def flush() -> None:
        text = "\n".join(body).strip()
        if text:
            chunks.append(Chunk(source, title, section, f"{title} > {section}\n{text}"))

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# ") and not chunks and not body:
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            section, body = line[3:].strip(), []
        else:
            body.append(line)
    flush()
    return chunks


def openai_embedder(model: str = EMBEDDING_MODEL) -> Embedder:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def embed(texts: Sequence[str]) -> np.ndarray:
        response = client.embeddings.create(model=model, input=list(texts))
        return np.array([d.embedding for d in response.data], dtype=float)

    return embed


def _unit(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.where(norms == 0, 1, norms)


class DocIndex:
    def __init__(self, chunks: list[Chunk], vectors: np.ndarray, embedder: Embedder):
        self.chunks = chunks
        self.vectors = _unit(vectors)
        self.embedder = embedder

    @classmethod
    def build(cls, sources: Sequence[str | Path], embedder: Embedder,
              cache_path: str | Path | None = None, model: str = EMBEDDING_MODEL) -> DocIndex:
        """Chunk every existing source and embed only the chunks the cache lacks."""
        chunks = [c for s in sources if Path(s).is_file() for c in split_markdown(s)]
        cached: dict[str, list[float]] = {}
        cache = Path(cache_path) if cache_path else None
        if cache and cache.is_file():
            stored = json.loads(cache.read_text(encoding="utf-8"))
            if stored.get("model") == model:
                cached = stored["vectors"]
        missing = [c for c in chunks if c.sha256 not in cached]
        if missing:
            for c, v in zip(missing, embedder([c.text for c in missing])):
                cached[c.sha256] = [float(x) for x in v]
        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            keep = {c.sha256: cached[c.sha256] for c in chunks}
            # Write then rename, so a reader never sees a half-written file.
            tmp = cache.with_suffix(f".{os.getpid()}.tmp")
            tmp.write_text(json.dumps({"model": model, "vectors": keep}), encoding="utf-8")
            tmp.replace(cache)
        vectors = np.array([cached[c.sha256] for c in chunks], dtype=float)
        return cls(chunks, vectors, embedder)

    def citations(self) -> set[str]:
        """Every "file name > section" an agent may cite."""
        return {f"{Path(c.source).name} > {c.section}" for c in self.chunks}

    def search(self, query: str, k: int = TOP_K) -> list[dict]:
        q = _unit(np.asarray(self.embedder([query]), dtype=float))[0]
        scores = self.vectors @ q
        best = np.argsort(scores)[::-1][:k]
        return [{"source": self.chunks[i].source, "section": self.chunks[i].section,
                 "cite_as": f"[{Path(self.chunks[i].source).name} > {self.chunks[i].section}]",
                 "score": round(float(scores[i]), 4), "text": self.chunks[i].text}
                for i in best]


_index: DocIndex | None = None
_index_lock = threading.Lock()


def default_index() -> DocIndex:
    """The project corpus, built once per process. Agents may call the search
    tool in parallel, so the first build is guarded by a lock."""
    global _index
    with _index_lock:
        if _index is None:
            _index = DocIndex.build(DEFAULT_SOURCES, openai_embedder(), CACHE_PATH)
    return _index


@tool("search_internal_docs")
def search_internal_docs_tool(query: str) -> str:
    """Search Harbor & Vale's internal documents (retention playbook, discount policy, past
    campaign results, competitor offers, the unit-change postmortem, the latest churn insights
    and model card). Returns the most relevant sections as JSON, each with its source file and
    section name to cite."""
    return json.dumps(default_index().search(query), ensure_ascii=False)
