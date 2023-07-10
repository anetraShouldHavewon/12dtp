//questions data
const quizData = [
    {
        question: "What age range are you in?",
        a: "Under 10",
        b: "10~13",
        c: "15~18",
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
        a: "Less than one hour",
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

//html for each question
let question_num = document.getElementById("question_number");
window.alert(question_num)
document.getElementById('question').innerHTML('Hello World!')