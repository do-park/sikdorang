<template>
  <div class="row m-0">
		<div class="col-10 p-0" @click="goDetail">
			<div class="item-title text-truncate">[{{item.area}}]{{item.title}} ({{item.now_person}}/{{item.limit_person}})</div>
			<div class="item-date">{{ item.start_date }}~{{ item.end_date }}</div>
		</div>
		<div class="col-2 p-0 row m-auto">
			<i class="fas fa-caret-square-down fa-2x mx-auto" @click="showPeople"></i>
			<i class="fas fa-caret-square-up fa-2x mx-auto d-none" @click="hidePeople"></i>
		</div>
		<div class="col-10 p-0 pt-2 row m-0 d-none">
			<div class="col-6 p-0 col-title">신청자명</div>
			<div class="col-6 p-0 col-title">연락처</div>
			<div class="col-12 p-0" v-for="person in people" :key="person.phone_number">
				<GuideApplicant :applicant="person" />
			</div>
		</div>
  </div>
</template>

<script>
import GuideApplicant from './GuideApplicant.vue'

export default {
	name: "GuideMyPageItem",
	components: {
    GuideApplicant,
  },
  props: {
		item: Object,
	},
	data() {
		return {
			people: null,
		}
	},
	watch: {
		item() {
			this.getPeople()
		}
	},
	mounted() {
		this.getPeople()
	},
  methods: {
		showPeople(e) {
			e.target.parentNode.nextSibling.classList.remove('d-none')
			e.target.nextSibling.classList.remove('d-none')
			e.target.classList.add('d-none')
		},
		hidePeople(e) {
			e.target.parentNode.nextSibling.classList.add('d-none')
			e.target.previousSibling.classList.remove('d-none')
			e.target.classList.add('d-none')
		},
		getPeople() {
			this.$axios
			.get(`/guide/paider/${this.item.id}`)
			.then((res) => {
						this.people = res.data
			})
			.catch((err) => {
				console.log(err);
			});
		},
		goDetail() {
			this.$router.push(`/trip/detail/${this.item.id}`)
		}
  },
  
}
</script>

<style>
.item-title {
	font-size: 16px;
}
.item-date {
	font-size: 12px;
}
.col-title {
	text-align: center;
	background-color: crimson;
	color: white;
}
</style>