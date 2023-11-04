var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var cvs_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [] }; 

function hide_canvas (){
    document.getElementById("paint").style.visibility = "hidden";
}

function clear (){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

$( "p" ).click(function() {
    var img_fname = $(this).text();
    $("#fname").val(img_fname);
    show_image(imag_fname);
});

function show_image (img_name){
    for(var key in py_data){
        if(key == img_name){
            file_data = JSON.parse(py_data[key]);
            for(var ptool in file_data){
                if(file_data[ptool].length != 0){
                    for(var i = 0; i < file_data[ptool].length; i++){
                        cvs_data[ptool].push(file_data[ptool][i]);
                        shape_draw(ptool, file_data[ptool][i]);
                    }
                }
            }
        }
    }
}

function shape_draw (ctool, shape){
    if (ctool == 'pencil'){
        var bg_x = shape.startx, bg_y = shape.starty, x = shape.endx, y = endy;
        ctx.lineWidth = shape.thick;
        ctx.strokeStyle = shape.color;
        ctx.beginPath();
        ctx.moveTo(bg_x, bg_y);
        ctx.lineTo(x, y);
        ctx.stroke();
    }
    else if (ctool == 'eraser'){
        var e_x = shape.endx, e_y = shape.endy;
        ctx.lineWidth = shape.thick;
        ctx.clearRect(curX, curY, 20, 20);
    }
}

