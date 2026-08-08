# XCA - X 证书和密钥管理 

## __修改说明__

* 最新版本为官方 XCA - *2.9.0*版本
* 新增了一些功能：
  * 修复翻译了一些中文语言包未翻译的字符
  * 在创建证书界面添加了自定义序列号的选项
  * 添加了SM2密钥创建、SM3哈希算法、SM4的对称加密。

## __官方更新日志：__

详细的官方更新日志可以在这里找到：

<https://hohnstaedt.de/xca/index.php/software/changelog>

## __XCA官方文档__

本应用程序的文档可在 *帮助* 菜单中查看，也可在这里查看：

<https://www.hohnstaedt.de/xca/index.php/documentation/manual>

## __从源码构建__

### 依赖项

构建 XCA 需要：
 - 一个工具链
 - cmake：https://cmake.org
 - Qt5 或 Qt6：https://www.qt.io（5.10.1 或更高版本）
 - OpenSSL：https://www.openssl.org（1.1.1 或更高版本）
   或 libressl-3.6.x
 - Sphinx-Build：https://www.sphinx-doc.org

### Linux / Unix

 - 安装依赖项
 
 - bash
 
 - Install the dependencies
   ```
   # Bookworm
   sudo apt install build-essential libssl-dev pkg-config cmake qttools5-dev python3-sphinxcontrib.qthelp
   # Bullseye
   sudo apt install build-essential libssl-dev pkg-config cmake qttools5-dev python3-sphinx
   # Either Qt5
   sudo apt install qtbase5-dev qttools5-dev-tools libqt5sql5 libqt5help5 qttools5-dev
   # Or Qt6
   sudo apt install qt6-base-dev qt6-tools-dev
   ```
 - 克隆: `git clone https://github.com/chris2511/xca.git`
 - 配置: `cmake -B build xca`
 - 编译: `cmake --build build -j5`
 - 安装: `sudo cmake --install build`
 - 或先安装到本地，之后以 root 身份复制: `DESTDIR=DEST cmake --install build --prefix /usr`

### Apple macOS

- 安装依赖项
  ```
  xcode-select --install
  brew install openssl@3 qt6 python3 cmake
  pip3 install sphinx
  ```
- 克隆：`git clone https://github.com/chris2511/xca.git`
- 配置：`cmake -B build xca`
- 编译：`cmake --build build -j5`
- 构建 DMG：`cd build && cpack`
- 构建 PKG：`cd build && cpack -G productbuild`

使用以下命令初始化目录后，XCA 即可在 Xcode 中使用：
`cmake -G Xcode -B .`
  
### Windows

- 安装依赖项
  - 从 Microsoft Store 或 https://www.python.org/downloads/windows/ 安装 Windows 版 Python 3.11
  - 从此处安装 OpenSSL：https://slproweb.com/download/Win64OpenSSL-3_1_5.msi，并从 https://github.com/slproweb/opensslhashes/blob/master/win32_openssl_hashes.json 校验 SHA256 哈希值
  - 使用 [aqtinstall](https://github.com/miurahr/aqtinstall) 安装 Qt 库、cmake 和 MinGW 编译器。Sphinx 用于生成文档
  
  
    ```
    pip3 install sphinx aqtinstall
    ```
 - 将 pip 显示的 PATH 添加到你的 PATH 中
  - 安装 Qt、cmake 和 MinGW 工具链
    ```
    aqt install-qt windows desktop 6.6.3 win64_mingw
    aqt install-tool windows desktop tools_mingw90 qt.tools.win64_mingw900
    aqt install-tool windows desktop tools_vcredist qt.tools.vcredist_64
    ```
  - 如果缺少 7z，从 Microsoft Store 安装 `7-Zip File Manager (unofficial)` 或从 7-zip.org 安装
  - 安装 "vcredist\\vcredist_64.exe"
  - 将 cmake、MinGW、OpenSSL 和 Qt6 添加到你的 PATH 中
    
    ```
    %USERPROFILE%\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts;
    %USERPROFILE%\AppData\Local\Microsoft\WindowsApps;
    %USERPROFILE%\Tools\CMake_64\bin;
    %USERPROFILE%\Tools\mingw_64\bin;
    %USERPROFILE%\6.6.3\mingw_64\bin;
    ```
 - 创建 `CMAKE_PREFIX_PATH` 环境变量：
    ```
    %USERPROFILE%\6.6.3\mingw_64\lib\cmake
    ```
  - 如需创建 MSI 安装程序，请安装 `https://wixtoolset.org/releases/`

- 克隆：`git clone https://github.com/chris2511/xca.git`
- 配置：`cmake -B build -G "MinGW Makefiles" xca`
- 编译：`cmake --build build -j5`
- 创建便携版应用：`cmake --build build -t install`
- 构建 MSI 安装程序（以及便携版应用）：`cd build ; cpack`

## __SQL 远程数据库驱动__

由于许可证问题，Qt 不再附带 MySQL 插件。

### Linux

- Debian：`libqt6sql6-psql` `libqt6sql6-mysql` 或 `libqt6sql6-odbc`。
- RPM：`libqt6-database-plugin-pgsql` `libqt6-database-plugin-mysql` `libqt6-database-plugin-odbc`

它们会自动拉取所有必要的依赖项。

### Apple macOS

- **PostgreSQL**：安装 https://postgresapp.com/
- **ODBC**：需要 `/usr/local/opt/libiodbc/lib/libiodbc.2.dylib`。通过 `brew` 安装 unixodbc 时，必须从 `/opt/homebrew/Cellar/libiodbc/3.52.16/lib/libiodbc.2.dylib` 创建该库的符号链接
- **MariaDB**：自 XCA 2.8.0 起内置驱动

### Windows

- **PostgreSQL**：https://www.enterprisedb.com/downloads/postgres-postgresql-downloads（命令行工具）。将 Postgres 安装目录下的 `bin` 目录添加到你的 PATH 中（C:\\Program Files\\PostgreSQL\\16）
- **ODBC**：使用 `ODBC Datasources 64bit app` 配置 SQL Server
- **MariaDB (MySQL)**：从此处安装插件：https://github.com/thecodemonkey86/qt_mysql_driver。选择 MinGW 版本，并按照文档说明进行安装。

