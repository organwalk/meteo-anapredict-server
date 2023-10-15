"""
    定义接口具体字段校验方法
    by organwalk 2023-08-15
"""
import re
import repository
from config import SHORT_TERM_MODEL_LIST, LONG_TERM_MODEL_LIST
from datetime import datetime, timedelta
from typing import Union, Dict


def validate_station(station: str) -> Union[str, Dict[str, str]]:
    """
    校验气象站编号字段的正确性
    :param station: 气象站编号
    :return:
        str or dict: station的值，如果校验不通过则返回错误消息

    by organwalk 2023-08-15
    """
    return station if isinstance(station, str) else _get_error_msg("station字段需要字符串类型的气象站编号")


def validate_date(station: str, date: str) -> Union[str, Dict[str, str]]:
    """
    校验起始日期和截止日期的有效性
    :param station: 气象站编号
    :param date: 日期
    :return:
        str or dict: date的值，如果校验不通过则返回错误消息

    by organwalk 2023-08-15
    """
    if isinstance(date, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        if repository.validate_station_date(station, date) > 0:
            return date
        else:
            return _get_error_msg(f"值为{date}的date相关字段，其日期下不存在有效数据，请重新指定")
    else:
        return _get_error_msg("date相关字段需要YYYY-MM-DD格式字符串")


def validate_which_or_correlation(elements: str) -> Union[str, Dict[str, str]]:
    """
    校验气象要素的正确性
    :param elements: 气象要素
    :return:
        str or dict: elements的值，如果校验不通过则返回错误消息

    by organwalk 2023-08-15
    """
    if isinstance(elements, str) and re.match(r'^[1-8,]+$', elements):
        numbers = [int(num) for num in elements.split(',') if num.isdigit()]
        if all(1 <= num <= 8 for num in numbers):
            return elements
    return _get_error_msg("气象要素相关字段需要以英文逗号分割的数字字符串格式数据，例如：1,2,3,范围在1-8")


def validate_model_type(model_type: str) -> Union[str, Dict[str, str]]:
    """
    校验模型类型的正确性
    :param model_type: 模型类型
    :return:
        str or dict: model_type的值，如果校验不通过则返回错误消息

    by organwalk 2023-08-20
    """

    if isinstance(model_type, str) and (model_type in SHORT_TERM_MODEL_LIST or model_type in LONG_TERM_MODEL_LIST):
        return model_type
    else:
        return _get_error_msg("model_type是字符串类型数据，其具体值已在接口文档中定义，请输入接口文档定义值")


def validate_five_day_date_range(start_date: str, end_date: str) -> bool:
    """
    校验日期范围是否大于等于五天
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
        bool: 大于等于五天时返回True，否则False

    by organwalk 2023-08-20
    """
    date_diff = abs(datetime.strptime(end_date, '%Y-%m-%d').date() - datetime.strptime(start_date, '%Y-%m-%d').date())
    return True if date_diff >= timedelta(days=5) else False


def _get_error_msg(msg: str) -> dict:
    """
    返回字典形式的错误消息
    :param msg: (str)错误消息
    :return:
        dict: 错误消息的字典形式

    by organwalk 2023-08-15
    """
    return {'msg': msg}
