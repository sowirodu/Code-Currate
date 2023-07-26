document.getElementById("quizForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const topic = document.getElementById("topic").value;
    const difficulty = document.getElementById("difficulty").value;
    const questionType = document.getElementById("questionType").value;
    const numQuestions = document.getElementById("numQuestions").value;

    fetch('/generate-quiz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            topic,
            difficulty,
            questionType,
            numQuestions
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
		console.log(data)
		displayQuiz(data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById("quizOutput").innerText = 'An error occurred while generating the quiz. Please try again later.';
    });
});

function displayQuiz(quizData) {
    let quizHTML = "";

    quizData.questions.forEach((question, index) => {
        if (question.type === "Multiple Choice") {
            quizHTML += `<div class="question">
                <p>${question.text}</p>
                ${question.choices.map((choice, idx) => 
                `<label><input type="radio" name="q${index}" value="${idx}">${choice}</label>`
                ).join('')}
            </div>`;
        } else if (question.type === "True/False") {
            quizHTML += `<div class="question">
                <p>${question.text}</p>
                <label><input type="radio" name="q${index}" value="true">True</label>
                <label><input type="radio" name="q${index}" value="false">False</label>
            </div>`;
        }
    });

    quizHTML += '<button id="submitAnswers">Submit Answers</button>';
    document.getElementById("quizOutput").innerHTML = quizHTML;

    document.getElementById("submitAnswers").addEventListener("click", function() {
        let userAnswers = [];
        quizData.questions.forEach((_, index) => {
            let userAnswer = document.querySelector(`input[name="q${index}"]:checked`);
            userAnswers.push(userAnswer ? userAnswer.value : null);
        });
        gradeQuiz(userAnswers, quizData);
    });
}

function gradeQuiz(userAnswers, quizData) {
    let correctAnswers = 0;

    userAnswers.forEach((answer, index) => {
        if (quizData.questions[index].type === "Multiple Choice") {
            if (parseInt(answer) === quizData.questions[index].answer) {
                correctAnswers++;
            }
        } else if (quizData.questions[index].type === "True/False") {
            if ((answer === "true" && quizData.questions[index].answer) || 
                (answer === "false" && !quizData.questions[index].answer)) {
                correctAnswers++;
            }
        }
    });

    let feedback = `You scored ${correctAnswers} out of ${quizData.questions.length}.`;
    document.getElementById("quizOutput").innerHTML = feedback;
}
