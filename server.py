#!/usr/bin/env python3

from flask import Flask
from os import listdir
from classes import Quizz

app = Flask(__name__)
quizzes = []

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    for f in listdir():
        if f.endswith('.md'):
            q = Quizz(filename=f)
            quizzes.append(q)
    print(quizzes[0])
    app.run(threaded=True)
