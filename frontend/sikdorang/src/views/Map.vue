<template>
  <div>
      <MapTheme/>
      <MapField/>
      
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