import os
import pandas

from datetime import datetime
from typing import Dict, Tuple
from revenue.album_and_goods_revenue import AlbumAndGoodsRevenue
from revenue.album_revenue import AlbumRevenue
from revenue.goods_revenue import GoodsRevenue
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
                    __goods_revenues.extend(create_revenue_list_from_file_path(root, file, GoodsRevenue.get_columns,
                                                                               GoodsRevenue.adapt_data_frame_element))
                elif root.endswith('album'):
                    print('[앨범]' + root + '/' + file)
                    __album_revenues.extend(create_revenue_list_from_file_path(root, file, AlbumRevenue.get_columns,
                                                                               AlbumRevenue.adapt_data_frame_element))
    return __album_revenues, __goods_revenues, __album_and_goods_revenues


album_revenues, goods_revenues, album_and_goods_revenues = collect_revenue_data()

# album_revenues.sort(key=lambda album: (album.registered_date, album.company_code))
# goods_revenues.sort(key=lambda goods: (goods.registered_date, goods.company_code))
# album_and_goods_revenues.sort(key=lambda album_and_goods: (album_and_goods.sales_date, album_and_goods.product_id))

print(len(album_revenues))
print(len(goods_revenues))
print(len(album_and_goods_revenues))

yg_revenues = list()

for _album in album_revenues:
    yg_revenues.append(YgRevenue.adapt_album_revenue(_album))

for _goods in goods_revenues:
    yg_revenues.append(YgRevenue.adapt_goods_revenue(_goods))

for _album_and_goods in album_and_goods_revenues:
    yg_revenues.append(YgRevenue.adapt_album_and_goods_revenue(_album_and_goods))

dict_of_yg_revenue: Dict[Tuple[str, str], YgRevenue] = dict()

for _revenue in yg_revenues:
    _key = (_revenue.revenue_date, _revenue.management_code)
    if _key not in dict_of_yg_revenue.keys():
        dict_of_yg_revenue[_key] = _revenue
    else:
        _yg_revenue = dict_of_yg_revenue[_key]
        _yg_revenue.quantity += _revenue.quantity
        _yg_revenue.revenue += _revenue.revenue


yg_revenues_final = [v for v in dict_of_yg_revenue.values()]
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
for _key in dict_of_yg_revenues_by_month:
    print("key: " + _key)
    print("length: " + str(len(dict_of_yg_revenues_by_month[_key])))

dict_of_yg_revenues_by_management_code: Dict[str, list] = dict()

for _revenue in yg_revenues_final:
    _key = _revenue.management_code
    if _key not in dict_of_yg_revenues_by_management_code:
        dict_of_yg_revenues_by_management_code[_key] = list()
        dict_of_yg_revenues_by_management_code[_key].append(_revenue)
    else:
        dict_of_yg_revenues_by_management_code[_key].append(_revenue)

print(" ::::: dict_of_yg_revenues_by_management_code")
for _key in dict_of_yg_revenues_by_management_code:
    print("key: " + _key)
    print("length: " + str(len(dict_of_yg_revenues_by_management_code[_key])))

