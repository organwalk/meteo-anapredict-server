# 信创技术下的气象数据预测服务

该项目目前定义了两个基于tensorflow训练的LSTM的气象数据预测模型，包括了短期（24h）和长期（7 days），以及基于flask服务的清洗、分析和预测服务接口。详见各级代码注释，以下进行简要说明。

## 目录结构

**meteo_data_csv**：此处存放数据集文件

**meteo_model**：此处存放训练模型

**server_code**：此处定义了一个可运行的falsk服务，用于开放清洗、分析、预测接口。该服务已注册入nacos中，运行前需本地运行nacos。

**train_code**：此处定义训练模型使用的代码

**train_log**：此处定义训练日志

**config.py**：此处定义基本配置信息

**data_utils.py**：此处定义通用的数据处理工作方法

**repository.py**：此处定义通用数据源

## 环境依赖

本项目运行于python 3.6，推荐使用虚拟环境搭建此python版本。使用以下命令安装依赖项：

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 数据集

训练使用的气象数据为：24小时内每分钟采集的气象数据。具有八个特征：

| Temperature | Humidity | Speed | Direction | Rain | Sunlight | PM2.5 | PM10 |
| ----------- | -------- | ----- | --------- | ---- | -------- | ----- | ---- |

在Temperature列前还具有 hh:mm:ss 格式的Time列

**相关法律法规**：

根据《中华人民共和国气象法》《气象行业管理若干规定》《涉外气象探测和资料管理办法》等相关规定，一般情况下，其他组织和个人开展气象探测须向省级气象主管机构备案，探测所获得的数据信息须向省级气象主管机构汇交。

据此，本项目不提供数据集文件。
