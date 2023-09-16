"""
    定义调用方请求接口校验的方法，返回错误消息，若校验通过则返回None
    by organwalk 2023-08-15
"""
from server_code.utils import fields_utils


def validate_json_user_req(api: str, user_req_json: dict, server_req_fields: list):
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
    missing_check = __validate_json_missing(user_req_json, server_req_fields)
    if missing_check:
        return f'调用方传递JSON格式数据存在空缺值，提示消息如下：{missing_check}'

    # 2.检验对应接口的JSON格式数据其值类型与格式是否正确
    error_msg = __validate_json_value(user_req_json, api)
    if error_msg is not None:
        return f'调用方传递JSON格式数据存在错误，提示消息如下：{error_msg}'

    return None


def __validate_json_missing(user_req_json: dict, server_req_fields: list):
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


def __validate_json_value(user_req_json: dict, api: str):
    """
    校验调用方JSON数据的类型与格式是否正确

    :param user_req_json: (dict)调用方传递的JSON数据
    :param api(str): API接口路径
    :return:
        str or None: 错误消息，如果校验通过则返回None

    by organwalk 2023-08-15
    """
    if api == '/anapredict/analyze/correlation':
        return __validate_api_correlation(user_req_json)
    if api == '/anapredict/model/prediction':
        return __validate_api_prediction(user_req_json)
    else:
        return None


def __validate_api_correlation(user_req_json: dict):
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


def __validate_api_prediction(user_req_json: dict):
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
                      fields_utils.validate_date(user_req_json['station'], user_req_json['end_date']),
                      fields_utils.validate_model_type(user_req_json['model_type'])]
    msg_list = [msg['msg'] for msg in error_msg_list if isinstance(msg, dict)]
    # error_msg_list的子元素错误消息为字典形式，若为str类型，则表示没有错误消息
    if all(isinstance(item, str) for item in error_msg_list):
        model_type = str(user_req_json['model_type'])
        start_date = str(user_req_json['start_date'])
        end_date = str(user_req_json['end_date'])
        # 0.检查24小时预测时模型选取是否正确
        if start_date == end_date and model_type.split('_')[0] != 'SHORTTERM':
            msg_list.append('当start_date与end_date相等时表示未来24小时预测，model_type应为SHORTTERM前缀的模型')
        elif start_date != end_date:
            # 1.检查未来七日预测时间是否小于五天（未达到前向填充标准）
            if not fields_utils.validate_five_day_date_range(start_date, end_date):
                msg_list.append('当start_date与end_date不相等时表示未来七日预测，日期相关字段应该保证五日以上的有效时间')
            # 2.检查未来七日预测时模型选取是否正确
            elif model_type.split('_')[0] != 'LONGTERM':
                msg_list.append('当start_date与end_date不相等时表示未来七日预测，model_type应为LONGTERM前缀的模型')
    return '；'.join(set(msg_list)) if msg_list else None
