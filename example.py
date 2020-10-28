import socket  # import module

# in python this is the main:
n1 = 1  # int
n2 = 1.1  # float or double
n3 = 'etni'  # string

print('hello world\n')  # output to console. \n = end of line

inp = input()  # input from user

if n1 == 0:  # if statement
    print(n3)

flag = 1
while flag == 1:  # while statement
    flag = input()


def fun1():  # function
    print('first function')


fun1()  # calling fun1

n5 = [-1, n2, 'etni', [1, 2]]  # list
print(n5[0])

n6 = (n1, n2)  # tuple
print(n6[0])

n7 = {'name': 'etni', 'id': 12345}  # dictionary of person
print("name: " + str(n7['name']) + " id: " + str(n7['id']))


class person:
    def __init__(self, name, id):  # constructor
        self.name = name
        self.id = id

    def eat(self):  # example function
        print("eat")

    def __str__(self):  # convert object to string
        return 'name: ' + self.name + ' id: ' + str(self.id)


etni = person('etni', 12345)
etni.eat()
print(etni)
