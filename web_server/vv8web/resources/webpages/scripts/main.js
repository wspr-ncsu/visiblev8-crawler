// On form submit, alert the user of the form data.
function submitForm() {
    var form = document.getElementById("search-container");
    var formData = new FormData(form);
    var xhr = new XMLHttpRequest();

    // Send the form data to the server.
    // The server is FastAPI
    // The URL is "/api/v1/url"
    xhr.open("POST", "/api/v1/url", true);
    xhr.send(formData);

    // xhr.open("POST", "/api/v1/url", true);
    // xhr.onload = function() {
    //     if (xhr.status === 200) {
    //         alert(xhr.responseText);
    //     }
    // };
    // xhr.send(formData);
    alert(formData.get("url"));
}

// Add event listener to form
const form = document.getElementById("search-container");
form.addEventListener("submit", submitForm);