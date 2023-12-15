#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect
from os import listdir
from classes import Quizz
from datetime import datetime
from auth import token_required, token_optional
from sqlmodel import Session, create_engine, select, SQLModel
from quizzes.model import CompletedQuizz
import json

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

engine = create_engine("sqlite:///quizzes.db")
SQLModel.metadata.create_all(engine)

quizzes_templates = json.load(open("quizzes/templates.json"))
quizzes = {}


@app.route("/")
@token_optional
def index(user):
    print(user)
    if user is None:
        return app.send_static_file("index.html")
    else:
        return render_template("index.html", user=user)

@app.route("/quizz/<quizz_id>", methods=["GET"])
@token_required
def quizz_view(user, quizz_id):
    print(user)
    if quizz_id in quizzes.keys():
        quizz_template = quizzes_templates[quizz_id]
        quizz = quizzes.get(quizz_id)
        return render_template("quizz.html", user=user, quizz=quizz, quizz_template=quizz_template)
    return "Quizz ID not found", 404


@app.route("/quizz/<quizz_id>", methods=["POST"])
@token_required
def quizz_post(user, quizz_id):
    points = 0
    answers = {}
    quizz = None
    quizz_template = None
    if quizz_id in quizzes.keys():
        quizz_template = quizzes_templates[quizz_id]
        quizz = quizzes.get(quizz_id)
        for question in quizz.questions:
            valid = None
            print(question.explanation)
            for answer in question.answers:
                print("Current answer : ", answer)
                print("User answered : ", request.form.get(answer['id']))
                if request.form.get(answer['id']) == "on" and answer['is_right'] and valid is None:
                    valid = True
                    points += 1
                elif request.form.get(answer['id']) == "on" and answer['is_right'] == False:
                    valid = False
                elif request.form.get(answer['id']) is None and answer['is_right'] == True:
                    valid = False
            answers[question.id] = {"valid": valid}
    else:
        return "Invalid quizz ID", 404
    print(answers)
    completed = CompletedQuizz(quizz_id=quizz_id, 
                               email=user['email'], 
                               answers=json.dumps(answers), 
                               score=points, 
                               max_score=len(quizz.questions), 
                               message=quizz_template['messages'][points] if points < len(quizz_template['messages']) else "")

    _id = None
    with Session(engine) as session:
        session.add(completed)
        session.commit()
        _id = completed.id
    return redirect("/review/%s" %_id, 302)

@app.route("/review/<review_id>", methods=["GET"])
@token_required
def review(user, review_id):
    quizz = None
    quizz_template = None
    with Session(engine) as session:
        query = select(CompletedQuizz).where(CompletedQuizz.id == review_id)
        completed_quizz = session.exec(query).one_or_none()
        if completed_quizz is None:
            return "Invalid review ID", 404
        if user['email'] != completed_quizz.email:
            return "You do not have the required permissions to access this resource.", 403
        if completed_quizz.quizz_id not in quizzes.keys():
            return "Quizz ID not found", 404
        quizz_template = quizzes_templates[completed_quizz.quizz_id]
        quizz = quizzes[completed_quizz.quizz_id]
    answers = json.loads(completed_quizz.answers)

    toupdate = []
    for key in answers.keys():
        toupdate += key
    for key in toupdate:
        answers[int(key)] = answers[key]
        del answers[key]
    return render_template("answers.html", user=user, answers=answers, completed_quizz=completed_quizz, quizz=quizz, quizz_template=quizz_template)

if __name__ == "__main__":
    for f in listdir("quizzes"):
        print(f)
        if f.endswith('.csv'):
            q = Quizz(f, filename="quizzes/"+f)
            quizzes[f.replace(".csv", "")] = q
    print(quizzes)
    app.run(threaded=True, debug=False)
