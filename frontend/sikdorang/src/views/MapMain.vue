<template>
  <div>
      <div>
          <MapTheme/>
      </div>
      <div>
          <MapField/>
      </div>
      
      
  </div>
</template>

<script>
import MapField from '../components/Map/MapField'
import MapTheme from '../components/Map/MapTheme'
export default {
    name:'MapMain',
    components : {
        MapField,
        MapTheme,
    },

}
</script>

<style>

</style>