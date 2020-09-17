<template>
  <div v-if="showModal">
      <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="false">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">
                    <div v-if="getClicked">{{getThreeRes[getClicked].title}}</div>
                    <div v-else>어떤 식당을 찾으시나요?</div>
                </h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="">닫기</button>
                <button type="button" class="btn btn-primary">일정 저장하기</button>
            </div>
            </div>
        </div>
        </div>
      <!-- <div class="modal fade in modal-active">
			<div class="modal-dialog">
					<div class="modal-content">
						<div class="modal-header">
							<button type="button" @click="$emit('close')" class="close"><span >&times;</span></button>
							<h4 class="modal-title">
								?????????????
							</h4>
						</div>
						<div class="modal-body">
								<slot></slot>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-default" @click="$emit('close')">Close</button>
							<button type="button" class="btn btn-primary">Save changes</button>
						</div>
				</div>
			</div>
		</div> -->
  </div>
</template>

<script>
import { mapGetters } from "vuex"
const mapEvent = "mapEvent"
export default {
    name : 'MarkerModal',
    computed : {
        ...mapGetters(mapEvent, [
            'getClicked',
            'getThreeRes',
        ])
    },

}
</script>

<style>
.modal-active{
	display:block;
}
</style>