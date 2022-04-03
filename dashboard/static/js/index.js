const IMG_KEY = [
    "brightness",
    "saturation",
    "contrast",
    "blue-blance",
    "red-blance",
    "reduce-highlight"
];
const CAMERA_KEY = [
    "width",
    "height",
    "fps",
    "brightness",
    "contrast",
    "saturation",
    "hue",
    "gain",
    "exposure"
];

function on_load() {
    includeHTML();
    hash_href();
}

var editor;
function import_monaco() {
    require.config({ paths: { vs: '../static/js/monaco-editor/min/vs' } });
    require(['vs/editor/editor.main'], function () {
        monaco.editor.setTheme('vs-dark');
        editor = monaco.editor.create(document.getElementById('monaco'), {
            language: 'python'
        });
        request_code();
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
            camera_change();
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
    if (value_pre == 0) {
        value_pre = 0;
    }
    obj.nextElementSibling.textContent = before + value_pre + after;
}
function slider_reset(obj, value=0) {
    obj.value = value;
    try {
        obj.oninput();
    }
    catch {}
    send_camera();
}

function camera_change() {
    let camera_id;
    try {
        camera_id = document.getElementById("camera-select").value;
    }
    catch {
        camera_id = 0;
    }
    let img = document.getElementById("camera-stream");
    img.src = "/camera_" + value + "?" + Date.now();
    request_camera();
    let hash = window.location.hash.replace("#", "");
    if (hash == "advance") {
        request_code();
    }
}

function request_camera() {
    let camera_id, config_id;
    try {
        camera_id = document.getElementById("camera-select").value;
    }
    catch {
        camera_id = 0;
    }
    try {
        config_id = document.getElementById("config-select").value;
    }
    catch {
        config_id = 0;
    }
    let data = {
        "camera-id": parseInt(camera_id),
        "config-id": parseInt(config_id),
    };
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader("Request-type", "request_camera");
    xhr.send(JSON.stringify(data));
    xhr.onload = function () {
        let img_data = JSON.parse(xhr.responseText).config.image;
        for (let i = 0; i < IMG_KEY.length; i++) {
            let key = IMG_KEY[i];
            let target_element = document.getElementById(key);
            target_element.value = img_data[key];
            try {
                target_element.oninput();
            }
            catch {}
        }
        let camera_data = JSON.parse(xhr.responseText).config.camera;
        for (let i = 0; i < CAMERA_KEY.length; i++) {
            let key = CAMERA_KEY[i];
            document.getElementById("camera-" + key).value = camera_data[key];
        }
    };
}
function send_camera() {
    let camera_id, config_id;
    try {
        camera_id = document.getElementById("camera-select").value;
    }
    catch {
        camera_id = 0;
    }
    try {
        config_id = document.getElementById("config-select").value;
    }
    catch {
        config_id = 0;
    }
    let data = {
        "camera-id": parseInt(camera_id),
        "config-id": parseInt(config_id),
        "config":{
            "image":{},
            "camera":{}
        }
    };
    for (let i = 0; i < IMG_KEY.length; i++) {
        let key = IMG_KEY[i];
        let value = document.getElementById(key).value;
        data.config.image[key] = parseFloat(value);
    }
    for (let i = 0; i < CAMERA_KEY.length; i++) {
        let key = CAMERA_KEY[i];
        let value = document.getElementById("camera-" + key).value;
        data.config.camera[key] = parseFloat(value);
    }
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader("Request-type", "send_camera");
    xhr.send(JSON.stringify(data));
}

function request_code() {
    let camera_id, config_id;
    try {
        camera_id = document.getElementById("camera-select").value;
    }
    catch {
        camera_id = 0;
    }
    try {
        config_id = document.getElementById("config-select").value;
    }
    catch {
        config_id = 0;
    }
    let data = {
        "camera-id": parseInt(camera_id),
        "config-id": parseInt(config_id),
    };
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader("Request-type", "request_code");
    xhr.send(JSON.stringify(data));
    xhr.onload = function () {
        code = JSON.parse(xhr.responseText).code;
        try {
            editor.setValue(code);
        }
        catch {}
        let switch_element = document.getElementById("enable-code");
        if (JSON.parse(xhr.responseText).enable) {
            switch_element.value = 1;
        }
        else {
            switch_element.value = 0;
        }
        switch_element.onclick();
    };
}
function send_code() {
    let camera_id, config_id, enable;
    try {
        camera_id = document.getElementById("camera-select").value;
    }
    catch {
        camera_id = 0;
    }
    try {
        config_id = document.getElementById("config-select").value;
    }
    catch {
        config_id = 0;
    }
    if (document.getElementById("enable-code").value == 0) {
        enable = false;
    }
    else {
        enable = true;
    }
    let data = {
        "camera-id": parseInt(camera_id),
        "config-id": parseInt(config_id),
        "code": editor.getValue(),
        "enable": enable
    };
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader("Request-type", "send_code");
    xhr.send(JSON.stringify(data));
}

function test() {
    console.log(editor.getValue());
}