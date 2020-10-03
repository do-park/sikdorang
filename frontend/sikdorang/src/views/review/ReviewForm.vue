<template>
  <div class="mt-5">
    <h5 class="text-center">{{ storeName }}</h5>
    <div class="rating">
      <ul class="list">
        <li @click="rate(star)" v-for="star in maxStars" :class="{ 'active': star <= reviewData.score }" :key="star.stars" class="star">
          <i :class="star <= reviewData.score ? 'fas fa-star' : 'far fa-star'"></i> 
        </li>
      </ul>
      <div v-if="hasCounter" class="info counter">
        <span class="score-rating">{{ reviewData.score }}</span>
        <span class="divider">/</span>
        <span class="score-max">{{ maxStars }}</span>
      </div>
    </div>
    <editor
      ref="toastuiEditor"
      :initialValue="editorText"
      :options="editorOptions"
      height="200px"
      initialEditType="wysiwyg"
      previewStyle="vertical"
    />
    <div class="text-center my-4">
      <button class="btn btn-secondary" @click="onClick()">작성완료</button>
    </div>
    
  </div>
</template>

<script>
import "codemirror/lib/codemirror.css";
import "@toast-ui/editor/dist/toastui-editor.css";
import { Editor } from "@toast-ui/vue-editor";

export default {
  name: "ReviewForm",
  components: {
    editor: Editor,
  },
  data() {
    return {
      maxStars: 5,
      hasCounter: "true",
      storeId: this.$cookies.get("review-store-id"),
      storeName: null,
      reviewData: {
        score: 3,
        content: null,
      },
      editorText: "방문 후기를 작성해주세요.",
      editorOptions: {
        hideModeSwitch: true,
      },
    };
  },
  mounted() {
    this.getStore()
  },
  methods: {
    getStore() {
      this.$axios.get(`trip/store_detail/${this.$cookies.get("review-store-id")}`)
      .then(res => {
          this.storeName = res.data.store_name
      })
      .catch(err => console.error(err))
    },
    rate(star) {
      if (typeof star === 'number' && star <= this.maxStars && star >= 0) {
        this.reviewData.score = this.reviewData.score === star ? star - 1 : star
      }
    },
    onClick() {
      this.getHtml();
      const requestHeaders = {
        headers: {
          Authorization: `JWT ${this.$cookies.get("auth-token")}`,
        },
      };
      this.$axios
        .post(`review/create_review/${this.storeId}`, this.reviewData, requestHeaders)
        .then((res) => {
          console.log(res);
          // 등록이 완료되면 마이페이지로 이동
          this.$router.push({ name: 'MyPageView' })
        })
        .catch((err) => console.error(err));
    },
    getHtml() {
      console.log(this.$refs);
      let html = this.$refs.toastuiEditor.invoke("getHtml");
      this.reviewData.content = html;
    },
  },
};
</script>

<style scoped lang="scss">
.rating {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    color: #b7b7b7;
    border-radius: 8px;
    .list {
        padding: 0;
        margin: 0;
        &:hover {
            .star {
                color: #ffe100;
            }
        }
        .star {
            display: inline-block;
            font-size: 24px;
            transition: all .2s ease-in-out; 
            cursor: pointer;
            &:hover {
                ~ .star:not(.active) {
                    color: inherit;
                }
            }
            &:first-child {
                margin-left: 0;
            }
            &.active {
                color: #ffe100;
            }
        }
    }
    .info {
        font-size: 20px;
        text-align: center;
        display: table;
        .divider {
            margin: 0 5px;
            font-size: 20px;
        }
        .score-max {
            font-size: 20px;
            vertical-align: sub;
        }
    }
}
</style>