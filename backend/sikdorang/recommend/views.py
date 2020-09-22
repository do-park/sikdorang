import numpy as np
import pandas as pd
import shutil
import scipy.sparse as sps
from sklearn.metrics.pairwise import cosine_similarity
import os
from django.http import HttpResponse
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
# @permission_classes([IsAuthenticated])
def get_tag_recommendation(request):
    user_pk = request.META['auth-token']
    user = request.user
    data = request.data
    lat = data.lat
    lng = data.lng
    stores = Store.objects.filter(
        Q(latitude__lte=lat+0.04) & Q(latitude__gte=lat-0.04) & Q(longitude__lte=lng+0.04) & Q(longitude__gte=lng-0.04)
    )
    recommendation = {}
    # 임시 데이터
    user_tags = [{"tag": 0, "count": 2}, {"tag": 1, "count": 5}, {"tag": 6, "count": 1}]
    user_categories = [{"category": 2, "count": 1}, {"category": 7, "count": 6}, {"category": 8, "count": 4}]
    store_tags = [
        {"store_id": 45, "tag": 0}, {"store_id": 45, "tag": 2}, {"store_id": 45, "tag": 5},
        {"store_id": 525, "tag": 2}, {"store_id": 525, "tag": 6}, {"store_id": 525, "tag": 7},
        {"store_id": 1244, "tag": 1}, {"store_id": 975, "tag": 0}, {"store_id": 975, "tag": 1},
        {"store_id": 4, "tag": 6}
    ]
    store_categories = [
        {"store_id": 45, "category": 2}, {"store_id": 525, "category": 8}, {"store_id": 1244, "category": 2},
        {"store_id": 975, "category": 2}, {"store_id": 4, "category": 7},
    ]
    for user_tag in user_tags:
        for store_tag in store_tags:
            if user_tag["tag"] == store_tag["tag"]:
                if store_tag["store_id"] not in recommendation:
                    recommendation[store_tag["store_id"]] = 0
                recommendation[store_tag["store_id"]] += user_tag["count"]
    for user_category in user_categories:
        for store_category in store_categories:
            if user_category["category"] == store_category["category"]:
                if store_category["store_id"] not in recommendation:
                    recommendation[store_category["store_id"]] = 0
                recommendation[store_category["store_id"]] += user_category["count"]
    recommendation = sorted(recommendation.items(), key=(lambda x: x[1]), reverse=True)
    print(recommendation)
