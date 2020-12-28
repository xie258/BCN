<template>
    <!-- 步骤条组件 -->
    <div class="divsteps">
      <el-steps :active="active" space="40%"  align-center  finish-status="success">
        <el-step title="步骤 1" ></el-step>
        <el-step title="步骤 2" ></el-step>
        <el-step title="步骤 3" ></el-step>
      </el-steps>
    </div>
  </template>
  
  <script>
  export default {
      name:"HomeHeader",
      data() {
        return {
          active: 1  //在哪一步
      };
    },

    methods: {
      // 步骤条状态改变函数，需绑定dom来调用
      next() {
        if (this.active++ > 2) this.active = 0;
      }
    }
  }

  </script>


  <style scoped>
  .divsteps{
  padding: 15px;
}
  </style>