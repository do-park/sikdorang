<template>
  <div>
      <h1>MAP MAIN</h1>
      <div v-if="flag">
          <SelectStart   
          @flag="flagValue"
          />
          
      </div>
      <div v-if="!flag">
          <MapTheme/>
          <MapField/>
          <MapCards :kakao="kakao"/>
      </div>    
       
  </div>
</template>

<script>
import SelectStart from '../components/Map/SelectStart'
import MapField from '../components/Map/MapField'
import MapTheme from '../components/Map/MapTheme'
import MapCards from '../components/Map/MapCards'
export default {
    name:'MapMain',
    components : {
        SelectStart,
        MapField,
        MapTheme,
        MapCards
    },
    mounted() {
        this.flag = true
    },
    data() {
        return {
            map : null,
            flag : true,
            destination : '',
        }
    },
    methods : {
        flagValue(value) {
            this.flag = value
        },
    },

}
</script>

<style>

</style>