// On form submit, alert the user of the form data.
function reqListener() {
    console.log(this.responseText)
}

function submitForm() {
    var urlForm = document.getElementById("search-container");
    var endpoint = "/api/v1/url"
    var formData = new FormData(urlForm);
    var xhr = new XMLHttpRequest();
    xhr.addEventListener("load", reqListener);

    // Send the form data to the server.
    xhr.open("POST", endpoint, true);
    xhr.send(formData);
    alert(formData.get("request"));
}

// Add event listener to form
const form = document.getElementById("search-container");
form.addEventListener("submit", submitForm);