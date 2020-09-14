<template>
  <div>
      <h1>음식점 골라골라</h1>
      <MapField/>
      <MapTheme/>
  </div>
</template>

<script>
import MapField from '../components/Map/MapField'
import MapTheme from '../components/Map/MapTheme'
export default {
    name:'Map',
    components : {
        MapField,
        MapTheme,
    },

}
</script>

<style>

</style>