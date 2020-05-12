import mongoengine


def mongodb_data_cloud(config: dict):
    """
    mongodb数据库(hq_data_cloud)
    :return:
    """
    if "db" not in config.keys() or "host" not in config.keys():
        raise Exception("未找到mongodb的相关配置：db、host")
    mongoengine.connect(config.get("db"), host=config.get("host"))


def mysql(config: dict):
    pass