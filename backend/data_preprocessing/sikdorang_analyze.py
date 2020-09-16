from parse import load_dataframes
import pandas as pd
import shutil
from konlpy.tag import Komoran
from wordcloud import WordCloud
import json

def save_to_json(data, save_file_name):
    save_file_path = f'./{save_file_name}.json'
    with open(save_file_path,'w') as outfile:
        json.dump(data, outfile, indent=4)

def make_category_data(dataframes):
    # info_idx = {"hansik":0,"bunsik":1,"pizza":2,"chicken":3,"don_Hoe_ilsik":4,"cafe_dessert_bakery":5,"asian":6,"western":7,"chinese":8,"dosirak":9,"fastfood":10,"alcohol":11,"jokbal":12,"zzim_tang":13}
  
    info = {'0': [],
        '1':["떡볶이","순대","라볶이"],
        '2': ["피자"],
        '3':['치킨','통닭','양념치킨','닭다리','후라이','파닭','크리스'],
        '4':['모밀','돈카츠','돈가스','돈까스','스시','도쿄라멘','메로','스키야키','참치','횟집','라멘','송어','삼치','문어','해삼','우럭','꼼장어','새우','참다랑어','고래고기','붕장어','꽁치','산천어','초밥','장어','낙지','대개','전복','조개','대하','방어','도미','회덮밥','풍천장어','우동','오코노','미야','광어','사시미','민물고기','감성돔','홍어','오니기리','회전','나가사끼','나가사키','소바','라멘','규동','미소라멘','돈부리','일본'],
        '5':['츄러스','베이커리','카페','홍차','커피','밀크티','마카롱','북카페','다쿠아즈','쿠키','고로케','빙수','파이','타르트','호두과자','마들렌','아메리카노','아이스크림','브레드','쥬스','브라우니','디저트','스콘','도넛','롤케이크','커피숍','티라미수','슈크림','빵집','머랭','케익','쇼콜라','바닐라','카푸치노','누텔라','만화','망고','크림','로스팅','와플','토스트','식빵','초콜렛','녹차','베이글','버블티','찻집','딸기','빼빼로','다방','떡집','더치','자몽','스터디','꽈배기','수플레','고양이','바게트','치즈케이크','컵케익','말차','파운드','티라미스','자전거','딸기우유','단팥빵','모찌','제과점','붕어빵','치아바타','소프트','과자','호떡','에스프레소','팬케이크','핸드','파르페','카페모카','다쿠아즈','통밀빵','프레첼','인절미','에이드','스무디','찹쌀떡','푸딩'],
        '6':['쌀국수','샤브샤브','월남쌈','아시아','베트','케밥','팟타이','카레','대만','커리','인도','중국','터키','라씨','태국','라쟈냐','밀푀유','딤섬','타코','싱가포르'],
        '7':['랍스터','멕시코','브라질','호주','퓨전','고르곤졸라','러시아','스테이크','프랑스','이탈라인','스파게티','브런치','벨기에','샐러드','파스타','레스토랑','양식','하와이','그리스','뉴욕','케냐','맥시칸','앵거스','오믈렛','함박','파니니','이태리','스페인','스튜','필라프','에그','햄버그','아보카도','독일','아스파라거스','라따뚜이','케밥','감바스','미국','드라이','이징','체코','웨지감자','칠리','바비큐','타파스'],
        '8':['짬뽕','중국','짜장면','중화요리','깐풍기','중국집','탕수육','훠궈','마파두부','홍콩','수타면','양고기','마라','샤오롱바오','사천','마라탕','자장면','군만두','오징어짬뽕'],
        '9':['샌드위치','도시락'],
        '10':['버거','치즈버거','치즈스틱'],
        '11':['펍','비어','소주','술집','맥주','이자카야','와인','카스','동동주','테라','기네스','전통주','선술집','흑맥주','포차','막걸리','치맥','칵테일','파전','생맥주','호프','위스키','포장마차','민속주','비어','전집','주점','보드카','에일'],
        '12':['족발','보쌈'],
        '13':['갈비찜','아구찜','안동찜닭','아귀찜','장탕','갈비탕','보신탕','닭볶음탕','도가니탕','곰탕','해물탕','설렁탕','뼈다귀','등뼈','내장','감자탕']
        }

    stores = pd.merge(dataframes["stores"], dataframes["reviews"],left_on="id",right_on="store", how="left")
    stores = stores.groupby(["id_x","store_name"]).mean()
    stores = pd.merge(stores,dataframes["stores"],left_on="id_x",right_on="id")

    category_data= []
    no_category = []
    only_store_name = []
    km = Komoran()
    words = {}

    for index, store in stores.iterrows():
        category = store.category
        category.encode('utf-8')
        try:

            nouns = km.nouns(category)

            if not nouns:
                if category:
                    v_flag = True
                    for key, value in info.items():
                        if v_flag:
                            for v in value:
                                if v in category:
                                    category_data.append({
                                        "store_id": store.id,
                                        "category": int(key)
                                    })
                                    v_flag = False
                                    break

                    if v_flag:            
                        category_data.append({
                            "store_id" : store.id,
                            "category" : 0,
                        })
                        continue
                else:
                    if store.score >= 3.5 :
                        no_category.append({
                            "store_id" : store.id,
                            "store_name" : store.name,
                        })
                continue

        except:
            pass
        
        # 한식인지 구분위한 flag
        flag = True

        for key, value in info.items():
            if flag:
                for v in value:
                    if v in nouns:
                        category_data.append({
                            "store_id": store.id,
                            "category": int(key)
                        })
                        flag = False
                        break
        if flag:
            category_data.append({
                "store_id": store.id,
                "category": 0,
            })

    save_to_json(category_data, "categorydata")

    return category_data


def make_tags_from_reviews(dataframes):
    tag_data = []
    tag_dict = {"가성비":0,"저렴":0,"깔끔":1,"신선":1,"위생":1,"깨끗":1,"친절":2,"분위기":3,"감성":3,"인테리어":4,"아침":5,"조식":5,"새벽":5,"점심시간":6,"점심":6,"낮":6,"퇴근":7,"석식":7,"술":7,"야식":7,"밤":7,"저녁":7,"친구":8,"연인":9,"데이트":9,"둘이서":9,"여자친구":9,"여친":9,"남자친구":9,"남친":9,"커플":9,"가족":10,"부모님":10,"주차장":11,"주차공간":11,"주차권":11}
    
    reviews = dataframes["reviews"]
    km = Komoran()
    words = {}
    test = reviews[["content","score","store"]]
 
    for index, review in test.iterrows():
        try:
            nouns = km.nouns(review.content)
        except:
            pass
        tags = set()
        for noun in nouns:
            if noun in tag_dict.keys() :
                if review.score >= 4 :
                   
                    tags.add(tag_dict[noun])

            if noun not in words:
                words[noun] = 0
            words[noun] += 1

        if tags :
            data = {
                    "store_id" : review.store,
                    "tags":list(tags)
                        }
            tag_data.append(data)

    # wc = WordCloud(font_path='NanumGothic.ttf', width=1600, height=1600)
    # wc_img = wc.generate_from_frequencies(words)
    # wc_img.to_file('review_words.jpg')

    save_to_json(tag_data, "tagdata")

    print(len(tag_data))
    return tag_data



def main():
    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    category_data = make_category_data(data)
    tag_data = make_tags_from_reviews(data)


if __name__ == "__main__":
    main()
