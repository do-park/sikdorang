<template>
  <div>
	<FoodIdealTagCup v-if="!isStoreStage" @done="done"/>
	<transition enter-active-class="animated fadeInLeft">
		<StoreIdealTagCup v-if="isStoreStage"/>
	</transition>
  </div>
</template>

<script>
import FoodIdealTagCup from '@/components/idealtagcup/FoodIdealTagCup.vue'
import StoreIdealTagCup from '@/components/idealtagcup/StoreIdealTagCup.vue'

export default {
	name: 'IdealTagCupView',
	components: {
		FoodIdealTagCup,
		StoreIdealTagCup,
	},
	data() {
		return {
			isStoreStage: false,
		}
	},
	methods: {
		done() {
			this.isStoreStage = true
		}
	}
}
</script>

<style scoped>
@import "https://cdn.jsdelivr.net/npm/animate.css@3.5.1";
</style>