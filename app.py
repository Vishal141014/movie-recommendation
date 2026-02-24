import os
import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8000")
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (modern, responsive, beautiful)
# =============================
st.markdown(
    """
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e0e0ff;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08);
}

/* ── Hero header ── */
.hero-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 18px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(228,73,225,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
    color: #ffffff;
    position: relative;
}
.hero-header p {
    font-size: 1rem;
    color: rgba(255,255,255,0.65);
    margin: 0;
    position: relative;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.8rem 0 1rem 0;
}
.section-header h3 {
    margin: 0;
    font-weight: 600;
    font-size: 1.25rem;
}
.section-badge {
    background: linear-gradient(135deg, #e44de1, #6c63ff);
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Movie card ── */
.movie-card {
    border-radius: 14px;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    cursor: pointer;
    position: relative;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0.5rem;
}
.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.25);
}
.movie-card img {
    border-radius: 14px 14px 0 0;
    width: 100%;
}
.movie-card-body {
    padding: 10px 12px 12px;
}
.movie-title {
    font-size: 0.88rem;
    font-weight: 600;
    line-height: 1.25rem;
    height: 2.5rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    color: inherit;
}

/* ── No-poster placeholder ── */
.no-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #2a2a3d, #1a1a2e);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    border-radius: 14px 14px 0 0;
    color: rgba(255,255,255,0.2);
}

/* ── Detail card ── */
.detail-card {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.5rem;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
}
.detail-card h2 {
    font-weight: 700;
    margin-bottom: 0.3rem;
}

/* ── Metadata pills ── */
.meta-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 0.8rem 0;
}
.meta-pill {
    background: rgba(108,99,255,0.15);
    color: #a5a0ff;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 5px 14px;
    border-radius: 20px;
    border: 1px solid rgba(108,99,255,0.2);
}

/* ── Overview block ── */
.overview-text {
    font-size: 0.95rem;
    line-height: 1.65;
    color: rgba(255,255,255,0.72);
    padding: 1rem 0 0.5rem;
}

/* ── Backdrop ── */
.backdrop-container {
    border-radius: 16px;
    overflow: hidden;
    margin: 1.2rem 0;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.backdrop-container img {
    width: 100%;
    border-radius: 16px;
}

/* ── Muted text ── */
.small-muted {
    color: rgba(255,255,255,0.45);
    font-size: 0.88rem;
}

/* ── Search bar ── */
.stTextInput > div > div > input {
    border-radius: 12px !important;
    padding: 0.7rem 1rem !important;
    font-size: 1rem !important;
    border: 2px solid rgba(108,99,255,0.3) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.35rem 1rem !important;
    transition: all 0.2s ease !important;
    border: 1px solid rgba(108,99,255,0.3) !important;
    background: rgba(108,99,255,0.1) !important;
    color: #a5a0ff !important;
}
.stButton > button:hover {
    background: rgba(108,99,255,0.25) !important;
    border-color: #6c63ff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(108,99,255,0.2) !important;
}

/* ── Back button special ── */
.back-btn button {
    background: linear-gradient(135deg, #6c63ff, #e44de1) !important;
    color: white !important;
    border: none !important;
    padding: 0.45rem 1.5rem !important;
    font-size: 0.9rem !important;
}
.back-btn button:hover {
    opacity: 0.9 !important;
    box-shadow: 0 6px 20px rgba(108,99,255,0.35) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    border-radius: 10px !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 1.2rem 0 !important;
}

/* ── Responsive poster images ── */
[data-testid="stImage"] img {
    border-radius: 14px;
    transition: transform 0.25s ease;
}
[data-testid="stImage"] img:hover {
    transform: scale(1.03);
}

/* ── Detail poster specific ── */
.detail-poster img,
.detail-poster [data-testid="stImage"] img {
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.markdown(
                        "<div class='no-poster'>🎬</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown("<div class='movie-card-body'>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='movie-title'>{title}</div>",
                    unsafe_allow_html=True,
                )
                if st.button("🎬 View", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)
                st.markdown("</div></div>", unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR (clean)
# =============================
with st.sidebar:
    st.markdown(
        "<div style='text-align:center; padding: 1rem 0 0.5rem;'>"
        "<span style='font-size:2.4rem;'>🎬</span><br>"
        "<span style='font-size:1.1rem; font-weight:700; color:#e0e0ff; letter-spacing:1px;'>MOVIE REC</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    if st.button("🏠  Home", use_container_width=True):
        goto_home()

    st.markdown("")
    st.markdown("<p style='color:rgba(255,255,255,0.4); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.3rem;'>Browse</p>", unsafe_allow_html=True)
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("")
    st.markdown("<p style='color:rgba(255,255,255,0.4); font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.3rem;'>Grid Size</p>", unsafe_allow_html=True)
    grid_cols = st.slider("Grid columns", 3, 8, 5, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; padding:0.5rem 0;'>"
        "<span style='color:rgba(255,255,255,0.25); font-size:0.75rem;'>Powered by TMDB & TF-IDF</span>"
        "</div>",
        unsafe_allow_html=True,
    )

# =============================
# HEADER
# =============================
st.markdown(
    "<div class='hero-header'>"
    "<h1>🎬 Movie Recommender</h1>"
    "<p>Search any movie, explore details, and discover personalized recommendations</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "Search by movie title (keyword)", placeholder="Type: avenger, batman, love..."
    )

    st.divider()

    # SEARCH MODE (Autocomplete + word-match results)
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Dropdown
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "-- Select a movie --":
                        # map label -> id
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown(
                    "<div class='section-header'>"
                    "<h3>🔍 Results</h3>"
                    "<span class='section-badge'>Search</span>"
                    "</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    cat_label = home_category.replace('_', ' ').title()
    st.markdown(
        f"<div class='section-header'>"
        f"<h3>🏠 {cat_label}</h3>"
        f"<span class='section-badge'>Home Feed</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Top bar
    _, back_col = st.columns([4, 1])
    with back_col:
        st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
        if st.button("← Back to Home", use_container_width=True):
            goto_home()
        st.markdown("</div>", unsafe_allow_html=True)

    # Details (your FastAPI safe route)
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Backdrop as hero
    if data.get("backdrop_url"):
        st.markdown("<div class='backdrop-container'>", unsafe_allow_html=True)
        st.image(data["backdrop_url"], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.5], gap="large")

    with left:
        st.markdown("<div class='detail-poster'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.markdown(
                "<div class='no-poster' style='height:400px;'>🎬</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
        title_text = data.get('title', '')
        st.markdown(f"<h2>{title_text}</h2>", unsafe_allow_html=True)

        release = data.get("release_date") or "-"
        genre_list = data.get("genres", [])

        # Metadata pills
        pills_html = "<div class='meta-pills'>"
        pills_html += f"<span class='meta-pill'>📅 {release}</span>"
        for g in genre_list:
            pills_html += f"<span class='meta-pill'>{g['name']}</span>"
        pills_html += "</div>"
        st.markdown(pills_html, unsafe_allow_html=True)

        overview = data.get("overview") or "No overview available."
        st.markdown(
            f"<div class='overview-text'>{overview}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    st.markdown(
        "<div class='section-header'>"
        "<h3>✅ Recommendations</h3>"
        "<span class='section-badge'>For You</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Recommendations (TF-IDF + Genre) via your bundle endpoint
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            st.markdown(
                "<div class='section-header'>"
                "<h3>🔎 Similar Movies</h3>"
                "<span class='section-badge'>TF-IDF</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown(
                "<div class='section-header'>"
                "<h3>🎭 More Like This</h3>"
                "<span class='section-badge'>Genre</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")