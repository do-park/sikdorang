<template>
  <div id="box">
        <div class="text-center">
            <v-btn
            color="red lighten-2"
            dark
            @click="getMyLocation"
            >
            내 위치
            </v-btn>

            <v-dialog
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
            </v-dialog>
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
#box{
    background : lightgray;
    margin : 2rem;
}
</style>