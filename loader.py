import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Union

from openpyxl import load_workbook
from pydantic import BaseModel

from vo import Restaurant

NAME_FALLBACKS = {"스시마카세(남부)": "스시마카세", "스시마카세(역삼)": "스시마카세 역삼점"}


class Row(BaseModel):
    name: Optional[str]
    lunch_price: Optional[Union[int, float, str, datetime]]
    dinner_price: Optional[Union[int, float, str, datetime]]
    address: Optional[str]


class Loader(ABC):
    def __init__(self, data_path: str):
        self.data_path = data_path

    @abstractmethod
    def load(self) -> List[Restaurant]:
        pass

    def _build_dataset(self, rows: List[Row]) -> List[Restaurant]:
        result = []

        for row in rows:
            if row.name in ("업장명", "", None):
                continue

            if row.name in ("쌩 메종",):
                # 얘네 가격이 유로임
                continue

            if row.name in ("롯데호텔모모야마",):
                # 변동가 ㅋㅋ
                continue

            if row.dinner_price in ("-",):
                continue

            if row.dinner_price is None:
                if row.lunch_price:
                    row.dinner_price = row.lunch_price
                else:
                    continue

            if isinstance(row.dinner_price, datetime):
                # 5/7 같이 표기한 경우 날짜로 인식됨 ㅋㅋ
                row.dinner_price = f"{row.dinner_price.month}/{row.dinner_price.day}"

            row.name = NAME_FALLBACKS.get(row.name, row.name)

            if row.name == "스시정미":
                row.dinner_price = (
                    int(re.findall(r"오마카세 (\d+)만", row.dinner_price)[0]) * 10000
                )

            result.append(
                Restaurant(
                    name=row.name,
                    dinner_prices=Restaurant.listify_price(row.dinner_price),
                    address=row.address,
                )
            )

        return result


# class CsvLoader(Loader):
#     def load(self) -> List[Restaurant]:
#         with open(self.data_path) as f:
#             data = list(csv.reader(f))
#
#         result = []
#
#         for row in data[7:]:
#             restaurant = self.build_restaurant(row)
#
#             if restaurant:
#                 result.append(restaurant)
#
#         return result


class XlsxLoader(Loader):
    def load(self) -> List[Restaurant]:
        workbook = load_workbook(self.data_path, data_only=True)

        rows = []
        for sheet in workbook.worksheets[:3]:
            for row in sheet.rows:
                rows.append(
                    Row(
                        name=row[4].value,
                        lunch_price=row[5].value,
                        dinner_price=row[6].value,
                        address=row[15].value,
                    )
                )

        rows = self._build_dataset(rows=rows)

        return rows
