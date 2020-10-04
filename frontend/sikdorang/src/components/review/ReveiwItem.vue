<template>
    <div>
      <div class="row m-0 target-top">
        <div class="col-8 p-0 my-auto" @click="ReviewDetail">
          <div class="store-name">
            {{ storeName }}
            <i class="fas fa-chevron-down down-arrow"></i>
            <i class="fas fa-chevron-up up-arrow d-none"></i>
          </div>
        </div>
        <div class="col-4 p-0 rating row m-0">
          <div class="col-12 p-0 list">
            <li @click="rate(star)" v-for="star in maxStars" :class="{ 'active': star <= review.score }" :key="star.stars" class="star">
              <i :class="star <= review.score ? 'fas fa-star' : 'far fa-star'"></i> 
            </li>
          </div>
          <div class="col-12 p-0 review-date">{{ review.updated_at.substr(0,10) }}</div>
        </div>
      </div>
      <viewer class="d-none" v-if="review.content" :initialValue="review.content"/>
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
      ReviewDetail(e) {
        var target = e.target
        while (!(target.classList.contains('target-top'))) {
          target = target.parentNode
        }
        var downArrow = target.firstChild.firstChild.firstChild.nextSibling
        var upArrow = target.firstChild.firstChild.firstChild.nextSibling.nextSibling
        if (target.nextSibling.classList.contains('d-none')) {
          target.nextSibling.classList.remove('d-none')
          upArrow.classList.remove('d-none')
          downArrow.classList.add('d-none')
        } else {
          target.nextSibling.classList.add('d-none')
          upArrow.classList.add('d-none')
          downArrow.classList.remove('d-none')
        }
      },
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
  text-align: right;
  .list {
    display: block;
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