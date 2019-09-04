import pandas as pd

from dataclasses import dataclass
from datetime import datetime
from revenue.abstract_revenue import AbstractRevenue


@dataclass
class AlbumAndGoodsRevenue(AbstractRevenue):
    sales_date: datetime  # 매출일자
    slip_id: str  # 전표번호
    account: str  # 매출처
    main_category: str  # 대분류
    product_id: str  # 품목
    yg_product_id: str  # 변환코드
    product_name: str  # 품목명
    product_type: str  # 세부규격
    product_group: str  # 품목군 artist
    product_specification: str  # 규격
    to_be_settled: str  # 정산대상여부
    sales_quantity: int  # 매출수량
    sales_amount: int  # 매출금액
    shipping_unit_price: int  # 출고단가
    total_shipping_unit_price: int  # 출고가합계
    supply_price: int  # 공급가액
    vat: int  # 부가세
    supply_cost: int  # 공급대가

    def adapt_to_data_frame_element(self):
        return pd.DataFrame({
            "매출일자": [self.sales_date],
            "전표번호": [self.slip_id],
            "매출처": [self.account],
            "대분류": [self.main_category],
            "품목": [self.product_id],
            "변환코드": [self.yg_product_id],
            "품목명": [self.product_name],
            "세부규격": [self.product_type],
            "품목군": [self.product_group],
            "규격": [self.product_specification],
            "정산대상여부": [self.to_be_settled],
            "매출수량": [self.sales_quantity],
            "매출금액": [self.sales_amount],
            "출고단가": [self.shipping_unit_price],
            "출고가합계": [self.total_shipping_unit_price],
            "공급가액": [self.supply_price],
            "부가세": [self.vat],
            "공급대": [self.supply_cost]
        })

    @classmethod
    def get_columns(cls):
        return ['매출일자', '전표번호', '매출처', '대분류', '품목', '변환코드', '품목명', '세부규격', '품목군', '규격', '정산대상여부', '매출수량', '매출금액',
                '출고단가', '출고가합계', '공급가액', '부가세', '공급대가']

    @classmethod
    def adapt_data_frame_element(cls, element, default_date):
        sales_date = super().default_if_invalid_datetime(str(element['매출일자']), '%Y/%m/%d', default_date)
        return AlbumAndGoodsRevenue(sales_date, element['전표번호'], element['매출처'], element['대분류'], element['품목'],
                                    element['변환코드'], element['품목명'], element['세부규격'], element['품목군'], element['규격'],
                                    element['정산대상여부'], element['매출수량'], element['매출금액'], element['출고단가'],
                                    element['출고가합계'], element['공급가액'], element['부가세'], element['공급대가'])
