from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import csv
import json
import re
import difflib
import unicodedata
import time
import hashlib
import ssl
import http.client
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Any
from collections.abc import Iterable
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from socket import timeout as TimeoutError

# =========================
# SSL + HTTP helpers
# =========================
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _SSL_CTX = ssl.create_default_context()

def _norm(s: str) -> str:
    s = (s or "").strip().lower()
    return re.sub(r"\s+", " ", s)
def _only_digits(s: str) -> str:
    return re.sub(r"\D+", "", (s or ""))

def _normalize_text(s: str) -> str:
    """
    Normalize strings for search:
    - Unicode NFKD + strip diacritics
    - lowercase
    - collapse whitespace
    - treat punctuation/symbols as spaces (so punctuation differences don't create near-duplicates)
    """
    if not s:
        return ""
    s = str(s)

    # Unicode NFKD and strip diacritics
    nfkd = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in nfkd if not unicodedata.combining(ch))

    # Normalize separators / punctuation
    s = s.replace("_", " ")
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)

    # Lowercase and collapse whitespace
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def _as_iterable(value) -> list[str]:
    """
    Normalize "maybe a string / list / dict" fields into a flat list[str]
    so search can treat multi-value fields consistently.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        full = (" ".join([str(value.get("first_name", "")).strip(), str(value.get("last_name", "")).strip()])).strip()
        if full:
            out.append(full)
        if value.get("name"):
            out.append(str(value.get("name")))
        return out

    if isinstance(value, Iterable):
        out: list[str] = []
        for v in value:
            if v is None:
                continue
            if isinstance(v, str):
                out.append(v)
            elif isinstance(v, dict):
                full = (" ".join([str(v.get("first_name", "")).strip(), str(v.get("last_name", "")).strip()])).strip()
                if full:
                    out.append(full)
                if v.get("name"):
                    out.append(str(v.get("name")))
            else:
                out.append(str(v))
        return out

    return [str(value)]


_SEARCH_STOPWORDS = {"the", "of", "and", "a", "an"}

def _safe_load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default
def _safe_write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
def _http_get(url: str, timeout: float = 6.0, retries: int = 2) -> bytes | None:
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "LibraryManager/1.0"})
            with urlopen(req, timeout=timeout, context=_SSL_CTX) as resp:
                return resp.read()

        except (
            HTTPError,
            URLError,
            TimeoutError,
            http.client.RemoteDisconnected,
            ConnectionResetError,
            socket.timeout,
            ssl.SSLError,
        ):
            if attempt < retries - 1:
                time.sleep(0.5 * (2 ** attempt))
                continue
            return None

# Priority order matters: first match wins.
_GENRE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Horror", ("horror", "ghost", "vampire", "zombie", "haunted", "supernatural horror")),
    ("Mystery", ("mystery", "detective", "whodunit", "crime fiction")),
    ("Thriller", ("thriller", "suspense", "psychological thriller")),
    ("Romance", ("romance", "love story", "romantic")),
    ("Fantasy", ("fantasy", "epic fantasy", "high fantasy", "magic", "dragons")),
    ("Science Fiction", ("science fiction", "sci-fi", "scifi", "sf", "space opera", "dystopia", "cyberpunk")),
    ("Historical Fiction", ("historical fiction", "historical novel")),
    ("Young Adult", ("young adult", "ya", "teen", "juvenile fiction")),
    ("Literary Fiction", ("literary fiction",)),
    ("Classics", ("classics", "classic literature")),
    # Nonfiction-ish buckets
    ("Biography", ("biography",)),
    ("Memoir", ("memoir", "autobiography")),
    ("History", ("history",)),
    ("Science", ("science", "physics", "chemistry", "biology", "astronomy")),
    ("Psychology", ("psychology",)),
    ("Self-Help", ("self-help", "self improvement", "personal development")),
    ("Business", ("business", "economics", "finance", "entrepreneurship")),
    ("True Crime", ("true crime",)),
    ("Politics", ("politics", "government")),
    ("Travel", ("travel",)),
    ("Art & Design", ("art", "design", "architecture", "graphic design")),
    ("Health & Wellness", ("health", "wellness", "medicine", "nutrition", "fitness")),
]

# Quick cleanup for “Genre: Horror, Fiction, Classics…” → tokens
def _split_subjects(s: str) -> list[str]:
    if not s:
        return []
    # subjects from OL are often comma-separated; sometimes semicolons too
    parts = re.split(r"[;,]", s)
    return [p.strip() for p in parts if p and p.strip()]

# =========================
# Tags (multi) derived from subjects_raw
# =========================

# words we do NOT want to treat as useful tags
_TAG_STOPWORDS = {
    "fiction", "nonfiction", "non-fiction", "books", "literature", "novel", "novels",
    "stories", "story", "general", "english", "american", "20th century", "21st century",
}

def _norm_tag(s: str) -> str:
    """Normalize tag for storage/dedup: lowercase, collapse whitespace."""
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s
def _looks_like_generic_tag(t: str) -> bool:
    t = _norm_tag(t)
    if not t:
        return True
    if t in _TAG_STOPWORDS:
        return True
    # avoid one-letter / junky tags
    if len(t) < 3:
        return True
    return False
def _genre_keyword(genre: str) -> str:
    """Lowercase keyword used to detect subgenre tags that include the genre term."""
    g = (genre or "").strip().lower()
    # normalize your two-word genre
    if g in ("science fiction", "sci fi", "sci-fi", "scifi"):
        return "science fiction"
    return g


# =========================
# Genre Subtags Constant
# =========================
# Known subgenre terms for each genre that don't include the genre word itself.
# Built once at module load; use frozenset to prevent accidental modification.
GENRE_SUBTAGS: dict[str, frozenset[str]] = {
    "science fiction": frozenset({
        "space opera", "dystopia", "cyberpunk", "time travel", "post-apocalyptic",
        "military science fiction", "hard science fiction", "soft science fiction",
        "alternate history", "alien invasion", "first contact", "near future",
    }),
    "fantasy": frozenset({
        "epic fantasy", "high fantasy", "urban fantasy", "dark fantasy",
        "sword and sorcery", "portal fantasy", "grimdark",
    }),
    "romance": frozenset({
        "historical romance", "paranormal romance", "romantic comedy",
        "contemporary romance", "dark romance",
    }),
    "horror": frozenset({
        "gothic horror", "cosmic horror", "body horror", "psychological horror",
        "supernatural horror",
    }),
    "mystery": frozenset({
        "cozy mystery", "police procedural", "noir", "detective fiction",
    }),
    "thriller": frozenset({
        "psychological thriller", "legal thriller", "political thriller",
    }),
    "young adult": frozenset({"coming of age"}),
}
def _derive_starter_tags(subject_str: str, genre: str) -> list[str]:
    """
    Starter tags behave like subgenres:
    - derived from subjects_raw
    - primary rule: phrases that contain the genre term (e.g. "historical romance")
    - fallback rule: allow known subgenre terms for each genre (e.g. Sci-Fi -> "space opera")
    
    Uses module-level GENRE_SUBTAGS constant for efficiency (built once at import).
    """
    tokens = _split_subjects(subject_str)
    if not tokens:
        return []

    gkw = _genre_keyword(genre)
    out: list[str] = []

    for raw in tokens:
        t = _norm_tag(raw)
        if _looks_like_generic_tag(t):
            continue

        # drop exact genre duplicates (science fiction -> not a tag)
        if gkw and t == gkw:
            continue

        # MAIN RULE: subgenre phrase that contains the genre term
        if gkw and re.search(rf"\b{re.escape(gkw)}\b", t):
            out.append(t)
            continue

        # FALLBACK: known subtags for that genre (space opera, cyberpunk, etc.)
        if gkw and t in GENRE_SUBTAGS.get(gkw, frozenset()):
            out.append(t)
            continue

    # Dedupe, stable order
    seen = set()
    final = []
    for t in out:
        if t not in seen:
            seen.add(t)
            final.append(t)

    return final
def _merge_tags(existing: list[str], incoming: list[str]) -> list[str]:
    """Union of tags, normalized/deduped, preserving existing order first."""
    ex = [_norm_tag(x) for x in (existing or []) if _norm_tag(x)]
    inc = [_norm_tag(x) for x in (incoming or []) if _norm_tag(x)]

    out: list[str] = []
    seen = set()

    for t in ex + inc:
        if _looks_like_generic_tag(t):
            continue
        if t not in seen:
            seen.add(t)
            out.append(t)

    return out





# =========================
# Data structures
# =========================
@dataclass
class ImportReport:
    imported: int = 0
    merged: int = 0
    created: int = 0
    skipped_no_isbn: int = 0
    skipped_existing_isbn: int = 0

# =========================
# LibraryData
# =========================
class LibraryData:
    FICTION_GENRES = [
        "Fantasy", "Contemporary", "Classics", "Childrens", "Manga", "Graphic Novels",
        "Horror", "LGBTQ+", "Mystery", "Supernatural", "Romance", "Science Fiction",
        "Short Stories", "Thriller", "Western", "Young Adult", "Poetry", "Drama",
        "Adventure", "Mythology",
    ]

    NONFICTION_GENRES = [
        "Art & Photography", "Memoirs", "Essays", "Food & Drink", "History", "How-To/Guides",
        "Social Sciences", "Humor", "Philosophy", "Religion", "Science & Technology",
        "Self-Help", "Travel", "True Crime", "Nature", "Health & Medicine", "Finance",
        "Education", "Parenting", "Hobbies", "Home & Garden", "Reference",
    ]

    ALL_ALLOWED_GENRES = set(FICTION_GENRES) | set(NONFICTION_GENRES)

    """
    Owns:
      - internal catalog storage (catalog.json) : dict[book_id, book_dict]
      - cover cache folder (covers/)
      - cover index (cover_index.json) mapping book_id -> cover filename
      - queues:
          sync_queue  = missing cover
          genre_queue = missing genre/subject
    """

    # ---------- Init / persistence ----------
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.covers_dir = self.data_dir / "covers"
        self.collection_images_dir = self.data_dir / "collection_images"
        self.collection_images_dir.mkdir(parents=True, exist_ok=True)
        self.catalog_path = self.data_dir / "catalog.json"
        self.cover_index_path = self.data_dir / "cover_index.json"

        self.queue_path = self.data_dir / "sync_queue.json"
        self.genre_queue_path = self.data_dir / "genre_queue.json"

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.covers_dir.mkdir(parents=True, exist_ok=True)

        self.catalog: dict[str, dict] = _safe_load_json(self.catalog_path, {})
        self.cover_index: dict[str, str] = _safe_load_json(self.cover_index_path, {})

        self.sync_queue: set[str] = set()
        self.genre_queue: set[str] = set()
        self._load_sync_queue()
        self._load_genre_queue()

        # --- Search suggestion cache (rebuilt lazily) ---
        self._cached_candidates: list[str] = []
        self._cached_norm_index: list[tuple[str, str]] = []  # (original, normalized)
        self._cached_norm_map: dict[str, str] = {}
        self._token_index: dict[str, set[str]] = {}

        # --- Collections (custom user lists) ---
        self.collections_path = self.data_dir / "collections.json"
        self.collections: dict[str, dict] = _safe_load_json(self.collections_path, {})
        if not isinstance(self.collections, dict):
            self.collections = {}

        # --- Recent tag history (persisted) ---
        self.recent_tags_path = self.data_dir / "recent_tags.json"
        self.recent_tags = _safe_load_json(self.recent_tags_path, [])
        if not isinstance(self.recent_tags, list):
            self.recent_tags = []
        self.recent_tags = [_norm_tag(t) for t in self.recent_tags if _norm_tag(t)]
        _safe_write_json(self.recent_tags_path, self.recent_tags)

        # --- User-defined genres (persisted) ---
        self.user_genres_path = self.data_dir / "user_genres.json"
        raw_ug = _safe_load_json(self.user_genres_path, [])
        if not isinstance(raw_ug, list):
            raw_ug = []
        self.user_genres: set[str] = set()
        for g in raw_ug:
            if isinstance(g, str) and g.strip():
                self.user_genres.add(g.strip().title())

        # --- Genre overrides (for renamed standard genres) ---
        # Maps original_name -> new_name for standard genres that have been renamed
        self.genre_overrides_path = self.data_dir / "genre_overrides.json"
        self.genre_overrides: dict[str, str] = _safe_load_json(self.genre_overrides_path, {})
        if not isinstance(self.genre_overrides, dict):
            self.genre_overrides = {}

        # --- App settings (persisted) ---
        self.settings_path = self.data_dir / "settings.json"
        self.settings: dict = _safe_load_json(self.settings_path, {})
        if not isinstance(self.settings, dict):
            self.settings = {}

        # Ensure defaults exist
        self.settings.setdefault("library_name", "Family Library")
        _safe_write_json(self.settings_path, self.settings)

        # --- Deleted genres (standard genres that user deleted) ---
        # These won't be restored during sync
        self.deleted_genres_path = self.data_dir / "deleted_genres.json"
        raw_dg = _safe_load_json(self.deleted_genres_path, [])
        if not isinstance(raw_dg, list):
            raw_dg = []
        self.deleted_genres: set[str] = set()
        for g in raw_dg:
            if isinstance(g, str) and g.strip():
                self.deleted_genres.add(g.strip().title())

        # Optional: normalize legacy keys into canonical (safe to re-run)
        changed = self.normalize_catalog_keys()
        changed2 = self.recanonize_all_genres()
        changed += changed2
        if changed:
            # normalization changes catalog, so queues may be stale
            self.rebuild_queues(force=True)  # Force rebuild after normalization
            self.save()

    def save(self):
        _safe_write_json(self.catalog_path, self.catalog)
        _safe_write_json(self.cover_index_path, self.cover_index)
        _safe_write_json(self.collections_path, self.collections)
        self._invalidate_search_cache()

    def factory_reset(self) -> None:
        """
        Deletes ALL stored library data on disk (covers + catalog + queues + any future
        customizable files like genres/tags/shelves/settings stored under data_dir).
        Then clears in-memory structures.
        """
        # 1) Delete everything inside data_dir
        try:
            if self.data_dir.exists():
                for p in self.data_dir.glob("*"):
                    try:
                        if p.is_file():
                            p.unlink()
                        elif p.is_dir():
                            # delete folder contents
                            for sub in p.rglob("*"):
                                try:
                                    if sub.is_file():
                                        sub.unlink()
                                except Exception:
                                    pass
                            # remove empty dirs bottom-up
                            for subdir in sorted([d for d in p.rglob("*") if d.is_dir()], reverse=True):
                                try:
                                    subdir.rmdir()
                                except Exception:
                                    pass
                            try:
                                p.rmdir()
                            except Exception:
                                pass
                    except Exception:
                        pass
        except Exception:
            pass

        # 2) Recreate required dirs
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.covers_dir.mkdir(parents=True, exist_ok=True)

        # 3) Clear in-memory state
        self.catalog = {}
        self.cover_index = {}
        self.sync_queue = set()
        self.genre_queue = set()
        self.user_genres = set()  # Clear custom user genres
        self.genre_overrides = {}  # Clear renamed standard genres (restore to defaults)
        self.deleted_genres = set()  # Clear deleted genres (restore standard genres)
        self.save()
        self._save_sync_queue()
        self._save_genre_queue()
        self._save_genre_overrides()
        self._save_deleted_genres()
        self.collections = {}
        self._migrate_collection_read_to_catalog()

    # =========================
    # Book accessors (UI-facing)
    # =========================

    def get_book(self, book_id: str) -> dict | None:
        """Return a single book by id."""
        bid = (book_id or "").strip()
        return self.catalog.get(bid)

    def get_library_name(self) -> str:
        """User-visible library name (persisted in settings.json)."""
        name = (self.settings or {}).get("library_name", "Family Library")
        if not isinstance(name, str):
            return "Family Library"
        name = name.strip()
        return name or "Family Library"

    def set_library_name(self, name: str, *, persist: bool = True) -> str:
        """Set and persist the library name. Returns the normalized saved value."""
        if not isinstance(name, str):
            name = ""

        cleaned = name.strip()
        if not cleaned:
            cleaned = "Family Library"

        self.settings["library_name"] = cleaned
        if persist:
            _safe_write_json(self.settings_path, self.settings)
        return cleaned


    # ---------- Global per-book "read" flag (persists in catalog.json) ----------
    def get_book_read(self, book_id: str) -> bool:
        b = self.get_book(str(book_id))
        return bool(b.get("read")) if isinstance(b, dict) else False

    def set_book_read(self, book_id: str, is_read: bool, *, persist: bool = True) -> None:
        bid = str(book_id)
        b = self.catalog.get(bid)
        if not isinstance(b, dict):
            return
        b["read"] = bool(is_read)
        self.catalog[bid] = b
        if persist:
            self.save()

    def toggle_book_read(self, book_id: str, *, persist: bool = True) -> bool:
        bid = str(book_id)
        cur = self.get_book_read(bid)
        nxt = not cur
        self.set_book_read(bid, nxt, persist=persist)
        return nxt

    def get_books_by_ids(self, ids: list[str]) -> list[dict]:
        """Resolve a list of book dicts by book_id, preserving order."""
        out: list[dict] = []
        for bid in (ids or []):
            b = self.catalog.get((bid or "").strip())
            if b:
                out.append(b)
        return out

    # ---------- Book identity ----------
    def build_book_id(self, row: dict) -> str:
        isbn = self.canonical_isbn(row)
        if isbn:
            return f"isbn:{isbn}"

        title = _norm(row.get("title", ""))
        author = _norm(self._author_display(row))
        year = _norm(self._year_from_row(row))

        base = f"{title}|{author}|{year}"
        h = hashlib.sha1(base.encode("utf-8")).hexdigest()[:16]
        return f"fallback:{h}"

    def _author_display(self, row: dict) -> str:
        first = (row.get("first_name") or "").strip()
        last = (row.get("last_name") or "").strip()
        creators = (row.get("creators") or "").strip()
        if first or last:
            return f"{first} {last}".strip()
        if creators:
            return creators
        return "Unknown author"

    def _year_from_row(self, row: dict) -> str:
        publish_date = (row.get("publish_date") or row.get("date_published") or "").strip()
        if publish_date:
            return publish_date.split("-")[0]
        return (row.get("_year") or "").strip()

    def bucket_genre_from_subjects(self, subject_str: str) -> str:
        s = (subject_str or "").lower()

        # --- Fiction buckets ---
        if any(k in s for k in ("fantasy", "magic", "dragon")): return "Fantasy"
        if any(k in s for k in ("mystery", "detective", "whodunit")): return "Mystery"
        if any(k in s for k in ("thriller", "suspense")): return "Thriller"
        if any(k in s for k in ("horror", "ghost", "vampire", "zombie", "haunted")): return "Horror"
        if any(k in s for k in ("romance", "love story", "romantic")): return "Romance"
        if any(k in s for k in
               ("science fiction", "sci-fi", "scifi", "dystopia", "cyberpunk", "space")): return "Science Fiction"
        if any(k in s for k in ("young adult", "ya", "juvenile fiction", "teen")): return "Young Adult"
        if "manga" in s: return "Manga"
        if any(k in s for k in ("graphic novel", "comics")): return "Graphic Novels"
        if any(k in s for k in ("mythology", "myths", "legend")): return "Mythology"
        if any(k in s for k in ("poetry", "poems")): return "Poetry"
        if any(k in s for k in ("drama", "plays", "theatre")): return "Drama"
        if any(k in s for k in ("adventure", "quest")): return "Adventure"
        if any(k in s for k in ("western", "cowboy")): return "Western"
        if any(k in s for k in ("classics", "classic literature")): return "Classics"
        if any(k in s for k in ("children", "childrens", "picture book")): return "Childrens"
        if any(k in s for k in ("lgbt", "lgbtq", "queer")): return "LGBTQ+"
        if "short story" in s: return "Short Stories"

        # --- Nonfiction buckets ---
        if any(k in s for k in ("memoir", "autobiography")): return "Memoirs"
        if "essay" in s: return "Essays"
        if "history" in s: return "History"
        if any(k in s for k in ("how-to", "guide", "handbook", "manual")): return "How-To/Guides"
        if any(k in s for k in ("social science", "sociology", "anthropology")): return "Social Sciences"
        if any(k in s for k in ("humor", "comedy")): return "Humor"
        if "philosophy" in s: return "Philosophy"
        if any(k in s for k in ("religion", "bible", "christian", "islam", "judaism", "buddh")): return "Religion"
        if any(
            k in s for k in ("science", "technology", "computer", "physics", "biology")): return "Science & Technology"
        if any(k in s for k in ("self-help", "self improvement", "personal development")): return "Self-Help"
        if "travel" in s: return "Travel"
        if any(k in s for k in ("true crime",)): return "True Crime"
        if any(k in s for k in ("nature", "wildlife", "environment")): return "Nature"
        if any(k in s for k in ("health", "medicine", "nutrition", "fitness")): return "Health & Medicine"
        if any(k in s for k in ("finance", "economics", "investing", "money")): return "Finance"
        if any(k in s for k in ("education", "teaching", "school")): return "Education"
        if "parenting" in s: return "Parenting"
        if any(k in s for k in ("hobby", "craft")): return "Hobbies"
        if any(k in s for k in ("home", "garden")): return "Home & Garden"
        if any(k in s for k in ("reference", "encyclopedia", "dictionary")): return "Reference"
        if any(k in s for k in ("art", "photography", "design")): return "Art & Photography"
        if any(k in s for k in ("food", "cook", "recipe", "drink")): return "Food & Drink"

        return ""

    def _starter_genre_only(self, g: str) -> str:
        g = (g or "").strip().title()
        allowed = set(self.FICTION_GENRES) | set(self.NONFICTION_GENRES)
        return g if g in allowed else ""

    def normalize_user_genre(self, value: str) -> str:
        """
        Accepts starter genres + user-defined genres.
        Returns '' if invalid or not user-selected.
        (Backend-safe: no UI dependencies)
        """
        g = (value or "").strip().title()
        if not g:
            return ""
        allowed = set(self.ALL_ALLOWED_GENRES) | set(getattr(self, "user_genres", set()))
        return g if g in allowed else ""

    

    # ---------- USER GENRES (PERSISTED) ----------
    def all_genres(self) -> list[str]:
        """Return starter + user-defined genres (sorted)."""
        base = set(self.ALL_ALLOWED_GENRES)
        base |= set(getattr(self, "user_genres", set()))
        return sorted(base, key=lambda s: s.lower())

    def add_user_genre(self, genre: str) -> None:
        """Add a new custom genre."""
        g = (genre or "").strip().title()
        if not g:
            return
        if not hasattr(self, "user_genres"):
            self.user_genres = set()
        self.user_genres.add(g)
        try:
            self.user_genres_path.write_text(json.dumps(sorted(self.user_genres), indent=2), encoding="utf-8")
        except Exception:
            pass

    def _save_genre_overrides(self) -> None:
        """Persist genre overrides to disk."""
        try:
            self.genre_overrides_path.write_text(
                json.dumps(self.genre_overrides, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def _save_deleted_genres(self) -> None:
        """Persist deleted genres to disk."""
        try:
            self.deleted_genres_path.write_text(
                json.dumps(sorted(self.deleted_genres), indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def _save_user_genres(self) -> None:
        """Persist user genres to disk."""
        try:
            self.user_genres_path.write_text(
                json.dumps(sorted(self.user_genres), indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def is_standard_genre(self, genre: str) -> bool:
        """Check if a genre is a standard (built-in) genre."""
        g = (genre or "").strip().title()
        return g in self.FICTION_GENRES or g in self.NONFICTION_GENRES

    def is_user_genre(self, genre: str) -> bool:
        """Check if a genre is a custom user genre (not a standard one)."""
        g = (genre or "").strip().title()
        if not g:
            return False
        if self.is_standard_genre(g):
            return False
        return hasattr(self, "user_genres") and g in self.user_genres

    def get_user_genres(self) -> list[str]:
        """Return sorted list of custom user genres."""
        if not hasattr(self, "user_genres"):
            return []
        return sorted(self.user_genres)

    def get_effective_genre_name(self, original_genre: str) -> str:
        """
        Get the effective (possibly renamed) name for a genre.
        If a standard genre was renamed, returns the new name.
        """
        g = (original_genre or "").strip().title()
        if not g:
            return g
        # Check if this genre has been renamed
        if g in self.genre_overrides:
            return self.genre_overrides[g]
        return g

    def get_original_genre_name(self, current_genre: str) -> str | None:
        """
        Get the original standard genre name if this is a renamed genre.
        Returns None if it's not a renamed standard genre.
        """
        g = (current_genre or "").strip().title()
        for original, renamed in self.genre_overrides.items():
            if renamed == g:
                return original
        return None

    def is_genre_deleted(self, genre: str) -> bool:
        """Check if a genre has been deleted by the user."""
        g = (genre or "").strip().title()
        return g in self.deleted_genres

    def delete_genre(self, genre: str) -> int:
        """
        Delete a genre (standard or custom) and clear it from all books.
        
        - Clears the genre field from all books that have this genre
        - For custom genres: removes from user_genres
        - For standard genres: adds to deleted_genres so it won't be restored during sync
        
        Returns the number of books that had their genre cleared.
        """
        g = (genre or "").strip().title()
        if not g:
            return 0

        # Check if it's a renamed standard genre - get the original name
        original = self.get_original_genre_name(g)
        
        # Clear the genre from all books first (mirrors rename_genre's behavior)
        books_updated = 0
        for bid, book in list(self.catalog.items()):
            book_genre = (book.get("genre") or "").strip().title()
            # Match both the current name and the original name if renamed
            if book_genre == g or (original and book_genre == original):
                book["genre"] = ""
                self.catalog[bid] = book
                books_updated += 1
        
        if self.is_user_genre(g):
            # Custom genre - remove from user_genres
            self.user_genres.discard(g)
            self._save_user_genres()
        elif self.is_standard_genre(g) or original:
            # Standard genre (or renamed standard genre)
            # Add original name to deleted_genres
            genre_to_delete = original if original else g
            self.deleted_genres.add(genre_to_delete)
            self._save_deleted_genres()
            
            # If it was renamed, also remove the override
            if original:
                self.genre_overrides.pop(original, None)
                self._save_genre_overrides()
        else:
            # Genre exists only in books but isn't tracked - still clear from books
            pass

        # Persist catalog changes if any books were updated
        if books_updated > 0:
            self.save()
            
        return books_updated

    def rename_genre(self, old_name: str, new_name: str) -> int:
        """
        Rename a genre (standard or custom) and update all books with that genre.
        - For standard genres: stores the rename in genre_overrides (reversible on factory reset)
        - For custom genres: updates user_genres
        Returns the number of books updated.
        """
        old = (old_name or "").strip().title()
        new = (new_name or "").strip().title()
        if not old or not new or old == new:
            return 0

        # Check if old_name is a renamed standard genre
        original_standard = self.get_original_genre_name(old)
        is_standard = self.is_standard_genre(old) or original_standard is not None
        is_custom = self.is_user_genre(old)

        # Update books in catalog
        count = 0
        for bid, book in self.catalog.items():
            book_genre = (book.get("genre") or "").strip().title()
            if book_genre == old:
                book["genre"] = new
                self.catalog[bid] = book
                count += 1

        if is_standard:
            # Standard genre - store the override
            # Use the original standard name as the key
            original_key = original_standard if original_standard else old
            self.genre_overrides[original_key] = new
            self._save_genre_overrides()
        elif is_custom:
            # Custom genre - update user_genres
            self.user_genres.discard(old)
            self.user_genres.add(new)
            self._save_user_genres()
        else:
            # It's a genre that exists in books but isn't tracked
            # Treat it as a new custom genre
            self.user_genres.add(new)
            self._save_user_genres()

        # Save catalog if any books were updated
        if count > 0:
            self.save()

        return count

    def get_all_active_genres(self) -> list[str]:
        """
        Get all active genres (for display in UI).
        - Standard genres (with any renames applied, excluding deleted)
        - Custom genres
        """
        genres = set()

        # Standard genres (with overrides applied, excluding deleted)
        for g in self.FICTION_GENRES + self.NONFICTION_GENRES:
            if self.is_genre_deleted(g):
                continue
            effective = self.get_effective_genre_name(g)
            genres.add(effective)

        # Custom genres
        genres.update(self.user_genres)

        return sorted(genres, key=str.lower)

    def should_apply_genre_from_sync(self, book_id: str, synced_genre: str) -> bool:
        """
        Determine if a genre from sync should be applied to a book.
        Returns False if the genre was deleted by the user.
        """
        g = (synced_genre or "").strip().title()
        if not g:
            return True  # No genre to apply

        # If the genre was deleted, don't apply it
        if self.is_genre_deleted(g):
            return False

        return True

    def apply_genre_from_sync(self, synced_genre: str) -> str:
        """
        Transform a genre from sync to the effective genre name.
        - If deleted: returns empty string
        - If renamed: returns the new name
        - Otherwise: returns the original
        """
        g = (synced_genre or "").strip().title()
        if not g:
            return ""

        # If deleted, return empty
        if self.is_genre_deleted(g):
            return ""

        # Return effective name (handles renames)
        return self.get_effective_genre_name(g)

    def _invalidate_search_cache(self) -> None:
        """Clear cached search candidates/indexes (called after catalog changes)."""
        self._cached_candidates = []
        self._cached_norm_index = []
        self._cached_norm_map = {}
        self._token_index = {}

    def _build_search_token_index(self) -> None:
        """Build token -> originals index for faster suggestions."""
        token_index: dict[str, set[str]] = {}
        for orig, norm in self._cached_norm_index:
            for t in (norm or "").split():
                if t and t not in _SEARCH_STOPWORDS:
                    token_index.setdefault(t, set()).add(orig)
        self._token_index = token_index

    # ---------- SEARCH CANDIDATES & MATCHING ----------





    
    # ---------- SEARCH CANDIDATES & MATCHING ----------

    def collect_search_candidates(self) -> list[str]:
        """
        Collect (and cache) unique searchable strings from the catalog for autocomplete/suggestions.

        - Handles multi-value fields (lists/dicts/strings) via _as_iterable.
        - Dedupes using _normalize_text (diacritics/punctuation/whitespace-insensitive).
        - Builds a cached normalized index + token index for fast search_matches().
        """
        out: list[str] = []
        seen: set[str] = set()

        for b in self.catalog.values():
            entries: list[str] = []

            # Titles / authors / publisher (some catalogs may still use 'author')
            entries += _as_iterable(b.get("title"))
            entries += _as_iterable(b.get("author"))
            entries += _as_iterable(b.get("publisher"))

            # Creators may be string, list[str], or list[dict]
            entries += _as_iterable(b.get("creators"))

            # First/last name (only if non-empty; collapse double spaces)
            first = str(b.get("first_name", "")).strip()
            last = str(b.get("last_name", "")).strip()
            full_name = (" ".join([first, last])).strip()
            if full_name:
                entries.append(full_name)

            for s in entries:
                s = (s or "").strip()
                if not s:
                    continue
                norm = _normalize_text(s)
                if not norm or norm in seen:
                    continue
                seen.add(norm)
                out.append(s)

        self._cached_candidates = out
        self._cached_norm_index = [(orig, _normalize_text(orig)) for orig in out]
        self._cached_norm_map = {orig: norm for orig, norm in self._cached_norm_index}
        self._build_search_token_index()
        return out

    def search_matches(self, query: str, limit: int = 6) -> list[str]:
        """
        Autocomplete-style matching:
        - prioritizes starts-with and word-prefix matches
        - falls back to substring matches
        - optionally tolerates small typos via lightweight fuzzy matching (difflib)

        Returns a list of original (display) strings.
        """
        q = _normalize_text(query)
        if not q:
            return []

        # Lazy cache build
        if not self._cached_norm_index:
            self.collect_search_candidates()

        q_tokens_all = [t for t in q.split() if t]
        q_tokens = [t for t in q_tokens_all if t not in _SEARCH_STOPWORDS]

        def score(norm_candidate: str) -> int:
            tokens = norm_candidate.split()

            starts_with = 100 if norm_candidate.startswith(q) else 0

            # For multi-word queries, prefer candidates that start with the first token
            word_prefix = 50 if (q_tokens and any(t.startswith(q_tokens[0]) for t in tokens)) else 0

            substring = 10 if q in norm_candidate else 0

            token_bonus = 0
            if q_tokens:
                token_bonus = sum(8 for qt in q_tokens if any(t.startswith(qt) for t in tokens))
                if all(any(t.startswith(qt) for t in tokens) for qt in q_tokens):
                    token_bonus += 20

            return starts_with + word_prefix + substring + token_bonus

        # Candidate narrowing via token index (faster on large catalogs)
        candidates: set[str] = set()
        if q_tokens and self._token_index:
            keys = list(self._token_index.keys())
            for qt in q_tokens:
                for token in keys:
                    if token.startswith(qt):
                        candidates |= self._token_index[token]

        # If token narrowing yields nothing, fall back to scanning cached list
        if not candidates:
            candidates = set(self._cached_candidates)

        scored: list[tuple[int, str]] = []
        for orig in candidates:
            norm = self._cached_norm_map.get(orig) or _normalize_text(orig)
            tokens = norm.split()
            if norm.startswith(q) or q in norm or any(t.startswith(q) for t in tokens):
                scored.append((score(norm), orig))

        scored.sort(key=lambda x: (-x[0], x[1]))

        results = [orig for _, orig in scored[:limit]]
        if len(results) >= limit:
            return results

        # --- Fuzzy fill (typo tolerance) ---
        # Only for longer queries to avoid noise.
        if len(q) >= 3:
            existing = set(results)
            fuzzy: list[tuple[int, str]] = []

            for orig, norm in self._cached_norm_index:
                if orig in existing:
                    continue

                # quick filter: share starting letter with any token (cheap & cuts noise)
                if not any(tok.startswith(q[0]) for tok in norm.split()):
                    continue

                sim = difflib.SequenceMatcher(a=q, b=norm).ratio()
                if sim < 0.62:
                    continue

                base = 0
                if norm.startswith(q):
                    base += 100
                elif any(t.startswith(q) for t in norm.split()):
                    base += 60
                elif q in norm:
                    base += 30

                fuzzy.append((base + int(sim * 100), orig))

            fuzzy.sort(key=lambda x: (-x[0], x[1]))
            for _, orig in fuzzy:
                results.append(orig)
                if len(results) >= limit:
                    break

        return results



    # ---------- COLLECTION GROUPING & SORTING ----------
    def group_books_by_genre(self, books: list[dict]) -> list[tuple[str, list[dict]]]:
        """
        Group a list of books by their genre, sorted alphabetically.
        
        Args:
            books: List of book dicts to group
            
        Returns:
            List of (genre_name, books_list) tuples, sorted by genre name.
            Books within each genre are sorted by title.
            Books without a genre are grouped under "Unknown".
        """
        from collections import defaultdict
        
        groups: dict[str, list[dict]] = defaultdict(list)
        for b in books:
            g = (b.get("genre") or "").strip() or "Unknown"
            groups[g].append(b)
        
        out: list[tuple[str, list[dict]]] = []
        for g in sorted(groups.keys(), key=str.lower):
            sorted_books = sorted(groups[g], key=lambda x: (x.get("title") or "").lower())
            out.append((g, sorted_books))
        return out

    def sort_collection_books(
        self, 
        collection_name: str, 
        books: list[dict], 
        mode: str = "title"
    ) -> list[dict]:
        """
        Sort books in a collection by the specified mode.
        
        Attaches _collection_last_updated metadata to each book for sorting.
        
        Args:
            collection_name: Name of the collection (for last-updated lookup)
            books: List of book dicts to sort
            mode: Sort mode - "last_updated", "genre", or "title" (default)
            
        Returns:
            Sorted list of books (with _collection_last_updated attached)
        """
        # Attach last-updated timestamp from collection metadata
        for b in books:
            bid = str(b.get("id") or b.get("book_id") or "")
            b["_collection_last_updated"] = self.get_collection_last_updated(collection_name, bid)
        
        if mode == "last_updated":
            # Most recently updated first, then by title
            return sorted(
                books,
                key=lambda b: (b.get("_collection_last_updated", 0.0), (b.get("title") or "").lower()),
                reverse=True
            )
        elif mode == "genre":
            # By genre, then by title within genre
            return sorted(
                books,
                key=lambda b: ((b.get("genre") or "Unknown").lower(), (b.get("title") or "").lower())
            )
        else:
            # Default: by title
            return sorted(books, key=lambda b: (b.get("title") or "").lower())

    def top_tags_for_books(self, book_ids: list[str], limit: int = 8) -> list[str]:
        """
        Get the most frequently used tags across a set of books.
        
        Args:
            book_ids: List of book IDs to analyze
            limit: Maximum number of tags to return (default 8)
            
        Returns:
            List of tag strings (lowercase, normalized) sorted by frequency descending
        """
        from collections import Counter
        
        books = self.get_books_by_ids(book_ids)
        counter: Counter[str] = Counter()
        
        for b in books:
            raw_tags = b.get("tags")
            if isinstance(raw_tags, list):
                for t in raw_tags:
                    nt = (str(t) or "").strip().lower()
                    if nt:
                        counter[nt] += 1
            elif isinstance(raw_tags, str):
                # Handle comma or semicolon separated string
                for t in re.split(r"[;,]", raw_tags):
                    nt = (t or "").strip().lower()
                    if nt:
                        counter[nt] += 1
        
        return [tag for tag, count in counter.most_common(limit)]

    # ---------- COVER IMPORT (PERSISTED IMMEDIATELY) ----------
    def set_cover_from_file(self, book_id: str, src_path: Path) -> None:
        """Copy a user-picked cover image into covers/ and update cover_index + queues, then persist immediately."""
        bid = (book_id or "").strip()
        if not bid:
            raise ValueError("Missing book_id")
        p = Path(src_path)
        if not p.exists():
            raise FileNotFoundError(str(p))

        ext = p.suffix.lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            ext = ".png"

        stamp = int(time.time() * 1000)
        h = hashlib.sha1((str(p) + str(stamp)).encode("utf-8")).hexdigest()[:10]
        filename = f"user_{bid}_{h}{ext}"
        dest = self.covers_dir / filename
        dest.write_bytes(p.read_bytes())

        self.cover_index[bid] = filename
        self.sync_queue.discard(bid)

        self.save()
        self._save_sync_queue()
# ---------- COLLECTION BOOK META (PERSISTED) ----------
    def _save_collections(self) -> None:
        """
        Compatibility helper (some UI code calls _save_collections()).
        Route to your existing persistence method.
        """
        # If your class already has `save()` that writes collections to disk, use it.
        self.save()

    def _resolve_collection_id(self, collection_name_or_id: str) -> str | None:
        s = (collection_name_or_id or "").strip()
        if not s:
            return None
        if s in self.collections:
            return s
        return self._find_collection_id_by_name(s)

    def get_collection_book_meta(self, collection_name_or_id: str, book_id: str) -> dict:
        cid = self._resolve_collection_id(collection_name_or_id)
        if not cid:
            return {}
        rec = self.collections.get(cid) or {}
        meta = rec.get("book_meta") or {}
        return meta.get(str(book_id), {}) if isinstance(meta, dict) else {}

    def set_collection_book_meta(self, collection_name_or_id: str, book_id: str, updates: dict) -> None:
        cid = self._resolve_collection_id(collection_name_or_id)
        if not cid:
            return
        rec = self.collections.setdefault(cid, {})
        meta = rec.setdefault("book_meta", {})
        if not isinstance(meta, dict):
            meta = {}
            rec["book_meta"] = meta

        bid = str(book_id)
        row = meta.get(bid) or {}
        if not isinstance(row, dict):
            row = {}
        row.update(dict(updates or {}))
        meta[bid] = row

        self._save_collections()

    def _migrate_collection_read_to_catalog(self) -> None:
        """
        One-time (safe to re-run) migration for older saves:
        - Old: collections.json stored per-collection read flags in collections[cid]["book_meta"][bid]["read"].
        - New: read is a GLOBAL per-book flag stored in catalog.json at catalog[bid]["read"].
        This migrates any True marks into the catalog and removes the legacy keys from collections.
        """
        changed = False
        for cid, rec in (self.collections or {}).items():
            if not isinstance(rec, dict):
                continue
            meta = rec.get("book_meta") or {}
            if not isinstance(meta, dict):
                continue

            for bid, m in list(meta.items()):
                if not isinstance(m, dict):
                    continue
                if bool(m.get("read")):
                    b = self.catalog.get(str(bid))
                    if isinstance(b, dict) and not bool(b.get("read")):
                        b["read"] = True
                        self.catalog[str(bid)] = b
                        changed = True

                # remove legacy key so we don't keep writing it forever
                if "read" in m:
                    m.pop("read", None)
                    meta[str(bid)] = m
                    changed = True

            rec["book_meta"] = meta
            self.collections[str(cid)] = rec

        if changed:
            self.save()

    def get_collection_read_marks(self, collection_name_or_id: str) -> set[str]:
        """Compatibility helper for older UI code.
        Returns the set of *book_ids in this collection* that are marked read globally in the catalog.
        """
        cid = self._resolve_collection_id(collection_name_or_id)
        if not cid:
            return set()
        rec = self.collections.get(cid) or {}
        ids = rec.get("book_ids") or []
        if not isinstance(ids, list):
            return set()

        out: set[str] = set()
        for bid in ids:
            bid = str(bid)
            if self.get_book_read(bid):
                out.add(bid)
        return out

    def set_collection_read(self, collection_name_or_id: str, book_id: str, is_read: bool) -> None:
        """Compatibility helper for older UI code.
        'read' is no longer stored per-collection; it is a global per-book flag.
        """
        self.set_book_read(str(book_id), bool(is_read), persist=True)

    def touch_collection_book(self, collection_name: str, book_id: str) -> None:
        """
        Call this whenever collection-specific details for this book are edited.
        """
        self.set_collection_book_meta(collection_name, book_id, {"last_updated": time.time()})

    def get_collection_last_updated(self, collection_name: str, book_id: str) -> float:
        meta = self.get_collection_book_meta(collection_name, book_id)
        ts = meta.get("last_updated")
        return float(ts) if ts is not None else 0.0

    # ---------- ISBN helpers ----------
    @staticmethod
    def _clean_isbn(value: str) -> str:
        """Remove all characters except digits and X (for ISBN-10 check digit)."""
        s = (value or "").strip()
        return "".join(ch for ch in s if ch.isdigit() or ch.upper() == "X")

    @classmethod
    def canonical_isbn(cls, row_or_value: dict | str) -> str:
        """
        Extract and normalize the best ISBN from a row dict or raw string.
        
        Priority:
        1. ISBN-13 (13 digits only) - preferred
        2. ISBN-10 (10 chars: 9 digits + digit or X)
        
        Returns:
        - For ISBN-13: 13 digits only (no dashes/spaces)
        - For ISBN-10: 10 chars uppercase (9 digits + check digit, may include X)
        - Empty string if no valid ISBN found
        
        This is the single source of truth for ISBN extraction/normalization.
        """
        # Handle direct string input
        if isinstance(row_or_value, str):
            candidates = [row_or_value]
        else:
            # Extract from dict - check all common ISBN field names
            row = row_or_value
            candidates = [
                row.get("ean_isbn13") or "",      # Prefer explicit ISBN-13 first
                row.get("isbn13") or "",
                row.get("ISBN13") or "",
                row.get("isbn") or "",            # Generic isbn field
                row.get("ISBN") or "",
                row.get("upc_isbn10") or "",      # ISBN-10 last
                row.get("isbn10") or "",
                row.get("ISBN10") or "",
            ]
        
        # Try to find best ISBN from candidates
        best_13: str = ""
        best_10: str = ""
        
        for raw in candidates:
            if not raw:
                continue
                
            cleaned = cls._clean_isbn(str(raw))
            if not cleaned:
                continue
            
            # Extract only digits for ISBN-13 check
            digits_only = _only_digits(cleaned)
            
            # Check for valid ISBN-13 (exactly 13 digits)
            if len(digits_only) == 13 and not best_13:
                best_13 = digits_only
                
            # Check for valid ISBN-10 (10 chars: digits + optional X at end)
            if len(cleaned) == 10:
                # ISBN-10: first 9 must be digits, 10th can be digit or X
                if cleaned[:9].isdigit() and (cleaned[9].isdigit() or cleaned[9].upper() == "X"):
                    if not best_10:
                        best_10 = cleaned.upper()
        
        # Prefer ISBN-13 over ISBN-10
        return best_13 or best_10

    def _extract_best_isbn(self, row: dict) -> str:
        """
        DEPRECATED: Use canonical_isbn() instead.
        Kept for backward compatibility - delegates to canonical_isbn.
        """
        return self.canonical_isbn(row)

    @classmethod
    def _best_isbn(cls, row: dict) -> str:
        """
        DEPRECATED: Use canonical_isbn() instead.
        Kept for backward compatibility - delegates to canonical_isbn.
        """
        return cls.canonical_isbn(row)

    # ---------- Cover / genre checks ----------
    def get_cover_path(self, book_id: str) -> Path | None:
        filename = self.cover_index.get(book_id, "")
        if not filename:
            return None
        p = self.covers_dir / filename
        return p if p.exists() else None

    def _has_genre(self, b: dict) -> bool:
        # For queues: only count a CLEAN canonical genre as "has genre"
        return self._genre_is_clean(b)

    def _needs_cover(self, b: dict) -> bool:
        bid = (b.get("book_id") or "").strip()
        return bool(bid) and not bool(self.get_cover_path(bid))

    def _needs_genre(self, b: dict) -> bool:
        return not self._genre_is_clean(b)

    def _genre_is_clean(self, b: dict) -> bool:
        """
        A "clean" genre is ONLY one of your starter genres.
        Nothing else counts as a genre (including any internet/raw subject strings).
        """
        g = (b.get("genre") or "").strip()
        if not g:
            return False

        # normalize casing to match your starter list keys
        g_norm = g.title()

        # must be exactly one of your allowed genres
        return g_norm in self.ALL_ALLOWED_GENRES

    def recanonize_all_genres(self) -> int:
        """
        Recompute bucket genre + starter tags for every book using existing subjects_raw/subject.
        - Does NOT call the network.
        - Does NOT override a user-set starter genre.
        - Ensures genre is always '' or a starter genre.
        - Ensures tags are derived/merged from subjects when possible.
        - Respects deleted genres (won't restore them).
        """
        changed = 0

        for b in self.catalog.values():
            current = (b.get("genre") or "").strip()
            current_norm = current.title() if current else ""

            subj = (b.get("subjects_raw") or b.get("subject") or "").strip()
            if not subj:
                # still ensure tags key exists
                if "tags" not in b or not isinstance(b.get("tags"), list):
                    b["tags"] = []
                    changed += 1
                continue

            # Keep user starter genre if valid; otherwise bucket it
            if current_norm in self.ALL_ALLOWED_GENRES:
                if current != current_norm:
                    b["genre"] = current_norm
                    changed += 1
                genre_for_tags = current_norm
            else:
                raw_bucket = self._starter_genre_only(self.bucket_genre_from_subjects(subj))
                # Apply genre transformations (respect deleted/renamed genres)
                bucket = self.apply_genre_from_sync(raw_bucket)
                if (b.get("genre") or "").strip() != bucket:
                    b["genre"] = bucket
                    changed += 1
                genre_for_tags = bucket or ""

            # ✅ derive/merge tags offline from subjects_raw
            derived = _derive_starter_tags(subj, genre_for_tags)
            existing_tags = b.get("tags")
            if not isinstance(existing_tags, list):
                existing_tags = []
            merged = _merge_tags(existing_tags, derived)
            if merged != existing_tags:
                b["tags"] = merged
                changed += 1

        return changed

    # IMPORTANT: sync means ONLY cover/genre (your requested definition)
    def _needs_sync(self, b: dict) -> bool:
        return self._needs_cover(b) or self._needs_genre(b)

    # ---------- Queues ----------
    def _load_sync_queue(self):
        try:
            if self.queue_path.exists():
                data = json.loads(self.queue_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self.sync_queue = set(str(x) for x in data if str(x).strip())
        except Exception:
            self.sync_queue = set()

    def _save_sync_queue(self):
        try:
            self.queue_path.write_text(json.dumps(sorted(self.sync_queue), indent=2), encoding="utf-8")
        except Exception:
            pass

    def _load_genre_queue(self):
        try:
            if self.genre_queue_path.exists():
                data = json.loads(self.genre_queue_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self.genre_queue = set(str(x) for x in data if str(x).strip())
        except Exception:
            self.genre_queue = set()

    def _save_genre_queue(self):
        try:
            self.genre_queue_path.write_text(json.dumps(sorted(self.genre_queue), indent=2), encoding="utf-8")
        except Exception:
            pass

    def rebuild_queues(self, force: bool = False):
        """
        Rebuild sync queues by scanning the catalog.
        
        Args:
            force: If True, always rebuild. If False, only rebuild if queues appear stale.
        """
        # Skip full rebuild if queues already have content and not forced
        # (incremental updates should keep them accurate)
        if not force and (self.sync_queue or self.genre_queue):
            # Just validate that queued books still exist in catalog
            self.sync_queue = {bid for bid in self.sync_queue if bid in self.catalog}
            self.genre_queue = {bid for bid in self.genre_queue if bid in self.catalog}
            self._save_sync_queue()
            self._save_genre_queue()
            return
        
        # Full rebuild (on first run, after factory reset, or when forced)
        self.sync_queue = {bid for bid, b in self.catalog.items() if self._needs_cover(b)}
        self.genre_queue = {bid for bid, b in self.catalog.items() if self._needs_genre(b)}
        self._save_sync_queue()
        self._save_genre_queue()

    def get_books_needing_update(self) -> list[dict]:
        """
        Union of:
          - missing covers (sync_queue)
          - missing genre/subject (genre_queue)
        Deduped by book_id.
        """
        merged: dict[str, dict] = {}

        for bid in self.sync_queue:
            b = self.catalog.get(bid)
            if b:
                merged[bid] = b

        for bid in self.genre_queue:
            b = self.catalog.get(bid)
            if b:
                merged[bid] = b

        return list(merged.values())

    def queue_book_for_sync(self, book_id: str, book: dict | None = None) -> None:
        """
        Add a single book to the appropriate sync queues if it needs updating.
        Call this when adding/importing a book instead of rebuild_queues().
        """
        bid = (book_id or "").strip()
        if not bid:
            return
        
        if book is None:
            book = self.catalog.get(bid)
        if not book:
            return
        
        # Check if needs cover
        if self._needs_cover(book):
            self.sync_queue.add(bid)
        
        # Check if needs genre
        if self._needs_genre(book):
            self.genre_queue.add(bid)
    
    def queue_books_for_sync(self, book_ids: list[str], save_queues: bool = True) -> None:
        """
        Queue multiple books for sync. More efficient than calling queue_book_for_sync
        in a loop when importing many books.
        
        Args:
            book_ids: List of book IDs to check and queue
            save_queues: If True, persist queues to disk after batch operation
        """
        for bid in book_ids:
            bid = (bid or "").strip()
            if not bid:
                continue
            book = self.catalog.get(bid)
            if not book:
                continue
            if self._needs_cover(book):
                self.sync_queue.add(bid)
            if self._needs_genre(book):
                self.genre_queue.add(bid)
        
        # Save queues after batch operation
        if save_queues:
            self._save_sync_queue()
            self._save_genre_queue()

    # ---------- Normalization (safe migration) ----------
    def normalize_catalog_keys(self) -> int:
        """
        Consolidates legacy genre-ish fields into canonical:
          - subject
          - genre
        Does not overwrite existing canonical values.
        Returns number of books changed.
        """
        changed = 0
        for b in self.catalog.values():
            updated = False

            legacy = []
            for k in ("Subjects", "Subject", "Genre", "group"):
                v = b.get(k)
                if isinstance(v, str) and v.strip():
                    legacy.append(v.strip())

            if legacy:
                # keep a raw-ish subject value if missing
                if not (b.get("subject") or "").strip():
                    b["subject"] = legacy[0]
                    updated = True

            # migrate legacy tags -> canonical tags list (do not overwrite existing tags)
            legacy_tags = b.get("tags")
            if isinstance(legacy_tags, str) and legacy_tags.strip():
                if not isinstance(b.get("tags"), list) or not b.get("tags"):
                    b["tags"] = [_norm_tag(x) for x in re.split(r"[;,]", legacy_tags) if _norm_tag(x)]
                    updated = True
            elif isinstance(legacy_tags, list):
                # normalize existing list
                b["tags"] = [_norm_tag(x) for x in legacy_tags if _norm_tag(x)]
                updated = True
            else:
                # ensure key exists
                if "tags" not in b:
                    b["tags"] = []
                    updated = True
            if updated:
                changed += 1

        return changed

    # ---------- Import / Export ----------
    def import_csv(
            self,
            csv_path: Path,
            *,
            add_new_isbn_only: bool = False,
            require_isbn: bool = False,
    ) -> ImportReport:
        report = ImportReport()
        incoming_rows: list[dict] = []
        imported_book_ids: list[str] = []  # Track IDs for incremental sync queue

        with Path(csv_path).open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                incoming_rows.append(row)

        report.imported = len(incoming_rows)

        # --- Build set of ISBNs already in catalog (canonical form) ---
        existing_isbns: set[str] = set()
        for b in self.catalog.values():
            isbn = self.canonical_isbn(b)
            if isbn:
                existing_isbns.add(isbn)

        for row in incoming_rows:
            # Always compute ISBN first using canonical helper
            isbn = self.canonical_isbn(row)

            # If you want only ISBN-based importing, skip rows without ISBN
            if (require_isbn or add_new_isbn_only) and not isbn:
                report.skipped_no_isbn += 1
                continue

            # If you want "only add NEW ISBNs", skip duplicates (no merge)
            if add_new_isbn_only and isbn:
                if isbn in existing_isbns:
                    report.skipped_existing_isbn += 1
                    continue

                book_id = f"isbn:{isbn}"
                normalized = self._normalize_row(row, book_id)
                self.catalog[book_id] = normalized
                imported_book_ids.append(book_id)  # Track for sync queue
                report.created += 1
                existing_isbns.add(isbn)
                continue

            # --- Default/legacy behavior (merge by book_id fallback allowed) ---
            book_id = self.build_book_id(row)
            normalized = self._normalize_row(row, book_id)

            if book_id in self.catalog:
                existing = self.catalog[book_id]
                self.catalog[book_id] = self._merge_books(existing, normalized)
                imported_book_ids.append(book_id)  # Track for sync queue (may need update)
                report.merged += 1
            else:
                self.catalog[book_id] = normalized
                imported_book_ids.append(book_id)  # Track for sync queue
                report.created += 1

        self.save()
        
        # Queue imported books for sync (incremental, not full rebuild)
        if imported_book_ids:
            self.queue_books_for_sync(imported_book_ids)
        
        return report

    def export_csv(self, out_path: Path, rows: list[dict] | None = None):
        """
        Export books to CSV with consistent column ordering.
        
        Column order:
        1. Preferred columns (in defined order, if present in data)
        2. Remaining columns (alphabetically sorted)
        
        All columns present in any row are included to prevent DictWriter errors.
        """
        if rows is None:
            rows = list(self.catalog.values())

        # Collect all unique headers from all rows
        all_headers: set[str] = set()
        for r in rows:
            all_headers.update(r.keys())

        # Define preferred column order for readability
        PREFERRED_COLUMNS = [
            "title", "creators", "first_name", "last_name",
            "date_published", "publish_date", "publisher", "isbn",
            "genre", "tags", "subject", "notes", "book_id"
        ]
        
        # Build final column order: preferred first (if present), then rest alphabetically
        preferred_present = [col for col in PREFERRED_COLUMNS if col in all_headers]
        remaining_sorted = sorted(all_headers - set(PREFERRED_COLUMNS))
        fieldnames = preferred_present + remaining_sorted

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow(r)

    def _normalize_row(self, row: dict, book_id: str) -> dict:
        r = dict(row)
        r["book_id"] = book_id

        r["title"] = (r.get("title") or r.get("Title") or r.get("book_title") or "").strip()
        r["creators"] = (r.get("creators") or r.get("Creators") or r.get("author") or r.get("Author") or "").strip()
        r["publisher"] = (r.get("publisher") or r.get("Publisher") or "").strip()

        raw_year = (r.get("date_published") or r.get("publish_date") or r.get("Year") or r.get("Year Published") or "").strip()
        r["date_published"] = raw_year.split("-")[0] if raw_year else ""

        raw_genre = (r.get("genre") or r.get("Genre") or "").strip()
        r["genre"] = self._starter_genre_only(raw_genre)  # already good
        # ensure stored value matches canonical casing
        if r["genre"]:
            r["genre"] = r["genre"].title()

        # Use canonical ISBN helper - single source of truth
        canonical = self.canonical_isbn(r)
        r["isbn"] = canonical
        
        # Derive isbn13/isbn10 from canonical or original fields
        if len(canonical) == 13:
            r["isbn13"] = canonical
            r["isbn10"] = self._clean_isbn(str(r.get("upc_isbn10") or r.get("isbn10") or ""))
        elif len(canonical) == 10:
            r["isbn10"] = canonical
            r["isbn13"] = self._clean_isbn(str(r.get("ean_isbn13") or r.get("isbn13") or r.get("ISBN13") or ""))
        else:
            # No valid canonical ISBN, try to preserve any partial data
            r["isbn13"] = self._clean_isbn(str(r.get("ean_isbn13") or r.get("isbn13") or r.get("ISBN13") or ""))
            r["isbn10"] = self._clean_isbn(str(r.get("upc_isbn10") or r.get("isbn10") or ""))

        raw_read = r.get("read")
        if isinstance(raw_read, str):
            r["read"] = raw_read.strip().lower() in {"1", "true", "t", "yes", "y", "read"}
        else:
            r["read"] = bool(raw_read) if raw_read is not None else False

        # --- tags: ensure always a list[str] ---
        raw_tags = r.get("tags")

        if isinstance(raw_tags, str):
            # allow CSV import where tags are comma-separated
            r["tags"] = [_norm_tag(x) for x in re.split(r"[;,]", raw_tags) if _norm_tag(x)]
        elif isinstance(raw_tags, list):
            r["tags"] = [_norm_tag(x) for x in raw_tags if _norm_tag(x)]
        else:
            r["tags"] = []

        return r

    def _merge_books(self, existing: dict, incoming: dict) -> dict:
        """
        Merge two book dicts.
        - Strings overwrite only if non-empty
        - Tags are UNIONED (never overwritten)
        """
        merged = dict(existing)

        for k, v in incoming.items():
            if v is None:
                continue

            # --- SPECIAL CASE: tags ---
            if k == "tags":
                ex = merged.get("tags")
                if not isinstance(ex, list):
                    ex = []
                inc = v if isinstance(v, list) else []
                merged["tags"] = _merge_tags(ex, inc)
                continue

            # --- normal merge rules ---
            if isinstance(v, str):
                if v.strip():
                    merged[k] = v
            else:
                merged[k] = v

        merged["book_id"] = existing.get("book_id") or incoming.get("book_id")
        return merged


    # =========================
    # Collections (custom user lists)
    # =========================
    def list_collections(self) -> list[dict]:
        """Returns all saved collections as a list of dicts."""
        out = list(self.collections.values())
        # ensure required keys exist
        for c in out:
            c.setdefault("collection_id", "")
            c.setdefault("name", "Untitled Collection")
            c.setdefault("created_at", 0.0)
            c.setdefault("updated_at", 0.0)
            c.setdefault("book_ids", [])
        return out

    def _now_ts(self) -> float:
        return float(time.time())

    def create_collection(self, name: str, book_ids: list[str] | None = None, *, persist: bool = True) -> dict:
        """Creates + saves a collection (future UI will call this)."""
        name = (name or "").strip() or "Untitled Collection"
        ts = self._now_ts()
        raw = f"{name}|{ts}"
        cid = "col:" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]

        rec = {
            "collection_id": cid,
            "name": name,
            "created_at": ts,
            "updated_at": ts,
            "book_ids": list(book_ids or []),
        }
        self.collections[cid] = rec
        if persist:
            self.save()
        return rec

    def delete_collection(self, collection_id: str, *, persist: bool = True) -> bool:
        cid = (collection_id or "").strip()
        if not cid:
            return False
        existed = cid in self.collections
        if existed:
            self.collections.pop(cid, None)
            self.clear_collection_photo(cid, persist=False)
            if persist:
                self.save()
        return existed

    def rename_collection(self, collection_id: str, new_name: str, *, persist: bool = True) -> bool:
        cid = (collection_id or "").strip()
        if cid not in self.collections:
            return False
        new_name = (new_name or "").strip()
        if not new_name:
            return False
        self.collections[cid]["name"] = new_name
        self.collections[cid]["updated_at"] = self._now_ts()
        if persist:
            self.save()
        return True

    def set_collection_books(self, collection_id: str, book_ids: list[str], *, persist: bool = True) -> bool:
        cid = (collection_id or "").strip()
        if cid not in self.collections:
            return False
        self.collections[cid]["book_ids"] = list(book_ids or [])
        self.collections[cid]["updated_at"] = self._now_ts()
        if persist:
            self.save()
        return True

    def get_collection_photo_path(self, collection_id: str):
        """Return absolute Path to the collection's stored photo, or None."""
        rec = (self.collections or {}).get(collection_id)
        if not isinstance(rec, dict):
            return None

        rel = (rec.get("photo") or "").strip()
        if not rel:
            return None

        p = self.data_dir / rel
        return p if p.exists() else None

    def set_collection_photo(self, collection_id: str, src_path: str, *, persist: bool = True) -> bool:
        """
        Copy an image into data_dir/collection_images and attach it to the collection record.
        Stores a RELATIVE path in rec["photo"] for portability.
        """
        import shutil
        import hashlib
        from pathlib import Path

        rec = (self.collections or {}).get(collection_id)
        if not isinstance(rec, dict):
            return False

        src = Path(src_path)
        if not src.exists() or not src.is_file():
            return False

        # Basic extension handling
        ext = src.suffix.lower()
        if ext not in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
            # You can widen this if you want
            return False

        # Remove old photo if present
        self.clear_collection_photo(collection_id, persist=False)

        # Stable-ish unique name based on file bytes + collection id
        try:
            b = src.read_bytes()
        except Exception:
            b = (str(src).encode("utf-8"))

        digest = hashlib.sha1((collection_id.encode("utf-8") + b)).hexdigest()[:16]
        fname = f"{collection_id.replace(':','_')}_{digest}{ext}"
        dst = self.collection_images_dir / fname

        try:
            shutil.copy2(src, dst)
        except Exception:
            return False

        # Store relative path so it works across machines
        rel = str((Path("collection_images") / fname).as_posix())
        rec["photo"] = rel
        rec["updated_at"] = self._now_ts()

        if persist:
            self.save()
        return True

    def clear_collection_photo(self, collection_id: str, *, persist: bool = True) -> bool:
        """Detach + delete the stored photo file for this collection (if any)."""
        from pathlib import Path

        rec = (self.collections or {}).get(collection_id)
        if not isinstance(rec, dict):
            return False

        rel = (rec.get("photo") or "").strip()
        if rel:
            p = self.data_dir / rel
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass

        if "photo" in rec:
            rec.pop("photo", None)
            rec["updated_at"] = self._now_ts()

        if persist:
            self.save()
        return True


    def _find_collection_id_by_name(self, name: str) -> str | None:
        target = (name or "").strip().lower()
        if not target:
            return None
        for cid, rec in (self.collections or {}).items():
            rec_name = (rec.get("name") or "").strip().lower()
            if rec_name == target:
                return cid
        return None

    def upsert_collection(self, name: str, book_ids: list[str] | None = None, *, persist: bool = True) -> dict:
        """
        Create if missing, otherwise update the existing collection with same name.
        This makes "Save Collection" behave the way users expect across sessions.
        """
        name = (name or "").strip() or "Untitled Collection"
        book_ids = list(book_ids or [])

        cid = self._find_collection_id_by_name(name)
        if cid is None:
            rec = self.create_collection(name, book_ids, persist=False)
            cid = rec["collection_id"]
        else:
            # ensure record exists (defensive)
            self.collections.setdefault(cid, {
                "collection_id": cid,
                "name": name,
                "created_at": self._now_ts(),
                "updated_at": self._now_ts(),
                "book_ids": [],
            })

        # update fields
        self.collections[cid]["name"] = name
        self.collections[cid]["book_ids"] = book_ids
        self.collections[cid]["updated_at"] = self._now_ts()

        if persist:
            self.save()

        return self.collections[cid]

    def add_book_to_collection(self, collection_name_or_id: str, book_id: str, *, persist: bool = True) -> bool:
        """
        Add a single book to a collection. Returns True if added, False if already present or error.
        Accepts either collection name or collection_id.
        """
        cid = self._resolve_collection_id(collection_name_or_id)
        if not cid or cid not in self.collections:
            return False

        book_id = (book_id or "").strip()
        if not book_id:
            return False

        book_ids = self.collections[cid].get("book_ids") or []
        if not isinstance(book_ids, list):
            book_ids = []

        if book_id in book_ids:
            return False  # Already in collection

        book_ids.append(book_id)
        self.collections[cid]["book_ids"] = book_ids
        self.collections[cid]["updated_at"] = self._now_ts()

        if persist:
            self.save()
        return True

    def remove_book_from_collection(self, collection_name_or_id: str, book_id: str, *, persist: bool = True) -> bool:
        """
        Remove a single book from a collection. Returns True if removed, False if not present or error.
        Accepts either collection name or collection_id.
        """
        cid = self._resolve_collection_id(collection_name_or_id)
        if not cid or cid not in self.collections:
            return False

        book_id = (book_id or "").strip()
        if not book_id:
            return False

        book_ids = self.collections[cid].get("book_ids") or []
        if not isinstance(book_ids, list):
            book_ids = []

        if book_id not in book_ids:
            return False  # Not in collection

        book_ids.remove(book_id)
        self.collections[cid]["book_ids"] = book_ids
        self.collections[cid]["updated_at"] = self._now_ts()

        if persist:
            self.save()
        return True

    # =========================
    # Tag editing (user-driven)
    # =========================
    def _split_user_tags(self, raw: str) -> list[str]:
        """Split a user entry into tags: commas/semicolons/newlines supported."""
        if not raw:
            return []
        parts = re.split(r"[,\n;]+", str(raw))
        out: list[str] = []
        for p in parts:
            t = _norm_tag(p)
            if t:
                out.append(t)
        return out

    def get_tags(self, book_id: str) -> list[str]:
        b = self.catalog.get(book_id) or {}
        tags = b.get("tags")
        if isinstance(tags, list):
            return [_norm_tag(x) for x in tags if _norm_tag(x)]
        if isinstance(tags, str):
            return self._split_user_tags(tags)
        return []

    def set_tags(self, book_id: str, tags: list[str], *, persist: bool = True) -> list[str]:
        b = self.catalog.get(book_id)
        if not b:
            return []
        # normalize + dedupe preserving order
        out: list[str] = []
        seen = set()
        for t in (tags or []):
            nt = _norm_tag(t)
            if not nt:
                continue
            if nt not in seen:
                seen.add(nt)
                out.append(nt)
        b["tags"] = out
        if persist:
            self.save()
        return out

    def add_tags(self, book_id: str, tags: str | list[str], *, persist: bool = True) -> list[str]:
        b = self.catalog.get(book_id)
        if not b:
            return []

        existing = self.get_tags(book_id)

        if isinstance(tags, str):
            incoming = self._split_user_tags(tags)
        else:
            incoming = [_norm_tag(x) for x in (tags or []) if _norm_tag(x)]

        out: list[str] = []
        seen = set()

        # keep existing order first, then append new uniques
        for t in existing + incoming:
            if t and t not in seen:
                seen.add(t)
                out.append(t)

        b["tags"] = out
        self._note_tag_use(incoming, persist=True)
        if persist:
            self.save()
        return out

    def remove_tag(self, book_id: str, tag: str, *, persist: bool = True) -> list[str]:
        b = self.catalog.get(book_id)
        if not b:
            return []

        target = _norm_tag(tag)
        tags = self.get_tags(book_id)

        out = [t for t in tags if _norm_tag(t) != target]
        b["tags"] = out
        self._prune_recent_tags(persist=True)
        if persist:
            self.save()
        return out

    def _all_tags_in_catalog(self) -> set[str]:
        """All tags that currently exist anywhere in the library."""
        out = set()
        for _bid, b in (self.catalog or {}).items():
            tags = b.get("tags")
            if isinstance(tags, list):
                for t in tags:
                    nt = _norm_tag(t)
                    if nt:
                        out.add(nt)
            elif isinstance(tags, str):
                for t in self._split_user_tags(tags):
                    nt = _norm_tag(t)
                    if nt:
                        out.add(nt)
        return out

    def _save_recent_tags(self) -> None:
        try:
            _safe_write_json(self.recent_tags_path, self.recent_tags)
        except Exception:
            pass

    def _note_tag_use(self, tags: list[str], *, persist: bool = True) -> None:
        """
        Move used tags to the front (most-recent-first), dedup case-insensitively.
        """
        if not isinstance(tags, list):
            return

        recent = getattr(self, "recent_tags", []) or []
        if not isinstance(recent, list):
            recent = []

        for t in tags:
            nt = _norm_tag(t)
            if not nt:
                continue
            # remove any existing occurrence
            recent = [r for r in recent if _norm_tag(r) != nt]
            # add to front
            recent.insert(0, nt)

        # keep a reasonable history
        self.recent_tags = recent[:50]

        if persist:
            self._save_recent_tags()

    def _prune_recent_tags(self, *, persist: bool = True) -> None:
        """Remove tags from history that no longer exist anywhere in the catalog."""
        existing = self._all_tags_in_catalog()
        recent = getattr(self, "recent_tags", []) or []
        if not isinstance(recent, list):
            recent = []
        self.recent_tags = [t for t in recent if _norm_tag(t) in existing]
        if persist:
            self._save_recent_tags()

    def get_recent_tags_global(self, limit: int = 6) -> list[str]:
        """
        Returns most-recent-first tags that still exist in the library.
        """
        try:
            recent = getattr(self, "recent_tags", [])
            if not isinstance(recent, list):
                recent = []
        except Exception:
            recent = []

        existing = self._all_tags_in_catalog()
        out = []
        seen = set()
        for t in recent:
            nt = _norm_tag(t)
            if nt and nt in existing and nt not in seen:
                seen.add(nt)
                out.append(nt)
            if len(out) >= int(limit):
                break
        return out

    # =========================
    # Open Library search + enrichment
    # =========================
    def _subjects_to_string(self, doc: dict, cap: int = 12) -> str:
        subs = doc.get("subject") or doc.get("subjects") or []
        if not isinstance(subs, list):
            return ""
        cleaned = [s.strip() for s in subs if isinstance(s, str) and s.strip()]
        return ", ".join(cleaned[:cap])

    def _apply_ol_enrichment(self, book: dict, doc: dict) -> bool:
        changed = False

        work_key = (doc.get("key") or "").strip()
        edition_key = doc.get("edition_key") or []
        if isinstance(edition_key, list) and edition_key:
            edition_key = edition_key[0]
        edition_key = (edition_key or "").strip()

        if work_key and not (book.get("openlibrary_work_key") or "").strip():
            book["openlibrary_work_key"] = work_key
            changed = True

        if edition_key and not (book.get("openlibrary_edition_key") or "").strip():
            book["openlibrary_edition_key"] = edition_key
            changed = True

        subject_str = self._subjects_to_string(doc)
        if subject_str:
            # Always store raw internet subjects in subjects_raw
            if not (book.get("subjects_raw") or "").strip():
                book["subjects_raw"] = subject_str
                changed = True

            current = (book.get("genre") or "").strip()
            current_norm = current.title() if current else ""
            user_already_set = (current_norm in self.ALL_ALLOWED_GENRES)

            # ✅ compute bucket FIRST (only if user didn't set a starter genre)
            bucket = ""
            if not user_already_set:
                raw_bucket = self._starter_genre_only(self.bucket_genre_from_subjects(subject_str))
                # Apply genre transformations (respect deleted/renamed genres)
                bucket = self.apply_genre_from_sync(raw_bucket)
                if (book.get("genre") or "").strip() != bucket:
                    book["genre"] = bucket
                    changed = True

            # ✅ derive tags using the final genre we intend to keep
            genre_for_tags = current_norm if user_already_set else (bucket or "")
            derived = _derive_starter_tags(subject_str, genre_for_tags)

            existing_tags = book.get("tags")
            if not isinstance(existing_tags, list):
                existing_tags = []

            merged_tags = _merge_tags(existing_tags, derived)
            if merged_tags != existing_tags:
                book["tags"] = merged_tags
                changed = True

        if not (book.get("publisher") or "").strip():
            pubs = doc.get("publisher") or []
            if isinstance(pubs, list) and pubs:
                book["publisher"] = str(pubs[0]).strip()
                changed = True

        if not (book.get("date_published") or "").strip():
            y = doc.get("first_publish_year")
            if y:
                book["date_published"] = str(y)
                changed = True

        if not (book.get("isbn") or "").strip():
            isbns = doc.get("isbn") or []
            if isinstance(isbns, list) and isbns:
                best = ""
                for cand in isbns[:15]:
                    digits = _only_digits(str(cand))
                    if len(digits) == 13:
                        best = digits
                        break
                if not best:
                    for cand in isbns[:15]:
                        digits = _only_digits(str(cand))
                        if len(digits) == 10:
                            best = digits
                            break
                if best:
                    book["isbn"] = best
                    changed = True

        return changed

    def _ol_search_best(self, title: str, author: str = "", isbn: str = "", limit: int = 5) -> dict | None:
        title = (title or "").strip()
        author = (author or "").strip()
        isbn = (isbn or "").strip()
        FIELDS = "key,cover_i,edition_key,subject,isbn,publisher,first_publish_year"

        # 1) Books API for ISBN
        if isbn:
            clean = _only_digits(isbn) or isbn.replace("-", "").replace(" ", "")
            url = (
                "https://openlibrary.org/api/books"
                f"?bibkeys=ISBN:{quote(clean)}&format=json&jscmd=data"
            )
            raw = _http_get(url)
            if raw:
                try:
                    data = json.loads(raw.decode("utf-8", "replace"))
                    rec = data.get(f"ISBN:{clean}")
                    if isinstance(rec, dict) and rec:
                        doc: dict[str, Any] = {}
                        if rec.get("key"):
                            doc["key"] = rec["key"]

                        subs = rec.get("subjects") or []
                        if isinstance(subs, list):
                            names: list[str] = []
                            for s in subs:
                                if isinstance(s, dict) and (s.get("name") or "").strip():
                                    names.append(s["name"].strip())
                                elif isinstance(s, str) and s.strip():
                                    names.append(s.strip())
                            if names:
                                doc["subject"] = names

                        pubs = rec.get("publishers") or []
                        if isinstance(pubs, list) and pubs:
                            p0 = pubs[0]
                            if isinstance(p0, dict) and (p0.get("name") or "").strip():
                                doc["publisher"] = [p0["name"].strip()]
                            elif isinstance(p0, str) and p0.strip():
                                doc["publisher"] = [p0.strip()]

                        pd = (rec.get("publish_date") or "").strip()
                        if pd:
                            m = re.search(r"\b(\d{4})\b", pd)
                            if m:
                                doc["first_publish_year"] = int(m.group(1))

                        ids = rec.get("identifiers") or {}
                        if isinstance(ids, dict):
                            isbns_out: list[str] = []
                            for k in ("isbn_13", "isbn_10"):
                                vals = ids.get(k) or []
                                if isinstance(vals, list):
                                    isbns_out.extend([str(v) for v in vals if str(v).strip()])
                            if isbns_out:
                                doc["isbn"] = isbns_out

                        return doc
                except Exception:
                    pass

        # 2) Search API isbn query
        if isbn:
            clean = _only_digits(isbn) or isbn.replace("-", "").replace(" ", "")
            url = f"https://openlibrary.org/search.json?q={quote('isbn:' + clean)}&limit=1&fields={FIELDS}"
            raw = _http_get(url)
            if raw:
                try:
                    data = json.loads(raw.decode("utf-8", "replace"))
                    docs = data.get("docs") or []
                    if docs:
                        return docs[0]
                except Exception:
                    pass

        # 3) Title/author query
        if not title:
            return None

        q_parts = [f"title:{title}"]
        if author:
            q_parts.append(f"author:{author}")
        q = " AND ".join(q_parts)

        url = f"https://openlibrary.org/search.json?q={quote(q)}&limit=1&fields={FIELDS}"
        raw = _http_get(url)
        if not raw:
            return None

        try:
            data = json.loads(raw.decode("utf-8", "replace"))
            docs = data.get("docs") or []
            return docs[0] if docs else None
        except Exception:
            return None

    # =========================
    # Sync (FAST + ONLY missing cover/genre)
    # =========================
    def sync_missing_data(
            self,
            books: list[dict],
            progress_cb: Callable[[int, int, str], Any] | None = None,
            stop_flag: Callable[[], bool] | None = None,
            polite_delay: float = 0.03,
            max_workers: int = 8,
    ) -> dict:
        """ONLY fills missing COVER and/or GENRE/SUBJECT.
           Parallel network work.
           Thread-safe catalog/cover writes.
           Does NOT call save() (GUI decides when to persist)."""
        total = len(books)
        books.sort(key=lambda b: 0 if (b.get("isbn") or "").strip() else 1)

        if progress_cb:
            progress_cb(0, total, "Starting sync…")

        done = 0
        downloaded = 0
        skipped = 0
        failed = 0
        enriched = 0

        lock = threading.Lock()

        # cache docs within a run to avoid repeated OL searches
        doc_cache: dict[str, dict | None] = {}
        doc_cache_lock = threading.Lock()

        def _canon_isbn(isbn: str) -> str:
            return _only_digits(isbn) or isbn.replace("-", "").replace(" ", "")

        def _needs_cover_for(b: dict) -> bool:
            return self._needs_cover(b)

        def _needs_genre_for(b: dict) -> bool:
            return self._needs_genre(b)

        def _get_doc_cached(title: str, author: str, isbn: str) -> dict | None:
            key = f"ISBN:{_canon_isbn(isbn)}" if isbn else f"TA:{_norm(title)}|{_norm(author)}"
            with doc_cache_lock:
                if key in doc_cache:
                    return doc_cache[key]
            doc = self._ol_search_best(title=title, author=author, isbn=isbn)
            with doc_cache_lock:
                doc_cache[key] = doc
            return doc

        def _fetch_cover_by_isbn(isbn: str) -> bytes | None:
            digits = _canon_isbn(isbn)
            if not digits:
                return None
            for size in ("L", "M"):
                url = f"https://covers.openlibrary.org/b/isbn/{digits}-{size}.jpg"
                data = _http_get(url)
                if data and len(data) > 1500:
                    return data
            return None

        def _store_cover(book_id: str, isbn_hint: str, data: bytes) -> None:
            digits = _canon_isbn(isbn_hint)
            filename = f"{digits}.jpg" if digits else f"{book_id}.jpg"
            with lock:
                (self.covers_dir / filename).write_bytes(data)
                self.cover_index[book_id] = filename
                # cover fixed → remove from cover queue
                self.sync_queue.discard(book_id)

        def _process_one(b: dict) -> tuple[str, bool, bool, bool]:
            def _stop_now() -> bool:
                return bool(stop_flag and stop_flag())

            if _stop_now():
                return ("Stopped", False, False, False)

            bid = (b.get("book_id") or "").strip()
            title = (b.get("title") or "Untitled").strip()
            if not bid:
                return (f"Skipped (no book_id): {title}", False, False, False)

            needs_cover = _needs_cover_for(b)
            needs_genre = _needs_genre_for(b)

            if not needs_cover and not needs_genre:
                return (f"Skipped (complete): {title}", False, False, False)

            isbn = self.canonical_isbn(b)
            author = self._author_display(b)

            cover_ok = False
            did_enrich = False
            doc = None

            if _stop_now():
                return ("Stopped", False, False, False)

            # --- cover: try direct isbn (fast)
            if needs_cover and isbn:
                if _stop_now():
                    return ("Stopped", False, False, False)
                data = _fetch_cover_by_isbn(isbn)
                if data:
                    _store_cover(bid, isbn, data)
                    cover_ok = True

            # --- cover: if still missing, use doc to find cover_i / other isbns
            if needs_cover and not cover_ok:
                if _stop_now():
                    return ("Stopped", False, False, False)

                doc = _get_doc_cached(title=title, author=author, isbn="")

                if doc:
                    # 1) FAST PATH: try cover_i first (usually 1 request)
                    cover_i = doc.get("cover_i")
                    if cover_i:
                        url = f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg"
                        data = _http_get(url)
                        if data and len(data) > 1500:
                            if _stop_now():
                                return ("Stopped", False, False, False)
                            with lock:
                                filename = f"olid_{cover_i}.jpg"
                                (self.covers_dir / filename).write_bytes(data)
                                self.cover_index[bid] = filename
                                self.sync_queue.discard(bid)
                            cover_ok = True

                    # 2) SLOWER PATH: try a FEW isbn candidates only if cover_i failed
                    if not cover_ok:
                        isbns = doc.get("isbn") or []
                        if isinstance(isbns, list):
                            tried = 0
                            for cand in isbns:
                                if tried >= 3:
                                    break
                                d = _only_digits(str(cand))
                                if len(d) in (10, 13):
                                    tried += 1
                                    data = _fetch_cover_by_isbn(d)
                                    if data:
                                        _store_cover(bid, d, data)
                                        cover_ok = True
                                        break

            # --- genre: doc only if needed
            if needs_genre:
                if doc is None:
                    doc = _get_doc_cached(title=title, author=author, isbn=isbn)
                if doc:
                    with lock:
                        if self._apply_ol_enrichment(b, doc):
                            did_enrich = True
                        # genre fixed → remove from genre queue if now present
                        if not self._needs_genre(b):
                            self.genre_queue.discard(bid)

            if polite_delay:
                time.sleep(polite_delay)

            parts = []
            if needs_cover:
                parts.append("Downloaded cover" if cover_ok else "Cover missing")
            if needs_genre:
                parts.append("Genre enriched" if not self._needs_genre(b) else "Genre missing")
            msg = f"{' + '.join(parts)}: {title}"

            did_fail = (needs_cover and not cover_ok) or (needs_genre and doc is None)
            return (msg, cover_ok, did_enrich, did_fail)

        # run
        stopped_early = False
        ex = ThreadPoolExecutor(max_workers=max_workers)
        futures = [ex.submit(_process_one, b) for b in books]

        try:
            for fut in as_completed(futures):
                if stop_flag and stop_flag():
                    stopped_early = True
                    break

                msg, did_dl, did_enrich_flag, did_fail = fut.result()

                with lock:
                    done += 1
                    if did_dl:
                        downloaded += 1
                    elif msg.startswith("Skipped") or msg == "Stopped":
                        skipped += 1
                    if did_enrich_flag:
                        enriched += 1
                    if did_fail:
                        failed += 1

                if progress_cb:
                    progress_cb(done, total, msg)

        finally:
            if stopped_early:
                ex.shutdown(wait=False, cancel_futures=True)
            else:
                ex.shutdown(wait=True)

            # queues changed in-memory → persist the queue files (small + fast)
            self._save_sync_queue()
            self._save_genre_queue()
            return {
                "total": total,
                "downloaded": downloaded,
                "skipped": skipped,
                "failed": failed,
                "enriched": enriched,
            }

    # =========================
    # Small testing helper
    # =========================
    def test_genre_lookup(
        self,
        sample_size: int = 25,
        apply_and_save: bool = False,
        polite_delay: float = 0.15,
    ) -> dict:
        missing = [b for b in self.catalog.values() if self._needs_genre(b)]
        sample = missing[:sample_size]

        found_doc = 0
        got_subjects = 0
        enriched = 0
        failed = 0

        for b in sample:
            title = (b.get("title") or "").strip()
            isbn = self.canonical_isbn(b)
            doc = self._ol_search_best(title=title, author=self._author_display(b), isbn=isbn)

            if not doc:
                failed += 1
                continue

            found_doc += 1
            subj = self._subjects_to_string(doc)
            if subj:
                got_subjects += 1

            if apply_and_save:
                if self._apply_ol_enrichment(b, doc):
                    enriched += 1

            time.sleep(polite_delay)

        if apply_and_save:
            self.save()

        return {
            "tested": len(sample),
            "found_doc": found_doc,
            "got_subjects": got_subjects,
            "enriched": enriched,
            "failed": failed,
            "total_missing_genre_in_catalog": len(missing),
        }