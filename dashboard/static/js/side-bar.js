function side_bar_on_hover(obj) {
    for (let i = 0; i < document.getElementsByClassName('side-label').length; i++) {
        document.getElementsByClassName('side-label')[i].style.visibility = "visible";
        document.getElementsByClassName('side-label')[i].style.backgroundColor = "transparent";
        document.getElementsByClassName('side-label')[i].firstElementChild.style.color = "transparent";
    }
    obj.parentElement.getElementsByClassName('side-label')[0].style.backgroundColor = "rgb(31, 31, 31, 0.7)";
    obj.parentElement.getElementsByClassName('side-icon')[0].style.backgroundColor = "rgb(31, 31, 31, 0.7)";
    obj.parentElement.getElementsByClassName('side-icon')[0].style.color = "rgb(254, 78, 69)";
    try {
        obj.nextElementSibling.firstElementChild.style.color = "rgb(254, 78, 69)";
    }
    catch {
        obj.firstElementChild.style.color = "rgb(254, 78, 69)";
    }
    obj.parentElement.style.borderLeftColor = "rgb(254, 78, 69)";
    document.getElementsByClassName('side-background')[0].style.visibility = "visible";
}

function side_bar_on_not_hover(obj) {
    for (let i = 0; i < document.getElementsByClassName('side-label').length; i++) {
        document.getElementsByClassName('side-label')[i].style.visibility = "hidden";
    }
    obj.parentElement.getElementsByClassName('side-label')[0].style.visibility = "hidden";
    obj.parentElement.getElementsByClassName('side-icon')[0].style.backgroundColor = "initial";
    obj.parentElement.getElementsByClassName('side-icon')[0].style.color = "rgb(169, 169, 169)";
    try {
        obj.nextElementSibling.firstElementChild.style.color = "rgb(169, 169, 169)";
    }
    catch {
        obj.firstElementChild.style.color = "rgb(169, 169, 169)";
    }
    obj.parentElement.style.borderLeftColor = "transparent";
    document.getElementsByClassName('side-background')[0].style.visibility = "hidden";
}
