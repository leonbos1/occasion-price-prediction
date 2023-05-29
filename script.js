function predictPrice() {
    var brand = document.getElementById("brand").value;
    var model = document.getElementById("model").value;
    var buildyear = document.getElementById("buildyear").value;
    var mileage = document.getElementById("mileage").value;
    var power = document.getElementById("power").value;

    if (brand == "" || model == "" || buildyear == "" || mileage == "" || power == "") {
        alert("Please fill in all fields");
        return;
    }

    var url = "http://localhost:8000/predict?brand=" + brand + "&model=" + model + "&buildyear=" + buildyear + "&mileage=" + mileage + "&power=" + power;

    var resultElement = document.getElementById("result");

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            resultElement.innerHTML = "The predicted price is: " + data.price;
        });
}