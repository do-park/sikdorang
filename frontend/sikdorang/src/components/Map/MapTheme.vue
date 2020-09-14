<template>
  <div>
      <div class="map-top">
			<div class="search-tap">	
				<!-- 길찾기  -->
				<span> 
					<input
					id="search-box"
					v-model="destination" 
					@keyup.enter="findPath()"
					placeholder="어디갈래?">
					<button id="search-btn" @click="findPath()" >아이콘</button>
				</span>
			</div>
			
			<div class="tag-tap">
				<button>#위대한</button>
				<button>#가성비</button>
				<button>#갬성</button>
				<button>#분위기</button>
				<!-- <button>#저쩌구</button>
				<button>#스크롤을</button>
				<button>#시도해보자</button> -->
			</div>
		</div>
  </div>
</template>

<script>
export default {
    name : 'MapTheme',
}
</script>

<style>
.map-top {
	position: absolute;
	z-index: 10;
	width: 100%;
	margin: auto;
	
}

.search-tap {
	background-color: rgba(255, 255, 255, 0.8);
	width: 400px;
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