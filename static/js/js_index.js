const X_TRSLT = -320;
let now_trslt = 0,
    now_show_dot = 1, //[1,2,3,4]
    img_count = 4,
    run = setInterval(next, 2000);

function auto() {
    run = setInterval(next, 2000);
}

function stop() {
    clearInterval(run);
}


function next(LorR = 1) {
    for (let i = 1; i <= img_count; i++) {
        let dot = document.getElementById(i.toString())
        if (dot.className === "dot_item dot_checked") {
            now_show_dot = i + LorR
        }
    }
    if (now_show_dot >= img_count + 1)
        now_show_dot = 1;
    if (now_show_dot <= 0)
        now_show_dot = img_count;
    picked(now_show_dot.toString())
}

function picked(index) {
    now_show_dot = parseInt(index)
    let bars = document.getElementById('img_bar');
    now_trslt = (parseInt(index) - 1) * X_TRSLT
    bars.style.transform = "translateX(" + now_trslt + "px)";
    for (let i = 1; i <= img_count; i++) {
        let clear_id = document.getElementById(i.toString());
        clear_id.className = "dot_item";
    }
    document.getElementById(index).className += " dot_checked";
}