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
1.  **Primary Stage**: Memory-based Collaborative Filtering (User-Item similarity) and Latent Factor Modeling (SVD).
2.  **Fallback Stage**: Content-based filtering using book metadata (Author, Publisher) for items with limited interaction history.
3.  **Cold Start Stage**: Popularity-based filtering as a fail-safe to ensure 100% service availability.

### 4. Key Features
- **Hybrid Scoring**: Combines collaborative and latent factor signals for improved accuracy.
- **Real-time Explainability**: Every recommendation includes a natural language justification (e.g., "Recommended because users with similar preferences liked this book").
- **Automated Optimization**: Integrated **Optuna** for hyperparameter tuning (hybrid weights).
- **Performance Optimized**: Multi-level caching (LRU) and asynchronous API handling.
- **Production Monitoring**: Structured logging and middleware for request/error tracking.

### 5. Tech Stack
- **Languages**: Python 3.11+, JavaScript (ES6+)
- **ML Frameworks**: Scikit-Learn, NumPy, Pandas, Joblib
- **Optimization**: Optuna
- **Backend**: FastAPI, Uvicorn, Gunicorn
- **Database**: SQLite (User Auth)
- **Frontend**: HTML5, CSS3, Vanilla JS
- **DevOps**: Docker, Docker Compose, Render

### 6. System Architecture
1.  **Data Layer**: Kaggle Book-Crossing dataset processed into optimized sparse matrices and serialized models.
2.  **Logic Layer**: [recommender.py](backend/recommender.py) handles the multi-stage recommendation logic.
3.  **API Layer**: [app.py](backend/app.py) provides RESTful endpoints with logging and CORS middleware.
4.  **Presentation Layer**: Responsive frontend communicating with the backend via dynamic API routing.

### 7. Dataset
Utilizes the **Book-Crossing Dataset** (Kaggle):
- **Users**: 278,858 users with anonymized IDs.
- **Books**: 271,360 books identified by ISBN.
- **Ratings**: 1,149,780 ratings (explicit/implicit) on a scale of 1-10.

### 8. Model Details
- **Collaborative Filtering**: Item-Item similarity computed via Cosine Similarity on user-rating vectors.
- **Matrix Factorization (SVD)**: Dimensionality reduction using `TruncatedSVD` to capture latent features and mitigate sparsity.
- **Hybrid Weighting**: A weighted combination of similarity scores, optimized via Bayesian optimization.
- **Content-Based Fallback**: Metadata matching on 'Book-Author' and 'Publisher' for the long-tail of items.

### 9. Evaluation Metrics
The system includes a dedicated evaluation suite ([evaluation.py](backend/evaluation.py)):
- **Precision@K**: Measures the relevance of the top-K recommended items.
- **Recall@K**: Measures the system's ability to capture all relevant items within the top-K.
- **Optuna Integration**: Automated searching for the optimal `alpha` (hybrid weight) to maximize Precision@K.

### 10. Explainability & Cold Start
- **Explainability**: The API response includes an `explanation` field for each book, enhancing user engagement and transparency.
- **Cold Start Handling**: Automatic transition to popularity-based results when interaction data is insufficient, preventing empty result sets.

### 11. Challenges Faced
- **Matrix Sparsity**: Resolved by implementing SVD to densify the latent space.
- **Scalability**: Addressed via `lru_cache` and optimized `pandas` operations for real-time inference.
- **Deployment Constraints**: Optimized the Docker image size and configured Gunicorn with Uvicorn workers for production stability.

### 12. Screenshots
![Home Page Placeholder](https://via.placeholder.com/800x400?text=Home+Page+UI)
*Figure 1: Responsive UI featuring popular carousels and explainable recommendations.*

---

### 13. How to Run

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

### 14. Project Structure
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

### 15. Future Improvements
- **Deep Learning**: Integration of Neural Collaborative Filtering (NCF).
- **Session-based Recs**: Real-time tracking of user clickstreams for intra-session personalization.
- **A/B Testing Framework**: Built-in support for comparing different model versions in production.

---

### 🚀 Deployment
This app is deployed on Render:  
🔗 **[Live App](https://book-recommendation-app-2-a76d.onrender.com)**

### Resume-Ready Description
*Engineered a multi-stage hybrid recommendation system utilizing Collaborative Filtering and SVD, achieving optimized Precision@K via Bayesian hyperparameter tuning (Optuna) and providing real-time explainability for enhanced user trust.*
