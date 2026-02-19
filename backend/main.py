from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from scipy.sparse import load_npz, vstack
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

# allow the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# load data into memory once at startup
movies_df = pd.read_csv("movies_db.csv")
tf_matrix = load_npz("tf_matrix.npz")

@app.get("/search")
def search(q: str):
    results = movies_df[movies_df['title'].str.contains(q, case=False)].head(10).copy()
    # we create display_name to make the dropdown options unique
    results['display_name'] = results['title'] + " (" + results['release_year'].astype(str) + ")"
    return results[['title', 'display_name']].to_dict(orient="records")

@app.post("/recommend")
def recommend(selected_display_names: list[str]):
    
    # create temporary df to match titles with dates appended
    temp_df = movies_df.copy()
    temp_df['display_name'] = temp_df['title'] + " (" + temp_df['release_year'].astype(str) + ")"
    
    indices = temp_df[temp_df['display_name'].isin(selected_display_names)].index.tolist()
    if not indices: return []

    user_vector = np.asarray(tf_matrix[indices].mean(axis=0))
    scores = cosine_similarity(user_vector, tf_matrix).flatten()
    best_matches = scores.argsort()[::-1]

    recs = []
    for idx in best_matches:
        movie = movies_df.iloc[idx]
        # check against title or display_name to avoid recommending what they picked
        if movie['title'] not in [name.split(" (")[0] for name in selected_display_names]:
            recs.append(movie.to_dict())
        if len(recs) >= 10: break
    return recs