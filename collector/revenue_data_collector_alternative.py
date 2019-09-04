import os
import pandas

from datetime import datetime
from revenue.album_and_goods_revenue import AlbumAndGoodsRevenue
from revenue.album_revenue import AlbumRevenue
from revenue.goods_revenue import GoodsRevenue


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


base_directory_path = r'../resources/revenue'
album_revenues = list()
goods_revenues = list()
album_and_goods_revenues = list()

current_directory_path = base_directory_path + '/album'
album_files = [f for f in os.listdir(current_directory_path) if
               os.path.isfile(os.path.join(current_directory_path, f)) and '.xlsx' in f]
for file in album_files:
    album_and_goods_revenues.extend(
        create_revenue_list_from_file_path(current_directory_path, file, AlbumAndGoodsRevenue.get_columns,
                                           AlbumAndGoodsRevenue.adapt_data_frame_element))

current_directory_path = base_directory_path + '/goods'
goods_files = [f for f in os.listdir(current_directory_path) if
               os.path.isfile(os.path.join(current_directory_path, f)) and '.xlsx' in f]
for file in goods_files:
    goods_revenues.extend(create_revenue_list_from_file_path(current_directory_path, file, GoodsRevenue.get_columns,
                                                             GoodsRevenue.adapt_data_frame_element))

current_directory_path = base_directory_path + '/album_and_goods'
album_and_goods_files = [f for f in os.listdir(current_directory_path) if
                         os.path.isfile(os.path.join(current_directory_path, f)) and '.xlsx' in f]
for file in album_and_goods_files:
    album_revenues.extend(create_revenue_list_from_file_path(current_directory_path, file, AlbumRevenue.get_columns,
                                                             AlbumRevenue.adapt_data_frame_element))

album_revenues.sort(key=lambda album: (album.registered_date, album.company_code))
goods_revenues.sort(key=lambda goods: (goods.registered_date, goods.company_code))
album_and_goods_revenues.sort(key=lambda album_and_goods: (album_and_goods.sales_date, album_and_goods.product_id))

print(len(album_revenues))
print(len(goods_revenues))
print(len(album_and_goods_revenues))
