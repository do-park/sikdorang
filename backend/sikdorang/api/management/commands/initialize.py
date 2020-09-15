from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from sikdorang import settings
from api import models
import json


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "dump.pkl")

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
            category = models.Category.objects.create(
                id = i,
                name = category_name[i]
            )
        print("[*] 태그 넣는중")
        tags_name = ["가성비", "청결", "친절", "분위기", "인테리어", "아침", "점심", "저녁", "친구", "연인", "가족", "주차장"]
        for j in range(12):
            tag = models.Tags.objects.create(
                id = j,
                name = tags_name[j]
            )

        print("[*] Loading data...")
        dataframes = self._load_dataframes()

        print("[*] Initializing stores...")
        models.Store.objects.all().delete()
        stores = dataframes["stores"]
        stores_bulk = [
            models.Store(
                id=store.id,
                store_name=store.store_name,
                branch=store.branch,
                tel=store.tel,
                address=store.address,
                latitude=store.latitude,
                longitude=store.longitude,
            )
            for store in stores.itertuples()
        ]
        models.Store.objects.bulk_create(stores_bulk)

        print("[+] Done")

    def handle(self, *args, **kwargs):
        self._initialize()
