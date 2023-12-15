(function () {
    window.quizz = {}
    window.quizz.activeQuestion = 0
    window.quizz.numQuestions = 0

    window.quizz.init = () => {

        document.querySelectorAll(".question").forEach((question) => {
            if (window.quizz.numQuestions == window.quizz.activeQuestion) {
                question.style.display = "block"
            } else {
                question.style.display = "none"
            }
            window.quizz.numQuestions += 1
        })
    
    }

    window.quizz.previous = () => {
        let i = 0
        if (window.quizz.activeQuestion > 0) {
            window.quizz.activeQuestion--
        }
        document.querySelectorAll(".question").forEach((question) => {
            if (i == window.quizz.activeQuestion) {
                question.style.display = "block"
            } else {
                question.style.display = "none"
                console.log("none", question)
            }
            i += 1
        })
    }

    window.quizz.next = () => {
        let i = 0
        if (window.quizz.activeQuestion < window.quizz.numQuestions) {
            window.quizz.activeQuestion++
        }
        document.querySelectorAll(".question").forEach((question) => {
            if (i == window.quizz.activeQuestion) {
                question.style.display = "block"
            } else {
                question.style.display = "none"
                console.log("none", question)
            }
            i += 1
        })
    }
})();