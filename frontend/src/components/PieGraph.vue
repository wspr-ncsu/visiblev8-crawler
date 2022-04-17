<template>
    <div>
        <svg width=200 height=200 id="pie" onload="generatePie()"></svg>
    </div>
</template>

<script>
    import * as d3 from "d3";

    export default{
        props: {
            gets: {
                type: Boolean,
                default: false
            },
            sets: {
                type: Boolean,
                default: false
            },
            calls: {
                type: Boolean,
                default: false
            },
            objects: {
                type: Boolean,
                default: false
            }
        },
        data(){
            return{
                data: [],
            }
        },
		methods: {
            generatePie: function(){
                console.log("this.gets = " + this.gets)
                if(this.gets){
                    this.data = [{
                        name: "get",
                        share: 40.01
                    }]
                }
                console.log(this.data)
                if(this.sets){
                    this.data.push({
                        name: "set",
                        share: 30.92
                    })
                }
                if(this.calls){
                    this.data.push({
                        name: "function calls",
                        share: 15.42
                    })
                }
                if(this.objects){
                    this.data.push({
                        name: "other",
                        share: 13.65
                    })
                }

                var svg = d3.select("#pie"),
                    width = svg.attr("width"),
                    height = svg.attr("height"),
                    radius = Math.min(width, height) / 2,
                    g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

                var color = d3.scaleOrdinal(['#4daf4a', '#377eb8', '#ff7f00', '#984ea3', '#e41a1c']);
                var ordScale = d3.scaleOrdinal()
                    .domain(this.data)
                    .range(['#ffd384', '#94ebcd', '#fbaccc', '#d3e0ea', '#fa7f72']);
                // Generate the pie
                var pie = d3.pie().value(function(d) {
                    return d.share;
                });

                // Generate the arcs
                var arc = d3.arc()
                    .innerRadius(0)
                    .outerRadius(radius);

                var label = d3.arc()
                    .innerRadius(0)
                    .outerRadius(radius + 20);

                //Generate groups
                var arcs = g.selectAll("arc")
                    .data(pie(this.data))
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
        },
        mounted(){
            this.generatePie()
        }
    }
</script>


<style scoped>

</style>