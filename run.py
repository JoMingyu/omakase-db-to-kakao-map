import logging
from typing import List

from map import KaKaoMap, BookmarkRequest
from restaurant import RestaurantLoader
from vo import Folder, Color

PUBLIC_TO_KAKAOMAP_STATUS = {True: "O", False: "P"}


last_request_fire_time = None
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Sync:
    def __init__(
        self, map: KaKaoMap, restaurant_loader: RestaurantLoader, folders: List[Folder]
    ):
        self.map = map
        self.restaurant_loader = restaurant_loader
        self.folders = folders

    def sync(self):
        for folder in self.folders:
            folder.id_on_map = self.map.create_folder(folder.name)

        restaurants = self.restaurant_loader.load()
        valid_restaurants = []

        for restaurant in restaurants:
            succeed = self.map.inject_data_for_request(restaurant)

            if succeed:
                valid_restaurants.append(restaurant)
            else:
                print(
                    f"{restaurant.name} skipped during load place id. address: {restaurant.address}"
                )

        request_specs = []

        for restaurant in valid_restaurants:
            restaurant_bookmarked = False

            for folder in self.folders:
                if folder.criteria_func(restaurant):
                    request_specs.append(
                        BookmarkRequest(
                            key=int(restaurant.id_on_map),
                            folderId=int(folder.id_on_map),
                            display1=restaurant.name,
                            display2=restaurant.address,
                            color=folder.color,
                            x=restaurant.x,
                            y=restaurant.y,
                        )
                    )
                    print(f"restaurant {restaurant.name} put {folder.name}.")
                    restaurant_bookmarked = True

                    if len(request_specs) == 10:
                        self.map.add_place_to_folder(
                            json=[req.dict() for req in request_specs]
                        )
                        request_specs.clear()

            if not restaurant_bookmarked:
                print(f"restaurant {restaurant.name} never bookmarked.")

        if request_specs:
            # 남은거 처리
            self.map.add_place_to_folder(json=[req.dict() for req in request_specs])


Sync(
    map=KaKaoMap(token="..."),
    restaurant_loader=RestaurantLoader(),
    folders=[
        Folder(
            name="미분류",
            memo="",
            public=True,
            color=Color.LIGHT_GREEN,
            criteria_func=lambda restaurant: len(restaurant.dinner_prices) == 0,
        ),
        Folder(
            name="디너 ~50,000",
            memo="",
            public=True,
            color=Color.GREEN,
            criteria_func=lambda restaurant: any(
                [price <= 50_000 for price in restaurant.dinner_prices]
            ),
        ),
        Folder(
            name="디너 50,001 ~ 100,000",
            memo="",
            public=True,
            color=Color.YELLOW,
            criteria_func=lambda restaurant: any(
                [50_000 < price <= 100_000 for price in restaurant.dinner_prices]
            ),
        ),
        Folder(
            name="디너 100,001 ~ 150,000",
            memo="",
            public=True,
            color=Color.PINK,
            criteria_func=lambda restaurant: any(
                [100_000 < price <= 150_000 for price in restaurant.dinner_prices]
            ),
        ),
        Folder(
            name="디너 150,001 ~ 200,000",
            memo="",
            public=True,
            color=Color.ORANGE,
            criteria_func=lambda restaurant: any(
                [150_000 < price <= 200_000 for price in restaurant.dinner_prices]
            ),
        ),
        Folder(
            name="디너 200,001 ~ 250,000",
            memo="",
            public=True,
            color=Color.RED,
            criteria_func=lambda restaurant: any(
                [200_000 < price <= 250_000 for price in restaurant.dinner_prices]
            ),
        ),
        Folder(
            name="디너 250,001 ~ 300,000",
            memo="",
            public=True,
            color=Color.PURPLE,
            criteria_func=lambda restaurant: any(
                [250_000 < price <= 300_000 for price in restaurant.dinner_prices]
            ),
        ),
        Folder(
            name="디너 300,001 ~ ",
            memo="",
            public=True,
            color=Color.PURPLE,
            criteria_func=lambda restaurant: any(
                [300_000 < price for price in restaurant.dinner_prices]
            ),
        ),
    ],
).sync()
