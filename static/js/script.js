/*
    Taken from https://codepen.io/julio_ok/pen/ozpqGO
*/

let canvas = document.getElementById("drawPlace");
let ctx = canvas.getContext("2d");
let pressedMouse = false;
let x;
let y;
let colorLine = "black";
let timeoutID;

// Set background to white and stroke width to 5
ctx.fillStyle = "#ffffff";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.lineWidth = 5;

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", drawLine);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("touchstart", startDrawing, { passive: false });
canvas.addEventListener("touchmove", drawLine, { passive: false });
canvas.addEventListener("touchend", stopDrawing, { passive: false });

function startDrawing(event) {
    pressedMouse = true;
    if (event.touches === undefined) {
        x = event.offsetX;
        y = event.offsetY;

    } else {
        event.preventDefault(); // Prevent default touch behavior
        let touch = event.touches[0];
        x = touch.pageX - canvas.offsetLeft;
        y = touch.pageY - canvas.offsetTop;
    }

    // if there exists a current timeout session, clear it
    // stopDrawing will create new session for current stroke
    clearTimeout(timeoutID);
}

function drawLine(event) {
    if (pressedMouse) {
        if (event.touches === undefined) {
            document.getElementById("drawPlace").style.cursor = "crosshair";
            let xM = event.offsetX;
            let yM = event.offsetY;
            drawing_line(colorLine, x, y, xM, yM, ctx);
            x = xM;
            y = yM;

        } else {
            event.preventDefault();
            document.getElementById("drawPlace").style.cursor = "crosshair";
            let touch = event.touches[0];
            let xM = touch.pageX - canvas.offsetLeft;
            let yM = touch.pageY - canvas.offsetTop;
            drawing_line(colorLine, x, y, xM, yM, ctx);
            x = xM;
            y = yM;
        }
    }
}

function stopDrawing(event) {
    if (event.touches !== undefined) {
        event.preventDefault();
    }

    pressedMouse = false;
    document.getElementById("drawPlace").style.cursor = "default";

    // Start a timeout to detect when the user has stopped drawing
    timeoutID = setTimeout(generateImage, 1000);
}

function drawing_line(color, x_start, y_start, x_end, y_end, board) {
    board.beginPath();
    board.strokeStyle = color;
    board.moveTo(x_start, y_start);
    board.lineTo(x_end, y_end);
    board.stroke();
    board.closePath();
}

function draw() {
    colorLine = "black";
    ctx.lineWidth = 5;
}

function erase() {
    colorLine = "white";
    ctx.lineWidth = 40;
}

function clearCanvas() {
    // Clear the entire canvas by setting the width and height to the same as the canvas element's width and height
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Set background to white
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function generateImage() {
    canvas.toBlob((blob) => {
        const reader = new FileReader();
        reader.readAsDataURL(blob);

        reader.onloadend = () => {
            const url = reader.result;

            fetch('/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    imageBase64: url,
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.output == null) {
                        console.log("y");
                        document.getElementById("answer").innerHTML = "";
                        document.getElementById("verify-text").innerHTML = "Draw an equal sign to solve";
                    } else {
                        console.log("x");
                        const removeEqualSign = data.output.slice(0, -1);
                        let solution = eval(removeEqualSign);
                        document.getElementById("answer").innerHTML = solution;
                        document.getElementById("verify-text").innerHTML = data.output + solution;
                    }
                });
        }
    });
}