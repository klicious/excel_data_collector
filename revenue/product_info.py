import pandas as pd

from dataclasses import dataclass

from revenue.abstract_excel_interchangable import AbstractExcelInterchangable


@dataclass
class Product(AbstractExcelInterchangable):
    product_id: str  # 제품코드
    product_type: str  # 분류
    product_group: str  # 품목군 Artist
    product_name: str  # 품목명
    unit_price: int  # 단가

    def adapt_to_data_frame_element(self):
        return pd.DataFrame({
            "제품코드": [self.product_id],
            "분류": [self.product_type],
            "품목군": [self.product_group],
            "품목명": [self.product_name],
            "단가": [self.unit_price]
        })

    @classmethod
    def adapt_data_frame_element(cls, element, default_date):
        return Product(str(element['제품코드']), str(element['분류']), str(element['품목군']), element['품목명'], element['단가'])

    @classmethod
    def get_columns(cls):
        return ['제품코드', '분류', '품목군', '품목명', '단가']
