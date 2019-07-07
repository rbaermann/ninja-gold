from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def index():
    if 'gold' not in session:
        session['gold'] = 0
    if 'moves' not in session:
        session['moves'] = 0
    if 'messages' not in session:
        session['messages'] = []
    if 'colors' not in session:
        session['colors'] = []
    session['moves'] += 1

    return render_template('index.html', gold = session['gold'], messages = session['messages'], colors = session['colors'], moves = session['moves'] - 1)

@app.route('/process_money', methods=['POST'])
def money():
    if 'reset' in request.form:
        session['reset'] = request.form['reset']
    
    if 'reset' in session:
        del session['reset']
        session['gold'] = 0
        session['moves'] = 0
        session['messages'] = []
        session['colors'] = []
        return redirect('/')

    else:
        loc = request.form['location']
        if loc == 'farm':
            gold = random.randint(10, 20)
        elif loc == 'cave':
            gold = random.randint(5, 10)
        elif loc == 'house':
            gold = random.randint(2, 5)
        elif loc == 'casino':
            gold = random.randint(-50, 50)
        
        if gold > 0:
            session['messages'].insert(0, 'You have earned ' + str(gold) + ' gold from the ' + loc)
            session['colors'].insert(0, 'green')
        elif gold == 0:
            session['messages'].insert(0, 'You have broken even, left with ' + str(gold) + ' gold from the ' + loc)
            session['colors'].insert(0, 'black')
        else:
            session['messages'].insert(0, 'You have been robbed by the ' + loc + '... ' + str(gold * -1) + ' was taken from your total gold')
            session['colors'].insert(0, 'red')

        session['gold'] += gold
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)