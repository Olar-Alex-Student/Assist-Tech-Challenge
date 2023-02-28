function toggle() {
    let elements = document.getElementsByClassName("toggle");
    for (let i = 0; i < elements.length; i++) {
        elements[i].classList.toggle("hide");
    }
    document.getElementsByClassName("box")[0].classList.toggle("hide");
}