document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        $(".loading").hide();
        $('body').css('overflow','scroll');
    }
  }




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



$(function() {
	var Accordion = function(el, multiple) {
		this.el = el || {};
		this.multiple = multiple || false;

		// Variables privadas
		var links = this.el.find('.link');
		// Evento
		links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
	}

	Accordion.prototype.dropdown = function(e) {
		var $el = e.data.el;
			$this = $(this),
			$next = $this.next();

		$next.slideToggle();
		$this.parent().toggleClass('open');

		if (!e.data.multiple) {
			$el.find('.submenu').not($next).slideUp().parent().removeClass('open');
		};
	}

	var accordion = new Accordion($('#accordion'), false);
});



logBreaker()
