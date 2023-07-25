console.log("Quiz it is");

const quizBox = document.getElementById("quiz-box");
const timerBox = document.getElementById("timer-box");
const url = window.location.href;

const activeTimer = (time) => {
    console.log(time);

    if(time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}</b>`
    }
    else {
        timerBox.innerHTML = `<b>${time}</b>`
    }

    let minutes = time - 1;
    let seconds = 60;
    let displayMinutes;
    let displaySeconds;

    const timer = (setInterval(()=>  {
        seconds --;
        if(seconds < 0) {
            seconds = 59;
            minutes--;
        }
        if(minutes.toString().length < 2) {
            displayMinutes = "0" + minutes;
        }
        else {
            displayMinutes = minutes;
        }
        if(seconds.toString().length < 2) {
            displaySeconds = "0" + seconds;
        }
        else {
            displaySeconds = seconds;
        }
        if(minutes === 0 && seconds === 0) {
            clearInterval(timer);
            console.log("Time over");
            alert("time up");
            document.getElementById('quiz-form').submit();
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`

    }, 1000))
}

fetch(`${url}data`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok. Status: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then(response => {
        // console.log(response);
        const data = response.data;

        // console.log(data);
        data.forEach(el => {
            // console.log(el);
            for (const [question, answers] of Object.entries(el)) {
                // console.log(question);
                // console.log(answers);
                quizBox.innerHTML += `
                <h3>${question}</h3>             
            `
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                    <div>
                        <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}" />
                        <label for="${question}">${answer}</label>
                    </div>
                `
                })
            }
        });
        activeTimer(response.time);

    })
    .catch(error => {
        console.error('Fetch Error:', error);
    });
