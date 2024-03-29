import pandas as pd
import math

from dataclasses import dataclass

from revenue.abstract_excel_interchangable import AbstractExcelInterchangable
from revenue.album_and_goods_revenue import AlbumAndGoodsRevenue
from revenue.album_revenue import AlbumRevenue
from revenue.goods_revenue import GoodsRevenue


def _reformat_management_code(_management_code):
    if type(_management_code) is float and math.isnan(_management_code):
        _management_code = '0'
    if _management_code is None:
        _management_code = '0'
    return str(_management_code).zfill(7)


@dataclass
class YgRevenue(AbstractExcelInterchangable):
    revenue_date: str  # 매출일자
    management_code: str  # 관리코드
    product_name: str  # 상품명
    artist: str  # 아티스트
    quantity: int  # 수량
    unit_price: int  # 단가
    revenue: int  # 매출액

    def adapt_to_data_frame_element(self):
        return pd.DataFrame({
            "매출일자": [self.revenue_date],
            "관리코드": [self.management_code],
            "상품명": [self.product_name],
            "아티스트": [self.artist],
            "수량": [self.quantity],
            "단가": [self.unit_price],
            "매출액": [self.revenue]
        })

    @classmethod
    def adapt_data_frame_element(cls, element, default_date):
        return YgRevenue(element['매출일자'].astype(str), element['관리코드'].astype(str), element['상품명'].astype(str),
                         element['아티스트'].astype(str), element['수량'], element['단가'], element['매출액'])

    @classmethod
    def get_columns(cls):
        return ["매출일자", "관리코드", "상품명", "아티스트", "수량", "단가", "매출액"]

    @staticmethod
    def adapt_album_revenue(_revenue: AlbumRevenue):
        _revenue_date: str = _revenue.registered_date.strftime('%Y%m')
        _management_code: str = _reformat_management_code(_revenue.management_code)
        return YgRevenue(_revenue_date, _management_code, _revenue.product_name, _revenue.product_specification,
                         _revenue.quantity, _revenue.unit_price, _revenue.total_amount)

    @staticmethod
    def adapt_goods_revenue(_revenue: GoodsRevenue):
        _revenue_date: str = _revenue.registered_date.strftime('%Y%m')
        _management_code: str = _reformat_management_code(_revenue.management_code)
        return YgRevenue(_revenue_date, _management_code, _revenue.product_name, _revenue.product_specification,
                         _revenue.quantity, _revenue.unit_price, _revenue.total_amount)

    @staticmethod
    def adapt_album_and_goods_revenue(_revenue: AlbumAndGoodsRevenue):
        _revenue_date: str = _revenue.sales_date.strftime('%Y%m')
        _management_code: str = _reformat_management_code(_revenue.yg_product_id)
        return YgRevenue(_revenue_date, _revenue.yg_product_id, _revenue.product_name, _revenue.product_specification,
                         _revenue.sales_quantity, _revenue.shipping_unit_price, _revenue.sales_amount)


