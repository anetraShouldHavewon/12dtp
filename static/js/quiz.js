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
        a: "Less than an hour and a half",
        b: "One to two hours",
        c: "Two to three hours",
        d: "Forever"
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

dicts = answerOps.addEventListener("click",getSelected)

function getSelected(e){
    var query = []
    var answerOp = e.target
    if (answerOp.tagName == "INPUT"){
        //Age of audience
        if (question_number === 1){
            var answerOpId = parseInt(e.target.id)
            let query_i = ""
            if (answerOpId === 1){
                query_i = "SELECT id FROM Movie WHERE film_rating IN (5,6)"
            }
            if (answerOpId === 2){
                query_i = "SELECT id FROM Movie WHERE film_rating IN (1,4,5,6)"
            }
            if (answerOpId === 3){
                query_i = "SELECT id FROM Movie WHERE film_rating IN (1,3,4,5,6,7,9,10)"
            }
            if (answerOpId === 4){
                query_i = "SELECT id FROM Movie WHERE film_rating IN (1,2,3,4,5,6,7,8,9,10)"
                
            }
            query[0] = query_i
            document.getElementById("test").innerText = query
        }
        //Recent or old movie?
        if (question_number === 2){
            var answerOpId = parseInt(e.target.id)
            let query_ii = ""
            if (answerOpId === 1){
                query_ii = "SELECT id FROM Movie WHERE release_year >= 2000"
                document.getElementById("test").innerText = answerOpId
            }
            if (answerOpId === 2){
                query_ii = "SELECT id FROM Movie WHERE release_year >= 1970 AND release_year < 2000"
                document.getElementById("test").innerText = answerOpId
            }
            if (answerOpId === 3){
                query_ii = "SELECT id FROM Movie WHERE release_year < 1970"
                document.getElementById("test").innerText = answerOpId
            }
            if (answerOpId === 4){
                query_ii = "SELECT id FROM Movie"
                document.getElementById("test").innerText = answerOpId
            }
            query[1] = query_ii
            document.getElementById("test").innerText = query
        }
        //How long should your movie be?
        if (question_number === 3){
            var answerOpId = parseInt(e.target.id)
            let query_iii = ""
            if (answerOpId === 1){
                document.getElementById("test").innerText = answerOpId
                query_iii = "SELECT id FROM Movie WHERE length(minutes) <= 90"
            }
            if (answerOpId === 2){
                document.getElementById("test").innerText = answerOpId
                query_iii = "SELECT id FROM Movie WHERE length(minutes) > 90 and length(minutes) <= 120"
            }
            if (answerOpId === 3){
                document.getElementById("test").innerText = answerOpId
                query_iii = "SELECT id FROM Movie WHERE length(minutes) > 120 and length(minutes) <= 180"
            }
            if (answerOpId === 4){
                document.getElementById("test").innerText = answerOpId
                query_iii = "SELECT id FROM Movie WHERE length(minutes) > 180"
            }
            query[2] = query_iii
            document.getElementById("test").innerText = query
        }
        //Do you want to switch on your brain?
        if (question_number === 5){
            var answerOpId = parseInt(e.target.id)
            let query_v = ""
            if (answerOpId === 1){
                document.getElementById("test").innerText = answerOpId
                query_v = "SELECT id FROM Movie WHERE use_of_tropes_rating IN (4,5) and moral_ambiguity_rating IN (4,5)"
            }
            if (answerOpId === 2){
                document.getElementById("test").innerText = answerOpId
                query_v = "SELECT id FROM Movie WHERE use_of_tropes_rating IN (1,2,3,4) and moral_ambiguity_rating IN (1,2,3,4)"
            }
            if (answerOpId === 3){
                document.getElementById("test").innerText = answerOpId
                query_v = "SELECT id FROM Movie"    
            }
            query[4] = query_v
            document.getElementById("test").innerText = query
        }
        //Mean Girls question
        if (question_number === 6){
            var answerOpId = parseInt(e.target.id)
            if (answerOpId === 4){
                var lastQmessage = "And yes. Mark Waters did indeed direct our Bible, Mean Girls."
                document.getElementById("test").innerText = answerOpId
            }else{
                var lastQmessage = "No. We recommend you dedicate your time to watching Mean Girls"
            }
            query[5] = lastQmessage
        }
        transferData(query)
    }
}

document.getElementById("test").innerText = dicts.lastMessage

//passing query to routes.py --> https://www.geeksforgeeks.org/pass-javascript-variables-to-python-in-flask/ 
//another stackoverflow --> https://stackoverflow.com/questions/18701282/what-is-content-type-and-datatype-in-an-ajax-request 

function transferData(query){
    $.ajax({
        url: "/quiz_results",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            'age_range': query[0],
            'movie_age': query[1],
            'movie_length': query[2],
            'genres': query[3],
            'movie_complexity': query[4],
            'last_question': query[5]
        }),
        success: function(response) {
            document.getElementById('output').innerHTML = response.result;
        },
        error: function(error) {
            let error = "error"
            console.log(error);
        }
    });
}

