from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, session
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, loginForm

import requests
import openai

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'e30b92ab25051f1ed6da06292f122baf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
openai.api_key = "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"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_page'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    is_logged_in = 'username' in session
    return render_template('login.html', form=form, is_logged_in=is_logged_in)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main_page'))



@app.route("/")
def main_page():
    is_logged_in = 'username' in session
    return render_template('homepage.html', is_logged_in=is_logged_in)

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main_page')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)



@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    topic = data.get("topic")
    difficulty = data.get("difficulty")
    question_type = data.get("questionType")
    num_questions = data.get("numQuestions")

    prompt = f"Generate a {difficulty} level quiz on the topic of {topic} with {num_questions} {question_type} questions."

    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=500
    )

    return jsonify({
        "quiz": response.choices[0].text.strip()
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
