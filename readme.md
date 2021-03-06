# hosts-manager(hman)

## 中文文档

### 使用方法

> 支持 Windows、Linux 和 MacOSX 平台。但并未在 Linux 和 MacOSX 平台进行测试。

#### 依赖环境：

1. python 环境（python2.7.x 或 python3.5.x 均可）
2. 第三方库 `pypiwin32`（仅 Windows 环境），安装：`pip install pypiwin32`
3. 第三方库 `readline`(Linux) 或 `pyreadline`(Windows) ，用于自动补全，非必需

> 注：
> 1. 依赖库已导出到 `requirements.txt` 文件，安装：`pip install -r requirements.txt`。
> 2. 推荐使用 `virtualenv` 管理依赖环境

#### 使用方法

1. 下载此项目到本地。`git clone` 或 直接下载 zip 压缩包均可；
2. 为了使用方便，将项目目录 `hosts-manager` 添加到 `PATH` 环境变量；
3. 以 **管理员权限** 打开控制台，输入 `hman.py` 即可打开工具；
4. 工具中已经内置了十多个活跃的 hosts 源，可方便地进行添加、删除等管理操作；
5. 主要命令：
    - `ls` 或 `list`：列出所有 hosts 源
    - `add`：添加 hosts 源
    - `rename`：重命名一个源
    - `reorder`：调整一个源在列表中的位置
    - `pull`：拉取 hosts 源并暂存到本地
    - `use`：切换到某个 hosts 源
    - `use`+`-p`：拉取并切换到
    - `h`：获取总体帮助
    - `help`：获取关于某条命令的帮助
6. 命令行支持 `<Tab>` 键自动补全

### 示例

打开 hosts-manager：

```bash
C:\Users\Haley
λ hman.py
Welcome to hosts-manager CLI. Type "h" to get general help. Type "help <command>" to get command help.

(hman)> h

Usage:
  hman <command> [<parameters>]

Commands:
  h:            Show this help message.
  add:          Add a new source.
  help:         Show help message for a specified command.
  list:         List all the sources available. Source in use starts with "*".
  ls:           Alias of `list`.
  pull:         Pull and store hosts from remote.
  rename:       Rename a source.
  ren:          Alias of `rename`.
  remove:       Remove existing source(s).
  rm:           Alias of `remove`.
  reorder:      Reorder a source.
  use:          Use specified source as system hosts.
```

获取某条命令的帮助：

```bash
(hman)> help ls
List all the hosts sources. Symbol "*" indicates the one in use.
        Usage: `list` or `ls`.
        Use extra parameter `-a` or `--all` to list detail information.
```

列出所有 hosts 源（"*" 表示当前正在使用的源）：

```bash
(hman)> ls
* gg:   https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts
  sy618-pc:     https://raw.githubusercontent.com/sy618/hosts/master/pc
  sy618-fq:     https://raw.githubusercontent.com/sy618/hosts/master/FQ
  wcm:  https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc
  wcm-ipv6:     https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-ipv6-pc
  lengers:      http://git.oschina.net/lengers/connector/raw/master/hosts
  ll-ipv6:      https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
  sly:  https://raw.githubusercontent.com/superliaoyong/hosts/master/hosts
  vokins-ad:    https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  racaljk:      https://raw.githubusercontent.com/racaljk/hosts/master/hosts
```

拉取并切换到某个 hosts 源：

```bash
(hman)> use w <Tab>
wcm      wcm-ipv6
(hman)> use wcm -p
[2017-09-12 10:58:12]:INFO: Downloading hosts from source [wcm]: https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc ...
[2017-09-12 10:58:17]:INFO: Success pulling hosts from source [wcm]
[2017-09-12 10:58:17]:INFO: Success backing up hosts

Windows IP 配置

已成功刷新 DNS 解析缓存。
[2017-09-12 10:58:17]:INFO: Success switching hosts to source [wcm]
(hman)> ls
  gg:   https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts
  sy618-pc:     https://raw.githubusercontent.com/sy618/hosts/master/pc
  sy618-fq:     https://raw.githubusercontent.com/sy618/hosts/master/FQ
* wcm:  https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc
  wcm-ipv6:     https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-ipv6-pc
  lengers:      http://git.oschina.net/lengers/connector/raw/master/hosts
  ll-ipv6:      https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
  sly:  https://raw.githubusercontent.com/superliaoyong/hosts/master/hosts
  vokins-ad:    https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  racaljk:      https://raw.githubusercontent.com/racaljk/hosts/master/hosts
```

