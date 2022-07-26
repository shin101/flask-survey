from flask import Flask, render_template, session, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jeesoo'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    return render_template("homepage.html",survey = survey)

@app.route('/first_q', methods=['POST'])
def first_question():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def handle_question():
    choice = request.form['radio_answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)) :
        return redirect("/complete")

    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if responses is None:
        return redirect("/")

    if (len(responses) == len(survey.questions)) :
        return redirect("/complete")

    if (len(responses)!= qid):
        flash("do not tinker with the url")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question=question)


@app.route('/complete')
def completed():
    return render_template("thanks.html")
