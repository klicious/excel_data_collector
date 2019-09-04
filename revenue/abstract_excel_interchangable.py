from datetime import datetime
from abc import ABCMeta, abstractmethod


class AbstractExcelInterchangable(metaclass=ABCMeta):

    @abstractmethod
    def adapt_to_data_frame_element(self):
        pass

    @classmethod
    @abstractmethod
    def adapt_data_frame_element(cls, element, default_date):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_columns(cls):
        raise NotImplementedError

    @staticmethod
    def default_if_invalid_datetime(date_text: str, datetime_format: str, default: datetime):
        try:
            return datetime.strptime(date_text, datetime_format)
        except ValueError:
            return default
