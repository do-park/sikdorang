<template>
  <div class="row m-0 wrap">
		<div class="col-6 p-0 ap-name">{{applicant.user_name}}</div>
		<div class="col-6 p-0 ap-phone">{{applicant.phone_number}}</div>
  </div>
</template>

<script>

export default {
  name: "GuideApplicant",
  props: {
		applicant: Object,
	},
  methods: {
		
  },
  
}
</script>

<style scoped>
.wrap {
	font-size: 14px;
	text-align: center;
	border-bottom: 1px lightgray solid;
}
</style>