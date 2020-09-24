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

DATA_DIR = "../../data"
DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

# Create your views here.
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
    category_name = ["한식", "분식", "피자", "치킨", "돈가스/회/일식", "카페/디저트/베이커리", "아시안", "양식", "중식", "도시락", "패스트푸드","술집", "족발/보쌈", "찜/탕"]
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    data = request.data
    div = data["category"]
    lat = float(data["lat"])
    lng = float(data["lng"])
    g_lat = lat + 0.02
    l_lat = lat - 0.02
    g_lng = lng + 0.02
    l_lng = lng - 0.02
    stores = Store.objects.filter(
        Q(latitude__lte=g_lat) & Q(latitude__gte=l_lat) & Q(longitude__lte=g_lng) & Q(longitude__gte=l_lng)
    )
    recommendation = {}
    user_tags_queryset = user.tagmodel_set.all()
    user_tags = []
    for tag in user_tags_queryset:
        user_tags.append({"tag": tag.name, "count": tag.count})
    user_categories_queryset = user.categoryuser_set.all()
    user_categories = []
    for category in user_categories_queryset:
        user_categories.append({"category": category_name[int(category.name)], "count": category.count})
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

    for user_tag in user_tags:
        for store_tag in store_tags:
            if user_tag["tag"] == store_tag["tag"]:
                if store_tag["store_id"] not in recommendation:
                    recommendation[store_tag["store_id"]] = 0
                recommendation[store_tag["store_id"]] += user_tag["count"]
    for user_category in user_categories:
        for store_category in store_categories:
            if div == "식당":
                if user_category["category"] == store_category["category"]:
                    if store_category["store_id"] not in recommendation:
                        recommendation[store_category["store_id"]] = 0
            elif div=="카페":
                if store_category["store_id"] not in recommendation:
                    recommendation[store_category["store_id"]] = 0
                recommendation[store_category["store_id"]] += user_category["count"]
    recommendation = sorted(recommendation.items(), key=(lambda x: x[1]), reverse=True)[:6]
    result = []
    for rec in recommendation:
        store = Store.objects.filter(id=rec[0])[0]
        result.append({
            "id": store.id,
            "name": store.store_name,
            "branch": store.branch,
            "tel": store.tel,
            "address": store.address,
            "latitude": store.latitude,
            "longtitude": store.longitude,
            "category": store.category.name,
            "tags": store.tags
        })
    return JsonResponse({"result": result})
