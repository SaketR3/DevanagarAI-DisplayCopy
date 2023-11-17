var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
ctx.lineWidth = 18;
var width = canvas.width;
var height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
var fill_value = true;
var stroke_value = false;
var canvas_data = {"pencil": [], "eraser": []}

// Array of all characters
const characters = [
    "क", "ख", "ग", "घ", "ङ",
    "च", "छ", "ज", "झ", "ञ",
    "ट", "ठ", "ड", "ढ", "ण",
    "त", "थ", "द", "ध", "न",
    "प", "फ", "ब", "भ", "म",
    "य", "र", "ल", "व", "श",
    "ष", "स", "ह", "क्ष",
    "त्र", "त्त", "०", "१", "२", "३",
    "४", "५", "६", "७", "८", "९"
];

// Dictionary with all characters and their names/sounds
const dictionary = new Map([
    ["क", "ka"],
    ["ख", "kha"],
    ["ग", "ga"],
    ["घ", "gha"],
    ["ङ", "kna"],
    ["च", "cha"],
    ["छ", "chha"],
    ["ज", "ja"],
    ["झ", "jha"],
    ["ञ", "yna"],
    ["ट", "taamatar"],
    ["ठ", "thaa"],
    ["ड", "daa"],
    ["ढ", "dhaa"],
    ["ण", "adna"],
    ["त", "tabala"],
    ["थ", "tha"],
    ["द", "da"],
    ["ध", "dha"],
    ["न", "na"],
    ["प", "pa"],
    ["फ", "pha"],
    ["ब", "ba"],
    ["भ", "bha"],
    ["म", "ma"],
    ["य", "yaw"],
    ["र", "ra"],
    ["ल", "la"],
    ["व", "waw"],
    ["श", "motosaw"],
    ["ष", "petchiryakha"],
    ["स", "patalosaw"],
    ["ह", "ha"],
    ["क्ष", "chhya"],
    ["त्र", "tra"],
    [ "त्त", "gya"],
    ["०", "0"],
    ["१", "1"],
    ["२", "2"],
    ["३", "3"],
    ["४", "4"],
    ["५", "5"],
    ["६", "6"],
    ["७", "7"],
    ["८", "8"],
    ["९", "9"],
]);

// As soon as the webpage is loaded,
// call generateNewCharacter to display the question 
var expected_answer = "";
generateNewCharacter();

// Generate and display a new randomly chosen character
function generateNewCharacter() {
    // Randomly pick new character from array "characters"
    expected_answer = characters[(Math.floor(Math.random() * characters.length))];

    // Find the name of the character in the dictionary 
    var newSound = dictionary.get(expected_answer);

    // Generate the new question to display
    var newText = "Draw the character representing '" + newSound + "'";

    // Change the element "question" (in paint.html) to display the new question 
    document.getElementById("question").innerHTML = newText;
}

function updateresult(){
    // Get the predicted letter from python
    var predicted_answer = "2"; //for testing
    if(predicted_answer == dictionary.get(expected_answer)){
        document.getElementById("result").innerHTML = "Good Job";
    } else {
        document.getElementById("result").innerHTML = "Incorrect, try again";
    }
}

function color(color_value){
    ctx.strokeStyle = color_value;
    ctx.filStyle = color_value;
}    
        
function add_pixel(){
    ctx.lineWidth += 1;
}
        
function reduce_pixel(){
    if (ctx.lineWidth == 1){
        ctx.lineWidth = 1;
    }
    else{
        ctx.lineWidth -= 1;
    }
}
        
function fill(){
    fill_value = true;
    stroke_value = false;
}
        
function outline(){
    fill_value = false;
    stroke_value = true;
}
               
function reset(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [] }
}
        
// pencil tool
        
function pencil(){
        
    canvas.onmousedown = function(e){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;
            
        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };
        
    canvas.onmousemove = function(e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };
        
    canvas.onmouseup = function(e){
        hold = false;
    };
        
    canvas.onmouseout = function(e){
        hold = false;
    };
        
    function draw(){
        ctx.lineTo(curX, curY);
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }
}
        
// eraser tool
        
function eraser(){
    
    canvas.onmousedown = function(e){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;
            
        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };
        
    canvas.onmousemove = function(e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };
        
    canvas.onmouseup = function(e){
        hold = false;
    };
        
    canvas.onmouseout = function(e){
        hold = false;
    };
        
    function draw(){
        ctx.lineTo(curX, curY);
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }    
}  

document.getElementById('save').addEventListener('click', function(e) {
    updateresult();
    generateNewCharacter();
    let canvasUrl = canvas.toDataURL("image/jpeg", 0.5);
    console.log(canvasUrl);
    const createEl = document.createElement('a');
    createEl.href = canvasUrl;
    createEl.download = "download-this-canvas";
    createEl.click();
    createEl.remove();
  });

function save(){
    var filename = document.getElementById("fname").value;
    var data = JSON.stringify(canvas_data);
    var image = canvas.toDataURL("image/jpeg", .5);
    console.log(canvasUrl);
    const createEl = document.createElement('a');
    createEl.href = image;
    createEl.download = "download-this-canvas";
    createEl.click();
    document.body.appendChild(a);
    createEl.remove();
    
    $.post("/", { save_fname: filename, save_cdata: data, save_image: image });
    alert(filename + " saved");
} 
