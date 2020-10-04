import numpy as np
import pandas as pd
import shutil
import scipy.sparse as sps
from sklearn.metrics.pairwise import cosine_similarity
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Store
from api.serializers import StoreSerializer

import datetime
import random

DATA_DIR = "../../data"
DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

TAG_NAME = ["가성비", "청결", "친절", "분위기", "인테리어", "아침", "점심", "저녁", "친구", "연인", "가족", "주차장"]
CATEGORY_NAME = ["한식", "분식", "피자", "치킨", "돈가스/회/일식", "카페/디저트/베이커리", "아시안", "양식", "중식", "도시락", "패스트푸드","술집", "족발/보쌈", "찜/탕"]

def recommend(request, user_pk):
    dataframe = load_dataframes()
    result = user_based(dataframe,user_pk)
    result_list = []
    result = result[['store_name', 'address', 'category']]
    for row in result.iterrows():
        result_list.append(row)
    return HttpResponse(result_list)


def load_dataframes():
    return pd.read_pickle(DUMP_FILE)


# @login_required
def user_based(dataframe, for_user):
        # 리뷰를 유저로 묶어서 그 개수를 카운트, 100개 이상 리뷰 작성한 유저를 activate_user로 지정

    user_review_counts = dataframe['reviews']['user'].value_counts().rename_axis('user').reset_index(name='counts')
    activate_user = user_review_counts[user_review_counts['counts'] >= 100]
    user_review_more_than_100 = pd.merge(
        dataframe['reviews'], activate_user, left_on="user", right_on="user", how="right"
    )
    clean_user_review_more_than_100 = user_review_more_than_100[['store', 'user', 'score']]

    df = clean_user_review_more_than_100.set_index(['store', 'user'])
    mat = sps.coo_matrix((df.score, (df.index.get_level_values(0), df.index.get_level_values(1))))


    # 각 유저의 평균 평점
    Mean = clean_user_review_more_than_100.groupby(by="user", as_index=False)['score'].mean()
    score_avg = pd.merge(clean_user_review_more_than_100, Mean, on='user')
    # adg_score: 유저별 정규화 된 등급 계산
    score_avg['adg_score'] = score_avg['score_x'] - score_avg['score_y']

    # 코사인 유사도 계산산
    final = pd.pivot_table(score_avg, values='adg_score', index='user', columns='store')
    final_store = final.fillna(final.mean(axis=0))
    final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)

    # user similarity on replacing NAN by user avg
    b = cosine_similarity(final_user)
    np.fill_diagonal(b, 0)
    similarity_with_user = pd.DataFrame(b, index=final_user.index)
    similarity_with_user.columns = final_user.index
    similarity_with_user.head()

    # user similarity on replacing NAN by item(store) avg
    cosine = cosine_similarity(final_store)
    np.fill_diagonal(cosine, 0)
    similarity_with_store = pd.DataFrame(cosine, index=final_store.index)
    similarity_with_store.columns = final_user.index
    similarity_with_store.head()


    def find_n_neighbours(df, n):
        order = np.argsort(df.values, axis=1)[:, :n]
        df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
                                          .iloc[:n].index,
                                          index=['top{}'.format(i) for i in range(1, n + 1)]), axis=1)
        return df


    sim_user_30_u = find_n_neighbours(similarity_with_user, 30)
    sim_user_30_m = find_n_neighbours(similarity_with_store, 30)


    def get_user_similar_stores(user1, user2):
        common_stores = score_avg[score_avg.user == user1].merge(
            score_avg[score_avg.user == user2],
            on="store",
            how="inner")
        return common_stores.merge(dataframe['stores'], left_on='store', right_on='id', how='inner')


    def User_item_score(user, item):
        a = sim_user_30_m[sim_user_30_m.index == user].values
        b = a.squeeze().tolist()
        c = final_store.loc[:, item]
        d = c[c.index.isin(b)]
        f = d[d.notnull()]
        avg_user = Mean.loc[Mean['user'] == user, 'score'].values[0]
        index = f.index.values.squeeze().tolist()
        corr = similarity_with_store.loc[user, index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score', 'correlation']
        fin['score'] = fin.apply(lambda x: x['adg_score'] * x['correlation'], axis=1)
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume / deno)
        return final_score

    score_avg = score_avg.astype({"store": str})
    Store_user = score_avg.groupby(by='user')['store'].apply(lambda x: ','.join(x))

    check = pd.pivot_table(score_avg, values='score_x', index='user', columns='store')


    def User_item_score1(user):
        Store_visited_by_user = check.columns[check[check.index == user].notna().any()].tolist()

        a = sim_user_30_m[sim_user_30_m.index == user].values
        b = a.squeeze().tolist()
        d = Store_user[Store_user.index.isin(b)]
        l = ','.join(d.values)
        Store_visited_by_similar_users = l.split(',')
        Store_under_consideration = list(
            set(Store_visited_by_similar_users) - set(list(map(str, Store_visited_by_user))))
        Store_under_consideration = list(map(int, Store_under_consideration))
        score = []
        for item in Store_under_consideration:
            c = final_store.loc[:, item]
            d = c[c.index.isin(b)]
            f = d[d.notnull()]
            avg_user = Mean.loc[Mean['user'] == user, 'score'].values[0]
            index = f.index.values.squeeze().tolist()
            corr = similarity_with_store.loc[user, index]
            fin = pd.concat([f, corr], axis=1)
            fin.columns = ['adg_score', 'correlation']
            fin['score'] = fin.apply(lambda x: x['adg_score'] * x['correlation'], axis=1)
            nume = fin['score'].sum()
            deno = fin['correlation'].sum()
            final_score = avg_user + (nume / deno)
            score.append(final_score)
        data = pd.DataFrame({'store': Store_under_consideration, 'score': score})
        top_5_recommendation = data.sort_values(by='score', ascending=False).head(5)
        Store_Name = top_5_recommendation.merge(dataframe['stores'], how='inner', left_on='store', right_on='id')
        return Store_Name

    def User_item_score2(user):
        Store_visited_by_user = check.columns[check[check.index == user].notna().any()].tolist()

        a = sim_user_30_m[sim_user_30_m.index == user].values
        b = a.squeeze().tolist()
        d = Store_user[Store_user.index.isin(b)]
        l = ','.join(d.values)
        Store_visited_by_similar_users = l.split(',')
        Store_under_consideration = list(
            set(Store_visited_by_similar_users) - set(list(map(str, Store_visited_by_user))))
        Store_under_consideration = list(map(int, Store_under_consideration))
        score = []
        for item in Store_under_consideration:
            c = final_store.loc[:, item]
            d = c[c.index.isin(b)]
            f = d[d.notnull()]
            avg_user = Mean.loc[Mean['user'] == user, 'score'].values[0]
            index = f.index.values.squeeze().tolist()
            corr = similarity_with_store.loc[user, index]
            fin = pd.concat([f, corr], axis=1)
            fin.columns = ['adg_score', 'correlation']
            fin['score'] = fin.apply(lambda x: x['adg_score'] * x['correlation'], axis=1)
            nume = fin['score'].sum()
            deno = fin['correlation'].sum()
            final_score = avg_user + (nume / deno)
            score.append(final_score)
        data = pd.DataFrame({'store': Store_under_consideration, 'score': score})
        top_5_recommendation = data.sort_values(by='score', ascending=False).head(5)
        Store_Name = top_5_recommendation.merge(dataframe['stores'], how='inner', left_on='store', right_on='id')
        return Store_Name

    result1 = User_item_score1(for_user)
    result2 = User_item_score2(for_user)
    return result1


