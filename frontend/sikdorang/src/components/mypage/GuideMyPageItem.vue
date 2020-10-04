<template>
  <div class="row m-0">
		<div class="col-10 p-0">
			<div class="item-title text-truncate">[{{item.area}}]{{item.title}} ({{item.now_person}}/{{item.limit_person}})</div>
			<div class="item-date">{{ item.start_date }}~{{ item.end_date }}</div>
		</div>
		<div class="col-2 p-0 row m-auto">
			<i class="fas fa-caret-square-down fa-2x mx-auto" @click="showPeople"></i>
			<i class="fas fa-caret-square-up fa-2x mx-auto d-none" @click="hidePeople"></i>
		</div>
		<div class="d-none">
			
		</div>
  </div>
</template>

<script>

export default {
  name: "GuideMyPageItem",
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
			console.log('fdsfsdfsdfsd')
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
				console.log(res)
				this.people = res.data
      })
      .catch((err) => {
        console.log(err);
      });
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
</style>