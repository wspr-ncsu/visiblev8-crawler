// document.onreadystatechange = function () {
//     if (document.readyState == "complete") {
//         $(".loading").hide();
//         $('body').css('overflow','scroll');
//     }
//   }

function logBreaker() {

  document
    .getElementById("fileInput")
    .addEventListener("change", function selectedFileChanged() {
      if (this.files.length === 0) {
        console.log("Choose file")
        return
      }

      const reader = new FileReader()
      reader.onload = function fileReadCompleted() {
        // after reading, the result is in reader.result
        console.log(reader.result)
        var left = document.getElementById("left_part")
        left.textContent = reader.result
        
      }
      reader.readAsText(this.files[0])
      
    })
}

logBreaker()
