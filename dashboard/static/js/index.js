function on_load() {
    includeHTML();
    hash_href()
}

var editor;
function import_monaco() {
    require.config({ paths: { vs: '../static/js/monaco-editor/min/vs' } });
    require(['vs/editor/editor.main'], function () {
        monaco.editor.setTheme('vs-dark');
        editor = monaco.editor.create(document.getElementById('monaco'), {
            value: "print(\"Hello World!\")",
            language: 'python'
        });
    });
}

function hash_href() {
    let hash = window.location.hash.replace("#", "");
    if (hash == "") {
        hash = "home";
    }
    let home = document.getElementById("home");
    let setting = document.getElementById("settings");
    let global = document.getElementById("global");
    let basic = document.getElementById("basic");
    let advance = document.getElementById("advance");
    switch (hash) {
        case "home":
        case "global":
        case "basic":
        case "advance":
            home.classList.remove("not-display");
            setting.classList.add("not-display");
            switch (hash) {
                case "global":
                    global.classList.remove("not-display");
                    basic.classList.add("not-display");
                    advance.classList.add("not-display");
                    break;
                case "basic":
                    basic.classList.remove("not-display");
                    global.classList.add("not-display");
                    advance.classList.add("not-display");
                    break;
                case "advance":
                    advance.classList.remove("not-display");
                    global.classList.add("not-display");
                    basic.classList.add("not-display");
                    let monaco = document.getElementById("monaco");
                    if (monaco.children.length == 0) {
                        import_monaco();
                    }
                    break;
            }
            break;
        case "settings":
            setting.classList.remove("not-display");
            home.classList.add("not-display");
            break;
    }
}

function slider_change(obj, before="", after="", percent=0) {
    let value_pre;
    if (percent == 0) {
        value_pre = obj.value;
    }
    else {
        value_pre = percent * obj.value / obj.max;
        value_pre = value_pre.toFixed(2);
    }
    obj.nextElementSibling.textContent = before + value_pre + after;
}

function slider_reset(obj, value=0) {
    obj.value = value;
    slider_change(obj);
}

function test() {
    console.log(editor.getValue());
}