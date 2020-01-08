import json
import random
from datetime import datetime

# package used for writing and reading python class json to txt files
# https://jsonpickle.github.io/
import jsonpickle
from flask import Flask, redirect, render_template, request

app = Flask('note_app')


# Comment model is used to create comment objects
class Comment:
    """docstring for Comment"""

    def __init__(self, movie, content, username):
        self.id = random.randint(0, 90000000000000000000)
        self.movie = movie
        self.content = content
        self.username = username
        self.date = str(datetime.now())

    def get_comments_count(id):
        comments = read_comment()
        comment_count = 0
        for comment in comments:
            if comment['movie'] == id:
                comment_count += 1
        return comment_count


class Answer:
    """docstring for Answer"""

    def __init__(self, comment, content, username):
        self.comment = comment
        self.content = content
        self.username = username
        self.date = str(datetime.now())


# Utils
# returns a json object containing all movie objects
def get_all_movies():
    with open('movies.txt') as json_file:
        data = json.load(json_file)
        return data


# returns a json object containing only specific movie using unique imbd id
def get_single_movie(imdbID):
    with open('movies.txt') as data:
        data_json = json.load(data)
        for movie in data_json:
            if movie['imdbID'] == imdbID:
                return movie


# returns a json object containing all the comments
def read_comment():
    with open('comment.txt') as outfile:
        data = json.loads(outfile.read())
        return data


# returns a json object containing all the answers
def read_answers():
    with open('answers.txt') as outfile:
        data = json.loads(outfile.read())
        return data


# gets an instance of Comment model as argument and writes it as json into txt file
def write_comment(comment):
    data = read_comment()
    with open('comment.txt', 'w') as outfile:
        json_comment = jsonpickle.encode(comment)
        json_comment = json.loads(json_comment)
        data.append(json_comment)
        data = json.dump(data, outfile)


# gets an instance of Answer model as argument and writes it as json into txt file
def write_answer(answer):
    data = read_answers()
    with open('answers.txt', 'w') as outfile:
        json_comment = jsonpickle.encode(answer)
        json_comment = json.loads(json_comment)
        data.append(json_comment)
        data = json.dump(data, outfile)


# Routes
@app.route('/detail/<id>', methods=['GET', 'POST'])
def detail(id):
    movie = get_single_movie(id)
    answers = read_answers()
    comments_json = read_comment()
    comments = []

    for item in comments_json:
        if item['movie'] == id:
            comments.append(item)
    # return 1 movie and all comments related to that movie. (Comment.movie is always the id of a specific movie)
    return render_template("detail.html", comments=comments, movie=movie, answers=answers)


@app.route('/add-answer/<id>', methods=['POST'])
def add_answer(id):
    if request.method == 'POST':
        username = request.form.get('username')
        print(username)
        answer = request.form.get('answer').strip()
        # prevent empty answers
        if len(answer) > 0:
            # prevent script tags
            if '<script' in answer:
                return render_template(
                    "index.html",
                    message='Script tag is not allowed in answer.<a href="/">Go back to Homepage</a>',
                )
            answer_comment = request.form.get('id')
            user_answer = Answer(answer_comment, answer, username)
            write_answer(user_answer)
            return redirect('/detail/' + id)
        else:
            return render_template(
                "index.html",
                message='Empty comments are not allowed. <a href="/">Go back to Homepage</a>',
            )


@app.route('/add-comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        username = request.form.get('username')
        comment = request.form.get('comment').strip()
        print(username)
        # prevent empty comments
        if len(comment) > 0:
            # prevent script tags
            if '<script' in comment:
                return render_template(
                    "index.html",
                    message='Script tag is not allowed in comment.<a href="/">Go back to Homepage</a>',
                )
            comment_movie = request.form.get('id')
            user_comment = Comment(comment_movie, comment, username)
            write_comment(user_comment)

            return redirect('/detail/' + comment_movie)
        else:
            return render_template(
                "index.html",
                message='Empty comments are not allowed. <a href="/">Go back to Homepage</a>',
            )


@app.route('/', methods=['GET', 'POST'])
def homepage():
    movies = get_all_movies()
    for movie in movies:
        # add number of comments for each movie displayed on the main page
        movie['comment_count'] = Comment.get_comments_count(movie['imdbID'])
    return render_template('index.html', movies=movies)
