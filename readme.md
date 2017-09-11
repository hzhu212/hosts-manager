# hosts-manager(hman)

## 中文文档

### 使用方法

> 支持 Windows、Linux 和 MacOSX 平台。但并未在 Linux 和 MacOSX 平台进行测试。

#### 依赖环境：

1. python 环境（python2.x 或 python3.x 均可）
2. Windows 下需要安装 python 第三方库 `pypiwin32`，安装命令为 `pip install pypiwin32`

#### 使用方法

1. 下载此项目到本地。`git clone` 或 直接下载 zip 压缩包均可；
2. 为了使用方便，将项目目录 `hosts-manager` 添加到 `PATH` 环境变量；
3. 打开控制台或终端，输入 `hman run` 即可更新 hosts 文件；
4. 输入 `hman help` 或 `hman` 查看其他功能。

### 示例

![mark](http://os09d5k4j.bkt.clouddn.com/image/170905/ajG0bEBLG1.png?imageslim)

执行 `hamn run` 命令后下载并更新 hosts：

![mark](http://os09d5k4j.bkt.clouddn.com/image/170904/H52l5FJb7b.png?imageslim)

访问 Google：

![mark](http://os09d5k4j.bkt.clouddn.com/image/170905/4G5m5cG0CD.png?imageslim)

访问 Youtube：

![mark](http://os09d5k4j.bkt.clouddn.com/image/170905/l90b5kkcFD.png?imageslim)

管理 hosts 源（切换、添加、删除以及重命名）

![mark](http://os09d5k4j.bkt.clouddn.com/image/170905/idLbAc1Kce.png?imageslim)

开启科学上网之旅吧~

### TODO

1. 命令行自动补全；
2. 更友好的方式请求管理员权限；
3. 使用装饰器重构 HostsManager 类中的参数判断
4. 解决 Python2 中存在的编解码问题

## English document

### Usage

> Supporting Windows, Linux and MacOSX platform, but not tested on Linux and MacOSX.

#### Required environment

1. Python(both 2.x and 3.x are fine)
2. On Windows platform, need third party library `pypiwin32`, use command `pip install pypiwin32` for installing.

#### How to use

1. Download this project to your PC. Use `git clone` or `download zip`.
2. In order to open hman everywhere, Add the project folder `hosts-manager` to environment variable `PATH`.
3. Open cmd and input `hman run`, your hosts file will get updated.
4. Input `hman help` or just `hman` to view other features.

### Example

![mark](http://os09d5k4j.bkt.clouddn.com/image/170905/ajG0bEBLG1.png?imageslim)

Download and update hosts after entering `hman run`:

![mark](http://os09d5k4j.bkt.clouddn.com/image/170904/H52l5FJb7b.png?imageslim)

google.com: 

![mark](http://os09d5k4j.bkt.clouddn.com/image/170905/4G5m5cG0CD.png?imageslim)

youtube.com:

![mark](http://os09d5k4j.bkt.clouddn.com/image/170905/l90b5kkcFD.png?imageslim)

Manage your hosts sources(switch, add, delete and rename)

![mark](http://os09d5k4j.bkt.clouddn.com/image/170905/idLbAc1Kce.png?imageslim)

hman makes it easy to cross the wall!
