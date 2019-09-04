import pandas as pd

from dataclasses import dataclass
from datetime import datetime
from revenue.abstract_excel_interchangable import AbstractExcelInterchangable


@dataclass
class GoodsRevenue(AbstractExcelInterchangable):
    registered_date: datetime  # 일자
    company_code: str  # ccode
    business_registration_number: str  # 사업자번호
    merchant: str  # 거래처
    storage_name: str  # 창고명
    loading_location: str  # 적재위치
    base_code: str  # 기본코드
    management_code: str  # 관리코드
    bar_code: str  # 바코드
    product_name: str  # 상 품 명
    product_specification: str  # 규격 artist
    unit: str  # 단위
    quantity: int  # 수량
    unit_price: int  # 단 가
    supply_price: int  # 공급가액
    vat: int  # 부가세
    discount_amount: int  # 할 인
    total_amount: int  # 합계액
    ordered_date_time: datetime  # Time
    row_key: str  # ROWKEY
    memo: str  # 비고

    def adapt_to_data_frame_element(self):
        return pd.DataFrame({
            "일자": [self.registered_date],
            "ccode": [self.company_code],
            "사업자번호": [self.business_registration_number],
            "거래처": [self.merchant],
            "창고명": [self.storage_name],
            "적재위치": [self.loading_location],
            "기본코드": [self.base_code],
            "관리코드": [self.management_code],
            "바코드": [self.bar_code],
            "상 품 명": [self.product_name],
            "규격": [self.product_specification],
            "단위": [self.unit],
            "수량": [self.quantity],
            "단 가": [self.unit_price],
            "공급가액": [self.supply_price],
            "부가세": [self.vat],
            "할 인": [self.discount_amount],
            "합계액": [self.total_amount],
            "Time": [self.ordered_date_time],
            "ROWKEY": [self.row_key],
            "비고": [self.memo]
        })

    @classmethod
    def get_columns(cls):
        return ['일자', 'ccode', '사업자번호', '거래처', '창고명', '적재위치', '기본코드', '관리코드', '바코드', '상 품 명', '규 격', '단위', '수량', '단 가',
                '공급가액', '부가세', '할 인', '합계액', 'Time', 'ROWKEY', '비고']

    @classmethod
    def adapt_data_frame_element(cls, element, default_date):
        registered_date_time = super().default_if_invalid_datetime(str(element['일자']), '%Y-%m-%d', default_date)
        ordered_date_time = super().default_if_invalid_datetime(str(element['Time']), '%Y-%m-%d %H:%M', default_date)
        company_code = str(element['ccode']).zfill(6)
        return GoodsRevenue(registered_date_time, company_code, str(element['사업자번호']), element['거래처'], element['창고명'],
                            element['적재위치'], element['기본코드'], str(element['관리코드']), element['바코드'], element['상 품 명'],
                            element['규 격'], element['단위'], element['수량'], element['단 가'], element['공급가액'],
                            element['부가세'],
                            element['할 인'], element['합계액'], ordered_date_time, element['ROWKEY'], element['비고'])
