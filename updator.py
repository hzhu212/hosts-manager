# -*- coding: utf-8 -*-

import os
import sys
import time
import platform
import hashlib
import shutil
import logging
import codecs

# import urllib
try:
    # For Python 3
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2
    from urllib2 import urlopen

SEPARATOR = '# -------------------- Modified -------------------- #'

INITIAL_HOSTS = '''# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#   127.0.0.1       localhost
#   ::1             localhost

'''

logger = logging.getLogger('HostsUpdator')
logger.setLevel(logging.INFO)
hd = logging.StreamHandler()
# formatter = logging.Formatter('[%(asctime)s] %(name)s: %(levelname)s: %(message)s')
formatter = logging.Formatter(fmt='[%(asctime)s]:%(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
hd.setFormatter(formatter)
logger.addHandler(hd)

class HostsUpdator(object):
    """Class to download and update hosts file.\n"""
    def __init__(self, source_name, source_url):
        self.name = source_name
        self.url = source_url
        self.system = platform.system()
        self.hosts_dir = self._get_hosts_dir()
        self.working_dir = self._get_working_dir()


    # 获取 hosts 文件所在目录
    def _get_hosts_dir(self):
        if self.system == 'Windows':
            return os.path.join(os.environ['SystemRoot'], 'System32', 'drivers', 'etc')
        if self.system in ('Linux', 'Darwin'):
            return '/etc/'
        raise Exception('System type error: unknown system: %s' %self.system)


    # 获取当前源的数据目录
    def _get_working_dir(self):
        app_root = os.path.dirname(os.path.abspath(sys.modules[self.__module__].__file__))
        working_dir = os.path.join(app_root, 'data', self.name)
        if not os.path.isdir(working_dir):
            os.makedirs(working_dir)
        return working_dir


    @staticmethod
    def safe_write(fobj, data):
        # python 3: "write" method requires str, not bytes
        try:
            fobj.write(data)
        except (TypeError, UnicodeDecodeError) as e:
            fobj.write(data.decode('utf8'))
        except UnicodeDecodeError as e:
            fobj.write(data.decode('gbk'))
        except UnicodeDecodeError as e:
            fobj.write(data.decode('utf8', errors='ignore'))


    # 判断 hosts 是否存在
    def hosts_exists(self):
        hosts_file = os.path.join(self.hosts_dir, 'hosts')
        return os.path.isfile(hosts_file)


    # 初始化 hosts（若用户的 hosts 目录下不存在 hosts 文件，则初始化一个新的）
    def init_hosts(self):
        logger.info('Hosts not exists, initializing ...')
        hosts_file = os.path.join(self.hosts_dir, 'hosts')
        with codecs.open(hosts_file, 'w', encoding='utf8') as f:
            f.write(INITIAL_HOSTS)
        logger.info('Success initializing hosts')


    # 从远端下载 hosts 文件
    def pull(self):
        # 获取上次更新时记录的 md5 码
        def get_last_md5(md5_file):
            last_md5 = ''
            if os.path.isfile(md5_file):
                with open(md5_file, 'r') as f:
                    last_md5 = f.read().strip()
            return last_md5

        def update_md5(md5_file, md5):
            with open(md5_file, 'w') as f:
                f.write(md5)

        logger.info('Downloading hosts from source [%s]: %s ...' %(self.name, self.url))
        data = urlopen(self.url).read()
        md5 = hashlib.md5(data).hexdigest()
        md5_file = os.path.join(self.working_dir, 'md5.txt')
        last_md5 = get_last_md5(md5_file)
        if md5 == last_md5:
            logger.info('Hosts is already up-to-date with source [%s]. Quit updating!' %self.name)
            return
        hosts_download = os.path.join(self.working_dir, 'hosts.txt')
        with codecs.open(hosts_download, 'w', encoding='utf8') as f:
            self.safe_write(f, data)
        update_md5(md5_file, md5)
        logger.info('Success pulling hosts from source [%s]' %self.name)


    # 备份 hosts 文件
    def backup_hosts(self):
        src = os.path.join(self.hosts_dir, 'hosts')
        dst = os.path.join(self.hosts_dir, 'hosts.'+time.strftime('%Y%m%d.%H%M%S', time.localtime())+'.bak')
        shutil.copy(src, dst)
        logger.info('Success backing up hosts')


    # 获取并保留 hosts 文件头部用户自己定义的行
    # 用户定义的 hosts 以 SEPARATOR 行与程序注入的 hosts 分割
    def get_user_hosts(self):
        hosts_file = os.path.join(self.hosts_dir, 'hosts')
        user_hosts = []
        with codecs.open(hosts_file, 'r', encoding='utf8') as f:
            line = f.readline()
            while line and not line.startswith(SEPARATOR):
                user_hosts.append(line)
                line = f.readline()
        return user_hosts


    # 切换 hosts 源之前做一些准备工作，如初始化 hosts(如果不存在)、备份 hosts 等
    def before_use(self):
        if not self.hosts_exists():
            self.init_hosts()
        self.backup_hosts()


    # 使用当前源更新系统 hosts
    def use(self):
        self.before_use()
        hosts_file = os.path.join(self.hosts_dir, 'hosts')
        hosts_download = os.path.join(self.working_dir, 'hosts.txt')
        user_hosts = self.get_user_hosts()
        with codecs.open(hosts_file, 'w', encoding='utf8') as f:
            f.writelines(user_hosts + [SEPARATOR, '\n'])
            with codecs.open(hosts_download, 'r', encoding='utf8') as d:
                self.safe_write(f, d.read())
        self.after_use()
        logger.info('Success switching hosts to source [%s]' %self.name)


    # hosts 更新之后，还需要刷新 DNS 或重启网络适配器等后续工作
    def after_use(self):
        if self.system == 'Windows':
            os.system('ipconfig /flushdns')
            return
        if self.system == 'Linux':
            os.system('sudo /etc/init.d/networking restart')
            return
        if self.system == 'Darwin':
            os.system('sudo ifconfig en0 down && sudo ifconfig en0 up')
            return
        raise Exception('System type error: unknown system "%s"' %self.system)