添加新的 hosts 源（需要名称、url、描述(可选)），并调整排序到适当的位置：

> 添加已存在的源名称将被视为编辑操作

```bash
(hman)> add gg-m https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts googlehosts的镜像
Added new source: gg-m - https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts

(hman)> ls
  gg:   https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts
  sy618-pc:     https://raw.githubusercontent.com/sy618/hosts/master/pc
  sy618-fq:     https://raw.githubusercontent.com/sy618/hosts/master/FQ
* wcm:  https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc
  wcm-ipv6:     https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-ipv6-pc
  lengers:      http://git.oschina.net/lengers/connector/raw/master/hosts
  ll-ipv6:      https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
  sly:  https://raw.githubusercontent.com/superliaoyong/hosts/master/hosts
  vokins-ad:    https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  racaljk:      https://raw.githubusercontent.com/racaljk/hosts/master/hosts
  gg-m: https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts

(hman)> reorder gg-m 2
(hman)> ls
  gg:   https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts
  gg-m: https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts
  sy618-pc:     https://raw.githubusercontent.com/sy618/hosts/master/pc
  sy618-fq:     https://raw.githubusercontent.com/sy618/hosts/master/FQ
* wcm:  https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc
  wcm-ipv6:     https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-ipv6-pc
  lengers:      http://git.oschina.net/lengers/connector/raw/master/hosts
  ll-ipv6:      https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
  sly:  https://raw.githubusercontent.com/superliaoyong/hosts/master/hosts
  vokins-ad:    https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  racaljk:      https://raw.githubusercontent.com/racaljk/hosts/master/hosts
```

拉取 hosts 源（不切换）：

```bash
(hman)> pull gg-m
[2017-09-12 11:06:08]:INFO: Downloading hosts from source [gg-m]: https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts ...
[2017-09-12 11:06:10]:INFO: Success pulling hosts from source [gg-m]
```

切换 hosts 源（不拉取）

```bash
(hman)> use gg-m
[2017-09-12 11:06:13]:INFO: Success backing up hosts

Windows IP 配置

已成功刷新 DNS 解析缓存。
[2017-09-12 11:06:14]:INFO: Success switching hosts to source [gg-m]
(hman)> exit

C:\Users\Haley
λ
```

### TODO

- [X] 命令行自动补全
- [X] 更友好的方式获取管理员权限
- [ ] 图形界面

---

## English document

### Usage

> Supporting Windows, Linux and MacOSX platform, but not tested on Linux and MacOSX.

#### Required environment

1. Python(both 2.x and 3.x are fine)
2. `pypiwin32`(only for Windows), use command `pip install pypiwin32` to install.
3. `readline`(for Linux/MaxOSX) or `pyreadline` for Windows. Not nessesary, only for command line autocomplete.

> note:
> 1. All the required packages are stored in `requirements.txt`. Type `pip install -r requirements.txt` to install them one-time.
> 2. We recommand using `virtualenv` to manage the environment.

#### How to use

1. Download this project to your PC. Use `git clone` or just download zip.
2. In order to open hman anywhere, add the project folder `hosts-manager` to the environment variable `PATH`.
3. Run cmd as admin(use "sudo" prefix on Linux or MacOSX), then type `hman.py` to open hosts-manager.
4. There are more than 10 built-in active hosts sources, you can add, delete and modify them conveniently. 
5. All the commands and their meaning are listed bellow:
    - `ls` or `list`: list all the hosts sources
    - `add`: add a hosts source
    - `rename`: rename some hosts source
    - `reorder`: change the position of some hosts source
    - `pull`: pull/download hosts from remote and store it into directory `data/`
    - `use`: switch to specified hosts(ie: replace system hosts with downloaded one)
    - `use`+`-p`: equivalent to `pull` and `use`
    - `h`: get general help message
    - `help`: get help for specified command

### Example

Open hosts-manager:

```bash
C:\Users\Haley
λ hman.py
Welcome to hosts-manager CLI. Type "h" to get general help. Type "help <command>" to get command help.

(hman)> h

Usage:
  hman <command> [<parameters>]

Commands:
  h:            Show this help message.
  add:          Add a new source.
  help:         Show help message for a specified command.
  list:         List all the sources available. Source in use starts with "*".
  ls:           Alias of `list`.
  pull:         Pull and store hosts from remote.
  rename:       Rename a source.
  ren:          Alias of `rename`.
  remove:       Remove existing source(s).
  rm:           Alias of `remove`.
  reorder:      Reorder a source.
  use:          Use specified source as system hosts.
```

Get help for specified command:

