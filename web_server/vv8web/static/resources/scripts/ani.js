// if finish loading, the loading animation stop
document.onreadystatechange = function() {
    if (document.readyState == "complete") {
        $(".loading").hide();
        $('body').css('overflow', 'scroll');
    }
}



// get the log file, not finished yet
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



    var data = [{
        name: "get",
        share: 40.01
    }, {
        name: "set",
        share: 30.92
    }, {
        name: "function calls",
        share: 15.42
    }, {
        name: "other",
        share: 13.65
    }];

    var svg = d3.select("#pie"),
        width = svg.attr("width"),
        height = svg.attr("height"),
        radius = Math.min(width, height) / 2,
        g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var color = d3.scaleOrdinal(['#4daf4a', '#377eb8', '#ff7f00', '#984ea3', '#e41a1c']);
    var ordScale = d3.scaleOrdinal()
        .domain(data)
        .range(['#ffd384', '#94ebcd', '#fbaccc', '#d3e0ea', '#fa7f72']);
    // Generate the pie
    var pie = d3.pie().value(function(d) {
        return d.share;
    });

    // Generate the arcs
    var arc = d3.arc()
        .innerRadius(70)
        .outerRadius(radius);

    var label = d3.arc()
        .innerRadius(30)
        .outerRadius(radius + 20);

    //Generate groups
    var arcs = g.selectAll("arc")
        .data(pie(data))
        .enter()
        .append("g")
        .attr("class", "arc")

    //Draw arc paths
    arcs.append("path")
        .attr("fill", function(d) {
            return ordScale(d.data.name);
        })
        .attr("d", arc);

    arcs.append('text')
        .attr("transform", function(d) {
            return "translate(" + label.centroid(d) + ")";
        })
        .text(function(d) {
            return d.data.name;
        })
        .style("font-family", "arial")
        .style("font-size", 15);

}


// for open and close the drawer
$(function() {
    var Accordion = function(el, multiple) {
        this.el = el || {};
        this.multiple = multiple || false;

        // Variables privadas
        var links = this.el.find('.link');
        // Evento
        links.on('click', { el: this.el, multiple: this.multiple }, this.dropdown)
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