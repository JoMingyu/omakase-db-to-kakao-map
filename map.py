from random import random
from time import sleep
from typing import Optional, List

from pydantic.main import BaseModel
from requests import get, post

from vo import Restaurant


class BookmarkRequest(BaseModel):
    key: int
    folderId: int
    display1: str
    display2: str
    color: str
    x: int
    y: int
    type: str = "place"
    memo: str = ""


class KaKaoMap:  # interface로 Map을 두면 다른 지도에 대응시키기 쉬워짐. 지금은 귀찮아서 안할랭
    def __init__(self, token: str):
        self.token = token

    @property
    def _headers(self) -> dict:
        return {
            "Cookie": f"_kawlt={self.token}",
            "Referer": "https://map.kakao.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        }

    def _get_folder_id_by_name(self, name_to_find: str) -> Optional[str]:
        resp = get("https://map.kakao.com/folder/list.json", headers=self._headers)

        for folder in resp.json()["result"]:
            if folder["title"] == name_to_find:
                return folder["folderId"]

    def _remove_folder(self, id: str):
        post(
            "https://map.kakao.com/folder/delete.json",
            headers=self._headers,
            json={"folderIds": [id]},
        )

    def _create_folder(self, name: str) -> id:
        resp = post(
            "https://map.kakao.com/folder/add.json",
            headers=self._headers,
            json={
                "title": name,
                "memo": "",
                "icon": "01",
                "status": "O",
            },
        )

        return resp.json()["req"]["folderId"]

    def _inject_place_data(self, place: dict, restaurant: Restaurant):
        restaurant.id_on_map = place["confirmid"]
        restaurant.address_on_kakaomap = place["new_address"]
        restaurant.x = place["x"]
        restaurant.y = place["y"]

    def inject_data_for_request(self, restaurant: Restaurant) -> bool:
        """
        Returns:
            succeed
        """

        sleep(random() / 2)

        resp = get(
            f"https://search.map.daum.net/mapsearch/map.daum?q={restaurant.name}&callback=",
            headers=self._headers,
        )

        places = resp.json()["place"]

        if len(places) == 1:
            self._inject_place_data(places[0], restaurant)
            return True

        for place in places:
            if restaurant.address in (place["address"], place["new_address"]):
                self._inject_place_data(place, restaurant)
                return True

        # fallback
        for place in places:
            if (
                restaurant.address[: len(restaurant.address) // 3] in place["address"]
                or restaurant.address[: len(restaurant.address) // 3]
                in place["new_address"]
            ):
                self._inject_place_data(place, restaurant)
                return True

        return False

    def create_folder(self, name: str) -> str:
        sleep(random() / 2)

        folder_id = self._get_folder_id_by_name(name_to_find=name)

        if folder_id:
            self._remove_folder(id=folder_id)

        return self._create_folder(name=name)

    def add_place_to_folder(self, json: List[dict]):
        sleep(random() * 5)

        resp = post(
            "https://map.kakao.com/favorite/add.json",
            headers=self._headers,
            json=json,
        )

        if resp.json()["status"]["code"] != "SUCCESS":
            print("사고가 났어요")
            print(resp.json)
