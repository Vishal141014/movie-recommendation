import os
import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = os.environ.get("API_BASE", "https://movie-recommendation-w2z0.onrender.com")
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (modern, responsive, beautiful)
# =============================
st.markdown(
    """
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

:root {
    --accent: #7c3aed;
    --accent-light: #a78bfa;
    --accent-glow: rgba(124,58,237,0.35);
    --pink: #ec4899;
    --bg-dark: #0b0b14;
    --bg-card: rgba(255,255,255,0.04);
    --border: rgba(255,255,255,0.07);
    --text-primary: #f1f5f9;
    --text-muted: rgba(255,255,255,0.5);
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* ── Animated background dots ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(2px 2px at 20% 30%, rgba(124,58,237,0.15), transparent),
        radial-gradient(2px 2px at 40% 70%, rgba(236,72,153,0.1), transparent),
        radial-gradient(2px 2px at 80% 40%, rgba(124,58,237,0.12), transparent),
        radial-gradient(2px 2px at 60% 80%, rgba(236,72,153,0.08), transparent);
    pointer-events: none;
    z-index: 0;
}

/* ── Hide Streamlit branding ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #131328 40%, #1a0d2e 100%);
    border-right: 1px solid rgba(124,58,237,0.15);
}
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e2d9f3;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(124,58,237,0.12);
}

/* ── Sidebar logo glow ── */
.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 1rem;
    position: relative;
}
.sidebar-logo .logo-icon {
    font-size: 3rem;
    display: block;
    filter: drop-shadow(0 0 20px rgba(124,58,237,0.5));
    animation: float 3s ease-in-out infinite;
}
.sidebar-logo .logo-text {
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 3px;
    background: linear-gradient(135deg, #a78bfa, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sidebar-label {
    color: rgba(255,255,255,0.35);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.sidebar-footer {
    text-align: center;
    padding: 0.6rem 0;
    font-size: 0.7rem;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.5px;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

/* ── Hero Header ── */
.hero-header {
    background: linear-gradient(135deg, #1e1145 0%, #1a1040 30%, #0f2847 70%, #0d1f3c 100%);
    border-radius: 22px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(124,58,237,0.2);
    box-shadow: 0 8px 40px rgba(124,58,237,0.12), inset 0 1px 0 rgba(255,255,255,0.05);
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -15%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(236,72,153,0.18) 0%, transparent 65%);
    border-radius: 50%;
    animation: pulse-glow 4s ease-in-out infinite;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 65%);
    border-radius: 50%;
    animation: pulse-glow 4s ease-in-out infinite reverse;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.6; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.08); }
}

.hero-header h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    position: relative;
    z-index: 1;
    background: linear-gradient(to right, #ffffff, #c4b5fd, #f9a8d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-header p {
    font-size: 1.02rem;
    color: rgba(255,255,255,0.55);
    margin: 0;
    position: relative;
    z-index: 1;
    font-weight: 300;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.2rem;
    position: relative;
    z-index: 1;
}
.hero-stat {
    display: flex;
    align-items: center;
    gap: 6px;
    color: rgba(255,255,255,0.45);
    font-size: 0.82rem;
    font-weight: 500;
}
.hero-stat .stat-icon {
    font-size: 1.1rem;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2rem 0 1.2rem 0;
}
.section-header h3 {
    margin: 0;
    font-weight: 700;
    font-size: 1.3rem;
    color: var(--text-primary);
}
.section-badge {
    background: linear-gradient(135deg, var(--accent), var(--pink));
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 2px 10px var(--accent-glow);
}

/* ── Movie Card ── */
.movie-card {
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    background: var(--bg-card);
    border: 1px solid var(--border);
    margin-bottom: 0.6rem;
}
.movie-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow:
        0 20px 40px rgba(0,0,0,0.3),
        0 0 30px var(--accent-glow);
    border-color: rgba(124,58,237,0.3);
}
.movie-card img {
    border-radius: 16px 16px 0 0;
    width: 100%;
}
.movie-card-body {
    padding: 10px 12px 14px;
    background: linear-gradient(180deg, transparent, rgba(124,58,237,0.03));
}
.movie-title {
    font-size: 0.85rem;
    font-weight: 600;
    line-height: 1.3rem;
    height: 2.6rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    color: var(--text-primary);
}

/* ── No-poster ── */
.no-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a1a30, #0f0f20);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    border-radius: 16px 16px 0 0;
    color: rgba(124,58,237,0.25);
    border-bottom: 1px solid var(--border);
}

/* ── Detail Card (glassmorphism) ── */
.detail-card {
    border: 1px solid rgba(124,58,237,0.15);
    border-radius: 20px;
    padding: 2rem;
    background: rgba(20,15,40,0.6);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05);
}
.detail-card h2 {
    font-weight: 800;
    font-size: 1.8rem;
    margin-bottom: 0.4rem;
    background: linear-gradient(to right, #ffffff, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Rating stars ── */
.star-rating {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(234,179,8,0.12);
    border: 1px solid rgba(234,179,8,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #fbbf24;
}
.star-rating .star { color: #fbbf24; }
.star-rating .star-empty { color: rgba(255,255,255,0.15); }

/* ── Meta Pills ── */
.meta-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 1rem 0;
}
.meta-pill {
    background: rgba(124,58,237,0.12);
    color: var(--accent-light);
    font-size: 0.78rem;
    font-weight: 500;
    padding: 6px 16px;
    border-radius: 24px;
    border: 1px solid rgba(124,58,237,0.18);
    transition: all 0.2s ease;
}
.meta-pill:hover {
    background: rgba(124,58,237,0.2);
    border-color: rgba(124,58,237,0.35);
    transform: translateY(-1px);
}
.meta-pill-pink {
    background: rgba(236,72,153,0.12);
    color: #f9a8d4;
    border: 1px solid rgba(236,72,153,0.18);
}

/* ── Overview ── */
.overview-text {
    font-size: 0.95rem;
    line-height: 1.75;
    color: rgba(255,255,255,0.65);
    padding: 1.2rem 0 0.5rem;
    font-weight: 300;
}
.overview-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.3);
    font-weight: 600;
    margin-top: 1rem;
}

/* ── Backdrop ── */
.backdrop-container {
    border-radius: 20px;
    overflow: hidden;
    margin: 1rem 0 1.5rem;
    box-shadow: 0 12px 50px rgba(0,0,0,0.4);
    position: relative;
    border: 1px solid var(--border);
}
.backdrop-container img {
    width: 100%;
    border-radius: 20px;
}
.backdrop-container::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40%;
    background: linear-gradient(transparent, rgba(11,11,20,0.8));
    pointer-events: none;
    border-radius: 0 0 20px 20px;
}

/* ── Search bar ── */
.stTextInput > div > div > input {
    border-radius: 14px !important;
    padding: 0.8rem 1.2rem !important;
    font-size: 1rem !important;
    font-family: 'Poppins', sans-serif !important;
    border: 2px solid rgba(124,58,237,0.25) !important;
    background: rgba(20,15,40,0.5) !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px var(--accent-glow), 0 4px 20px rgba(124,58,237,0.15) !important;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(255,255,255,0.3) !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    font-family: 'Poppins', sans-serif !important;
    padding: 0.4rem 1.1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid rgba(124,58,237,0.25) !important;
    background: rgba(124,58,237,0.08) !important;
    color: var(--accent-light) !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: rgba(124,58,237,0.2) !important;
    border-color: var(--accent) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px var(--accent-glow) !important;
    color: white !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Back button ── */
.back-btn button {
    background: linear-gradient(135deg, var(--accent), var(--pink)) !important;
    color: white !important;
    border: none !important;
    padding: 0.5rem 1.8rem !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px var(--accent-glow) !important;
}
.back-btn button:hover {
    box-shadow: 0 8px 30px var(--accent-glow) !important;
    transform: translateY(-2px) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    border-radius: 12px !important;
    border-color: rgba(124,58,237,0.2) !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--pink)) !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(124,58,237,0.08) !important;
    margin: 1.2rem 0 !important;
}

/* ── Poster images ── */
[data-testid="stImage"] img {
    border-radius: 14px;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
[data-testid="stImage"] img:hover {
    transform: scale(1.03);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

/* ── Detail poster ── */
.detail-poster [data-testid="stImage"] img {
    border-radius: 18px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 30px rgba(124,58,237,0.15);
}

/* ── Info/Warning/Error boxes ── */
.stAlert > div {
    border-radius: 12px !important;
    border-left: 4px solid var(--accent) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(124,58,237,0.3);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(124,58,237,0.5);
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: rgba(255,255,255,0.2);
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}
.app-footer a {
    color: var(--accent-light);
    text-decoration: none;
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
        "<div class='sidebar-logo'>"
        "<span class='logo-icon'>🎬</span>"
        "<span class='logo-text'>CINEVERSE</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    if st.button("🏠  Home", use_container_width=True):
        goto_home()

    st.markdown("")
    st.markdown("<p class='sidebar-label'>📌 Browse</p>", unsafe_allow_html=True)
    cat_icons = {
        "trending": "🔥 Trending",
        "popular": "⭐ Popular",
        "top_rated": "🏆 Top Rated",
        "now_playing": "🎬 Now Playing",
        "upcoming": "📅 Upcoming",
    }
    home_category = st.selectbox(
        "Category",
        list(cat_icons.keys()),
        index=0,
        format_func=lambda x: cat_icons[x],
        label_visibility="collapsed",
    )

    st.markdown("")
    st.markdown("<p class='sidebar-label'>🔲 Grid Size</p>", unsafe_allow_html=True)
    grid_cols = st.slider("Grid columns", 3, 8, 5, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(
        "<div class='sidebar-footer'>"
        "Powered by <strong>TMDB</strong> & <strong>TF-IDF</strong><br>"
        "Built with ❤️ using Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )

# =============================
# HEADER
# =============================
st.markdown(
    "<div class='hero-header'>"
    "<h1>🎬 CineVerse</h1>"
    "<p>Discover movies you'll love — powered by AI recommendations</p>"
    "<div class='hero-stats'>"
    "<span class='hero-stat'><span class='stat-icon'>🎬</span> 45,000+ Movies</span>"
    "<span class='hero-stat'><span class='stat-icon'>🧠</span> TF-IDF Engine</span>"
    "<span class='hero-stat'><span class='stat-icon'>🌍</span> TMDB Powered</span>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    st.markdown("<p style='color:rgba(255,255,255,0.4); font-size:0.8rem; margin-bottom:0.3rem;'>🔍 Search for a movie...</p>", unsafe_allow_html=True)
    typed = st.text_input(
        "Search", placeholder="Try: Inception, The Dark Knight, Avengers...",
        label_visibility="collapsed",
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
        vote_avg = data.get("vote_average")

        # Star rating
        if vote_avg and vote_avg > 0:
            full_stars = int(vote_avg / 2)
            empty_stars = 5 - full_stars
            stars_html = (
                "<span class='star'>★</span>" * full_stars
                + "<span class='star-empty'>★</span>" * empty_stars
            )
            st.markdown(
                f"<div class='star-rating'>{stars_html} {vote_avg:.1f}/10</div>",
                unsafe_allow_html=True,
            )

        # Metadata pills
        pills_html = "<div class='meta-pills'>"
        pills_html += f"<span class='meta-pill'>📅 {release}</span>"
        for i, g in enumerate(genre_list):
            cls = 'meta-pill-pink' if i % 2 else 'meta-pill'
            pills_html += f"<span class='{cls}'>{g['name']}</span>"
        pills_html += "</div>"
        st.markdown(pills_html, unsafe_allow_html=True)

        overview = data.get("overview") or "No overview available."
        st.markdown("<p class='overview-label'>Overview</p>", unsafe_allow_html=True)
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

    # Footer
    st.markdown(
        "<div class='app-footer'>"
        "Made with ❤️ by CineVerse • Powered by TMDB & TF-IDF"
        "</div>",
        unsafe_allow_html=True,
    )