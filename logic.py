import numpy as np
import pandas as pd
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read the dataset
df = pd.read_csv("udemy_course_data.csv")

# Clean the course titles
df['Clean_title'] = df['course_title'].apply(nfx.remove_stopwords)
df['Clean_title'] = df['Clean_title'].apply(nfx.remove_special_characters)

# Calculate the cosine similarity matrix
countvect = CountVectorizer()
cvmat = countvect.fit_transform(df['Clean_title'])
cos_sim = cosine_similarity(cvmat)

# Function to recommend courses
def recommend_courses(query, dataset):
    if not query.strip():
        return pd.DataFrame(columns=['course_title', 'content_duration', 'price', 'url'])

    df = dataset.copy()
    df['Clean_title'] = df['course_title'].apply(nfx.remove_stopwords)
    df['Clean_title'] = df['Clean_title'].apply(nfx.remove_special_characters)

    countvect = CountVectorizer()
    cvmat = countvect.fit_transform(df['Clean_title'])
    cos_sim = cosine_similarity(cvmat)

    try:
        query_idx = df[df['course_title'].str.lower().str.contains(query.lower())].index[0]
    except IndexError:
        return pd.DataFrame(columns=['course_title', 'content_duration', 'price', 'url'])  # If query not found, return empty DataFrame

    scores = list(enumerate(cos_sim[query_idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_n = 10   
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    
    recommendations = df.loc[top_indices, ['course_title', 'content_duration', 'price', 'url']]

    return recommendations

# Example usage
query = "How To Maximize Your Profits Trading Options"
recommended_courses = recommend_courses(query, df)

# Display the recommendations in a tabular format
if not recommended_courses.empty:
    print(recommended_courses.to_string(index=False))
else:
    print("No recommendations found.")
