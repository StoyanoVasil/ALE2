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
        console.log(json);
        document.getElementById("aut-img").src = "../static/pics/" + json["img"] + ".png";
        document.getElementById("aut-type").innerText = "DFA: " + json["dfa"].toString();
    }
};
