# 🎬 MovieMind: Vector-Based Recommendation Engine

**MovieMind** is a full-stack web application that leverages **Natural Language Processing (NLP)** and **Vector Space Modeling** to provide personalized movie recommendations. By analyzing movie metadata—including genres, keywords, directors, and cast—the engine identifies deep semantic relationships between films to suggest titles that align with a user's specific "Taste Profile."

## 🚀 Technical Stack

- **Frontend:** React 18, Mantine UI, Axios
- **Backend:** FastAPI (Python), Uvicorn
- **Data Science:** Pandas, Scikit-Learn (TF-IDF), SciPy (Sparse Matrices)
- **Build Tools:** Vite, PostCSS

## 🧠 System Architecture & Logic

### 1. The Vector Space Model
The core of the engine uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to transform raw movie metadata into a high-dimensional vector space. This allows the system to weight unique attributes (like a specific director or niche genre) more heavily than generic terms.

### 2. Centroid-Based Preference Calculation
When a user selects multiple movies, the backend calculates the **centroid (mean vector)** of those selections. This aggregate vector represents the user's "Taste Profile" in the vector space.

### 3. Cosine Similarity Engine
The system measures the "distance" between the User Profile vector and all 10,000+ movies in the database using **Cosine Similarity**. The movies with the highest similarity scores (closest proximity in space) are returned as recommendations.

### 4. Frontend Optimization
- **Debounced Search:** Implemented a 400ms delay on keystrokes to minimize API overhead and prevent network socket congestion.
- **Asynchronous State Management:** Utilized React Hooks (`useEffect`, `useState`) to manage live search results and recommendation fetching without UI blocking.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+


### 1. Backend Configuration
Navigate to the backend directory and install dependencies:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend Configuration
Navigate to the frontend directory and launch the development server:
```bash
cd frontend
npm install
npm run dev
```
## Future Plans

- Integrate TMDB poster paths for more expressive recommendation cards