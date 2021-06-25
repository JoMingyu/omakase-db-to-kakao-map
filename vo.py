import re
from enum import Enum
from typing import List, Callable, Optional, Union

from pydantic.main import BaseModel


class RestaurantInfoInMap(BaseModel):
    id: Optional[str]
    address: Optional[str]
    x: Optional[int]
    y: Optional[int]


class Restaurant(BaseModel):
    name: str
    dinner_prices: List[int]
    address: Optional[str]
    info_in_map: Optional[RestaurantInfoInMap]

    @classmethod
    def listify_price(cls, v: Union[int, str]) -> List[int]:
        if isinstance(v, int):
            return [v]

        if ":" in v:
            # A : 6 / B : 9 형태
            v = "/".join(re.findall(r": (\d+)", v))

        separator_removed_price = v.replace(",", "")

        if "/" in separator_removed_price:
            # 코스 따라 다른 경우

            result = []

            prices = [price.strip() for price in separator_removed_price.split("/")]

            for price in prices:
                price = price.rstrip("만")
                # "5.5만" 같은 케이스가 있음

                if "." in price:
                    # 4.4, 6.6 같은 format

                    result.append(int(float(price) * 10000))
                else:
                    result.append(int(price))
        else:
            result = [int(separator_removed_price)]

        return result


class Color(str, Enum):
    RED = "01"
    YELLOW = "02"
    ORANGE = "03"
    LIGHT_GREEN = "04"
    GREEN = "05"
    PURPLE = "06"
    PINK = "07"


class Folder(BaseModel):
    name: str
    memo: str
    public: bool
    color: Color  # place 단위로 설정할 수 있으나 폴더수준에서 일관성 있게 하는게 보기 좋을것 같아서
    criteria_func: Callable[[Restaurant], bool]
    icon: str = "01"
    id_on_map: Optional[str] = None
