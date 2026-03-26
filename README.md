📚 Hybrid-Lens: Advanced Multi-Stage Book Recommendation System

An end-to-end, production-ready recommendation engine that leverages hybrid filtering techniques, matrix factorization (SVD), and real-time explainability to deliver personalized book discovery experiences.

### 🌐 Live Demo

[![Live App](https://img.shields.io/badge/Frontend-Live-green)](https://book-recommendation-app-2-a76d.onrender.com/)  
[![API Docs](https://img.shields.io/badge/API-Docs-blue)](https://book-recommendation-app-2-a76d.onrender.com/docs)

------------------------------------------------------------

### 1. Overview
**Hybrid-Lens** is a sophisticated recommendation system designed to bridge the gap between user interest and relevant literature. By integrating collaborative signals, content metadata, and latent factor models (SVD), the system provides high-precision recommendations while maintaining robust performance across various data sparsity scenarios.

------------------------------------------------------------

### 2. Problem Statement
In a library of millions of titles, users often face decision paralysis. Traditional recommendation systems struggle with:

- **Data Sparsity**: Limited interactions per user/item  
- **Cold Start**: Difficulty recommending new items or new users  
- **Transparency**: "Black-box" recommendations that reduce user trust  

------------------------------------------------------------

### 3. Solution Approach
The system implements a **Multi-Stage Recommendation Pipeline**:

- **Primary Layer**: Hybrid filtering combining memory-based Collaborative Filtering and Latent Factor Modeling (SVD).  
- **Fallback Layer**: Content-based filtering using metadata (Author, Publisher) for long-tail items.  
- **Baseline Layer**: Popularity-based recommendations for cold-start scenarios.  

Additionally:
- **Automated Optimization**: Integrated **Optuna** for Bayesian hyperparameter tuning of hybrid weights.
- **Explainability Engine**: Provides natural language justifications for every recommendation.

------------------------------------------------------------

### 4. Key Features
- **Hybrid Recommendation Engine**: Seamlessly blends collaborative and latent factor signals.
- **Advanced Model Evaluation**: Integrated suite for **Precision@K** and **Recall@K** metrics.
- **Real-time Explainability**: Contextual labels explaining "why" a book was recommended.
- **Production-Grade API**: FastAPI backend with structured logging, caching (LRU), and error middleware.
- **Containerized Architecture**: Fully orchestrated with Docker and Nginx.

------------------------------------------------------------

### 5. Tech Stack
- **Languages**: Python 3.11+, JavaScript (ES6+)
- **ML Frameworks**: Scikit-Learn, NumPy, Pandas, Joblib
- **Optimization**: Optuna
- **Backend**: FastAPI, Uvicorn, Gunicorn
- **DevOps**: Docker, Docker Compose, Nginx

------------------------------------------------------------

### 6. System Architecture
- **Data Layer**: Optimized ingestion of the Kaggle Book-Crossing dataset.
- **Inference Layer**: [recommender.py](backend/recommender.py) handles hybrid logic and multi-stage fallbacks.
- **Evaluation Layer**: [evaluation.py](backend/evaluation.py) provides metrics and optimization trials.
- **API Layer**: [app.py](backend/app.py) exposes RESTful endpoints with comprehensive logging.

------------------------------------------------------------

### 7. Dataset
**Book-Crossing Dataset (Kaggle)**:
- **Users**: 278,858 anonymized profiles.
- **Books**: 271,360 unique titles.
- **Ratings**: 1,149,780 interactions on a 1-10 scale.

------------------------------------------------------------

### 8. Model Details
- **Collaborative Filtering**: Cosine similarity computed on user-item interaction matrices.
- **Matrix Factorization**: **SVD** implementation via `TruncatedSVD` to capture latent features and mitigate sparsity.
- **Hybrid Approach**: 
  - Optimized weight balancing (alpha) between collaborative and content signals.
  - Multi-tier fallback strategy (Collaborative -> Metadata -> Popularity).

------------------------------------------------------------

### 9. Evaluation Metrics
The system features an automated evaluation suite:
- **Precision@K**: Measures the relevance of the top-K recommended items.
- **Recall@K**: Measures the ability to capture relevant items within the top-K.
- **Latency (P99)**: Sub-50ms inference time achieved via LRU caching.

------------------------------------------------------------

### 10. Explainability
Integrated natural language justifications for enhanced transparency:
- "Recommended using advanced hybrid filtering (Collaborative + Matrix Factorization)"
- "Recommended because it is by the same author ([Author]) or publisher ([Publisher])"
- "Fallback recommendation: Top popular books (Cold Start)"

------------------------------------------------------------

### 11. Challenges Faced
- **Matrix Sparsity**: Resolved using SVD to densify the latent space.
- **Cold Start**: Handled via metadata-based and popularity-based fallback layers.
- **Scalability**: Addressed through optimized vector operations and multi-level caching.

------------------------------------------------------------

### 12. Screenshots
![Home Page Placeholder](https://via.placeholder.com/800x400?text=Home+Page+UI+Carousel)
*Figure 1: Responsive UI featuring explainable recommendations and carousels.*

------------------------------------------------------------

### 13. How to Run

**Local Setup**:
1. Clone repository and setup environment:
   ```bash
   git clone https://github.com/Azad62000/book-recommendation-app.git
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Start Backend:
   ```bash
   uvicorn backend.app:app --reload --port 8000
   ```
3. Run Evaluation:
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   python3 -m backend.evaluation
   ```

**Docker**:
```bash
docker compose up --build
```

------------------------------------------------------------

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

------------------------------------------------------------

### 15. Future Improvements
- **Deep Learning**: Integration of Neural Collaborative Filtering (NCF).
- **Session-based Recs**: Real-time tracking of user clickstreams for intra-session personalization.
- **Search Optimization**: Implementing Elasticsearch for hybrid full-text and semantic retrieval.

------------------------------------------------------------

🚀 **Project Description**
Engineered a production-ready hybrid recommendation system utilizing Collaborative Filtering and SVD, achieving optimized Precision@K via Bayesian hyperparameter tuning (Optuna). Features a multi-stage fallback architecture for cold-start handling and real-time explainability, all containerized for scalable deployment.
