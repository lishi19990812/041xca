#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XCA-041专属修改版 - 正式版文件提取工具 (Portable)
按照官方发布版目录结构，从各源目录提取所需文件到桌面 XCA Release 文件夹
"""

import os
import shutil
import glob
import sys

# ==================== 路径配置 ====================
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(PROJECT_DIR, "build")
DESKTOP_DIR = os.path.join(os.path.expanduser("~"), "Desktop")
RELEASE_DIR = os.path.join(DESKTOP_DIR, "XCA Release")

# Qt 路径
QT_BIN_DIR = r"D:\041\Qt\6.7.3\msvc2019_64\bin"
QT_PLUGINS_DIR = r"D:\041\Qt\6.7.3\msvc2019_64\plugins"

# OpenSSL 路径
OPENSSL_BIN_DIR = r"D:\041\OpenSSL-Win64\bin"

# VS Redist 可能的位置
VS_REDIST_CANDIDATES = [
    r"D:\041\Microsoft Visual Studio\18\Community\VC\Redist\MSVC",
    r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Redist\MSVC",
    r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Redist\MSVC",
]
# ==================== 配置结束 ====================

# 需要提取的 Qt6 DLL 列表
QT6_DLLS = [
    "Qt6Core.dll",
    "Qt6Gui.dll",
    "Qt6Help.dll",
    "Qt6Network.dll",
    "Qt6Sql.dll",
    "Qt6Svg.dll",
    "Qt6Test.dll",
    "Qt6Widgets.dll",
]

# 需要提取的 Qt 插件子目录
QT_PLUGIN_DIRS = ["platforms", "sqldrivers", "styles"]

# OpenSSL DLL
OPENSSL_DLLS = ["libcrypto-3-x64.dll", "libssl-3-x64.dll"]

# XCA 数据文件
XCA_DATA_FILES = ["dn.txt", "eku.txt", "oids.txt"]

# 统计
stats = {"copied": 0, "skipped": 0, "failed": 0, "size": 0}


def log_ok(msg):
    print(f"  [OK] {msg}")
    stats["copied"] += 1


def log_skip(msg):
    print(f"  [跳过] {msg}")
    stats["skipped"] += 1


def log_fail(msg):
    print(f"  [警告] {msg}")
    stats["failed"] += 1


def copy_file(src, dst_dir, filename=None):
    """复制单个文件，返回是否成功"""
    if not os.path.isfile(src):
        return False
    fname = filename or os.path.basename(src)
    dst = os.path.join(dst_dir, fname)
    shutil.copy2(src, dst)
    stats["size"] += os.path.getsize(src)
    return True


def copy_dir(src, dst):
    """复制整个目录"""
    if not os.path.isdir(src):
        return False
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    for root, _, files in os.walk(dst):
        for f in files:
            fp = os.path.join(root, f)
            try:
                stats["size"] += os.path.getsize(fp)
            except OSError:
                pass
            stats["copied"] += 1
    return True


def find_file_in_dirs(filename, dirs):
    """在多个目录中搜索文件"""
    for d in dirs:
        path = os.path.join(d, filename)
        if os.path.isfile(path):
            return path
    return None


def find_vs_redist():
    """搜索 vc_redist.x64.exe"""
    for base in VS_REDIST_CANDIDATES:
        if not os.path.isdir(base):
            continue
        for root, _, files in os.walk(base):
            for f in files:
                if f.lower() == "vc_redist.x64.exe":
                    return os.path.join(root, f)
    return None


def main():
    print()
    print("=" * 60)
    print("  XCA-041专属修改版 - 正式版文件提取工具")
    print("=" * 60)
    print()

    # 检查 build 目录
    if not os.path.isdir(BUILD_DIR):
        print(f"[错误] build 目录不存在: {BUILD_DIR}")
        sys.exit(1)

    # 创建输出目录（清空旧的）
    print("[1/9] 准备输出目录...")
    if os.path.exists(RELEASE_DIR):
        shutil.rmtree(RELEASE_DIR)
        print(f"  已清空旧目录")
    os.makedirs(RELEASE_DIR)
    print(f"  输出到: {RELEASE_DIR}")
    print()

    # [2/9] XCA.exe
    print("[2/9] 提取 XCA 主程序...")
    exe_found = False
    # 优先精确查找 xca.exe（不区分大小写）
    for name in ["xca.exe", "XCA.exe"]:
        exe_path = os.path.join(BUILD_DIR, name)
        if os.path.isfile(exe_path):
            copy_file(exe_path, RELEASE_DIR)
            log_ok(name)
            exe_found = True
            break
    if not exe_found:
        # 回退：查找其他 exe（排除已知的工具和测试程序）
        exclude = {
            "windeployqt.exe", "cmake.exe", "vcpkg.exe", "test.exe",
            "testxca.exe", "fuzzcert.exe", "fuzzkey.exe",
        }
        exe_files = glob.glob(os.path.join(BUILD_DIR, "*.exe"))
        for exe in exe_files:
            basename = os.path.basename(exe).lower()
            if basename not in exclude and not basename.startswith("test"):
                copy_file(exe, RELEASE_DIR)
                log_ok(os.path.basename(exe))
                exe_found = True
                break
    if not exe_found:
        log_fail("未在 build 目录找到 xca.exe")
    print()

    # [3/9] Qt6 DLLs
    print("[3/9] 提取 Qt6 运行库...")
    for dll in QT6_DLLS:
        src = os.path.join(QT_BIN_DIR, dll)
        if copy_file(src, RELEASE_DIR):
            log_ok(dll)
        else:
            log_fail(f"未找到 {dll} (路径: {QT_BIN_DIR})")
    print()

    # [4/9] Qt 插件目录
    print("[4/9] 提取 Qt 插件目录...")
    for subdir in QT_PLUGIN_DIRS:
        src = os.path.join(QT_PLUGINS_DIR, subdir)
        dst = os.path.join(RELEASE_DIR, subdir)
        if copy_dir(src, dst):
            count = sum(len(files) for _, _, files in os.walk(dst))
            log_ok(f"{subdir}/ ({count} 个文件)")
        else:
            log_fail(f"未找到插件目录 {subdir}/ (路径: {QT_PLUGINS_DIR})")
    print()

    # [5/9] OpenSSL DLLs
    print("[5/9] 提取 OpenSSL 运行库...")
    for dll in OPENSSL_DLLS:
        src = os.path.join(OPENSSL_BIN_DIR, dll)
        if copy_file(src, RELEASE_DIR):
            log_ok(dll)
        else:
            log_fail(f"未找到 {dll} (路径: {OPENSSL_BIN_DIR})")

    # legacy.dll
    legacy_dirs = [
        OPENSSL_BIN_DIR,
        os.path.join(os.path.dirname(OPENSSL_BIN_DIR), "lib", "ossl-modules"),
    ]
    legacy_path = find_file_in_dirs("legacy.dll", legacy_dirs)
    if legacy_path:
        copy_file(legacy_path, RELEASE_DIR)
        log_ok("legacy.dll")
    else:
        log_skip("legacy.dll (未找到，不影响核心功能)")
    print()

    # [6/9] XCA 数据文件
    print("[6/9] 提取 XCA 数据文件...")
    data_search_dirs = [BUILD_DIR, os.path.join(PROJECT_DIR, "lib")]
    for data_file in XCA_DATA_FILES:
        found = find_file_in_dirs(data_file, data_search_dirs)
        if found:
            copy_file(found, RELEASE_DIR)
            log_ok(data_file)
        else:
            log_fail(f"未找到 {data_file}")
    print()

    # [7/9] html 帮助文档目录
    print("[7/9] 提取帮助文档 (html/)...")
    html_search_dirs = [
        os.path.join(BUILD_DIR, "html"),
        os.path.join(PROJECT_DIR, "doc", "html"),
        os.path.join(PROJECT_DIR, "html"),
    ]
    html_found = False
    for html_dir in html_search_dirs:
        if os.path.isdir(html_dir):
            dst = os.path.join(RELEASE_DIR, "html")
            copy_dir(html_dir, dst)
            count = sum(len(files) for _, _, files in os.walk(dst))
            log_ok(f"html/ ({count} 个文件)")
            html_found = True
            break
    if not html_found:
        log_fail("未找到 html/ 目录")
    print()

    # [8/9] settings 目录
    print("[8/9] 提取配置目录 (settings/)...")
    settings_search_dirs = [
        os.path.join(BUILD_DIR, "settings"),
        os.path.join(PROJECT_DIR, "settings"),
    ]
    settings_found = False
    for sdir in settings_search_dirs:
        if os.path.isdir(sdir):
            dst = os.path.join(RELEASE_DIR, "settings")
            copy_dir(sdir, dst)
            count = sum(len(files) for _, _, files in os.walk(dst))
            if count > 0:
                log_ok(f"settings/ ({count} 个文件)")
            else:
                log_ok("settings/ (空目录)")
            settings_found = True
            break
    if not settings_found:
        log_skip("settings/ (源中不存在，运行时自动创建)")
    print()

    # [9/9] VC++ Redistributable
    print("[9/9] 提取 VC++ 运行时安装包...")
    redist = find_vs_redist()
    if redist:
        copy_file(redist, RELEASE_DIR, "vc_redist.x64.exe")
        log_ok("vc_redist.x64.exe")
    else:
        log_skip("vc_redist.x64.exe (未找到，可从微软官网下载)")
    print()

    # 汇总
    size_mb = stats["size"] / (1024 * 1024)
    print("=" * 60)
    print("  提取完成！")
    print(f"  输出目录: {RELEASE_DIR}")
    print(f"  成功复制: {stats['copied']} 项")
    print(f"  跳过:     {stats['skipped']} 项")
    print(f"  失败:     {stats['failed']} 项")
    print(f"  总大小:   {size_mb:.1f} MB")
    print("=" * 60)

    # 列出最终目录结构
    print()
    print("最终目录结构:")
    for item in sorted(os.listdir(RELEASE_DIR)):
        full = os.path.join(RELEASE_DIR, item)
        if os.path.isdir(full):
            count = sum(len(files) for _, _, files in os.walk(full))
            print(f"  [DIR]  {item}/ ({count} 个文件)")
        else:
            size = os.path.getsize(full)
            if size > 1024 * 1024:
                print(f"  [FILE] {item} ({size / 1024 / 1024:.1f} MB)")
            else:
                print(f"  [FILE] {item} ({size / 1024:.0f} KB)")

    print()
    try:
        input("按回车键退出...")
    except EOFError:
        pass


if __name__ == "__main__":
    main()


'''
步骤	提取内容	来源路径
1/9	准备输出目录	清空桌面 XCA Release 并重建
2/9	XCA.exe	build/*.exe
3/9	Qt6 运行库 (8个DLL)	D:\041\Qt\6.7.3\msvc2019_64\bin\
4/9	Qt 插件目录 (platforms/sqldrivers/styles)	D:\041\Qt\6.7.3\msvc2019_64\plugins\
5/9	OpenSSL DLL (libcrypto-3-x64.dll/libssl-3-x64.dll/legacy.dll)	D:\041\OpenSSL-Win64\bin\
6/9	XCA 数据文件 (dn.txt/eku.txt/oids.txt)	build/ 或 lib/
7/9	帮助文档 (html/)	build/html 或 doc/html
8/9	配置目录 (settings/)	build/settings 或 settings/
9/9	VC++ 运行时 (vc_redist.x64.exe)	VS 安装目录下自动搜索

输的出目录结构：
XCA Release/
├── XCA.exe
├── Qt6Core.dll
├── Qt6Gui.dll
├── Qt6Help.dll
├── Qt6Network.dll
├── Qt6Sql.dll
├── Qt6Svg.dll
├── Qt6Test.dll
├── Qt6Widgets.dll
├── libcrypto-3-x64.dll
├── libssl-3-x64.dll
├── legacy.dll
├── dn.txt
├── eku.txt
├── oids.txt
├── vc_redist.x64.exe
├── platforms/
├── sqldrivers/
├── styles/
├── html/
└── settings/
'''

