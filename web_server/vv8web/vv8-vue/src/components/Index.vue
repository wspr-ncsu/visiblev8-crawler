<script>

</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
          <ul class="navigation">
            <li class="left"><a href="history.html">History</a></li>
            <li class="title">
                <h1><a href="index.html">Visible V8</a></h1>
            </li>
            <li class="right"><a href="#/about">About</a></li>
        </ul>
      </el-header>
      <el-main>
          <video width="500" height="400" muted="" autoplay="">
            <source src="@/assets/vv8logo/vv8logo.webm" type="video/webm">
            <source src="@/assets/vv8logo/vv8logo.mp4" type="video/mp4">
          </video>
        <div class="index-search">
            <form class="index-search-container" id="search-container">
                <input name="request" type="text" placeholder="Enter URL here">
                <button type="submit"><i class="fa fa-search"></i></button>
            </form>
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

