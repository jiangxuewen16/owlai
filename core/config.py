CONFIG: dict = {}


def get_config(name: str):
    """
    获取配置
    :return:
    """
    return CONFIG.get(name)

def set_config(name: str, value: str):
    pass
