<template>
  <div>
    <div class="text-center">
        <button type="button" class="btn btn-secondary" @click="getMyLocation">내 위치</button>
        <!-- Button trigger modal -->
        <button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#exampleModal">
        다른 지역
        </button>

        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">지역 검색하기</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                여행을 시작할 지역을 검색해보세요!
                    <input
                        v-model="destination" 
                        @keyup.enter="findPath(destination)"
                        label="어디 갈래?"
                        placeholder="XX동 or XX동 775-5"
                        
                    />
                    <button @click="findPath(destination)">
                        검색
                    </button>
                    <br>
                    {{message}}
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">닫기</button>
                <button type="button" class="btn btn-primary" @click="check">확인</button>
            </div>
            </div>
        </div>
        </div>




            <!-- <v-dialog
            v-model="dialog"
            width="500"
            >
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                color="red lighten-2"
                dark
                v-bind="attrs"
                v-on="on"
                >
                다른 지역
                </v-btn>
            </template>

            <v-card>
                <v-card-title class="headline grey lighten-2">
                지역 검색하기
                </v-card-title>
                <div>
                    <v-card-text>
                    여행을 시작할 지역을 검색해보세요!
                   
                    <template>
                    <v-form>
                        <span>
                        <v-text-field
                            v-model="destination" 
                            @keyup.enter="findPath(destination)"
                            label="어디 갈래?"
                            placeholder="XX동 or XX동 775-5"
                            
                        ></v-text-field>
                        <v-btn
                            color="primary"
                            text
                            @click="findPath(destination)"
                        >
                            검색
                        </v-btn>
                        {{message}}
                        </span>
                    </v-form>
                   
                    </template>
           
                    </v-card-text>
                </div>

                <v-divider></v-divider>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="primary"
                    text
                    @click="check"
                >
                    확인
                </v-btn>
                </v-card-actions>
            </v-card>
            </v-dialog> -->
        </div>
        <!-- <div id="map"></div> -->
  </div>
</template>

<script>
export default {
    name : 'SelectStart',
    data() {
        return {
            Latitude: null,
            Longitude: null,
            dialog: false,
            destination: '',
            message : '',
        }
    },
 
    methods : {
        check() {
            this.dialog = false
            this.message = ''
            this.$cookies.set("searchMethod", "Regions")
            this.destination = ''
            this.$emit("flag",false)
           
        },
        getMyLocation() {	
			if('geolocation' in navigator) {
                
                //위치 요청
				navigator.geolocation.getCurrentPosition(function(pos) {
					this.Latitude = pos.coords.latitude;
					this.Longitude = pos.coords.longitude;
                    alert("현재 위치는 : " + this.Latitude + ", "+ this.Longitude);
                    
                    //시작 위도,경도 쿠키에 올리기
                    console.log(this.Latitude,this.Longitude)
                    this.$cookies.set('startLatitude',this.Latitude)
                    this.$cookies.set('startLongitude',this.Longitude)
                    this.$cookies.set("searchMethod", "myLocation")
                    this.$emit("flag",false)
                    
                }.bind(this));
                
			} else {
                
                //위치정보 사용 불가능 
				console.log("위치 정보 사용이 불가능합니다.")
			}
        },
        
        findPath(destination) {
            this.destination = destination
            this.message = `${destination}에서 시작해볼까요?`
            this.$cookies.set("destination", destination)
        },
      
    }

}
</script>

<style>

</style>