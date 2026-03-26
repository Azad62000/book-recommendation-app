# 📚 Hybrid-Lens: Advanced Hybrid Book Recommendation System

An end-to-end, production-ready recommendation engine that leverages hybrid filtering techniques, matrix factorization (SVD), and natural language explainability to deliver personalized book discovery experiences.

---

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
- **Transparency**: Black-box recommendations reduce user trust  

------------------------------------------------------------

### 3. Solution Approach
The system implements a **Multi-Stage Recommendation Pipeline**:

- **Primary Layer**: Hybrid filtering combining collaborative filtering and matrix factorization (SVD)  
- **Fallback Layer**: Content-based filtering using metadata (Author, Publisher)  
- **Baseline Layer**: Popularity-based recommendations for cold-start scenarios  

Additionally:
- Automated hyperparameter optimization using Optuna  
- Personalized scoring using implicit feedback signals  
- Natural language explainability for recommendations  

------------------------------------------------------------

### 4. Key Features
- Hybrid recommendation system (Collaborative + SVD + Content-based)  
- Multi-stage fallback architecture  
- Evaluation pipeline with Precision@K and Recall@K  
- Hyperparameter optimization using Optuna  
- FastAPI backend with structured logging, middleware, and admin endpoints  
- LRU caching for high-performance inference (sub-50ms latency)  
- Docker-based containerized deployment  

------------------------------------------------------------

### 5. Tech Stack
- **Languages**: Python 3.11+, JavaScript (ES6+)  
- **ML Libraries**: Scikit-Learn, NumPy, Pandas, Joblib  
- **Optimization**: Optuna  
- **Backend**: FastAPI, Uvicorn, Gunicorn  
- **DevOps**: Docker, Docker Compose, Nginx  

------------------------------------------------------------

### 6. System Architecture
- **Data Layer**: Book-Crossing dataset ingestion  
- **Inference Layer**: recommender.py (hybrid logic + caching)  
- **Evaluation Layer**: evaluation.py (metrics + optimization)  
- **API Layer**: app.py (REST endpoints, logging, middleware)  
- **Frontend Layer**: UI interacting with backend  

------------------------------------------------------------

### 7. Dataset
**Book-Crossing Dataset (Kaggle)**:
- Users: 278,858  
- Books: 271,360  
- Ratings: 1,149,780  

------------------------------------------------------------

### 8. Model Details
- **Collaborative Filtering**: Cosine similarity on user-item matrix  
- **Matrix Factorization**: SVD (TruncatedSVD) for latent feature extraction  
- **Content-Based Filtering**: Metadata similarity (Author, Publisher)  
- **Hybrid Model**:
  - Weighted combination of CF + SVD + Content-based methods  
  - Optimized using Optuna  

------------------------------------------------------------

### 9. Evaluation Metrics
- Precision@K  
- Recall@K  
- Retrieval Coverage  
- Latency (P99)  

Example:
- Precision@10: ~0.7 (dataset dependent)

------------------------------------------------------------

### 10. Explainability
Integrated natural language justifications:
- "Recommended using hybrid filtering (Collaborative + SVD)"
- "Recommended because it is by the same author/publisher"
- "Fallback recommendation: Popular books (Cold Start)"

------------------------------------------------------------

### 11. Challenges Faced
- Matrix sparsity → resolved using SVD and hybrid modeling  
- Cold start → handled via metadata and popularity fallback  
- Scalability → optimized through caching and efficient vector operations  

------------------------------------------------------------

### 12. Screenshots
(Add your UI screenshots here)

------------------------------------------------------------

### 13. How to Run

Local Setup:
git clone https://github.com/Azad62000/book-recommendation-app.git  
python3 -m venv .venv && source .venv/bin/activate  
pip install -r backend/requirements.txt  

Run Backend:
uvicorn backend.app:app --reload --port 8000  

Run Evaluation:
export PYTHONPATH=$PYTHONPATH:.  
python3 -m backend.evaluation  

------------------------------------------------------------

Docker:
docker compose up --build  

------------------------------------------------------------

### 14. Project Structure

backend/
  app.py
  recommender.py
  evaluation.py
  requirements.txt

books_data/
frontend/
docker-compose.yml

------------------------------------------------------------

### 15. Future Improvements
- Deep learning recommenders (NCF)  
- Session-based personalization  
- Search optimization (Elasticsearch)  

------------------------------------------------------------

🚀 **Project Description**
Engineered a production-grade hybrid recommendation system combining collaborative filtering and SVD-based matrix factorization, optimized using Optuna and evaluated via Precision@K and Recall@K. Designed a multi-stage fallback architecture for cold-start handling and integrated natural language explainability. Deployed on Render with a FastAPI backend and Docker containerization, achieving sub-50ms latency.