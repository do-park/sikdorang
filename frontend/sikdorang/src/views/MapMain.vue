<template>
  <div>
      <div v-if="flag">
          <SelectStart   
          @flag="flagValue"
          />
          
      </div>
      <div v-if="!flag">
          <MapTheme/>
          <MapField @getKakao="getKakao" @selectedMarker="selectedMarker"/>
          <MapCards :kakao="kakao" :selected="selected"/>
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
        MapCards,
    
    },
    mounted() {
        this.flag = true
    },
    data() {
        return {
            map : null,
            flag : true,
            destination : '',
            kakao : null,
            selected : null,
            showModal : false,
        }
    },
    methods : {
        flagValue(value) {
            this.flag = value
        },
        getKakao(kakao) {
            this.kakao = kakao
        },
        selectedMarker(idx) {
            this.selected = idx
        }
    },

}
</script>

<style>

</style>