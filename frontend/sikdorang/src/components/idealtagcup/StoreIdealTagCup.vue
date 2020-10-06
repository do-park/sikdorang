<template>
	<div>
		<h3 class="text-center">{{ roundCount }}</h3>

		<div>
			<img class="img" :src="imgs[tags[leftIndex]]" alt="left Image" @click="onClick('left')" v-if="!isDone">
		</div>
		<div class="vs-wrap">
			<img class="vs" v-if="!isDone" src="@/assets/vs.png">
		</div>
		<div>
			<img class="img" :src="imgs[tags[rightIndex]]" alt="right Image" @click="onClick('right')" v-if="!isDone">
		</div>
		<div v-if="isDone" @click="done">
			<h2>1위</h2>
			<img :src="imgs[tags[0]]">
		</div>
	</div>
</template>

<script>
export default {
	name: "StoreIdealTagCup",
	data() {
		return {
			imgs: [
				require("@/assets/store_cup/cheap.jpg"),
				require("@/assets/store_cup/clean.jpg"), 
				require("@/assets/store_cup/kind.jpg"), 
				require("@/assets/store_cup/mood.jpg"), 
				require("@/assets/store_cup/interior.jpg"),
				require("@/assets/store_cup/breakfast.jpg"),
				require("@/assets/store_cup/lunch.jpg"),
				require("@/assets/store_cup/dinner.jpg"),
				require("@/assets/store_cup/friends.jpg"),
				require("@/assets/store_cup/couple.jpg"),
				require("@/assets/store_cup/family.jpg"),
				require("@/assets/store_cup/parking.jpg")
			],
			tags: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
			leftIndex: 0,
			rightIndex: 1,
			round: 1,
			clickCount: -1,
			userChoice: [],
			isDone: false,
		}
	},
	computed: {
		roundCount() {
		if (this.tags.length === 2) {
			return '결승'
		} else if (this.tags.length === 1) {
			return '우승'
		} else {
			return `${this.tags.length} 강`
		}
		},
		gameCount() {
		if (this.clickCount === -1) {
			return `1 / ${Math.round(this.tags.length / 2)}`
		} else if (this.clickCount === 1) {
			return `2 / ${Math.round(this.tags.length / 2)}`
		} else {
			return `${Math.round(this.clickCount / 2)+1} / ${Math.round(this.tags.length / 2)}`
		}
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
			if (this.tags.length === 3) {
				this.tagsSave()
			}
		},
		nextRound() {
			this.leftIndex = 0
			this.rightIndex = 1
			this.tags = this.userChoice
			this.userChoice = []
			this.round += 1
			this.clickCount = -1
			// console.log('round:', this.round)
			// console.log('tags:', this.tags)
			if (this.tags.length === 1) {
				this.isDone = true
			}
		},
		tagsSave() {
			const requestHeaders = {
				headers: {
					Authorization: `JWT ${this.$cookies.get('auth-token')}`
				}
			}
			this.$axios.post('trip/idealtag', {tags: this.tags}, requestHeaders)
			.then(() => {
				this.$store.state.mypage.userInfo.done_cup = true
			})
			.catch(err => console.erro(err))
		},
		done() {
			this.$router.push('/')
		}
	}
}
</script>

<style scoped>
.img {
	width: 400px;
	cursor: pointer;
}
.vs-wrap {
	position: relative;
	widows: 400px;
}
.vs {
	width: 100px;
	left: 50%;
	transform:translateX(-50%);
	bottom: -40px;
	position: absolute;
}
</style>