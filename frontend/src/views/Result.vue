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
				loading: true,
				loaded: false,
				error: null,
				data: Tree = [
					{
						label: 'Level one 1',
						children: [
						{
							label: 'Level two 1-1',
							children: [
							{
								label: 'Level three 1-1-1',
							},
							],
						},
						],
					},
					{
						label: 'Level one 2',
						children: [
						{
							label: 'Level two 2-1',
							children: [
							{
								label: 'Level three 2-1-1',
							},
							],
						},
						{
							label: 'Level two 2-2',
							children: [
							{
								label: 'Level three 2-2-1',
							},
							],
						},
						],
					},
					{
						label: 'Level one 3',
						children: [
						{
							label: 'Level two 3-1',
							children: [
							{
								label: 'Level three 3-1-1',
							},
							],
						},
						{
							label: 'Level two 3-2',
							children: [
							{
								label: 'Level three 3-2-1',
							},
							],
						},
						],
					},
				]
			}
		},
		methods: {
			swapLoad () {
				this.loading = !this.loading
				this.loaded = !this.loaded
				console.log(await getGetsCount(4))
			}
			
		},
	}
</script>

<template>
	<div>
		<div v-if="loading" class="loading">
			<el-progress
				:percentage="25"
				:indeterminate="true"
				:show-text=false
				:stroke-width=10
				@click.native="swapLoad"
			/>
		</div>

		<div v-if="loaded" class="results">
			<el-row>
				<el-col class="treeCol" :span="12">
					<el-tree
						:data="data"
						node-key="id"
						:expand-on-click-node="false"
						:render-content="renderContent"
					/>
				<div class="grid-content bg-purple" /></el-col>
				<!--
					TODO
					fill in the results
				-->
				<el-col :span="12">
					<el-row class="graphs">
						<PieGraph class="graph" />
						<BarGraph />
					</el-row>
					<el-row class="source">
						example source text
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

