"Step-1 Install Required Libraries"
pip install pandas scikit-learn surprise
"Step 2: Load the Dataset"
import pandas as pd

# Load dataset
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Preview the datasets
print(movies.head())
print(ratings.head())
"Step 3: Content-Based Filtering"

"1. Preprocess the Movie Dataset"
# Merge ratings with movie titles
df = pd.merge(ratings, movies, on='movieId')

# Extract genres as features
df['genres'] = df['genres'].str.split('|')
df['genres'] = df['genres'].apply(lambda x: ' '.join(x))

# Vectorize the genres using TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['genres'])

# Preview the shape of the TF-IDF matrix
print(tfidf_matrix.shape)
"2. Calculate Similarity Between Movies"
from sklearn.metrics.pairwise import cosine_similarity

# Compute cosine similarity between all movies
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get movie recommendations
def get_content_based_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie
    idx = df[df['title'] == title].index[0]

    # Get pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort by similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get top 10 similar movies
    sim_scores = sim_scores[1:11]
    
    # Get the indices of these movies
    movie_indices = [i[0] for i in sim_scores]

    # Return the titles of the most similar movies
    return df['title'].iloc[movie_indices]

# Example usage
print(get_content_based_recommendations('Toy Story (1995)'))
"Step 4: Collaborative Filtering"
"1. Set Up the Dataset in Surprise"
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic

# Load data into Surprise format
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Split into training and testing sets
trainset, testset = train_test_split(data, test_size=0.2)
"2. Train a Collaborative Filtering Model (User-Based)"
# Use KNN for collaborative filtering
algo = KNNBasic(sim_options={'name': 'cosine', 'user_based': True})

# Train the algorithm on the trainset
algo.fit(trainset)

# Test the algorithm on the testset
predictions = algo.test(testset)

# Example: Get top N movie recommendations for a user
from collections import defaultdict

def get_top_n_recommendations(predictions, n=10):
    # Map the predictions to each user
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Sort the predictions for each user and retrieve the top N
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

top_n = get_top_n_recommendations(predictions, n=10)

# Example: Get recommendations for a user (e.g., user 1)
user_id = 1
recommended_movie_ids = [iid for iid, _ in top_n[user_id]]
recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]
print(recommended_movies[['movieId', 'title']])
