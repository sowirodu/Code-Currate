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
        // Check if the response is successful (status code in the range 200-299)
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("quizOutput").innerText = data.quiz;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById("quizOutput").innerText = 'An error occurred while generating the quiz. Please try again later.';
    });
});
