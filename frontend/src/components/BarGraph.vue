<template>
    <div>
        <svg width=430 height=345 id="bar" onload="generateBar()"></svg>
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
            generateBar: function(){
                if(this.gets){
                    // TODO = Replace with api call for gets/count
                    this.data = [{
                        name: "get",
                        share: 40.01
                    }]
                }
                if(this.sets){
                    // TODO = Replace with api call for sets/count
                    this.data.push({
                        name: "set",
                        share: 30.92
                    })
                }
                if(this.calls){
                    // TODO = Replace with api call for calls/count
                    this.data.push({
                        name: "function calls",
                        share: 15.42
                    })
                }
                if(this.objects){
                    // TODO = Replace with api call for objects/count
                    this.data.push({
                        name: "other",
                        share: 13.65
                    })
                }

                var svg = d3.select("#bar"),
                    margin = 200,
                    width = svg.attr("width") - margin,
                    height = svg.attr("height") - margin
                svg.append("text")
                    .attr("transform", "translate(100,0)")
                    .attr("x", 50)
                    .attr("y", 50)
                    .attr("font-size", "24px");

                var xScale = d3.scaleBand().range([0, width]).padding(0.4),
                    yScale = d3.scaleLinear().range([height, 0]);

                xScale.domain(this.data.map(function(d) {
                    return d.name;
                }));
                yScale.domain([0, d3.max(this.data, function(d) {
                    return d.share;
                })]);

                var g = svg.append("g")
                    .attr("transform", "translate(" + 25 + "," + 25 + ")");

                g.append("g")
                    .attr("transform", "translate(0," + height + ")")
                    .call(d3.axisBottom(xScale));

                g.append("g")
                    .call(d3.axisLeft(yScale).tickFormat(function(d) {
                        return d;
                    }).ticks(10))
                    .append("text")
                    .attr("y", 6)
                    .attr("dy", "0.71em")
                    .attr("text-anchor", "end")
                    .text("value");
                g.selectAll(".bar")
                    .data(this.data)
                    .enter().append("rect")
                    .attr("class", "bar")
                    .attr("x", function(d) {
                        return xScale(d.name);
                    })
                    .attr("y", function(d) {
                        return yScale(d.share);
                    })
                    .attr("width", xScale.bandwidth())
                    .attr("height", function(d) {
                        return height - yScale(d.share);
                    });
            }
        },
        mounted(){
            this.generateBar()
        }
    }

    
</script>


<style scoped>

</style>