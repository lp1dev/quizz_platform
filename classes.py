import csv

""" CSV HEADER 

Question,Question Type (multiple-choice or multi-select),Answer Option 1,Answer Option 2,Answer Option 3,Answer Option 4,Answer Option 5,Answer Option 6,Answer Option 7,Answer Option 8,Answer Option 9,Answer Option 10,Answer Option 11,Answer Option 12,Answer Option 13,Answer Option 14,Answer Option 15,Correct Response,Explanation,Knowledge Area

"""

def parse(file):
    csv_reader = csv.reader(file, delimiter=',')
    print(csv_reader)
    questions = []
    for line in csv_reader:
        print(line)
        if len(line) != 20:
            raise Exception("CSV file does not contain 20 fields in "+line)
        else:
            q = Question(len(questions), line[0], line[1], line[18], line[19])
            for index, question in enumerate(line[2:-3]):
                if len(question):
                    q.add_answer(question, (index + 1) == int(line[17]))
            questions.append(q)
    return questions

class Question:
    def __init__(self, id, title, type, explanation, knowledge_area):
        self.id = id
        self.title = title
        self.type = type
        self.explanation = explanation
        self.knowledge_area = knowledge_area
        self.answers = []
        return

    def add_answer(self, answer, is_right):
        self.answers.append({"title":answer, "is_right":is_right, "id": "%s_%s" %(self.id, len(self.answers))})
    
    def __str__(self):
        return self.title + "%s" %self.answers

class Quizz:
    def __init__(self, title, filename):
        self.questions = []
        self.title = title
        with open(filename) as f:
            self.questions = parse(f.readlines())

    def __str__(self):
        return self.title + "%s" %self.questions
