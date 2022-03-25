#!/usr/bin/env python3

from flask import Flask, request
from os import listdir
from classes import Quizz
from datetime import datetime

app = Flask(__name__)
quizzes = []

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/quizz/<quizz_id>", methods=["GET"])
def quizz_view(quizz_id):
    return quizzes[int(quizz_id)].html()

@app.route("/quizz/<quizz_id>", methods=["POST"])
def quizz_post(quizz_id):
    name = request.form.get('name')
    if not name:
        return "Invalid Name"
    dt = datetime.now().strftime("%d_%m_%Y-%H:%M:%S")
    output_f = "answers/%s-%s.txt" %(name, dt)
    
    points = 0
    
    with open(output_f, "a+") as f:
        f.write('Student : %s\n' %name)
        for question in quizzes[int(quizz_id)].questions:
            f.write('----\n\n'+question.title+'\n')
            valid = True
            for answ_id, answer in enumerate(question.answers):
                if answer.get('is_right') and request.form.get(answer.get('title')) != 'on':
                    valid = False
                if not answer.get('is_right') and request.form.get(answer.get('title')) == 'on':
                    valid = False
                f.write(' - '+answer.get('title')+ ('[OK]' if valid else '[KO]') + '\n')
            if valid:
                points += 1
        f.write('\nGrade : '+str(points)+' / '+ str(len(quizzes[int(quizz_id)].questions)) + '\n')
    return "Vos réponses ont bien été prises en compte!"

if __name__ == "__main__":
    for f in listdir():
        if f.endswith('.md'):
            q = Quizz(filename=f)
            quizzes.append(q)
    app.run(threaded=True)
