<template>
  <div>
      
      <div v-for="theme in themes" :key="theme.id" class="d-flex">
          <img class="img-circle" :src="require(`../../../public/photos/${posefiles[idx].file_reference}`)">
          <div>{{theme.store_name}}</div>
      </div>
  </div>
</template>

<script>
export default {
    name : 'ThemePage',
}
</script>

<style scoped>
.img-circle {
  display: inline-block;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border : 2px solid rgba(242, 157, 143);

  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
}

</style>