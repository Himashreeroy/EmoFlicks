from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup as Soup
import re
import requests as HTTP

app = Flask(__name__)

# Dictionary mapping emotions to movie genres
emotions_to_genres = {
    "Sad": "drama",
    "Disgust": "musical",
    "Anger": "action",
    "Surprise": "adventure",
    "Fear": "horror",
    "Happy": "comedy",
    # Add more emotions and their corresponding genres here
}

# Function to recommend movies based on emotion
def recommend_movies(emotion):
    genre = emotions_to_genres.get(emotion)
    if genre:
        url = f'http://www.imdb.com/search/title?genres={genre}&title_type=feature&sort=moviemeter,asc'
        response = HTTP.get(url)
        soup = Soup(response.text, "lxml")
        movie_links = soup.find_all("a", attrs={"href": re.compile(r'\/title\/tt+\d*\/')})
        count = 0
        recommendations = []

        for link in movie_links:
            movie_name = link.text.strip()
            recommendations.append(movie_name)
            count += 1
            if count > 10:  # Limit to 10 movie recommendations
                break

        return recommendations
    else:
        return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    emotion = data.get('emotion')
    print("Received emotion:", emotion)  # Add this line for debugging
    recommendations = recommend_movies(emotion)
    print("Recommendations:", recommendations)  # Add this line for debugging
    if recommendations:
        return jsonify({'recommendations': recommendations})
    else:
        return jsonify({'error': 'Invalid emotion'}), 400

if __name__ == '__main__':
    app.run(debug=True)



    