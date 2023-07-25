
const modalBtns = [...document.getElementsByClassName("modal-btn")];
const modalBody = document.getElementById("modal-body-confirm");
const startBtn = document.getElementById("start-btn");

const url = window.location.href;

modalBtns.forEach(modalBtn => modalBtn.addEventListener("click", () => {
    const pk = modalBtn.getAttribute("data-pk");
    const name = modalBtn.getAttribute("data-quiz");
    const totalQuestions = modalBtn.getAttribute("data-questions");
    const time = modalBtn.getAttribute("data-time");

    modalBody.innerHTML = `
        <h5>Are you sure you want to start ${name}?</h5>
        <div>
            <ul>
                <li>Number of questions: ${totalQuestions}</li>
                <li>Duration: ${time} min</li>
            </ul>
        </div>
    `

    startBtn.addEventListener("click", ()=> {
        window.location.href = url + "quiz/" + pk; 
    })
}));