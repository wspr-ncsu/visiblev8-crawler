<script>
	import ElementPlus from 'element-plus'
	import * as apis from "@/apis/getResults"
	import router from '@/router';
	
	export default {
		name: 'History',
		data(){
			return{
				historyData: []
			}
		},
		methods: {
			getHistory: function () {
				apis.getHistory().then(res => {
					// For each result in the response data, append to the historyData array
					for (var i = 0; i < res.data.length; i++) {
						this.historyData.push( {
							// Add the id
							"id": res.data[i].submission_id,
							// Add the url
							"url": res.data[i].url,
							// Parse the date and time
							"timeStamp": new Date(res.data[i].start_time),
						});
					}
				});
			},
			/**
			 * When a row is clicked, redirect to the corresponding result page
			 * @param {*} row Get the id of the row that was clicked
			 * @param {*} column The column that was clicked
			 * @param {*} event 
			 */
			goToResult: function(row, column, event) {
				// console.log(row.id)
				router.push("/result/" + row.id)
			}
		},
		mounted: function() {
			this.getHistory();
		}
	}
</script>

<template>
	<div>
    	<div class="history">
			<h1>History</h1>
			<!-- When the row is clicked, go to the result page tied to its id -->
			<el-table :data="historyData" style="width: 100%" @row-click="goToResult">
				<el-table-column prop="url" label="URL" />
				<el-table-column prop="timeStamp" label="TimeStamp" />
			</el-table>
		</div>
	</div>
</template>

<style>
.history{
	text-align: center;
	margin-left: 5%;
	margin-right: 5%;
}

</style>

