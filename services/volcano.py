import getpass
import threading
import logging
import logging.handlers

from rpyc.utils.server import ThreadedServer

from services.kos import Kos
import torch


def run(host, user, passwd):
    print('燃烧吧!')
    t = ThreadedServer(Kos(host, user, passwd), port=18861)
    t.start()


def reset_option():
    global special
    special = input('欢迎回到您的世界!\n')


# 配置logger
logging_handler = logging.handlers.RotatingFileHandler(
    'logs/volcano.log',
    'a',
    1024 * 1024,
    10,
    'utf-8'
)
logging_format = logging.Formatter(
    '%(asctime)s [%(name)s - %(levelname)s] %(message)s'
)
logging_handler.setFormatter(logging_format)
logger = logging.getLogger()
logger.addHandler(logging_handler)
logger.setLevel(logging.DEBUG)

print('准备点燃火山...')
host = input('请指定火山位置(默认为本地): ') or 'localhost'
user = input('以谁的名义点燃? ')
passwd = getpass.getpass('出示您的密令: ')

lighted, message = torch.light_up(host, user, passwd)
if lighted:
    print('尊者! 火山已为您点燃!')
    conn = torch.connect(
        host, user, passwd, 'information_schema'
    )
    if torch.seek_hera(conn):
        special = None
        thread_reset_option = threading.Thread(
            target=reset_option
        )
        thread_reset_option.daemon = True
        thread_reset_option.start()
        thread_reset_option.join(6)  # 等待用户输入(10秒)
        if special == 'Hera':
            while True:
                passwd1 = getpass.getpass('请重置主宰的密令: ')
                passwd2 = getpass.getpass('请再次确认您的密令: ')
                if passwd1 == passwd2:
                    try:
                        dominated_name = torch.reset_hera(
                            host, user, passwd, passwd1
                        )
                        print('主宰{}的密令已重置!'.format(dominated_name))
                    except Exception as e:
                        print('重置过程发生了一些问题...请查阅日志')
                        logging.error(
                            "{} occured".format(type(e).__name__),
                            exc_info=True
                        )
                    finally:
                        break
                else:
                    print('分配的密令似乎有些问题...请重新输入')
        run(host, user, passwd)
    else:
        name = input('请为新世界的主宰命名: ')
        while True:
            passwd1 = getpass.getpass('请分配密令给新世界的主宰: ')
            passwd2 = getpass.getpass('请再次确认您分配的密令: ')
            if passwd1 == passwd2:
                try:
                    torch.set_fire(
                        host, user, passwd, name, passwd1
                    )
                    print('如您所愿! 新世界的主宰已经诞生!')
                    run(host, user, passwd)
                except Exception as e:
                    print('创建过程发生了一些问题...请查阅日志')
                    logging.error(
                        "{} occured".format(type(e).__name__),
                        exc_info=True
                    )
                finally:
                    break
            else:
                print('分配的密令似乎有些问题...请重新输入')
else:
    print('此身份未被认可! 凡人勿进!\n{}'.format(message))
