window.onload = (event) => {
    // Setting this in JavaScript so it still appears if JavaScript is disabled
    let el = document.getElementById("replay-comment-edit");
    if (el) {
        el.style.display = "none";
    }
}

const editReplayComment = () => {
    document.getElementById("replay-comment").style.display = "none";
    document.getElementById("replay-comment-edit").style.display = "block";
}
