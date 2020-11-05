import numpy as np

def chose_answer(list):
    rev_list = list.reverse()
    # list = ["correct answer", "option D", "option C", "option B", "option A", "question"]

    mylist = list(dict.fromkeys(rev_list))
    # We removed the duplicate in the list (and the correct answer is always at the first place)

    answer = np.random.choice(mylist, 1, p=[0.75, 0.05, 0.05, 0.05, 0])
    return answer