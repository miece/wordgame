
from flask import Flask, render_template, url_for, request, redirect, flash, session

import time
import random
import itertools
import sys
import logging

from collections import OrderedDict
from threading import Thread
from contains import *


app = Flask(__name__)




contents = open("words.txt").read()


@app.route('/')
def display_home():
    return render_template("home.html",
                            the_title="Welcome to the WordGame",
                            game_url=url_for("play"),
                            showscores_url=url_for("showallscore"),
			    the_person=session.get('username', 'unknown'), )


@app.route('/play')
def play():
    
    return render_template("enter.html",
                           the_title="Before we begin...",
                           the_game_url=url_for("startgame") )


@app.route('/wordgame', methods=["POST"])
def startgame():
   
        session['time_start'] = time.time()
        lines = open('words.txt').read().replace("'", "").splitlines()
        greaterThan7 = [word for word in lines if len(word) >= 7]
        with open('source.txt', 'w') as f:
            for s in greaterThan7:
                f.write(s + '\n')
        getword = open('source.txt').read().splitlines()
        myline = random.choice(getword)
        session['source_word'] = myline
        return render_template("show.html",
                                the_title="Enter 7 words as quick as you can!",
                                the_data=myline,
                                home_link=url_for("display_home"),
                                the_save_url=url_for("saveformdata"))
        


@app.route('/saveform', methods=["POST"])
def saveformdata():

    getSource = session.get('source_word')
    getWord1 = request.form['word1']
    getWord2 = request.form['word2']
    getWord3 = request.form['word3']
    getWord4 = request.form['word4']
    getWord5 = request.form['word5']
    getWord6 = request.form['word6']
    getWord7 = request.form['word7']
    get_Words = []
    get_Words.extend((getWord1,getWord2, getWord3, getWord4, getWord5, getWord6, getWord7))
    get_Words = [x.strip(' ') for x in get_Words]


    session['my_words'] = get_Words

    score = 0
    valid = []
    for s in get_Words:
        valid.append(contains(getSource, s))

    # get the time elapsed
    timer = session.get('time_start')
    elapsed = round(time.time() - timer)

    # check for digit in list to get the score, append to a list and sum the values
    my_list = str(valid)
    score = [s for s in my_list if s.isdigit()]
    result = list(map(int,score))
    result = sum(result)

    session['the_result'] = result
    session['the_elapsed'] = elapsed

    # remove brackets and clean the list
    cleaned = [i[0] for i in valid]

    session['cleaned'] = cleaned
    tester1 = checkDupe(get_Words)

    test = list(zip(get_Words,cleaned))

    
    # pass variables to the log file
    if(result == 0):
        the_message = ("You didn't even get one right!! Go and play it again and try harder!")
    elif(result >= 1 and result <=3):
        the_message =("At least you got a few right, but it's not good enough. Try again!")
    elif(result >= 4 and result <=6):
        the_message = ("Nearly got them all right, but nearly never caught the bus. You must try again!")
    else:
        #the_message = ("At long last you got them all right! Congrats")
        
        return redirect(url_for('winner'))

    return render_template("thanks.html",
				the_title="Thanks for playing !",
				the_score=result,
				source=getSource,
				test=test,
				timer=elapsed,
				the_message=the_message,
				name1=session.get('username','unknown'),
                                play_again=url_for("play"),
				home_link=url_for("display_home"), )

def update_log(name,time):
    with open('comments.log', 'a') as log:
        print(name,time,file=log, sep='.')

@app.route('/highscores', methods=["POST"])
def showallscores():

    all_ok = True
    session['username'] = request.form['name']
    print (session.get('username'))
    if(session.get('username')) == '':
        all_ok = False
        print("Sorry. You must tell me your name. Try again")
        session['username'] = "Unknown"
    if all_ok:
        name = request.form['name']
        time = session.get('the_elapsed')

        session['username'] = request.form['name']

        update_log(name,time)

        with open('comments.log') as f:
            cred = [x.strip().split('.') for x in f.readlines()]
    
        u = []
        p = []

        for username,password in cred:
            u.append(username)
            p.append(int(password))


        z = list(zip(u,p))
        sortTup = sorted(z,key=lambda x: x[1])
    
        location = (sortTup.index((name, time)))+1

        mylist = sortTup[:10]

        return render_template("showscores.html",
                            the_title="Here are the high scores",
                            the_dict=(mylist),
			    the_location=(location),
                            result=session.get('the_result'),
                            home_link=url_for("display_home"))
    else:
        return redirect(url_for('showallscores'))



@app.route('/highscore')
def showallscore():

    with open('comments.log') as f:
        cred = [x.strip().split('.') for x in f.readlines()]
    
    u = []
    p = []

    for username,password in cred:
        tup = (username,int(password))
        u.append(username)
        p.append(int(password))


    z = list(zip(u,p))
    sortTup = sorted(z,key=lambda x: x[1])

    mylist = sortTup[:10]

    return render_template("showscore.html",
                            the_title="Here are the high scores",
                            the_dict=(mylist),
                            result=session.get('the_result'),
                            home_link=url_for("display_home"))





@app.route('/winner')
def winner():

        cleaned = []
        cleaned = session.get('cleaned')
        thewords = session.get('my_words')
        source = session.get('source_word')

        test = list(zip(thewords,cleaned))

        return render_template("winner.html",
                            the_title="Here are the high scores",
 			    source=source,
			    test=test,
                            the_score=session.get('the_result'),
			    timer=session.get('the_elapsed'),
                            the_game_url=url_for("showallscores"))

app.config['SECRET_KEY'] = 'thisismysecretkeywhichyouwillneverguesshahahahahahahaha'

if __name__ == '__main__':
    app.run(debug=True)
