class Question:
    def __init__(self, title):
        self.title = title
        self.answers = []
        return

    def add_answer(self, answer, is_right):
        self.answers.append({answer:is_right})
    
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
        for line in content:
            if line.strip().startswith('### '):
                if q and q not in self.questions:
                    self.questions.append(q)
                q = Question(line.strip()[3:])
            elif line.strip().startswith('# '):
                self.title = line.strip()[2:]
            elif q and line.strip().startswith('- '):
                q.add_answer(line.strip()[2:], "#true" in line)
            if q and q not in self.questions:
                self.questions.append(q)
        return

    def __str__(self):
        return self.title + "%s" %self.questions
