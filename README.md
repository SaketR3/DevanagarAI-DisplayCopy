<h1 align="center">DevanagarAI</h1>



<h4 align="center">Concept</h4>
Handwriting is important for full language comprehension, but there are few online resources addressing this. This is especially so for non-Western scripts such as Devanagari: the script used for languages such as Hindi, which is spoken by hundreds of millions of people.
<br />
<br />
That's where DevanagarAI comes in. DevanagarAI is a web app that will help users practice your handwriting of Devanagari characters. The web app randomly displays different Devanagari characters, which users then have to draw on the on-screen drawing pad. Once a user submits their answer, a convolutional neural network (CNN) analyzes what they drew and predicts what character they drew. If the character they drew doesn't match the character that was assigned, users can redraw the character until they get it right. 
<br />
<br />
This was a <strong>team project</strong> part of the CS Honors program at UIUC. I designed part of web app front-end, connected the front-end to the back-end API, and wrote some of the logic (i.e. for checking whether the predicted and assigned character match, programming some of the buttons like 'Skip', etc.). The project was admitted to the course Hall of Fame! 

<br />
<br />



<h4 align="center">Tech Stack</h4>
<ul>
    <li>Flask for serving the model</li>
    <li>AJAX for API</li>
    <li>JavaScript, HTML, & CSS for front-end</li>
    <li>TensorFlow for model</li>
<ul>

<br />



<h4 align="center">Images</h4>
<div align="center">
Incorrect Drawing Example:

![Drawing pad with user's drawing and text indicating that the character drawn is wrong](https://github.com/user-attachments/assets/79175db9-03d3-4529-9220-a03c525107d3)

<br />
 
Correct Drawing Example: 

![Drawing pad with user's drawing and text indicating that the character drawn is correct!](https://github.com/user-attachments/assets/2da40730-03d6-4414-b3d3-8e625b60de92)

</div>

Team Members: as203, aidansa2, laiwei4, aizzani2, yr17, saketr3

Project Manager: muktaj2



