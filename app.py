from flask import Flask, render_template, redirect, url_for, request, flash, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dont-tell'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

responses = []

@app.route('/')
def start_survey():
    return render_template('start.html', title='Customer Satisfaction Survey', instructions='Please fill out a survey about your experience with us.')

@app.route('/questions/<int:question_number>')
def next_question(question_number):
    if question_number == len(responses):
        current_question = satisfaction_survey.questions[question_number]
        return render_template('question.html', question=current_question)
    elif question_number < len(responses):
        return redirect(url_for('questions', question_number=len(responses)))
    else:
        return redirect(url_for('survey_complete'))

@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def questions(question_number):
    if question_number == len(responses):
        current_question = satisfaction_survey.questions[question_number]

        if request.method == 'POST':
            user_response = request.form['choice']
            responses.append(user_response)

            if question_number + 1 < len(satisfaction_survey.questions):
                next_question_number = question_number + 1
                return redirect(url_for('questions', question_number=next_question_number))
            else:
                return redirect(url_for('survey_complete'))
        
        return render_template('question.html', question=current_question)
    elif question_number < len(responses):
        flash("You've already answered this question")
        return redirect(url_for('questions', question_number=len(responses)))
    else:
        flash("You're trying to access an invalid question.")
        return redirect(url_for('survey_complete'))


@app.route('/survey-complete')
def survey_complete():
    return 'Thank you for completing the survey.'

if __name__ == '__main__':
    app.run(debug=True)
