<script>
	import ElementPlus from 'element-plus'
	import Header from "./Header.vue"

	class Tree{
		label
		children
	}

	export default {
		name: 'Result',
		components: {
      		Header: Header,
		},
		data(){
			return{
				loading: false,
				loaded: true,
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
			
		},
	}
</script>

<template>
	<div>
		<el-row>
			<el-col :span="24"><Header /></el-col>
		</el-row>
		<div v-if="loading" class="loading">
			<!--
				TODO
				replace this with the loading bar Richardo made
			-->
		</div>

		<div v-if="loaded" class="results">
			<el-row>
				<!--
					TODO
					fill in the tree
				-->
				<el-col :span="12">
					<!--<el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick" />-->
					<el-tree
						:data="data"
						show-checkbox
						node-key="id"
						:expand-on-click-node="false"
						:render-content="renderContent"
					/>
				<div class="grid-content bg-purple" /></el-col>
				<!--
					TODO
					fill in the results
				-->
				<el-col :span="12">b<div class="grid-content bg-purple-light" /></el-col>
			</el-row>
		</div>
	</div>
</template>

<style>


</style>

