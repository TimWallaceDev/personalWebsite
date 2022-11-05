fetch("http://127.0.0.1:8000/generator/gold")
.then((response) => response.text())
.then((data) => console.log("data", data ,"endofdata"));