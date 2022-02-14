// On form submit, alert the user of the form data.
function submitForm() {
    var form = document.getElementById("search-container");
    var formData = new FormData(form);
    var xhr = new XMLHttpRequest();
    // xhr.open("POST", "/submit", true);
    // xhr.onload = function() {
    //     if (xhr.status === 200) {
    //         alert(xhr.responseText);
    //     }
    // };
    // xhr.send(formData);
    alert(formData);
}
