//questions data
const quizData = [
    {
        question: "What age range are you in?",
        a: "Under 13",
        b: "13~15",
        c: "16~17",
        d: "18+",
    },
    {
        question: "Recent or old cinema?",
        a: "Only movies made in this century",
        b: "70s~90s",
        c: "Old Hollywood!",
        d: "Don't really mind"
    },
    {
        question: "How long should your movie be?",
        a: "One to two hours",
        b: "Two to three hours",
        c: "Forever"
    },
    {
        question: "What are you into? (Pick all that apply)",
        a: "Horror",
        b: "Comedy",
        c: "Sci-Fi/Fantasy",
        d: "Animation",
        e: "Western",
        f: "Thriller",
        g: "Romance",
        h: "Martial Arts",
        i: "Documentary",
        j: "Drama"
    },
    {
        question: "Do you want to switch on your brain?",
        a: "Yes!",
        b: "Not really",
        c: "Don't really mind"
    },
    {
        question: "Who directed the world renowned chick flick Mean Girls?",
        a: "Joe Biden",
        b: "Amy Poehler",
        c: "Tina Fey",
        d: "Mark Waters"
    }
];

//checking the id of the page: passing the variable "question_num" via an undisplayed
//label tag and assigning the number of options to the page depending on the id of the page

let question_num = document.getElementById("question_number").innerText;
let question_number = parseInt(question_num);

const four_option_questions = [1,2,3,6];
const three_option_questions = [5];
const ten_option_questions = [4];
var question_options = 0;

let four_option_true = four_option_questions.includes(question_number)
let three_option_true = three_option_questions.includes(question_number)
let ten_option_true = ten_option_questions.includes(question_number)

if (four_option_true === true){
    question_options = 4
}else if (three_option_true === true){
    question_options = 3
}else if (ten_option_true === true){
    question_options = 10
}

//testing line
//document.getElementById("test").innerHTML = question_options

//prints out the quiz questions and options for each page:

const option_set = quizData[question_number -1]
document.getElementById("question").innerHTML = option_set.question
delete option_set.question

//creating html elements: https://softauthor.com/create-html-element-in-javascript/ and https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_document_createelement4 
let keys = Object.keys(option_set);

let num = 0;
for (let x of keys){
    ++num;
    let append_el = document.getElementById("options")
    let question = option_set[x]
    let new_el = document.createElement("input")
    new_el.setAttribute("type","button")
    new_el.setAttribute("class","options")
    new_el.setAttribute("value", question)
    new_el.setAttribute("id",num)
    append_el.appendChild(new_el)
}

//cumulates data from the quiz to give you your film selection
//determining which button leads to which sql query

const answerOps = document.getElementById("options")
//getting the id of the button selected
//can help: https://stackoverflow.com/questions/37360486/change-a-variable-when-button-is-clicked

answerOps.addEventListener("click",getSelected)

function getSelected(e){
    var answerOp = e.target
    if (answerOp.tagName == "INPUT"){
        var answerOpId = parseInt(e.target.id)
        transferData(answerOpId,question_number)
    }
}

        