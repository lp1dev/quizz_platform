from flask import escape
import csv

""" CSV HEADER 

Question,Question Type (multiple-choice or multi-select),Answer Option 1,Answer Option 2,Answer Option 3,Answer Option 4,Answer Option 5,Answer Option 6,Answer Option 7,Answer Option 8,Answer Option 9,Answer Option 10,Answer Option 11,Answer Option 12,Answer Option 13,Answer Option 14,Answer Option 15,Correct Response,Explanation,Knowledge Area

"""

def parse(file):
    csv_reader = csv.reader(file, delimiter=',')
    questions = []
    for line in csv_reader:
        if len(line) != 20:
            raise Exception("CSV file does not contain 20 fields in "+line)
        else:
            q = Question(line[0], line[1], line[18], line[19])
            for index, question in enumerate(line[2:-3]):
                q.add_answer(question, index == int(line[17]))
            questions.append(q)
    return

class Question:
    def __init__(self, title, type, explanation, knowledge_area):
        self.title = title
        self.type = type
        self.explanation = explanation
        self.knowledge_area = knowledge_area
        self.answers = []
        return

    def add_answer(self, answer, is_right):
        self.answers.append({"title":answer, "is_right":is_right})
    
    def __str__(self):
        return self.title + "%s" %self.answers

class Quizz:
    def __init__(self, title, filename):
        self.questions = []
        self.title = title
        with open(filename) as f:
            self.parse(f)
        return

    def parse(self, file):
        self.questions = parse(file)
        return

    def __str__(self):
        return self.title + "%s" %self.questions

    def html(self):
        output = f"""<h1>{self.title}</h1>
<form method="POST"><h3>0 - Indiquez votre NOM + Prénom (utilisés pour la notation)</h3><div><input type="text" name="name" id="name"/></div>"""
        for q_id, question in enumerate(self.questions):
            output += f"""<h3>{question.title}</h3>"""
            for count, answer in enumerate(question.answers):
                output +=  f"""<div><input type="checkbox" id="{count}" name="{q_id}_{count}"><label>{escape(answer['title'])}</label></div>"""
        output += "<br/><div><input type='submit' value='Valider mes réponses'/></div></form>"
        return output
