import os
import platform


from configparser import ConfigParser
# 使用相对目录确定文件位置
_conf_dir = os.path.dirname(__file__)
_conf_file = os.path.join(_conf_dir, 'config.ini')

# 继承ConfigParser，写一个将结果转为dict的方法
class MyParser(ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d

# 读取所有配置，以字典方式输出结果
def _get_all_conf():
    _config = MyParser()
    result = {}
    if os.path.isfile(_conf_file):
        try:
            _config.read(_conf_file, encoding='UTF-8')
            result = _config.as_dict()
        except OSError:
            raise ValueError("Read config file failed: %s" % OSError)
    #为了方便使用platform ,这里向字段里面加入platfrom
    result['platform'] = {'system':platform.system()}
    return result

# 将各配置读取出来，放在变量中，后续其它文件直接引用这个这些变量
config = _get_all_conf()

sys_cfg = config['sys']
smtp_cfg = config['smtp']
platform = config['platform']
data_type = config['dataType']
# print(config)
# print(platform['system'])
# print(smtp_cfg)
# print(smtp_cfg['host'])

log_cfg = config['log']

email_cfg = config['email']


