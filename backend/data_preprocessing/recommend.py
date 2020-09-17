# https://medium.com/sfu-cspmp/recommendation-systems-user-based-collaborative-filtering-using-n-nearest-neighbors-bf7361dc24e0

from parse import load_dataframes
import numpy as np
import pandas as pd
import shutil
import scipy.sparse as sps
from sklearn.metrics.pairwise import cosine_similarity


def UB_DF(dataframe, for_user):
    print(for_user)

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

    print(for_user)

    result1 = User_item_score1(for_user)
    print(result1[['store_name', 'address', 'category']])

    result2 = User_item_score2(for_user)
    print(result2[['store_name', 'address', 'category']])
    return



def main():
    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    print("[음식점을 추천해봅시다]")
    print("input user number")
    # 75794
    for_user = int(input())
    print(f"{separater}\n")
    UB_DF(data, for_user)
    print(f"{separater}\n")
    print('end')


if __name__ == "__main__":
    main()