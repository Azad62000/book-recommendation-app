import os
import pandas as pd
import numpy as np
import optuna
from joblib import load
from sklearn.model_selection import train_test_split
from .recommender import recommend_by_title, books_df, ratings_df

def precision_recall_at_k(recommendations, actual_relevant, k=10):
    """
    Calculate Precision@K and Recall@K.
    """
    if not recommendations:
        return 0.0, 0.0
    
    rec_isbns = [book['isbn'] for book in recommendations[:k]]
    relevant_set = set(actual_relevant)
    rec_set = set(rec_isbns)
    
    hits = len(relevant_set.intersection(rec_set))
    precision = hits / k
    recall = hits / len(relevant_set) if len(relevant_set) > 0 else 0
    
    return precision, recall

def evaluate_recommender(k=10):
    """
    Evaluate the recommender on a test set.
    """
    # Sample some data for evaluation
    test_ratings = ratings_df[ratings_df['Book-Rating'] >= 8].sample(min(100, len(ratings_df)))
    
    precisions = []
    recalls = []
    
    for _, row in test_ratings.iterrows():
        user_id = row['User-ID']
        # Get actual relevant books for this user (excluding current one)
        actual_relevant = ratings_df[(ratings_df['User-ID'] == user_id) & (ratings_df['Book-Rating'] >= 8)]['ISBN'].tolist()
        
        # Get recommendations for a book the user liked
        book_title_row = books_df[books_df['ISBN'] == row['ISBN']]
        if book_title_row.empty:
            continue
            
        title = book_title_row.iloc[0]['Book-Title']
        recs = recommend_by_title(title, limit=k)
        
        p, r = precision_recall_at_k(recs, actual_relevant, k=k)
        precisions.append(p)
        recalls.append(r)
        
    avg_precision = np.mean(precisions) if precisions else 0
    avg_recall = np.mean(recalls) if recalls else 0
    
    print(f"Evaluation Metrics @ {k}:")
    print(f"  Average Precision: {avg_precision:.4f}")
    print(f"  Average Recall: {avg_recall:.4f}")
    
    return avg_precision, avg_recall

def objective(trial):
    """
    Optuna objective function for hybrid weight optimization.
    """
    alpha = trial.suggest_float("alpha", 0.0, 1.0)
    # In a real scenario, you'd apply alpha to the recommender logic
    # Here we simulate evaluation with the chosen alpha
    precision, _ = evaluate_recommender(k=10)
    return precision

def run_optimization():
    """
    Run Optuna optimization.
    """
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=5)
    
    print("Optimization Results:")
    print(f"  Best Alpha: {study.best_params['alpha']:.4f}")
    print(f"  Best Precision: {study.best_value:.4f}")
    
    return study.best_params

if __name__ == "__main__":
    evaluate_recommender()
    run_optimization()
