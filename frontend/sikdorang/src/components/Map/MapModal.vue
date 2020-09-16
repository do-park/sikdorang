<template>
  <div v-if="true">
       <!-- template for the modal component -->
    <script type="text/x-template" id="modal-template">
      <transition name="modal">
        <div class="modal-mask">
          <div class="modal-wrapper">
            <div class="modal-container">

              <div class="modal-header">
                <slot name="header">
                  default header
                </slot>
              </div>

              <div class="modal-body">
                <slot name="body">
                  default body
                </slot>
              </div>

              <div class="modal-footer">
                <slot name="footer">
                  default footer
                  <button class="modal-default-button" @click="$emit('close')">
                    OK
                  </button>
                </slot>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </script>
        <!-- <div id="myModal" class="modal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">모달창 확인</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                            <div v-if="getClicked">
                                여기 관련 정보 들어가겠죠
                            </div>
                            <div v-else>클릭 아직 안했습니다..</div>
                            
                        </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary">일정에 저장</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">닫기</button>
                </div>
                </div>
            </div>
            </div> -->
  </div>
  <div v-else></div>
</template>

<script>
import {mapGetters} from "vuex"
const mapEvent = "mapEvent"

export default {
    name: 'MapModal',
    watch : {
        getClicked() {
            console.log(this.getClicked,"디테일 모달입니다.")
        },
    },
    computed : {
        ...mapGetters(mapEvent, [
            'getClicked'
        ])
    },
}
</script>

<style>

</style>