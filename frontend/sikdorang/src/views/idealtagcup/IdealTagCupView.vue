<template>
  <div>
		<FoodIdealTagCup v-if="!isStoreStage" @done="done"/>
		<StoreIdealTagCup v-if="!isStoreStage"/>
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

<style>

</style>