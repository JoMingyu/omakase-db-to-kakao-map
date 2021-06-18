import csv
from typing import List, Optional

from pydantic import ValidationError

from vo import Restaurant

NAME_FALLBACKS = {"스시마카세(남부)": "스시마카세", "스시마카세(역삼)": "스시마카세 역삼점"}


class RestaurantLoader:  # 더 잘 디자인하기 포기
    def build_restaurant(self, row: dict) -> Optional[Restaurant]:
        name = row[4]
        name = NAME_FALLBACKS.get(name, name)

        if name == "":
            return None

        lunch_price = row[5]
        dinner_price = row[6]

        if dinner_price == "":
            # lunch, dinner 똑같아서 column 합쳐진 경우
            dinner_price = lunch_price

        address = row[15]

        try:
            restaurant = Restaurant(
                name=name,
                dinner_prices=Restaurant.listify_price(dinner_price),
                address=address,
            )

            return restaurant
        except (ValidationError, ValueError) as e:
            print(f"{name} skipped during make VO. reason: {e}")
            return None

    def load(self) -> List[Restaurant]:
        with open("data.csv") as f:
            data = list(csv.reader(f))

        result = []

        for row in data[7:]:
            restaurant = self.build_restaurant(row)

            if restaurant:
                result.append(restaurant)

        return result
