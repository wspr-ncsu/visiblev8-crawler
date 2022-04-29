<template>
    <div>
        <svg width=430 height=345 id="bar" onload="generateBar()"></svg>
    </div>
</template>

<script>
    import * as d3 from "d3";
    import * as apis from "@/apis/getResults"

    export default{
        // Props to be passed in
        props: {
            // If true, render the get requests
            gets: {
                type: Boolean,
                default: false
            },
            // If true, render the set requests
            sets: {
                type: Boolean,
                default: false
            },
            // If true, render the call requests
            calls: {
                type: Boolean,
                default: false
            },
            // If true, render the object requests
            objects: {
                type: Boolean,
                default: false
            },
            // Use the id passed from the parent component
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
                d3.select("#bar").selectAll("*").remove();
                this.data = [];
            },
            /**
             * Gets the data based on the props passed in
             */
            getData: function() {
                // If the gets prop is true, get the number of gets made
                if(this.gets) {
                    // Make a request to get the data
                    apis.getGetsCount(this.id).then(res => {
                        // Add the data to the data array
                        this.data.push({
                            name: "get",
                            share: res.data
                        });
                    });
                }
                // If the sets prop is true, get the number of sets made
                if(this.sets){
                    apis.getSetsCount(this.id).then(res => {
                        // Add the data to the data array
                        this.data.push({
                            name: "set",
                            share: res.data
                        });
                    });
                }
                // If the calls prop is true, get the number of calls made
                if(this.calls){
                    apis.getCallsCount(this.id).then(res => {
                        // Add the data to the data array
                        this.data.push({
                            name: "function calls",
                            share: res.data
                        });
                    });
                }
                // If the objects prop is true, get the number of objects made
                if(this.objects){
                    apis.getConstructionsCount(this.id).then(res => {
                        // Add the data to the data array
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
                    this.generateBar()
                }, 1000);
            },
            /**
             * Generates the Bar graph
             */
            generateBar: function() {
                if(this.gets){
                    this.data = [{
                        name: "get",
                        share: apis.getGetsCount(this.id)
                    }]
                }
                if(this.sets){
                    this.data.push({
                        name: "set",
                        share: apis.getSetsCount(this.id)
                    })
                }
                if(this.calls){
                    this.data.push({
                        name: "function calls",
                        share: apis.getCallsCount(this.id)
                    })
                }
                if(this.objects){
                    this.data.push({
                        name: "objects",
                        share: apis.getConstructionsCount(this.id)
                    })
                }
                // Code to generate the bar graph
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
        /**
         * When the component is created, get the data
         */
        mounted(){
            // get the data
            this.getData()
            // generate the bar
            // this.generateBar()
        }
    }

    
</script>


<style scoped>

</style>