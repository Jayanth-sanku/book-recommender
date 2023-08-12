from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

popularity_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
                           book_name = list(popularity_df['Book-Title'].values),
                           author = list(popularity_df['Book-Author'].values),
                           image = list(popularity_df['Image-URL-M'].values),
                           votes = list(popularity_df['num_ratings'].values),
                           rating = list(popularity_df['avg_ratings'].values),
                           )
    
    
@app.route('/recommend_books', methods = ["POST"])
def recommend_book():
    
    user_input = request.form.get('user_input')
    
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1], reverse=True)[1:6]
    data= []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
        
    return render_template('recommendation.html',data= data)


        
    
    
@app.route('/recommend')
def recommend():
    return render_template('recommendation.html', 
                           book_name = list(popularity_df['Book-Title'].values),
                           author = list(popularity_df['Book-Author'].values),
                           image = list(popularity_df['Image-URL-M'].values),
                           votes = list(popularity_df['num_ratings'].values),
                           rating = list(popularity_df['avg_ratings'].values),
                           )
if __name__ == '__main__':
    app.run(debug=True)