<script>
  import URLSubmissionVue from "@/components/URLSubmission.vue";

  export default {
    name: 'App',
    components: {
      URLSubmission: URLSubmissionVue,
    },
  }
</script>

<template>
  <div class="common-layout">
    <el-container class="centered">
      <el-main>
          <video width="500" height="400" muted="" autoplay="">
            <source src="@/assets/vv8logo/vv8logo.webm" type="video/webm">
            <source src="@/assets/vv8logo/vv8logo.mp4" type="video/mp4">
          </video>
          <div class="container">
            <URLSubmission />
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

