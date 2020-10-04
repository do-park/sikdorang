<template>
  <div class="row m-0">
		<div class="col-10 p-0">
			<div class="item-title text-truncate">[{{item.area}}]{{item.title}} ({{item.now_person}}/{{item.limit_person}})</div>
			<div class="item-date">{{ item.start_date }}~{{ item.end_date }}</div>
		</div>
		<div class="col-2 p-0">
			<i class="fas fa-caret-square-down"></i>
		</div>
		
  </div>
</template>

<script>

export default {
  name: "GuideMyPageItem",
  props: {
    item: Object
	},
  methods: {

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