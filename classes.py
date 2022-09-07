class Question:
    def __init__(self, title):
        self.title = title
        self.answers = []
        return

    def add_answer(self, answer, is_right):
        self.answers.append({"title":answer, "is_right":is_right})
    
    def __str__(self):
        return self.title + "%s" %self.answers

class Quizz:
    def __init__(self, filename):
        self.questions = []
        with open(filename) as f:
            self.parse(f.readlines())
        return

    def parse(self, content):
        q = None
        commented = False
        for line in content:
            if "<!--" in line:
                commented = True
            if "-->" in line:
                commented = False
            if commented:
                break
            if line.strip().startswith('### '):
                if q and q not in self.questions:
                    self.questions.append(q)
                q = Question(line.strip()[3:])
            elif line.strip().startswith('# '):
                self.title = line.strip()[2:]
            elif q and line.strip().startswith('- '):
                q.add_answer(line.strip()[2:].replace('#true', ''), "#true" in line)
            if q and q not in self.questions:
                self.questions.append(q)
        return

    def __str__(self):
        return self.title + "%s" %self.questions

    def html(self):
        output = f"""<h1>{self.title}</h1>
<form method="POST"><h3>0 - Indiquez votre NOM + Prénom (utilisés pour la notation)</h3><div><input type="text" name="name" id="name"/></div>"""
        for q_id, question in enumerate(self.questions):
            output += f"""<h3>{question.title}</h3>"""
            for count, answer in enumerate(question.answers):
                output +=  f"""<div><input type="checkbox" id="{count}" name="{q_id}_{count}"><label>{answer['title']}</label></div>"""
        output += "<br/><div><input type='submit' value='Valider mes réponses'/></div></form>"
        return output
