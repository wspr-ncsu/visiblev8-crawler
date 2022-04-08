<script>
	import ElementPlus from 'element-plus'
	import Header from "./Header.vue"

	export default {
		name: 'History',
		components: {
      		Header: Header,
		},
		data(){
			return{
				historyData: [
				{
					url: 'https://example.com',
					timeStamp: '2022-04-01 13:23:49',
				},
				{
					url: 'https://sample.org',
					timeStamp: '2022-04-01 13:25:34',
				},
				{
					url: 'https://cnn.com',
					timeStamp: '2022-04-01 13:30:12',
				},
				{
					url: 'https://test.com',
					timeStamp: '2022-04-01 13:33:53',
				},
				]
			}
		}
	}
</script>

<template>
  <div>
	<el-row>
		<el-col :span="24"><Header /></el-col>
	</el-row>
    <div class="history">
		<h1>History</h1>
		<el-table :data="historyData" style="width: 100%">
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

