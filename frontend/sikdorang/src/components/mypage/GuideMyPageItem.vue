<template>
  <div>
		<div class="item-title">{{item.title}}</div>
		<div class="item-people">({{item.now_person}}/{{item.limit_person}})</div>
		<div class="item-date">{{ item.start_date }}~{{ item.end_date }}</div>
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

</style>