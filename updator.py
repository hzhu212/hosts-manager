# -*- coding: utf-8 -*-

import os
import time
import platform
import hashlib
import shutil

# import urllib
try:
    # For Python 3
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2
    from urllib2 import urlopen

import config

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

# 获取 hosts 文件所在目录的路径
def get_hosts_dir(system):
    if system == 'Windows':
        return os.path.join(os.environ['SystemRoot'], 'System32', 'drivers', 'etc')
    if system in ('Linux', 'Darwin'):
        return '/etc/'
    raise Exception('System type error: unknown system "%s"' %system)

# 文件路径，记录了上一次下载的 hosts 的 md5 校验码
def get_md5_file():
    return os.path.join(os.path.dirname(__file__), 'last-md5.txt')

# 判断 hosts 是否存在
def hosts_exists(hosts_dir):
    hosts_file = os.path.join(hosts_dir, 'hosts')
    return os.path.isfile(hosts_file)

# 初始化 hosts（若用户的 hosts 目录下不存在 hosts 文件，则初始化一个新的）
def init_hosts(hosts_dir):
    print('Hosts not exists, creating a new one...')
    hosts_file = os.path.join(hosts_dir, 'hosts')
    with open(hosts_file, 'w') as f:
        f.write(INITIAL_HOSTS)
    print('Hosts initialize success!')

# 从 url 处下载 hosts 文件
def download_hosts(url):
    print('Downloading hosts...')
    data = urlopen(url).read()
    print('Hosts download success!')
    return data

# 获取上次更新时记录的 md5 码
def get_last_md5(md5_file):
    last_md5 = ''
    if os.path.isfile(md5_file):
        with open(md5_file, 'r') as f:
            last_md5 = f.read().strip()
    return last_md5

# hosts 更新成功后，更新 md5 校验码
def update_md5(md5_file, md5):
    with open(md5_file, 'w') as f:
        f.write(md5)

# 备份 hosts 文件
def backup_hosts(hosts_dir):
    src = os.path.join(hosts_dir, 'hosts')
    dst = os.path.join(hosts_dir, 'hosts.'+time.strftime('%Y%m%d.%H%M%S', time.localtime())+'.bak')
    shutil.copy(src, dst)
    print('Hosts backup success!')

# 截断 hosts 文件，保留头部用户自己定义的 hosts，剩余部分丢弃
# 用户定义的 hosts 以 SEPARATOR 行与程序注入的 hosts 分割
def truncate_hosts(hosts_dir):
    hosts_file = os.path.join(hosts_dir, 'hosts')
    user_hosts = []
    with open(hosts_file, 'r') as f:
        line = f.readline()
        while line and not line.startswith(SEPARATOR):
            user_hosts.append(line)
            line = f.readline()

    with open(hosts_file, 'w') as f:
        f.writelines(user_hosts)
        f.writelines([SEPARATOR, '\n\n'])
    print('Hosts truncate success!')

# 更新 hosts
def update_hosts(hosts_dir, data):
    hosts_file = os.path.join(hosts_dir, 'hosts')
    with open(hosts_file, 'a') as f:
        try:
            f.write(data)
        except TypeError:
            # python 3
            f.write(data.decode('utf8', errors='ignore'))
    print('Hosts update success!')

# hosts 更新之后，还需要刷新 DNS 或重启网络适配器等后续工作
def after_update(system):
    if system == 'Windows':
        os.system('ipconfig /flushdns')
        return
    if system == 'Linux':
        os.system('sudo /etc/init.d/networking restart')
        return
    if system == 'Darwin':
        os.system('sudo ifconfig en0 down && sudo ifconfig en0 up')
        return
    raise Exception('System type error: unknown system "%s"' %system)

# 主程序
def main(url):
    system = platform.system()
    hosts_dir = get_hosts_dir(system)
    md5_file = get_md5_file()
    if not hosts_exists(hosts_dir):
        init_hosts(hosts_dir)
    data = download_hosts(url)
    md5 = hashlib.md5(data).hexdigest()
    last_md5 = get_last_md5(md5_file)
    if md5 == last_md5:
        print('Hosts already up-to-date!\nQuit')
        return
    backup_hosts(hosts_dir)
    truncate_hosts(hosts_dir)
    update_hosts(hosts_dir, data)
    after_update(system)
    update_md5(md5_file, md5)
    print('\n*** All success! Try to google something~ ***\n')


if __name__ == '__main__':
    url = config.sources[config.current]
    try:
        main(url)
    except Exception as e:
        print('An error occured:')
        print(e)
    finally:
        os.system('pause')
