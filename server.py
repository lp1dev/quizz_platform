#!/usr/bin/env python3

from flask import Flask, request, render_template
from os import listdir
from classes import Quizz
from datetime import datetime
from auth import token_required, token_optional

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
quizzes = []


@app.route("/")
@token_optional
def index(user):
    print(user)
    if user is None:
        return app.send_static_file("index.html")
    else:
        return render_template("index.html", user=user)

@app.route("/quizz/<quizz_id>", methods=["GET"])
def quizz_view(quizz_id):
    return quizzes[int(quizz_id)].html()

@app.route("/quizz/<quizz_id>", methods=["POST"])
def quizz_post(quizz_id):
    print(request.form)
    name = request.form.get('name')
    if not name:
        return "Invalid Name"
    dt = datetime.now().strftime("%d_%m_%Y-%H:%M:%S")
    output_f = "answers/%s-%s.txt" %(name, dt)
    
    points = 0
    
    with open(output_f, "a+") as f:
        f.write('Student : %s\n' %name)
        for q_id, question in enumerate(quizzes[int(quizz_id)].questions):
            f.write('----\n\n'+question.title+'\n')
            valid = True
            for answ_id, answer in enumerate(question.answers):
                print(request.form)
                if answer.get('is_right') and request.form.get('%s_%s' %(q_id, answ_id)) != 'on':
                    valid = False
                if not answer.get('is_right') and request.form.get('%s_%s' %(q_id, answ_id)) == 'on':
                    valid = False
                f.write(' - '+answer.get('title')+ ('[OK]' if valid else '[KO]') + '\n')
            if valid:
                points += 1
        f.write('\nGrade : '+str(points)+' / '+ str(len(quizzes[int(quizz_id)].questions)) + '\n')
    return "Vos réponses ont bien été prises en compte!"

if __name__ == "__main__":
    print("RUNNING")
    for f in listdir("quizzes"):
        print(f)
        if f.endswith('.csv'):
            q = Quizz(f, filename="quizzes/"+f)
            quizzes.append(q)
    print(quizzes)
    app.run(threaded=True, debug=False)
