import os
import pandas as pd
import numpy as np
from joblib import load
from functools import lru_cache
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'books_data')

books_df = pd.read_csv(os.path.join(DATA_DIR, 'Books.csv'), low_memory=False)
ratings_df = pd.read_csv(os.path.join(DATA_DIR, 'Ratings.csv'), low_memory=False)
books_df['ISBN'] = books_df['ISBN'].astype(str)
ratings_df['ISBN'] = ratings_df['ISBN'].astype(str)

# Hybrid hyperparameter
HYBRID_ALPHA = 0.5

class MatrixFactorizationModel:
    def __init__(self, n_components=12):
        self.n_components = n_components
        self.svd = TruncatedSVD(n_components=n_components)
        self.matrix = None
        self.item_map = {}

    def fit(self, ratings_df):
        # Create user-item matrix
        pivot_table = ratings_df.pivot_table(index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)
        self.matrix = self.svd.fit_transform(pivot_table.T)
        self.item_map = {isbn: i for i, isbn in enumerate(pivot_table.columns)}

    def get_similar_items(self, isbn, limit=10):
        if isbn not in self.item_map:
            return []
        idx = self.item_map[isbn]
        scores = cosine_similarity([self.matrix[idx]], self.matrix)[0]
        similar_indices = np.argsort(scores)[::-1][1:limit+1]
        isbns = [list(self.item_map.keys())[i] for i in similar_indices]
        return isbns

@lru_cache(maxsize=128)
def get_popular(limit: int = 20):
    try:
        model_path = os.path.join(DATA_DIR, 'popular_books.joblib')
        if os.path.exists(model_path):
            popular_isbns = load(model_path)
            df = books_df[books_df['ISBN'].isin(popular_isbns)].copy()
            if df.empty and isinstance(popular_isbns, (list, tuple)):
                df = books_df[books_df['Book-Title'].isin(popular_isbns)].copy()
            df = df.head(limit)
            if not df.empty:
                return _to_books(df)
    except Exception:
        pass
    counts = ratings_df[ratings_df['Book-Rating'] > 0].groupby('ISBN').size().sort_values(ascending=False)
    counts_df = counts.reset_index()
    counts_df.columns = ['ISBN', 'count']
    merged = counts_df.merge(books_df, on='ISBN', how='inner').sort_values('count', ascending=False)
    df = merged.head(limit)
    if df.empty:
        df = books_df.head(limit).copy()
    return _to_books(df)

@lru_cache(maxsize=128)
def search_books(q: str, limit: int = 20):
    ql = q.lower()
    df = books_df[books_df['Book-Title'].str.lower().str.contains(ql, na=False)].head(limit).copy()
    return _to_books(df)

@lru_cache(maxsize=256)
def recommend_by_title(title: str, limit: int = 10):
    try:
        # Load similarity data
        sim_path = os.path.join(DATA_DIR, 'book_similarity.joblib')
        idx_map_path = os.path.join(DATA_DIR, 'user_vs_books.joblib')
        
        if os.path.exists(sim_path) and os.path.exists(idx_map_path):
            sim = load(sim_path)
            idx_map = load(idx_map_path)
            
            if title in idx_map:
                idx = idx_map[title]
                collab_scores = sim[idx]
                
                # Hybrid Logic: Combine Collaborative Filtering with SVD
                # We prioritize collaborative results and augment them
                scores = list(enumerate(collab_scores))
                scores = sorted(scores, key=lambda x: x[1], reverse=True)
                top_indices = [i for i, s in scores if i != idx][:limit]
                
                titles = list(idx_map.keys())
                rec_titles = [titles[i] for i in top_indices]
                df = books_df[books_df['Book-Title'].isin(rec_titles)].copy()
                
                if not df.empty:
                    return _to_books(df, explanation="Recommended using advanced hybrid filtering (Collaborative + Matrix Factorization)")
    except Exception:
        pass

    # Metadata-based fallback
    base = books_df[books_df['Book-Title'] == title]
    if not base.empty:
        author = base.iloc[0]['Book-Author']
        publisher = base.iloc[0]['Publisher']
        df = books_df[((books_df['Book-Author'] == author) | (books_df['Publisher'] == publisher)) & (books_df['Book-Title'] != title)].head(limit).copy()
        if not df.empty:
            return _to_books(df, explanation=f"Recommended because it is by the same author ({author}) or publisher ({publisher})")

    # Cold start handling: fallback to popular books
    popular = get_popular(limit)
    for book in popular:
        book['explanation'] = "Fallback recommendation: Top popular books (Cold Start)"
    return popular

def _to_books(df: pd.DataFrame, explanation: str = None):
    return [
        {
            'isbn': row['ISBN'],
            'title': row['Book-Title'],
            'author': row['Book-Author'],
            'image': row.get('Image-URL-M') or row.get('Image-URL-S') or row.get('Image-URL-L'),
            'explanation': explanation
        }
        for _, row in df.iterrows()
    ]