@api_view(['POST'])
def get_tag_recommendation(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    data = request.data
    div = data["category"]
    lat = float(data["lat"])
    lng = float(data["lng"])
    beforeCategories = data["bc"]
    g_lat = lat + 0.01
    l_lat = lat - 0.01
    g_lng = lng + 0.01
    l_lng = lng - 0.01
    stores = Store.objects.filter(
        Q(latitude__lte=g_lat) & Q(latitude__gte=l_lat) & Q(longitude__lte=g_lng) & Q(longitude__gte=l_lng)
    )
    recommendation = {}
    
    # 유저 태그 가져오기 - 태그는 보존
    user_tags_queryset = user.tagmodel_set.all()
    user_tags = []
    for tag in user_tags_queryset:
        user_tags.append({"tag": tag.name, "count": tag.count})
        
    # 유저 카테고리 가져오기
    user_categories_queryset = user.categoryuser_set.all()
    user_categories = []
    temp_user_categories = []
    selected_categories = []
    for category in user_categories_queryset:
        # 저번에 선택한 카테고리는 제외
        if div == "카페" or CATEGORY_NAME[int(category.name)] not in beforeCategories:
            temp_user_categories.append(["category", CATEGORY_NAME[int(category.name)], "count", category.count])
            selected_categories.append(CATEGORY_NAME[int(category.name)])

    # 유저 카테고리 자르기
    temp_user_categories.sort(key=lambda x: x[3])
    temp_user_categories = temp_user_categories[:4]
    for i in range(len(temp_user_categories)-2):
        ran_num = random.randint(0, len(temp_user_categories)-1)
        del temp_user_categories[ran_num]
    for category in temp_user_categories:
        user_categories.append({"category": category[1], "count": category[3]})
    # 포함되지 않은 카테고리 추가
    while 1:
        ran_num = random.randint(0, len(CATEGORY_NAME)-1)
        if ran_num not in selected_categories:
            user_categories.append({"category": CATEGORY_NAME[ran_num], "count": 5})
            break
        
    store_tags = []
    store_categories = []
    for store in stores:
        if div=="식당" and store.category.name == "카페/디저트/베이커리":
            continue
        elif div=="카페" and store.category.name != "카페/디저트/베이커리":
            continue
        if store.tags:
            tag = ""
            for i in range(len(store.tags)):
                if store.tags[i] != ",":
                    tag += store.tags[i]
                elif (store.tags[i] == ","):
                    store_tags.append({"store_id": store.id, "tag": int(tag)})
                    tag = ""
            store_tags.append({"store_id": store.id, "tag": int(tag)})
        store_categories.append({"store_id": store.id, "category": store.category.name})
    tags = set()
    for user_tag in user_tags:
        for store_tag in store_tags:
            tags.add(TAG_NAME[store_tag["tag"]])
            if user_tag["tag"] == store_tag["tag"]:
                if store_tag["store_id"] not in recommendation:
                    recommendation[store_tag["store_id"]] = 0
                recommendation[store_tag["store_id"]] += user_tag["count"]
    for user_category in user_categories:
        for store_category in store_categories:
            tags.add(store_category["category"])
            if div == "식당":
                if user_category["category"] == store_category["category"]:
                    if store_category["store_id"] not in recommendation:
                        recommendation[store_category["store_id"]] = 0
            elif div=="카페":
                if store_category["store_id"] not in recommendation:
                    recommendation[store_category["store_id"]] = 0
                recommendation[store_category["store_id"]] += user_category["count"]
    recommendation = sorted(recommendation.items(), key=(lambda x: x[1]), reverse=True)[:30]
    random.shuffle(recommendation)
    result = []
    for rec in recommendation[:6]:
        store = Store.objects.filter(id=rec[0])[0]
        result.append({
            "id": store.id,
            "name": store.store_name,
            "branch": store.branch,
            "tel": store.tel,
            "address": store.address,
            "latitude": store.latitude,
            "longitude": store.longitude,
            "category": store.category.name,
            "tags": store.tags
        })
    if len(result) == 0:
        for store in stores[:6]:
            result.append({
                "id": store.id,
                "name": store.store_name,
                "branch": store.branch,
                "tel": store.tel,
                "address": store.address,
                "latitude": store.latitude,
                "longitude": store.longitude,
                "category": store.category.name,
                "tags": store.tags
            })
    return JsonResponse({"result": result, "tags": list(tags)})


@api_view(['POST'])
def get_tag_stores(request):
    data = request.data
    tag = data["tag"]
    lat = float(data["lat"])
    lng = float(data["lng"])
    g_lat = lat + 0.01
    l_lat = lat - 0.01
    g_lng = lng + 0.01
    l_lng = lng - 0.01
    store_list = []
    result = []
    stores = Store.objects.filter(
        Q(latitude__lte=g_lat) & Q(latitude__gte=l_lat) & Q(longitude__lte=g_lng) & Q(longitude__gte=l_lng)
    )
    if tag in TAG_NAME:
        for store in stores:
            if str(TAG_NAME.index(tag)) in store.tags:
                store_list.append(store)
    elif tag in CATEGORY_NAME:
        for store in stores:
            if tag == store.category.name:
                store_list.append(store)
        
    for store in store_list:
        result.append({
            "id": store.id,
            "name": store.store_name,
            "branch": store.branch,
            "tel": store.tel,
            "address": store.address,
            "latitude": store.latitude,
            "longitude": store.longitude,
            "category": store.category.name,
            "tags": store.tags
        })
    return JsonResponse({"result": result})

@api_view(['GET'])
def coldstart(request):
    startpoint = [[148912, 305741, 161207, 35736, 154632, 236604, 214585, 100791, 261913, 97851, 314528, 3898, 73522, 176721, 68900, 121543, 276131, 278687, 252755, 70953, 83525, 46319, 239444, 304420, 323242, 334509, 138460, 296624],
    [145030, 346836, 160799, 320057, 319442, 329194, 157481, 239920, 303270, 106124, 119088, 271833, 229027, 166870, 121556, 76200, 353580, 309336, 160821, 117711, 241525, 321485, 307939, 165925, 194238, 195025, 266128, 90383],
    [147432, 145030, 309336, 321390, 297934, 305906, 267510, 36441, 229027,  288945, 275702, 26012, 119088,  227258, 321485, 348398, 239920, 106124, 43727, 335278, 319442, 132516, 187601, 172674, 134200, 232883, 346836, 353580],
    [145030, 26012, 187601, 305906, 150885, 317547, 321485, 335279, 106124, 160821, 206721, 36441, 249091, 177298, 322993, 309336, 251106, 312290, 104405, 66900, 61406, 282527, 61747, 40626, 267181, 359300, 213774, 284308],
    [213774, 187601, 309336, 61406, 168430, 26012, 145030, 70803, 319884, 73001, 332467, 187613, 348398, 203418, 283888, 302264, 29609, 45445, 152068, 20936, 137024, 329491, 296060, 305906, 317547, 147555, 232883, 282973],
    [327509, 166193, 213577, 2515, 336589, 288140, 179945, 250658, 94409, 173666, 642, 62920, 286236, 187168, 166871, 164392, 280629, 241692, 170604, 186418, 267206, 197226, 164208, 62012, 86697, 106098, 81939, 166898]]
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y')
    agecode = (int(nowDate) - int(user.age))//10
    agecode -= 1
    if agecode < 0:
        agecode = 0
    if agecode > 5:
        agecode = 5
    rstore = get_object_or_404(Store, id=startpoint[agecode][random.randrange(0, 28)])
    serializer = StoreSerializer(rstore)
    return Response(serializer.data)

    
