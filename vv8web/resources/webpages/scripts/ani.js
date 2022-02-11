document.onreadystatechange = function () {
    if (document.readyState == "complete") {    
        $(".loading").hide();
        $('body').css('overflow','scroll');
    }
  }