```bash
(hman)> help ls
List all the hosts sources. Symbol "*" indicates the one in use.
        Usage: `list` or `ls`.
        Use extra parameter `-a` or `--all` to list detail information.
```

List all the hosts sources("*" indicates the one in use):

```bash
(hman)> ls
* gg:   https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts
  sy618-pc:     https://raw.githubusercontent.com/sy618/hosts/master/pc
  sy618-fq:     https://raw.githubusercontent.com/sy618/hosts/master/FQ
  wcm:  https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc
  wcm-ipv6:     https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-ipv6-pc
  lengers:      http://git.oschina.net/lengers/connector/raw/master/hosts
  ll-ipv6:      https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
  sly:  https://raw.githubusercontent.com/superliaoyong/hosts/master/hosts
  vokins-ad:    https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  racaljk:      https://raw.githubusercontent.com/racaljk/hosts/master/hosts
```

Pull and switch to some hosts source:

```bash
(hman)> use w <Tab>
wcm      wcm-ipv6
(hman)> use wcm -p
[2017-09-12 10:58:12]:INFO: Downloading hosts from source [wcm]: https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc ...
[2017-09-12 10:58:17]:INFO: Success pulling hosts from source [wcm]
[2017-09-12 10:58:17]:INFO: Success backing up hosts

Windows IP 配置

已成功刷新 DNS 解析缓存。
[2017-09-12 10:58:17]:INFO: Success switching hosts to source [wcm]
(hman)> ls
  gg:   https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts
  sy618-pc:     https://raw.githubusercontent.com/sy618/hosts/master/pc
  sy618-fq:     https://raw.githubusercontent.com/sy618/hosts/master/FQ
* wcm:  https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc
  wcm-ipv6:     https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-ipv6-pc
  lengers:      http://git.oschina.net/lengers/connector/raw/master/hosts
  ll-ipv6:      https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
  sly:  https://raw.githubusercontent.com/superliaoyong/hosts/master/hosts
  vokins-ad:    https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  racaljk:      https://raw.githubusercontent.com/racaljk/hosts/master/hosts
```

Add a new hosts source(need source name, url, and remark), and then change its position properly.

> Adding an existing source will be treated as modifing. 

```bash
(hman)> add gg-m https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts "mirror of googlehosts"
Added new source: gg-m - https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts

(hman)> ls
  gg:   https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts
  sy618-pc:     https://raw.githubusercontent.com/sy618/hosts/master/pc
  sy618-fq:     https://raw.githubusercontent.com/sy618/hosts/master/FQ
* wcm:  https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc
  wcm-ipv6:     https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-ipv6-pc
  lengers:      http://git.oschina.net/lengers/connector/raw/master/hosts
  ll-ipv6:      https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
  sly:  https://raw.githubusercontent.com/superliaoyong/hosts/master/hosts
  vokins-ad:    https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  racaljk:      https://raw.githubusercontent.com/racaljk/hosts/master/hosts
  gg-m: https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts

(hman)> reorder gg-m 2
(hman)> ls
  gg:   https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts
  gg-m: https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts
  sy618-pc:     https://raw.githubusercontent.com/sy618/hosts/master/pc
  sy618-fq:     https://raw.githubusercontent.com/sy618/hosts/master/FQ
* wcm:  https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-pc
  wcm-ipv6:     https://raw.githubusercontent.com/wangchunming/2017hosts/master/hosts-ipv6-pc
  lengers:      http://git.oschina.net/lengers/connector/raw/master/hosts
  ll-ipv6:      https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
  sly:  https://raw.githubusercontent.com/superliaoyong/hosts/master/hosts
  vokins-ad:    https://raw.githubusercontent.com/vokins/yhosts/master/hosts
  racaljk:      https://raw.githubusercontent.com/racaljk/hosts/master/hosts
```

Pull some hosts source(do not switch):

```bash
(hman)> pull gg-m
[2017-09-12 11:06:08]:INFO: Downloading hosts from source [gg-m]: https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts-files/hosts ...
[2017-09-12 11:06:10]:INFO: Success pulling hosts from source [gg-m]
```

Switch to some hosts source(do not pull)

```bash
(hman)> use gg-m
[2017-09-12 11:06:13]:INFO: Success backing up hosts

Windows IP 配置

已成功刷新 DNS 解析缓存。
[2017-09-12 11:06:14]:INFO: Success switching hosts to source [gg-m]
(hman)> exit

C:\Users\Haley
λ
```

### TODO

- [X] command line autocomplete
- [X] get administrator privileges more friendly
- [ ] GUI
