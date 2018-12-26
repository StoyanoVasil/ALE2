const request = new XMLHttpRequest();

document.getElementById("submit").addEventListener("click", function () {
    var text = document.getElementById("input").value;
    if (text.length < 1) {
        alert("Please provide input!");
    } else {
        document.getElementById("list-possible-words").style.display = "none";
        document.getElementById("list-container").style.display = "none";
        json = JSON.stringify({"text": text});
        request.open("POST", "/generate", true);
        request.setRequestHeader("Content-Type", "application/json");
        request.send(json);
    }
});

document.getElementById("regex").addEventListener("click", function () {
    var text = document.getElementById("regex-input").value;
    if (text.length < 1) {
        alert("Please provide input!");
    } else {
        document.getElementById("list-possible-words").style.display = "none";
        document.getElementById("list-container").style.display = "none";
        json = JSON.stringify({"regex": text});
        request.open("POST", "/regex", true);
        request.setRequestHeader("Content-Type", "application/json");
        request.send(json);
    }
});

request.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
        var json = JSON.parse(this.responseText);
        document.getElementById("aut-img").src = "../static/pics/" + json["img"] + ".png";
        document.getElementById("aut-type").innerText = "DFA: " + json["dfa"].toString();
        document.getElementById("finite").innerText = "Finite: " + json["finite"].toString();
        var list = document.getElementById("list-container");
        list.innerHTML = returnListItems(json["words"]);
        list.style.display = "block";
        if(json["finite"]) {
            var words = document.getElementById("list-possible-words");
            words.innerHTML = returnPossibleWords(json["possible_words"]);
            words.style.display = "block";
        }
    }
};

function returnListItems(array) {

    list_items = "";
    for(var i = 0; i < array.length; i++){
        var el = array[i];
        if(el[1]) {
            list_items += '<li class="list-group-item list-group-item-success">' + el[0] + '</li>';
        } else {
            list_items += '<li class="list-group-item list-group-item-danger">' + el[0] + '</li>';
        }
    }
    return '<h3>Words check:</h3><ul class="list-group">' + list_items + '</ul>';
}

function returnPossibleWords(array) {
    var textarea = document.getElementById("input");
    textarea.value += "\n\nPossible words:\n";
    list_items = "";
    for(var i = 0; i < array.length; i++){
        var el = array[i];
        textarea.value += el + "\n";
        list_items += '<li class="list-group-item list-group-item-primary">' + el + '</li>';
    }
    return '<h3>Possible Words:</h3><ul class="list-group">' + list_items + '</ul>';
}
