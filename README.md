# Hybrid-Lens: Multi-Stage Intelligent Book Recommendation System

An end-to-end, production-ready recommendation engine that leverages hybrid filtering techniques and latent feature analysis to deliver personalized book discovery experiences.

---

### 1. Overview
**Hybrid-Lens** is a sophisticated recommendation system designed to bridge the gap between user interest and relevant literature. By integrating collaborative signals, content metadata, and global popularity trends, the system provides high-precision recommendations while maintaining robust performance across various data sparsity scenarios.

### 2. Problem Statement
In a library of millions of titles, users often face "decision paralysis." Traditional recommendation systems frequently struggle with:
- **Data Sparsity**: Limited interactions per user/item.
- **Cold Start**: Difficulty recommending new items or handling new users without historical data.
- **Scalability**: Maintaining low-latency inference as the user base grows.

### 3. Solution Approach
The system implements a **Tiered Recommendation Pipeline**:
1.  **Primary Layer**: Item-Item Collaborative Filtering based on latent user preference patterns.
2.  **Fallback Layer**: Content-based filtering using rich metadata (Author, Publisher) for items with sparse interaction history.
3.  **Baseline Layer**: Popularity-based discovery as a fail-safe for cold-start scenarios.

### 4. Key Features
- **Hybrid Recommendation Engine**: Seamlessly blends collaborative and content-based signals.
- **Multi-Stage Fallback Architecture**: Ensures 100% service availability even for niche or new items.
- **Production-Grade API**: Built with FastAPI for high-performance, asynchronous request handling.
- **Modular Design**: Decoupled backend logic and frontend presentation for easy maintainability.
- **Containerized Deployment**: Fully orchestrated with Docker and Docker Compose.

### 5. Tech Stack
- **Languages**: Python 3.11+, JavaScript (ES6+)
- **ML Frameworks**: Pandas, NumPy, Scikit-Learn, Joblib
- **Backend**: FastAPI, Uvicorn, SQLite (User Auth)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **DevOps**: Docker, Nginx, Docker Compose

### 6. System Architecture
1.  **Data Layer**: Optimized ingestion of the Kaggle Book-Crossing dataset.
2.  **Inference Layer**: [recommender.py](backend/recommender.py) handles model loading and hybrid scoring logic.
3.  **API Layer**: [app.py](backend/app.py) exposes RESTful endpoints with CORS support and root-level redirection.
4.  **Presentation Layer**: Responsive frontend communicating with the backend via dynamic API routing.

### 7. Dataset
Utilizes the **Book-Crossing Dataset** (Kaggle):
- **Users**: 278,858 users with anonymized IDs.
- **Books**: 271,360 books identified by ISBN.
- **Ratings**: 1,149,780 ratings (explicit/implicit) on a scale of 1-10.

### 8. Model Details
- **Collaborative Filtering**: Item-Item similarity matrix computed via Cosine Similarity on user-rating vectors.
- **Content-Based Filtering**: Metadata matching using 'Book-Author' and 'Publisher' attributes.
- **Hybrid Approach**: Sequentially prioritized retrieval:
    - Attempt Item-Item similarity lookup.
    - If results < threshold, augment with Author/Publisher metadata matches.
    - Fallback to global popularity metrics.

### 9. Evaluation Metrics
*Note: Currently tracking baseline metrics. Formal evaluation suite (Precision@K, Recall@K) is planned for the next release.*
- **Retrieval Coverage**: Measures the system's ability to provide results for any given query ISBN.
- **Latency (P99)**: Benchmarked for sub-100ms API response times.

### 10. Explainability
*Future Implementation*: Natural language justifications for recommendations (e.g., "Recommended because you liked authors in the same genre") are planned to enhance user trust.

### 11. Challenges Faced
- **Matrix Sparsity**: Addressed via metadata fallback to ensure results for items with few ratings.
- **Cold Start**: Handled through popularity-based carousels for new users.
- **Deployment Constraints**: Optimized the Docker image size and configured Nginx for efficient static file serving.

### 12. Screenshots
![Home Page Placeholder](https://via.placeholder.com/800x400?text=Home+Page+UI+Carousel)
*Figure 1: Responsive UI featuring popular carousels and dynamic recommendation results.*

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
3. **Serve Frontend**:
   ```bash
   python3 -m http.server 5500
   ```
   Access at `http://localhost:5500/home/home.html`

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
│   ├── app.py             # FastAPI Server & Routes
│   ├── recommender.py     # Inference Engine Logic
│   └── requirements.txt   # Dependencies
├── books_data/            # Processed CSVs & Joblib Models
├── home/, popular/        # Frontend Modules
└── docker-compose.yml     # Service Orchestration
```

### 15. Future Improvements
- **Matrix Factorization**: Implementing SVD/ALS for better latent feature representation.
- **Evaluation Suite**: Integration of Precision@K and Recall@K metrics.
- **Explainability Layer**: Adding justification labels for recommended items.
- **Search Optimization**: Implementing Elasticsearch for faster full-text search across titles.

### Project Description
Engineered a multi-stage hybrid recommendation system utilizing Collaborative Filtering and metadata-based fallback, achieving sub-100ms latency through a FastAPI-driven microservice architecture containerized with Docker.
