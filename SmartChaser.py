import numpy as np
import Questions

class SmartChaser:
    chaser_step = 0

    def get_step(self):
        return self.chaser_step

    def step_plus_one(self):
        self.chaser_step += 1

    def chose_answer(self, answers_list):
        answers_list.reverse()
        # list = ["correct answer", "option D", "option C", "option B", "option A", "question"]

        mylist = list(dict.fromkeys(answers_list))
        # We removed the duplicate in the list (and the correct answer is always at the first place)

        answer = np.random.choice(mylist, 1, p=[0.75, 0.25/3, 0.25/3, 0.25/3, 0])

        if answer == mylist[0]:   # reponse dans le premier truk?
            return True
        else:
            return False
            # return answer

    def chaser_answer(self, lvl, qnum):
        global correct_answer, q
        global chaser_step
        q = Questions.get_question(lvl, qnum)
        answer = SmartChaser.chose_answer(q)
        if answer == True:
            return True
        else:
            return False
        # if (correct_answer == q[ord(answer) - 96]):
        # chaser_step+=1
        # return True
        # else:
        # return False