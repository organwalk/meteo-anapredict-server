"""
    Flask应用接口服务，同时将服务注册到nacos中
    by organwalk 2023-08-15
"""
from flask import Flask, request
from flask_cors import CORS
from server_code.config import result
from config.application import register_to_nacos
from server_code.repository import repository
import entity.req_entity as server_req
from utils import req_utils
from service import analyze_service


app = Flask(__name__)
CORS(app)


@app.route('/anapredict/model/info', methods=['GET'])
def __api_model_info():
    """
    从数据库中获取并返回模型信息

    :return:
        json: 根据获取状态返回相应的消息以及数据

    by organwalk 2023-08-15
    """
    info_data = repository.get_model_info()
    return result.success('成功获取模型信息', info_data) if info_data else result.not_found('未能获取模型信息')


@app.route('/anapredict/analyze/correlation', methods=['POST'])
def __api_data_correlation():
    """
    对给定的要求进行气象数据分析

    :return:
        json: 根据获取状态返回相应的消息以及数据

    by organwalk 2023-08-15
    """
    validate = req_utils.validate_json_user_req('/anapredict/analyze/correlation',
                                                request.get_json(),
                                                server_req.CORRELATION)
    if validate is None:
        correlation_list = analyze_service.get_correlation_list(**request.get_json())
        return result.success('已成功计算出协相关矩阵结果', correlation_list) if correlation_list is not None \
            else result.error('计算过程中发生了错误，请稍后再试')
    else:
        return result.fail_entity(validate)


@app.route('/anapredict/model/prediction', methods=['POST'])
def __api_model_prediction():
    validate = req_utils.validate_json_user_req('/anapredict/model/prediction',
                                                request.get_json(),
                                                server_req.PREDICTION)
    if validate is None:
        return result.success('成功', request.get_json())
    else:
        return result.fail_entity(validate)


@app.errorhandler(404)
def __server_api_notfound(e):
    return result.not_found(f'{e.name},该接口不存在，请修改后重试')


@app.errorhandler(405)
def handle_method_not_allowed(e):
    return result.fail_method(f"该接口仅支持 {', '.join([method for method in e.valid_methods if (method != 'OPTIONS')])} 方法")


@app.errorhandler(500)
def __server_error(e):
    return result.error(f'{e.name},内部服务处理错误')


if __name__ == '__main__':
    register_to_nacos()
    app.run(host='0.0.0.0', port=9594)
