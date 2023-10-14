"""
    定义调用方请求接口校验的方法，返回错误消息，若校验通过则返回None
    by organwalk 2023-08-15
"""
from server_code.utils import fields_utils
from typing import Optional
from datetime import datetime, timedelta
import server_code.repository.repository as repository


def validate_json_user_req(api: str, user_req_json: dict, server_req_fields: list) -> Optional[str]:
    """
    校验调用方请求中的 JSON 数据
    :param api: API 接口路径
    :param user_req_json: 调用方请求中的 JSON 数据
    :param server_req_fields: 服务器端要求的 JSON 数据字段
    :return:
        str or None: 错误消息，如果校验通过则返回 None

    by organwalk 2023-08-15
    """
    # 0.检验调用方请求是否存在JSON格式数据
    if not user_req_json:
        return '调用方未能正确传递JSON格式数据'
    # 1.检验JSON格式数据是否存在空缺值
    missing_check = _validate_json_missing(user_req_json, server_req_fields)
    if missing_check:
        return f'调用方传递JSON格式数据存在空缺值，提示消息如下：{missing_check}'
    # 2.检验对应接口的JSON格式数据其值类型与格式是否正确
    error_msg = _validate_json_value(user_req_json, api)
    if error_msg is not None:
        return f'调用方传递JSON格式数据存在错误，提示消息如下：{error_msg}'

    return None


def _validate_json_missing(user_req_json: dict, server_req_fields: list) -> Optional[str]:
    """
    校验调用方请求中的 JSON 数据是否含有空缺值
    :param user_req_json: 调用方请求中的 JSON 数据
    :param server_req_fields: 服务器端要求的 JSON 数据字段
    :return:
        str or None: 错误消息，如果校验通过则返回 None

    by organwalk 2023-08-15
    """
    missing_fields = [field for field in server_req_fields if not user_req_json.get(field)]
    if missing_fields:
        missing_fields_str = "、".join(missing_fields)
        return f"字段{missing_fields_str}不能为空"
    return None


def _validate_json_value(user_req_json: dict, api: str) -> Optional[str]:
    """
    校验调用方JSON数据的类型与格式是否正确
    :param user_req_json: (dict)调用方传递的JSON数据
    :param api(str): API接口路径
    :return:
        str or None: 错误消息，如果校验通过则返回None

    by organwalk 2023-08-15
    """
    if api == '/anapredict/model/report':
        return _validate_api_report(user_req_json)
    if api == '/anapredict/cleaned':
        return _validate_api_cleaned(user_req_json)
    if api == '/anapredict/analyze/correlation':
        return _validate_api_correlation(user_req_json)
    if api == '/anapredict/model/prediction':
        return _validate_api_prediction(user_req_json)
    else:
        return None


def _validate_api_report(user_req_json: dict) -> Optional[str]:
    """
    校验/anapredict/model/report接口的JSON数据
    :param user_req_json: 调用方传递的JSON数据：
        model_type: (str) 模型类型
    :return:
        str or None: 错误消息，如果校验通过则返回None

    by organwalk 2023-10-14
    """
    error_msg_list = [fields_utils.validate_model_type(user_req_json.get('model_type'))]
    msg_list = [msg['msg'] for msg in error_msg_list if isinstance(msg, dict)]
    return '；'.join(set(msg_list)) if msg_list else None


def _validate_api_cleaned(user_req_json: dict) -> Optional[str]:
    """
    校验/anapredict/cleaned接口的json数据
    :param user_req_json: 调用方传递的JSON数据：
        station: (str) 气象站编号
        start_date: (str) 起始日期
        end_date: (str) 结束日期
    :return:
        str or None: 错误消息，如果校验通过则返回None

    by organwalk 2023-10-14
    """
    error_msg_list = [fields_utils.validate_station(user_req_json['station']),
                      fields_utils.validate_date(user_req_json['station'], user_req_json['start_date']),
                      fields_utils.validate_date(user_req_json['station'], user_req_json['end_date'])]
    msg_list = [msg['msg'] for msg in error_msg_list if isinstance(msg, dict)]
    return '；'.join(set(msg_list)) if msg_list else None


def _validate_api_correlation(user_req_json: dict) -> Optional[str]:
    """
    校验/anapredict/analyze/correlation接口的JSON数据
    :param:
        user_req_json: 调用方传递的JSON数据:
            station: (str) 气象站编号
            start_date: (str) 起始日期
            end_date: (str) 结束日期
            correlation: (str) 需要计算相关系数矩阵的气象要素
    :return:
        str or None: 错误消息，如果校验通过则返回None

    by organwalk 2023-08-15
    """
    error_msg_list = [fields_utils.validate_station(user_req_json['station']),
                      fields_utils.validate_date(user_req_json['station'], user_req_json['start_date']),
                      fields_utils.validate_date(user_req_json['station'], user_req_json['end_date']),
                      fields_utils.validate_which_or_correlation(user_req_json['correlation'])]
    msg_list = [msg['msg'] for msg in error_msg_list if isinstance(msg, dict)]
    return '；'.join(set(msg_list)) if msg_list else None


def _validate_api_prediction(user_req_json: dict) -> Optional[str]:
    """
    校验/anapredict/model/prediction接口的JSON数据
    :param:
        user_req_json: 调用方传递的JSON数据:
            station: (str) 气象站编号
            start_date: (str) 起始日期
            end_date: (str) 结束日期
            model_type: (str) 模型类型
    :return:
        str or None: 错误消息，如果校验通过则返回None

    by organwalk 2023-08-15
    """
    error_msg_list = [fields_utils.validate_station(user_req_json['station']),
                      fields_utils.validate_date(user_req_json['station'], user_req_json['start_date']),
                      fields_utils.validate_model_type(user_req_json['model_type'])]
    msg_list = [msg['msg'] for msg in error_msg_list if isinstance(msg, dict)]
    # error_msg_list的子元素错误消息为字典形式，若为str类型，则表示没有错误消息
    if user_req_json.get("model_type") == "LONGTERM_LSTM":
        date = (datetime.strptime(user_req_json.get("start_date"), '%Y-%m-%d')
                + timedelta(days=-6)).strftime('%Y-%m-%d')
        check = repository.validate_station_date_range(station=user_req_json.get('station'),
                                                       start_date=date,
                                                       end_date=user_req_json.get('start_date'))
        if check < 7:
            msg_list.append(f"该日期{user_req_json.get('start_date')}不可作为起始日期，原因：气象站缺失连续时间段内数据")
    return '；'.join(set(msg_list)) if msg_list else None
