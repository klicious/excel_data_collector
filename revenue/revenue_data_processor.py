import os
import pandas

from datetime import datetime
from typing import Dict, Tuple, List
from revenue.album_and_goods_revenue import AlbumAndGoodsRevenue
from revenue.album_revenue import AlbumRevenue
from revenue.goods_revenue import GoodsRevenue
from revenue.product_info import Product
from revenue.yg_revenue import YgRevenue


def create_revenue_list_from_file_path(__root: str, __file: str, get_columns, adapt_data_frame_element):
    revenues = list()
    ym = __file[:6]
    ymd_string = ym + '01'
    path = os.path.join(__root, __file)
    d = pandas.read_excel(path)
    df = pandas.DataFrame(d, columns=get_columns())
    for i, r in df.iterrows():
        __ar = adapt_data_frame_element(r, datetime.strptime(ymd_string, '%Y%m%d'))
        if __ar is not None:
            revenues.append(__ar)

    return revenues


def collect_product_information_data():
    _products = list()
    _file_path = r'../resources/product/product_infos.xlsx'
    _d = pandas.read_excel(_file_path)
    _df = pandas.DataFrame(_d, columns=Product.get_columns())
    for i, r in _df.iterrows():
        _ar = Product.adapt_data_frame_element(r, datetime.now())
        if _ar is not None:
            _products.append(_ar)
    return _products


def collect_revenue_data():
    file_directory_path = r'../resources/revenue'
    __album_revenues = list()
    __goods_revenues = list()
    __album_and_goods_revenues = list()
    for root, directories, files in os.walk(file_directory_path):
        print('current root is: ' + root)
        for file in files:
            if '.xlsx' in file:
                if root.endswith('album_and_goods'):
                    print('[앨범&상품]' + root + '/' + file)
                    __album_and_goods_revenues.extend(
                        create_revenue_list_from_file_path(root, file, AlbumAndGoodsRevenue.get_columns,
                                                           AlbumAndGoodsRevenue.adapt_data_frame_element))
                elif root.endswith('goods'):
                    print('[상품]' + root + '/' + file)
                    __goods_revenues.extend(
                        create_revenue_list_from_file_path(root, file, GoodsRevenue.get_columns,
                                                           GoodsRevenue.adapt_data_frame_element))
                elif root.endswith('album'):
                    print('[앨범]' + root + '/' + file)
                    __album_revenues.extend(
                        create_revenue_list_from_file_path(root, file, AlbumRevenue.get_columns,
                                                           AlbumRevenue.adapt_data_frame_element))
    return __album_revenues, __goods_revenues, __album_and_goods_revenues


# 매출 데이터 수집
album_revenues, goods_revenues, album_and_goods_revenues = collect_revenue_data()

print(len(album_revenues))
print(len(goods_revenues))
print(len(album_and_goods_revenues))

# 최종 형태로 변환
yg_revenues = list()

for _album in album_revenues:
    yg_revenues.append(YgRevenue.adapt_album_revenue(_album))

for _goods in goods_revenues:
    yg_revenues.append(YgRevenue.adapt_goods_revenue(_goods))

for _album_and_goods in album_and_goods_revenues:
    yg_revenues.append(YgRevenue.adapt_album_and_goods_revenue(_album_and_goods))

unique_management_codes = {_revenue.management_code for _revenue in yg_revenues}
for _code in unique_management_codes:
    print(_code)

# 상품 정보 조회 및 주입
products: List[Product] = collect_product_information_data()
dict_products: Dict[str, Product] = {p.product_id: p for p in products}
for _revenue in yg_revenues:
    _key = _revenue.management_code
    if _key in dict_products.keys():
        _product = dict_products[_key]
        _revenue.product_name = _product.product_name
        _revenue.unit_price = _product.unit_price
        _revenue.artist = _product.product_group

# 월별 매출 취합
dict_of_yg_revenue: Dict[Tuple[str, str], YgRevenue] = dict()

for _revenue in yg_revenues:
    _key = (_revenue.revenue_date, _revenue.management_code)
    if _key not in dict_of_yg_revenue.keys():
        dict_of_yg_revenue[_key] = _revenue
    else:
        _yg_revenue = dict_of_yg_revenue[_key]
        _yg_revenue.quantity += _revenue.quantity
        _yg_revenue.revenue += _revenue.revenue

# 월별 매출 분류
yg_revenues_final: List[YgRevenue] = [v for v in dict_of_yg_revenue.values()]
yg_revenues_final.sort(key=lambda r: (r.revenue_date, r.management_code))

print(" ::::: yg_revenues_final")
for _revenue in yg_revenues_final:
    print(_revenue)

dict_of_yg_revenues_by_month: Dict[str, list] = dict()

for _revenue in yg_revenues_final:
    _key = _revenue.revenue_date
    if _key not in dict_of_yg_revenues_by_month:
        dict_of_yg_revenues_by_month[_key] = list()
        dict_of_yg_revenues_by_month[_key].append(_revenue)
    else:
        dict_of_yg_revenues_by_month[_key].append(_revenue)

print(" ::::: dict_of_yg_revenues_by_month")
# for _key in dict_of_yg_revenues_by_month:
#     print("key: " + _key)
#     print("length: " + str(len(dict_of_yg_revenues_by_month[_key])))

dict_of_yg_revenues_by_management_code: Dict[str, list] = dict()

for _revenue in yg_revenues_final:
    _key = _revenue.management_code
    if _key not in dict_of_yg_revenues_by_management_code:
        dict_of_yg_revenues_by_management_code[_key] = list()
        dict_of_yg_revenues_by_management_code[_key].append(_revenue)
    else:
        dict_of_yg_revenues_by_management_code[_key].append(_revenue)

print(" ::::: dict_of_yg_revenues_by_management_code")
# for _key in dict_of_yg_revenues_by_management_code:
#     print("key: " + _key)
#     print("length: " + str(len(dict_of_yg_revenues_by_management_code[_key])))

# 마무리
