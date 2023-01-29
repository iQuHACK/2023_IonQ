let button = document.getElementById("button");
let output = document.getElementById("output");

button.addEventListener("click", function() {
    if (button.value=="Play") {
        button.value = "Play again?";
        output.style.display = "block";
        var size = document.querySelector('input[name="size"]:checked').value;
        var speed = document.querySelector('input[name="speed"]:checked').value;
        var vis = document.querySelector('input[name="vis"]:checked').value;
        var fight = document.querySelector('input[name="fight"]:checked').value;
        
        if(fight == 0) {
            if(size == 1 || speed == 1 || vis == 1) {
                output.innerHTML = "Mandalorian lost!";
            }
            else {
                output.innerHTML = "Mandalorian survived!";
            }
        }
        if(fight == 1) {
            if(speed == 1 || vis == 1) {
                output.innerHTML = "Mandalorian lost!";
            }
            else {
                output.innerHTML = "Mandalorian survived!";
            }
        }
    }
    else {
        button.value = "Play"
        window.location.href = "http://127.0.0.1:5000/";
    };
});