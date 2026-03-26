import os
import pandas as pd
from joblib import load

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'books_data')

books_df = pd.read_csv(os.path.join(DATA_DIR, 'Books.csv'), low_memory=False)
ratings_df = pd.read_csv(os.path.join(DATA_DIR, 'Ratings.csv'), low_memory=False)
books_df['ISBN'] = books_df['ISBN'].astype(str)
ratings_df['ISBN'] = ratings_df['ISBN'].astype(str)

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

def search_books(q: str, limit: int = 20):
    ql = q.lower()
    df = books_df[books_df['Book-Title'].str.lower().str.contains(ql, na=False)].head(limit).copy()
    return _to_books(df)

def recommend_by_title(title: str, limit: int = 10):
    try:
        sim_path = os.path.join(DATA_DIR, 'book_similarity.joblib')
        if os.path.exists(sim_path):
            sim = load(sim_path)
            idx_map_path = os.path.join(DATA_DIR, 'user_vs_books.joblib')
            if os.path.exists(idx_map_path):
                idx_map = load(idx_map_path)
                if title in idx_map:
                    idx = idx_map[title]
                    scores = list(enumerate(sim[idx]))
                    scores = sorted(scores, key=lambda x: x[1], reverse=True)
                    scores = [i for i, s in scores if i != idx][:limit]
                    titles = list(idx_map.keys())
                    rec_titles = [titles[i] for i in scores]
                    df = books_df[books_df['Book-Title'].isin(rec_titles)].copy()
                    return _to_books(df)
    except Exception:
        pass
    base = books_df[books_df['Book-Title'] == title]
    if base.empty:
        return []
    author = base.iloc[0]['Book-Author']
    publisher = base.iloc[0]['Publisher']
    df = books_df[((books_df['Book-Author'] == author) | (books_df['Publisher'] == publisher)) & (books_df['Book-Title'] != title)].head(limit).copy()
    return _to_books(df)

def _to_books(df: pd.DataFrame):
    return [
        {
            'isbn': row['ISBN'],
            'title': row['Book-Title'],
            'author': row['Book-Author'],
            'image': row.get('Image-URL-M') or row.get('Image-URL-S') or row.get('Image-URL-L')
        }
        for _, row in df.iterrows()
    ]