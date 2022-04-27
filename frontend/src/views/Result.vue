<script>
	import ElementPlus from 'element-plus'
	import PieGraph from "@/components/PieGraph.vue"
	import BarGraph from "@/components/BarGraph.vue"
	import TreeStructure from "@/components/Tree.vue"
	import * as apis from "@/apis/getResults"
	
	import { useRouter, useRoute } from "vue-router"

	const router = useRouter()

	export default {
		name: 'Result',
		components: {
			PieGraph: PieGraph,
			BarGraph: BarGraph,
			TreeStructure: TreeStructure
		},
		data(){
			return{
				currentContext: 4,
				data: [],
				sourceText: "",
			}
		},
		methods: {
			getSourceText: function() {
				apis.getSource(this.$route.params.id, this.currentContext).then(res => {
					this.sourceText = res.data
				});
			},
			onload () {
				console.log("id")
				console.log(this.$route.params.id)
				// Get the source text
				this.getSourceText()
				console.log("sourceText" + this.sourceText)
				// reload the component
				this.$forceUpdate()
			},
			onTargetSelect(data){
				this.currentContext = data.node-key;
				onload()
			},
			onTreeClick(data){
				console.log(data)
				this.currentContext = data;
				this.getSourceText()
			},
		},
		onload(){
			this.onload()
		},
		beforeRouteLeave(to, from, next) {
			console.log("beforeRouteLeave")
			// remove the pie and bar graphs
			PieGraph.methods.clearData();
			BarGraph.methods.clearData();
			next();
		},
	}
</script>

<template>
	<div onload="onload()">
		<!--
		<div v-if="loading" class="loading">
			<el-progress
				:percentage="25"
				:indeterminate="true"
				:show-text=false
				:stroke-width=10
				@click.native="swapLoad"
			/>
		</div>-->

		<div class="results">
			<el-row>
				<el-col class="treeCol" :span="12">
					<Tree :id="this.$route.params.id" @clicked="onTreeClick"/>
				<div class="grid-content bg-purple" /></el-col>
				<el-col :span="12">
					<el-row class="graphs" justify="center">
						<!-- Put new graphs here as Vue.js components -->
						<PieGraph class="graph" :gets=true :sets=true :id="this.$route.params.id" />
						<BarGraph :sets=true :calls=true :objects=true :id="this.$route.params.id" />
					</el-row>
					<el-row class="source">
						{{ this.sourceText == "" ? "No source code available, please select an execution context from the tree." : this.sourceText }}
					</el-row>
				</el-col>
			</el-row>
		</div>
	</div>
</template>

<style scoped>
.loading{
	min-height: 10px;
	width: 95%;
	margin: 0 auto;
}
.graphs{
	width: 50vw;
	min-height: 49vh;
	border-bottom: 2px solid black;
}
.source{
	width: 50vw;
	min-height: 49vh;
	overflow: scroll;
}
.treeCol{
	float: left;
	width: 50vw;
	min-height: 100vh;
	border-right: 2px solid black;
}

.graph{
	margin: 5px;
}

</style>

