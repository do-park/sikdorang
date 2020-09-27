<template>
    <div>
      <div>{{ review.score }}</div>
      <viewer v-if="review.content" :initialValue="review.content"/>
    </div>
</template>

<script>
import '@toast-ui/editor/dist/toastui-editor-viewer.css'
import { Viewer } from '@toast-ui/vue-editor'

export default {
		name: "ReviewtItem",
		components: {
      viewer: Viewer,
    },
    props: {
        review: Object,
    },
    methods: {
     
    }
}
</script>

<style>

</style>