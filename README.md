# 🎬 Movie Recommendation System

A full-stack movie recommendation app built with **FastAPI** (backend) and **Streamlit** (frontend). It combines **TF-IDF content-based filtering** with **TMDB API** data to deliver movie suggestions, search, and browsing — all in a modern, responsive UI.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?logo=streamlit&logoColor=white)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Home Feed** | Browse trending, popular, top-rated, now playing, and upcoming movies |
| **Keyword Search** | Type a keyword → get dropdown suggestions + poster grid results |
| **Movie Details** | Cinematic backdrop, poster, genre pills, overview |
| **TF-IDF Recommendations** | Content-based similar movies using TF-IDF cosine similarity on local dataset |
| **Genre Recommendations** | TMDB-powered "More Like This" based on the movie's primary genre |
| **Responsive UI** | Modern dark theme with hover effects, gradient accents, and adaptive grid |

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌────────────┐
│   Streamlit UI  │ ──────▶ │  FastAPI Backend  │ ──────▶ │  TMDB API  │
│   (app.py)      │  HTTP   │  (main.py)        │  HTTP   │            │
└─────────────────┘         └──────────────────┘         └────────────┘
                                    │
                                    ▼
                            ┌──────────────┐
                            │ Pickle Files │
                            │ (TF-IDF Model)│
                            └──────────────┘
```

- **app.py** — Streamlit frontend (search, grid, details, routing)
- **main.py** — FastAPI backend (TMDB proxy, TF-IDF recommendations, genre discovery)
- **movies.ipynb** — Jupyter notebook for data preprocessing and model training
- **Pickle files** — Pre-trained TF-IDF model artifacts:
  - `df.pkl` — Processed movie DataFrame
  - `indices.pkl` — Title → index mapping
  - `tfidf_matrix.pkl` — Sparse TF-IDF feature matrix
  - `tfidf.pkl` — Fitted TF-IDF vectorizer

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free [TMDB API key](https://www.themoviedb.org/settings/api)

### 1. Clone the repository

```bash
git clone https://github.com/Vishal141014/movie-recommendation.git
cd movie-recommendation-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

### 4. Generate model files (if not present)

Run the Jupyter notebook to preprocess data and generate pickle files:

```bash
jupyter notebook movies.ipynb
```

This reads `movies_metadata.csv` and creates `df.pkl`, `indices.pkl`, `tfidf_matrix.pkl`, and `tfidf.pkl`.

### 5. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Visit `/docs` for the interactive Swagger UI.

### 6. Start the Streamlit frontend

In a **separate terminal**:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/home?category=popular&limit=24` | Home feed (trending, popular, top_rated, now_playing, upcoming) |
| `GET` | `/tmdb/search?query=batman` | TMDB keyword search (raw results) |
| `GET` | `/movie/id/{tmdb_id}` | Movie details by TMDB ID |
| `GET` | `/recommend/tfidf?title=Inception&top_n=10` | TF-IDF recommendations only |
| `GET` | `/recommend/genre?tmdb_id=27205&limit=18` | Genre-based recommendations |
| `GET` | `/movie/search?query=Inception` | Bundle: details + TF-IDF recs + genre recs |

---

## 🧠 How the Recommendation Engine Works

1. **Data Preprocessing** — Movie metadata is cleaned and combined into a single text feature (genres, keywords, cast, overview, etc.)
2. **TF-IDF Vectorization** — `sklearn.feature_extraction.text.TfidfVectorizer` converts text features into a sparse matrix
3. **Cosine Similarity** — For a given movie, the system computes similarity scores against all other movies using sparse matrix multiplication (`tfidf_matrix @ query_vector.T`)
4. **Ranking** — Results are sorted by descending similarity score, excluding the query movie itself
5. **TMDB Enrichment** — Each recommendation is enriched with poster, release date, and rating from the TMDB API

---

## 📁 Project Structure

```
Movie Recommendation System/
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend
├── movies.ipynb            # Data preprocessing & model training
├── movies_metadata.csv     # Raw movie dataset
├── requirements.txt        # Python dependencies
├── .env                    # TMDB API key (create manually)
├── df.pkl                  # Processed DataFrame
├── indices.pkl             # Title-to-index mapping
├── tfidf_matrix.pkl        # Sparse TF-IDF matrix
└── tfidf.pkl               # Fitted TF-IDF vectorizer
```

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit with custom CSS (dark theme, gradient accents, responsive grid)
- **Backend:** FastAPI with async HTTPX client
- **ML Model:** scikit-learn TF-IDF + cosine similarity
- **Data:** TMDB API + local CSV dataset
- **Serialization:** Pickle for model persistence

---

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TMDB_API_KEY` | Yes | Your TMDB API key |
| `API_BASE` | No | Backend URL (default: `http://127.0.0.1:8000`) |

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
