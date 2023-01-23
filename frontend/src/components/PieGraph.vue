<template>
    <div>
        <svg width=200 height=200 id="pie" onload="generatePie()"></svg>
    </div>
</template>

<script>
    import * as d3 from "d3";
    import * as apis from "@/apis/getResults"

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
            },
            id: {
                type: Number,
                required: true
            }
        },
        data(){
            return{
                data: [],
            }
        },
		methods: {
            /**
             * Clear the data array and the graph
             */
            clearData: function() {
                d3.select("#pie").selectAll("*").remove();
                this.data = [];
            },
            /**
             * Gets the data based on the props passed in
             */
            getData: function () {
                if(this.gets) {
                    apis.getGetsCount(this.id).then(res => {
                        this.data.push({
                            name: "get",
                            share: res.data
                        });
                    });
                }
                if(this.sets){
                    apis.getSetsCount(this.id).then(res => {
                        this.data.push({
                            name: "set",
                            share: res.data
                        });
                    });
                }
                if(this.calls){
                    apis.getCallsCount(this.id).then(res => {
                        this.data.push({
                            name: "function calls",
                            share: res.data
                        });
                    });
                }
                if(this.objects){
                    apis.getConstructionsCount(this.id).then(res => {
                        this.data.push({
                            name: "objects",
                            share: res.data
                        });
                    });
                }
                // wait a second
                setTimeout(() => {
                    // log the data
                    // console.log(this.data)
                    // generate the pie
                    this.generatePie()
                }, 1000);
            },
            generatePie: function(){

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
            // Get the data and wait for it to be loaded
            this.getData();
            // Once the data is loaded, generate the pie
            // this.generatePie();
        }
    }
</script>


<style scoped>

</style>