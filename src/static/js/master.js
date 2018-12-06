const request = new XMLHttpRequest();

document.getElementById("submit").addEventListener("click", function () {
    var text = document.getElementById("input").value;
    if (text.length < 1) {
        alert("Please provide input!");
    } else {
        json = JSON.stringify({"text": text});
        request.open("POST", "/generate", true);
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
        document.getElementById("list-container").innerHTML = returnListItems(json["words"]);
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
    return '<ul class="list-group">' + list_items + '</ul>';
}
