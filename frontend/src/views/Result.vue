<script>
	import ElementPlus from 'element-plus'
	import PieGraph from "@/components/PieGraph.vue"
	import BarGraph from "@/components/BarGraph.vue"
	import { getGetsCount } from "@/apis/getResults"
	
	import { useRouter, useRoute } from "vue-router"

	const router = useRouter()
	

	class Tree{
		label
		children
	}

	export default {
		name: 'Result',
		components: {
			PieGraph: PieGraph,
			BarGraph: BarGraph,
		},
		data(){
			return{
				currentContext = 0
				data: Tree = [
					
				]
			}
		},
		methods: {
			onload () {
				getSource(this.$route.params.id, currentContext).then( function(res){
					this.data.sourceText = res
				})
			},
			onTargetSelect(data){
				this.currentContext = data.node-key;
				onload()
			}
		},
	}
</script>

<template>
	<div>
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
					<el-tree
						:data="data"
						node-key="id"
						:expand-on-click-node="false"
						:render-content="renderContent"
						@node-click="onTargetSelect"
					/>
				<div class="grid-content bg-purple" /></el-col>
				<el-col :span="12">
					<el-row class="graphs">
						<!-- Put new graphs here as Vue.js components -->
						<PieGraph class="graph" :gets=true :sets=true :id="this.$route.params.id" />
						<BarGraph :sets=true :calls=true :objects=true :id="this.$route.params.id" />
					</el-row>
					<el-row class="source">
						{{ this.sourceText }}
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

