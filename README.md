# Hybrid-Lens: Advanced Multi-Stage Book Recommendation System

An end-to-end, production-ready recommendation engine that leverages hybrid filtering techniques, matrix factorization, and real-time explainability to deliver personalized book suggestions.

---

### 1. Overview
**Hybrid-Lens** is a sophisticated recommendation system designed to navigate the complexities of user preference discovery. By integrating collaborative filtering, content-based metadata matching, and latent factor models (SVD), the system provides high-precision recommendations while maintaining robustness through a multi-stage fallback architecture.

### 2. Problem Statement
In the era of information overload, users often struggle to find relevant content among millions of options. Traditional recommendation systems frequently suffer from:
- **Data Sparsity**: Limited interactions per user/item.
- **Cold Start**: Difficulty recommending new items or handling new users.
- **Lack of Transparency**: "Black-box" recommendations that reduce user trust.

### 3. Solution Approach
The system implements a **Multi-Stage Recommendation Pipeline**:
1.  **Primary Stage**: Memory-based Collaborative Filtering (User-Item similarity) combined with Latent Factor Modeling (SVD).
2.  **Fallback Stage**: Content-based filtering using book metadata (Author, Publisher) for items with limited interaction history.
3.  **Cold Start Stage**: Popularity-based filtering as a fail-safe to ensure 100% service availability even for new users.

### 4. Key Features
- **Hybrid Scoring Engine**: Combines collaborative and latent factor signals for improved accuracy.
- **Real-time Explainability**: Every recommendation includes a natural language justification (e.g., "Recommended using advanced hybrid filtering (Collaborative + Matrix Factorization)").
- **Automated Optimization**: Integrated **Optuna** for Bayesian hyperparameter tuning of hybrid weights.
- **High-Performance Architecture**: Multi-level caching (LRU) and asynchronous API handling for sub-100ms inference.
- **Production Monitoring**: Structured logging and FastAPI middleware for comprehensive request/error tracking.

### 5. Tech Stack
- **Languages**: Python 3.11+, JavaScript (ES6+)
- **ML Frameworks**: Scikit-Learn, NumPy, Pandas, Joblib
- **Optimization**: Optuna
- **Backend**: FastAPI, Uvicorn, Gunicorn
- **Database**: SQLite (User Auth)
- **Frontend**: HTML5, CSS3, Vanilla JS
- **DevOps**: Docker, Docker Compose, Nginx

### 6. System Architecture
1.  **Data Layer**: Kaggle Book-Crossing dataset processed into optimized sparse matrices and serialized models.
2.  **Logic Layer**: [recommender.py](backend/recommender.py) handles the multi-stage recommendation logic and model inference.
3.  **Evaluation Layer**: [evaluation.py](backend/evaluation.py) provides Precision@K and Recall@K metrics via automated testing.
4.  **API Layer**: [app.py](backend/app.py) provides RESTful endpoints with logging and CORS middleware.
5.  **Presentation Layer**: Responsive frontend communicating with the backend via dynamic API routing.

### 7. Dataset
Utilizes the **Book-Crossing Dataset** (Kaggle):
- **Users**: 278,858 users with anonymized IDs.
- **Books**: 271,360 books identified by ISBN.
- **Ratings**: 1,149,780 ratings (explicit/implicit) on a scale of 1-10.

### 8. Model Details
- **Collaborative Filtering**: Item-Item similarity computed via Cosine Similarity on user-rating vectors.
- **Matrix Factorization (SVD)**: Dimensionality reduction using `TruncatedSVD` to capture latent features and mitigate sparsity.
- **Hybrid Approach**: A weighted combination of similarity scores, dynamically balanced to optimize retrieval precision.
- **Content-Based Fallback**: Metadata matching on 'Book-Author' and 'Publisher' for the long-tail of items.

### 9. Evaluation Metrics
The system includes a dedicated evaluation suite ([evaluation.py](backend/evaluation.py)):
- **Precision@K**: Measures the relevance of the top-K recommended items.
- **Recall@K**: Measures the system's ability to capture all relevant items within the top-K.
- **Optuna Integration**: Automated searching for the optimal `alpha` (hybrid weight) to maximize Precision@K.

### 10. Explainability
To enhance user trust and transparency, the system provides real-time justifications for each recommendation:
- **Collaborative**: "Recommended using advanced hybrid filtering (Collaborative + Matrix Factorization)"
- **Content-Based**: "Recommended because it is by the same author ([Author]) or publisher ([Publisher])"
- **Popularity**: "Fallback recommendation: Top popular books (Cold Start)"

### 11. Challenges Faced
- **Matrix Sparsity**: Resolved by implementing SVD to densify the latent space and capture hidden relationships.
- **Cold Start**: Addressed via a tiered fallback mechanism (Metadata -> Popularity).
- **Scalability**: Optimized via `lru_cache` and vectorized `numpy`/`pandas` operations to handle large-scale inference requests.

### 12. Results / Performance
- **Average Precision@10**: ~0.0286 (on sparse testing set)
- **Optimized Alpha**: 0.7972 (Best weight for collaborative signals)
- **Inference Latency**: < 50ms with caching enabled.

### 13. Screenshots
![Home Page Placeholder](https://via.placeholder.com/800x400?text=Home+Page+UI+Carousel)
*Figure 1: Responsive UI featuring popular carousels and explainable recommendations.*

---

### 14. How to Run

#### Local Development
1. **Clone & Setup**:
   ```bash
   git clone https://github.com/Azad62000/book-recommendation-app.git
   cd book-recommendation-app
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. **Start Backend**:
   ```bash
   uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
   ```
3. **Run Evaluation**:
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   python3 -m backend.evaluation
   ```

#### Production (Docker)
```bash
docker compose up -d --build
```
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`

---

### 15. Project Structure
```text
├── backend/
│   ├── app.py             # FastAPI Server & Middleware
│   ├── recommender.py     # Hybrid Engine & MF Logic
│   ├── evaluation.py      # Metrics & Optuna Optimization
│   └── requirements.txt   # Dependencies
├── books_data/            # Raw Data & Serialized Models
├── home/, popular/        # Frontend Modules
└── docker-compose.yml     # Service Orchestration
```

### 16. Future Improvements
- **Deep Learning Integration**: Implementing Neural Collaborative Filtering (NCF) for non-linear user-item relationships.
- **Session-based Tracking**: Real-time tracking of user interactions for intra-session personalization.
- **Elasticsearch Integration**: For faster full-text search and hybrid retrieval at scale.
- **A/B Testing Framework**: Built-in support for comparing model versions in production.

---

**Summary**: Engineered a multi-stage hybrid recommendation system utilizing Collaborative Filtering and SVD, achieving optimized Precision@K via Bayesian hyperparameter tuning (Optuna) and providing real-time explainability for enhanced user trust.
