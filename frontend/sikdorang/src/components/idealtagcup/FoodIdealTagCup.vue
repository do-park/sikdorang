<template>
	<div>
		<div v-if="!isDone">
			<img :src="imgs[tags[leftIndex]]" alt="left Image" @click="onClick('left')">
		</div>
		<div v-if="!isDone">
			<img :src="imgs[tags[rightIndex]]" alt="right Image" @click="onClick('right')">
		</div>
		<div v-if="isDone" @click="done">
			<h2>1위</h2>
			<img :src="imgs[tags[0]]">
		</div>
	</div>
</template>

<script>
export default {
	name: "FoodIdealTagCup",
	data() {
		return {
			imgs: [
				require("@/assets/food_cup/hansik.jpg"),
				require("@/assets/food_cup/bunsik.jpg"), 
				require("@/assets/food_cup/pizza.jpg"), 
				require("@/assets/food_cup/chicken.jpg"), 
				require("@/assets/food_cup/don_Hoe_ilsik.jpg"),
				require("@/assets/food_cup/cafe_dessert_bakery.jpg"),
				require("@/assets/food_cup/asian.jpg"),
				require("@/assets/food_cup/western.jpg"),
				require("@/assets/food_cup/chinese.jpg"),
				require("@/assets/food_cup/dosirak.jpg"),
				require("@/assets/food_cup/fastfood.jpg"),
				require("@/assets/food_cup/alcohol.jpg"),
				require("@/assets/food_cup/jokbal.jpg"),
				require("@/assets/food_cup/zzim_tang.jpg"),
			],
			tags: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
			leftIndex: 0,
			rightIndex: 1,
			round: 1,
			clickCount: -1,
			userChoice: [],
			isDone: false,
		}
	},
	methods: {
		onClick(direction) {
			this.clickCount += 2
			if (direction === 'left') {
				this.userChoice.push(this.tags[this.leftIndex])
			} else {
				this.userChoice.push(this.tags[this.rightIndex])
			}
			if (this.clickCount >= (this.tags.length-1)) {
				this.nextRound()
			} else {
				this.leftIndex = this.leftIndex+2
				this.rightIndex = this.rightIndex+2
				if (this.rightIndex > (this.tags.length-1)) {
					this.userChoice.push(this.tags[this.leftIndex])
					this.nextRound()
				}
			}
			if (this.tags.length == 2) {
				this.tagsSave()
			}
		},
		nextRound() {
			this.tags = this.userChoice
			this.userChoice = []
			this.round += 1
			this.clickCount = -1
			console.log('round:', this.round)
			console.log('tags:', this.tags)
			if (this.tags.length === 1) {
				console.log('종료 로직을 실행합니다.')
				this.isDone = true
			}
			this.leftIndex = 0
			this.rightIndex = 1
		},
		tagsSave() {
			console.log('유저 정보와 태그를 서버에 보내 저장합니다.')
			this.$axios.post()
		},
		done() {
			this.$emit('done')
		}
	},
}
</script>

<style scoped>
img {
	width: 100vh;
	height: 50vh;
}
</style>