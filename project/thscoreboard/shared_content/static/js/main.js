if(localStorage.getItem("darktheme")) {
    document.body.classList.add("darktheme");
}

const toggleTheme = () => {
    if(localStorage.getItem("darktheme")) {
        localStorage.removeItem("darktheme");
        document.body.classList.remove("darktheme");
    } else {
        localStorage.setItem("darktheme", true);
        document.body.classList.add("darktheme");
    }
}