<template>
  <div>
      <div class="map-top">
			<!-- <div class="search-tap">	
				<input
				id="search-box"
				v-model="destination" 
				@keyup.enter="findPath()"
				placeholder="어디갈래?">
				<button id="search-btn" @click="findPath()" >아이콘</button>
			</div> -->
			
			<div class="tag-tap">
				<button v-for="(tag, idx) in tags" :key="idx" @click="onClick(tag)">{{ tag }}</button>
			</div>
		</div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
    name : 'MapTheme',
    data() {
        return{
            destination : "",
			tags: [],
        }
	},
	computed: {
		...mapGetters('mapEvent', ['getTags'])
	},
	watch: {
		getTags() {
			this.tags = this.getTags
		},
	},
	methods: {
		...mapActions('mapEvent', ['actionSelectTag']),
		onClick(tag) {
			this.actionSelectTag(tag)
		}
	}
}
</script>

<style>
.map-top {
	position: absolute;
	z-index: 10;
	width: 400px;
	margin: auto;
	
}

.search-tap {
	background-color: rgba(255, 255, 255, 0.8);
	width: 400px;
	height: 30px;
	margin: auto;
}

#search-box {
    width: 342px;
    height: 30px;
    float: left;
}

#search-btn {
    width: 50px;
    height: 36px;
    float: right;
}

.tag-tap {
	width: 400px;
	margin: auto;
}

.tag-tap > button {
	margin: 10px;
	background-color: yellow;
}



</style>