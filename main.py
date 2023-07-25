from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_behind_proxy import FlaskBehindProxy
import requests
import openai

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'e30b92ab25051f1ed6da06292f122baf'
openai.api_key = "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"


@app.route("/")
def main_page():
    return render_template('homepage.html')

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

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
    app.run(debug=True, host="0.0.0.0")
