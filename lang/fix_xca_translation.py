#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XCA 中文翻译修复脚本 (fix_xca_translation.py)

功能：
  修复 xca_zh_CN.ts 翻译文件中空的/错误的翻译条目，
  特别是 numerus="yes" 复数形式翻译为空导致界面显示英文的问题。

问题表现：
  - 删除私钥时显示: "Delete the EC private key(s) '1'?"
  - 删除证书时显示: "Delete the 1 certificate(s): '1'?"
  - 删除模板时显示: "Delete the 1 XCA template(s): '1'?"
  等等...

原因：
  .ts 文件中 numerus="yes" 的消息，其 <numerusform> 标签内容为空，
  导致 Qt 回退显示英文原文。

使用方法：
  python fix_xca_translation.py [xca_zh_CN.ts 路径]

  如果不指定路径，默认在当前目录查找 xca_zh_CN.ts

注意：
  运行前会自动创建 .bak 时间戳备份文件。
  修复完成后需重新执行 cmake 编译生成 .qm 文件。
"""

import re
import sys
import os
import shutil
from datetime import datetime


# ====================================================================
#  翻译映射表
# ====================================================================

# --- numerus="yes" 复数形式翻译 ---
# 中文没有复数形式区别，只需一个 <numerusform>
NUMERUS_FIXES = {
    "Delete the %n %1 public key(s) '%2'?":
        "删除 %1 公钥 '%2'？",
    "Delete the %n %1 private key(s) '%2'?":
        "删除 %1 私钥 '%2'？",
    "Delete the %n revocation list(s): '%1'?":
        "删除吊销列表 '%1'？",
    "Delete the %n token key(s): '%1'?":
        "删除令牌密钥 '%1'？",
    "Delete the %n XCA template(s): '%1'?":
        "删除XCA模板 '%1'？",
    "Delete the %n certificate(s): '%1'?":
        "删除证书 '%1'？",
    "Delete the %n PKCS#10 certificate request(s): '%1'?":
        "删除证书签名请求 '%1'？",
    "%n selected item(s)":
        "已选择 %n 个条目",
    "Please enter the password to encrypt all %n exported private key(s) in: %1":
        "请输入密码，用于加密所有导出的私钥到：%1",
}

# --- 普通（非复数）翻译修复 ---
SIMPLE_FIXES = {
    "Successfully imported the %1 public key '%2'":
        "成功导入 %1 公钥 '%2'",
    "Successfully imported the %1 private key '%2'":
        "成功导入 %1 私钥 '%2'",
    "Successfully created the %1 private key '%2'":
        "成功创建 %1 私钥 '%2'",
    "No verification errors found.":
        "未发现验证错误。",
    "Please enter the password to encrypt the key of certificate '%1' in the PKCS#12 file: %2":
        "请输入密码，用于在PKCS#12文件中加密证书 '%1' 的密钥：%2",
}


# ====================================================================
#  XML 工具函数
# ====================================================================

def escape_xml(text):
    """将文本转义为 XML 安全格式"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace("'", '&apos;')
    text = text.replace('"', '&quot;')
    return text


# ====================================================================
#  核心修复逻辑
# ====================================================================

def fix_translation(content, source_text, chinese_text, is_numerus):
    """
    在文件内容中查找指定 source 的翻译并修复。

    返回: (修复后的内容, 是否成功修复)
    """
    escaped_xml_src = escape_xml(source_text)
    escaped_chinese = escape_xml(chinese_text)

    src_tag = '<source>' + escaped_xml_src + '</source>'

    # 正则：从 <source>特定文本</source> 匹配到最近的 <translation>...</translation>
    pattern = re.compile(
        r'(' + re.escape(src_tag) + r')'
        r'.*?'
        r'<translation[^>]*>.*?</translation>',
        re.DOTALL
    )

    match = pattern.search(content)
    if not match:
        return content, False

    if is_numerus:
        new_translation = (
            '<translation>\n'
            '            <numerusform>' + escaped_chinese + '</numerusform>\n'
            '        </translation>'
        )
    else:
        new_translation = '<translation>' + escaped_chinese + '</translation>'

    matched_text = match.group(0)
    new_block = re.sub(
        r'<translation[^>]*>.*?</translation>',
        new_translation,
        matched_text,
        count=1,
        flags=re.DOTALL
    )

    new_content = content[:match.start()] + new_block + content[match.end():]
    return new_content, True


def process_ts_file(filepath):
    """处理整个 .ts 文件"""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = filepath + '.bak_' + timestamp
    shutil.copy2(filepath, backup_path)
    print("已创建备份文件: " + backup_path)
    print()

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fix_count = 0
    skip_count = 0

    print("=" * 60)
    print("  修复复数形式 (numerus) 翻译")
    print("=" * 60)
    for source, chinese in NUMERUS_FIXES.items():
        content, fixed = fix_translation(content, source, chinese, is_numerus=True)
        if fixed:
            fix_count += 1
            print("  [OK] " + source[:55])
            print("       -> " + chinese)
        else:
            skip_count += 1
            print("  [SKIP] 未找到: " + source[:55])

    print()
    print("=" * 60)
    print("  修复普通翻译")
    print("=" * 60)
    for source, chinese in SIMPLE_FIXES.items():
        content, fixed = fix_translation(content, source, chinese, is_numerus=False)
        if fixed:
            fix_count += 1
            print("  [OK] " + source[:55])
            print("       -> " + chinese)
        else:
            skip_count += 1
            print("  [SKIP] 未找到: " + source[:55])

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print()
    print("=" * 60)
    print("  修复完成! 共修复 " + str(fix_count) + " 处, 跳过 " + str(skip_count) + " 处")
    print("  备份文件: " + backup_path)
    print("=" * 60)
    print()
    print("提示: 请重新编译项目以生成 .qm 翻译文件:")
    print("  cmake --build .")
    print()

    return fix_count


# ====================================================================
#  主入口
# ====================================================================

if __name__ == '__main__':
    print()
    print("======================================================")
    print("  XCA Chinese Translation Fix Script")
    print("  fix_xca_translation.py")
    print("======================================================")
    print()

    if len(sys.argv) > 1:
        ts_file = sys.argv[1]
    else:
        ts_file = 'xca_zh_CN.ts'

    if not os.path.exists(ts_file):
        print("Error: File not found: " + ts_file)
        print()
        print("Usage:")
        print("  python fix_xca_translation.py [path/to/xca_zh_CN.ts]")
        sys.exit(1)

    print("Target: " + os.path.abspath(ts_file))
    print()

    process_ts_file(ts_file)
