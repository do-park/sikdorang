<template>
    <div>
      <div class="row m-0">
        <div class="">{{ storeName }}</div>
        <div class="rating">
          <ul class="list">
            <li @click="rate(star)" v-for="star in maxStars" :class="{ 'active': star <= review.score }" :key="star.stars" class="star">
              <i :class="star <= review.score ? 'fas fa-star' : 'far fa-star'"></i> 
            </li>
          </ul>
        </div>
      </div>
      <viewer v-if="review.content" :initialValue="review.content"/>
      <div class="text-right">
        <small>{{ review.updated_at }}</small>
      </div>
      <hr>
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
    data() {
      return {
        maxStars: 5,
        storeName: null,
      }
    },
    mounted() {
      this.getStore()
    },
    methods: {
      getStore() {
        this.$axios.get(`trip/store_detail/${this.review.store_id}`)
        .then(res => {
            console.log(res)
            this.storeName = res.data.store_name
        })
        .catch(err => console.error(err))
      }
    }
}
</script>

<style scoped lang="scss">
.rating {
    color: #b7b7b7;
    .list {
        padding: 0;
        margin: 0;
        .star {
            display: inline-block;
            font-size: 15px; 
            &:first-child {
                margin-left: 0;
            }
            &.active {
                color: #ffe100;
            }
        }
    }
}
</style>