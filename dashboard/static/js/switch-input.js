function switch_input(obj) {
    let root = document.documentElement;
    if (obj.value == 0) {
        root.style.setProperty('--switch-background-color', "rgb(62, 62, 62)");
        root.style.setProperty('--switch-foreground-color', "rgb(180, 180, 180)");
    }
    else {
        root.style.setProperty('--switch-background-color', "rgb(180, 180, 180)");
        root.style.setProperty('--switch-foreground-color', "rgb(62, 62, 62)");
    }
}