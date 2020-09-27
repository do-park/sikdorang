<template>
  <div>
    <div class="rating">
        <ul class="list">
            <li @click="rate(star)" v-for="star in maxStars" :class="{ 'active': star <= reviewData.stars }" :key="star.stars" class="star">
                <i :class="star <= reviewData.stars ? 'fas fa-star' : 'far fa-star'"></i> 
            </li>
        </ul>
        <div v-if="hasCounter" class="info counter">
            <span class="score-rating">{{ reviewData.stars }}</span>
            <span class="divider">/</span>
            <span class="score-max">{{ maxStars }}</span>
        </div>
    </div>
    <editor
      ref="toastuiEditor"
      :initialValue="editorText"
      :options="editorOptions"
      height="500px"
      initialEditType="wysiwyg"
      previewStyle="vertical"
    />
    <button class="btn btn-primary" @click="onClick()">생성</button>
  </div>
</template>

<script>
import "codemirror/lib/codemirror.css";
import "@toast-ui/editor/dist/toastui-editor.css";
import { Editor } from "@toast-ui/vue-editor";

export default {
  name: "TripScheduleForm",
  components: {
    editor: Editor,
  },
  data() {
    return {
      maxStars: 5,
      hasCounter: "true",
      reviewData: {
        stars: 3,
        content: null,
      },
      editorText: "방문 후기를 작성해주세요.",
      editorOptions: {
        hideModeSwitch: true,
      },
    };
  },
  methods: {
    rate(star) {
      if (typeof star === 'number' && star <= this.maxStars && star >= 0) {
        this.reviewData.stars = this.reviewData.stars === star ? star - 1 : star
      }
    },
    // onClick() {
    //   this.getHtml();
    //   const requestHeaders = {
    //     headers: {
    //       Authorization: `JWT ${this.$cookies.get("auth-token")}`,
    //     },
    //   };

    //   this.$axios
    //     .post("review", this.reviewData, requestHeaders)
    //     .then((res) => {
    //       console.log(res);
    //       // 등록이 완료되면 리턴되는 객체에서 id 값을 이용해 push한다.
    //       // this.$router.push(`/trip/detail/${res.data.id}`);
    //     })
    //     .catch((err) => console.error(err));
    // },
    getHtml() {
      console.log(this.$refs);
      let html = this.$refs.toastuiEditor.invoke("getHtml");
      this.tripSchedule.content = html;
    },
  },
};
</script>

<style scoped lang="scss">
.rating {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 50px;
    color: #b7b7b7;
    border-radius: 8px;
    .list {
        padding: 0;
        margin: 0 20px 0 0;
        &:hover {
            .star {
                color: #ffe100;
            }
        }
        .star {
            display: inline-block;
            font-size: 42px;
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
        margin-top: 15px;
        font-size: 40px;
        text-align: center;
        display: table;
        .divider {
            margin: 0 5px;
            font-size: 30px;
        }
        .score-max {
            font-size: 30px;
            vertical-align: sub;
        }
    }
}
</style>