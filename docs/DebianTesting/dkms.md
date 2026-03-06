THIS IS NOT A TUTORIAL FOR BEGINNER! THIS DOCUMENT ASSUME READER FAIMILIAR WITH LINUX DKMS. THIS DOCUMENT IS USED TO RECORD CONFIG FILE LOCATIONS, AND QUICKLY REVIEW THE SYSTEM ARCHITECTURE.
这不是为新手准备的教学文档！本文档默认了读者熟悉linux dkms体系， 主要用于记录配置文件位置， 以及快速的体系架构回顾

# DKMS Concepts & Configs

## DKMS Concepts
DKMS 是一个内核模块管理系统。 他将一些依赖于内核api的驱动编译， 启动时加载， 更新等操作进行自动化。这些驱动可以是：Nvidia显卡驱动， v4l2摄像机驱动， Realtek网卡驱动， 等等。 DKMS可以做到： 敲一行命令就自动从源码仓库拉取代码更新， 自动重编译。 也可以在内核头文件更新时自动触发相关模块重编译

- DKMS Architecture
```
          +----------------------+
          |  /usr/src/<module>   |  模块源码
          +----------+-----------+
                     |
                     v
          +----------------------+
          |   DKMS framework     | Binaries for building, installing
          |   /usr/sbin/dkms     |
          +----------+-----------+
                     |
                     v
        +--------------------------+
        | /var/lib/dkms/<module>   |
        | 编译缓存 / 构建状态         | build caches & artifacts
        +----------+---------------+
                   |
                   v
        +----------------------------+
        | /lib/modules/<kernel>/     |
        | modules installed here     | 
        +----------------------------+
```
- DKMS Procedure
源码 -> DKMS -> 编译 -> 安装到内核模块目录

## DKMS Directories
- DKMS Key Directories
    - Module Sources
        `/usr/src/<module>-<version>/`

        例如：
        ```
        /usr/src/rtl8812au-5.13.6
        /usr/src/nvidia-550.54
        /usr/src/zfs-2.2.2
        ```
        里面必须包含：
        ```
        dkms.conf
        Makefile
        source code
        ```

    - DKMS 工作目录
        `/var/lib/dkms/`

        例如：
        `/var/lib/dkms/rtl8812au/5.13.6/`

        里面包含：
        ```
        build/      # 编译目录
        source/     # 指向 /usr/src
        6.8.0/      # 对应 kernel build
        ```
        示例：
        ```
        /var/lib/dkms/rtl8812au/5.13.6/
        ├── source -> /usr/src/rtl8812au-5.13.6
        ├── 6.8.0-amd64/
        │    └── x86_64/
        │         └── module/
        └── 6.7.12-amd64/
        ```
        DKMS 为每个 kernel 单独编译一份模块。
    - 内核模块安装位置

        最终模块放在：

        `/lib/modules/<kernel>/updates/dkms/`

        例如：

        `/lib/modules/6.8.0-amd64/updates/dkms/`

        这里的模块会被 depmod 识别。
    - DKMS 配置文件

        每个模块必须有：

        dkms.conf

        位置：

        `/usr/src/<module>-<version>/dkms.conf`

        示例：
        ```
        PACKAGE_NAME="rtl8812au"
        PACKAGE_VERSION="5.13.6"

        BUILT_MODULE_NAME[0]="8812au"
        DEST_MODULE_LOCATION[0]="/kernel/drivers/net/wireless"

        MAKE[0]="make"
        CLEAN="make clean"

        AUTOINSTALL="yes"
        ```
        解释：

        字段	作用
        PACKAGE_NAME	模块名
        PACKAGE_VERSION	版本
        BUILT_MODULE_NAME	生成模块
        DEST_MODULE_LOCATION	安装路径
        MAKE	编译命令
        AUTOINSTALL	是否自动编译


## DKMS Commands
- check stataus
    `dkms status`

    查看所有模块的状态
- add

    注册模块：

    `dkms add <module>/<version>`

    实际就是：

    `/usr/src → /var/lib/dkms`
- build
    普通地为当前内核构建：
    `dkms build module/version`

    为某个 kernel 编译：

    `dkms build -m module -v version -k kernel`

    例如：

    `dkms build -m rtl8812au -v 5.13.6 -k 6.8.0-amd64`
- buildall

    为所有 kernel 构建模块：

    `dkms buildall -m module -v version`
- install

    安装模块：

    `dkms install -m module -v version`

    安装到：

    `/lib/modules/<kernel>/updates/dkms`

- delete

    删除模块：

    `dkms remove module/version --all`

    删除：

    `/var/lib/dkms/<module>/<version>`

    `/lib/modules/<kernel>/updates/dkms/<module>-<version>.ko`
    But this command won't remove module source code from your PC!


## DKMS position in system
dkms只是帮你自动化构建和管理内核模块，但并不是所有的内核模块都归他管。
内核模块分两种：

内核自带
`/lib/modules/.../kernel/`

编译时构建。

DKMS
`/lib/modules/.../updates/dkms`

第三方模块。

优先级：

`updates/dkms > kernel`