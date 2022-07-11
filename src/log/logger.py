import os
import time
from loguru import logger

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(f"log base directory 日志文件目录:\t{basedir}")  
# 定位到log日志文件
log_path = os.path.join(basedir, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)
if not os.path.exists(log_path):
    os.mkdir(log_path)

all_log = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_log.log')
error_log = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')


logger.add("log/default.log", rotation="500 MB",retention='3 months',encoding='utf-8')
#logger.add("log/info.log", rotation="500 MB",retention='3 months',encoding='utf-8',level='info')
#logger.add("log/warning.log", rotation="500 MB",retention='3 months',encoding='utf-8',level='warning')
#logger.add("log/debug.log", rotation="500 MB",retention='3 months',encoding='utf-8',level="debug")

# logger.add(log_path_all, rotation="500 MB", retention="30 days", enqueue=True)
# logger.add(log_path_error, rotation="500 MB", retention="30 dats", enqueue=True,level='ERROR')


# format 参数： {time} {level} {message}、  {time:YYYY-MM-DD at HH:mm:ss} | {level} | {message} 记录参数
# level 日志等级
# rotation 参数：1 week 一周、00:00每天固定时间、 500 MB 固定文件大小
# retention 参数： 10 days 日志最长保存时间
# compression 参数： zip 日志文件压缩格式
# enqueue 参数 True 日志文件异步写入
# serialize 参数： True 序列化json
# encoding 参数： utf-8 字符编码、部分情况会出现中文乱码问题
# logger.info('If you are using Python {}, prefer {feature} of course!', 3.6, feature='f-strings') 格式化输入内容
#  可通过等级不同对日志文件进行分割储存