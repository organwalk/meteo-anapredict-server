"""
    封装响应中的实体
    by organwalk 2023-08-15
"""
from collections import OrderedDict


def set_model_info(version: str, cn_des: str, technology: str, support: str, update: str) -> OrderedDict:
    """
    封装/anapredict/correlation接口的响应数据
    :param version: 版本信息
    :param cn_des: 中文描述
    :param technology: 模型使用的技术栈
    :param support: 支持的模型类别
    :param update: 最后一次更新日期
    :return:
        OrderedDict: model_info的有序字典

    by organwalk 2023-08-15
    """
    return OrderedDict([
        ('version', version),
        ('cn_des', cn_des),
        ('technology', technology),
        ('support', support),
        ('update', update)
    ])


def set_model_report(date: str, rmse: str, mae: str, r2: str, train_loss: str, val_loss: str) -> OrderedDict:
    """
    封装/anapredict/model/report接口的响应数据
    :param date: 报告最后更新日期
    :param rmse: 均方根误差
    :param mae: 平均绝对误差
    :param r2: 决定系数
    :param train_loss: 训练集损失函数
    :param val_loss: 验证集损失函数
    :return:
        OrderedDict: model_report的有序字典

    by organwalk 2023-10-14
    """
    return OrderedDict([
        ('date', date),
        ('rmse', rmse),
        ('mae', mae),
        ('r2', r2),
        ('train_loss', train_loss),
        ('val_loss', val_loss)
    ])

