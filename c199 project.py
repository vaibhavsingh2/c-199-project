import socket
from threading import Thread
import random

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address='127.0.0.1'
port=8000

server.bind((ip_address,port))
server.listen()

clients=[]

questions=[

    "Write the answer in a, b,c or d form \n What is The chemistry of lithium is very similar to that of magnesium even though they are placed in different groups. Its reason is: \n Both are found together in nature \n Both have nearly the same size \n Both have similar electronic configuration \n The ratio of their charge and size",

    "The element with atomic number 35 belongs to \n d – Block \n  f – Block \n p – Block \n s – Block"
    ]

answers=['d', 'c']

print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn))
    new_thread.start()
