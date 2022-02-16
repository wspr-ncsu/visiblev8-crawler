// On form submit, alert the user of the form data.
function submitForm() {
    var form = document.getElementById("search-container");
    var formData = new FormData(form);
    var xhr = new XMLHttpRequest();

    // Send the form data to the server.
    // xhr.open("POST", "/api/v1/url", true);
    // xhr.send(formData);
    alert(formData.get("url"));
}

// Add event listener to form
const form = document.getElementById("search-container");
form.addEventListener("submit", submitForm);