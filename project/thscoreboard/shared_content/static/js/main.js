"use strict";

const THEME_PROP = "thscoreboard-theme";
document.body.classList.remove("theme-light");

const themes = [ "theme-light", "theme-dark" ];

let theme = localStorage.getItem(THEME_PROP);
if(!themes.includes(theme)) {
    theme = "theme-light";
    localStorage.setItem(THEME_PROP, theme);
}

document.body.classList.add(theme);

const toggleTheme = () => {
    document.body.classList.remove(theme)
    switch(theme) {
    case "theme-light":
        theme = "theme-dark";
        break;
    case "theme-dark": default:
        theme = "theme-light"
        break;
    }
    document.body.classList.add(theme);
    localStorage.setItem(THEME_PROP, theme);
}

