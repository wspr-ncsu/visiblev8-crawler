<script>
  import URLSubmissionVue from "@/components/URLSubmission.vue";
  import { reactive } from 'vue';

  export default {
    name: 'App',
    components: {
      URLSubmission: URLSubmissionVue,
    },
    data() {
      return {
        loading : false
      }
    },
    methods: {
      changeLoading() {
        this.loading = !this.loading
      }
    },
    setup() {
      // might need it for future
      // function getLoading(val){
      //   console.log('something')
      //   console.log('loading', loading)
      //   loading = !loading
      //   console.log('loading', loading)
      // }
      // return {getLoading, loading}
      
    }
  }
</script>

<template>
  <div class="common-layout">
    
		<div v-if="loading" class="loading">
			<el-progress
				:percentage="25"
				:indeterminate="true"
				:show-text=false
				:stroke-width=10
				@click.native="swapLoad"
			/>
		</div>
    <el-container class="centered">
      <el-main>
          <video width="500" height="400" muted="" autoplay="">
            <source src="@/assets/vv8logo/vv8logo.webm" type="video/webm">
            <source src="@/assets/vv8logo/vv8logo.mp4" type="video/mp4">
          </video>
          <div class="container">
            <URLSubmission @loading="changeLoading"/>
          </div>
        </el-main>
    </el-container>
  </div>
</template>

<style>

.el-header {
    --el-header-padding: 0;
    box-sizing: border-box;
    flex-shrink: 0;
    height: var(--el-header-height);
}

.el-main {
    align-self: center;
}

</style>

