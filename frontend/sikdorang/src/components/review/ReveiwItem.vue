<template>
    <div>
      <div class="row m-0">
        <div class="col-8 p-0">
          <div class="store-name">{{ storeName }}</div>
          <div class="review-date">{{ review.updated_at.substr(0,10) }}</div>
        </div>
        <div class="col-4 p-0 rating row m-0">
          <div class="my-auto list">
            <li @click="rate(star)" v-for="star in maxStars" :class="{ 'active': star <= review.score }" :key="star.stars" class="star">
              <i :class="star <= review.score ? 'fas fa-star' : 'far fa-star'"></i> 
            </li>
          </div>
        </div>
      </div>
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
        display: inline-block;
        margin-left: auto;
        margin-right: 5px;
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
.store-name {
    font-size: 15px;
    font-weight: bolder;
}
.review-date {
    font-size: 13px;
}
</style>