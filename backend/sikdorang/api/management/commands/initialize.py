from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from sikdorang import settings
from api.models import *
from achievement.models import *
import json


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "store_tag_dump.pkl")

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] 카테고리 넣는중")
        category_name = ["한식", "분식", "피자", "치킨", "돈가스/회/일식", "카페/디저트/베이커리", "아시안", "양식", "중식", "도시락", "패스트푸드","술집", "족발/보쌈", "찜/탕"]
        for i in range(14):
            Category.objects.create(
                id = i,
                name = category_name[i]
            )

        print("[*] 업적 필드 넣는중")
        theme_name = ["빵집", "케익", "만두", "떢볶이", "짬뽕", "짜장면", "수제버거",
            "돈가스", "전국 터미널 맛집", "기차역 맛집", "고속도로 휴게소 맛집"]
        for i in range(1, 12):
            Themes.objects.create(
                id = i,
                name = theme_name[i-1]
            )

        print("[*] 업적 넣는중")
        file_path = str(Command.DATA_DIR / "achievement.json")
        with open(file_path, "rt", encoding="UTF-8") as json_file:
            json_data = json.load(json_file)
        for i in json_data:
            AchiveStore.objects.create(
                id = i['id'],
                store_name = i['store_name'],
                tel = i['tel'],
                address = i['address'],
                image = "/media/achieveimg/" + i['image'],
                theme_id = i['theme'],
                description = i['description'],
            )

        print("[*] Loading data...")
        dataframes = self._load_dataframes()

        print("[*] Initializing stores...")
        Store.objects.all().delete()
        stores = dataframes
        stores_bulk = [
            Store(
                id=store.id,
                store_name=store.store_name,
                tel=store.tel,
                address=store.address,
                latitude=store.latitude,
                longitude=store.longitude,
                category_id=store.new_category,
                tags=store.tags, 
            )
            for store in stores.itertuples()
        ]
        Store.objects.bulk_create(stores_bulk)
        print("[+] Done")

    def handle(self, *args, **kwargs):
        self._initialize()
