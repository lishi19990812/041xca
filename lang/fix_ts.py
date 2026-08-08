import re
import os

# 自动获取当前脚本所在目录下的 xca_zh_CN.ts
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xca_zh_CN.ts')

if not os.path.exists(file_path):
    print(f"找不到文件: {file_path}")
    exit()

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 普通翻译映射
translations = {
    "Validation": "验证",
    "Purposes": "用途",
    "Strict RFC 5280 validation": "严格的 RFC 5280 验证",
    "Hide unusable certificates": "隐藏不可用的证书",
    "vCalendar entry ( *.ics )": "vCalendar条目 ( *.ics )",
    "OpenVPN file ( *.ovpn )": "OpenVPN文件 ( *.ovpn )",
    "OpenVPN tls-auth key ( *.key )": "OpenVPN TLS认证密钥 ( *.key )",
    "Each Item in a separate file": "每个条目导出为单独的文件",
    "Same encryption password for all items": "所有条目使用相同的加密密码",
    "The path: &apos;%1&apos; exist, but is not a file": "路径 &apos;%1&apos; 存在，但不是一个文件",
    "The path: &apos;%1&apos; exist, but is not a directory": "路径 &apos;%1&apos; 存在，但不是一个目录",
    "The directory: &apos;%1&apos; does not exist. Should it be created?": "目录 &apos;%1&apos; 不存在。是否创建？",
    "Failed to create directory &apos;%1&apos;": "创建目录 &apos;%1&apos; 失败",
    "Korean": "韩语",
    "SSH Private Keys ( *.priv )": "SSH私钥 ( *.priv )",
    "Microsoft PVK Keys ( *.pvk )": "Microsoft PVK密钥 ( *.pvk )",
    "Name Constraints": "名称约束",
    "OpenVPN tls-auth key ( *.key );;": "OpenVPN TLS认证密钥 ( *.key );;",
    "The Name Constraints are invalid": "名称约束无效",
    "A name constraint of the issuer &apos;%1&apos; is violated: %2": "违反了签发人 &apos;%1&apos; 的名称约束: %2",
    "Failed to write PEM data to &apos;%1&apos;": "写入PEM数据到 &apos;%1&apos; 失败",
    "Export Password": "导出密码",
    "Clipboard format": "剪贴板格式",
    "PEM selected": "选定的PEM",
    "Concatenated list of all selected certificates in one PEM text file": "将所有选定的证书合并到一个PEM文本文件中",
    "All unusable": "所有不可用的",
    "Concatenation of all expired or revoked certificates in one PEM file": "将所有过期或已吊销的证书合并到一个PEM文件中",
    "PKCS #7 unusable": "PKCS#7 不可用",
    "PKCS#7 encoded collection of all expired or revoked certificates": "将所有过期或已吊销的证书编码到一个PKCS#7文件中",
    "JSON Web Kit": "JSON Web Key",
    "The public key of the certificate in JSON Web Kit format with X.509 Certificate Thumbprint (x5t)": "证书的公钥，以JSON Web Key格式编码，包含X.509证书指纹(x5t)",
    "JSON Web Kit chain": "JSON Web Key 证书链",
    "The public key of the certificate in JSON Web Kit format with X.509 Certificate Thumbprint (x5t) and certificate chain (x5c)": "证书的公钥，以JSON Web Key格式编码，包含X.509证书指纹(x5t)和证书链(x5c)",
    "XCA template in PEM-like format. Templates include the internal name and comment": "XCA模板（PEM-like格式），包含内部名称和备注",
    "All selected XCA templates in PEM-like format. Templates include the internal name and comment": "所有选定的XCA模板（PEM-like格式），包含内部名称和备注",
    "JSON Web Key private": "JSON Web Key 私钥",
    "Unencrypted private key in JSON Web Key format": "未加密的私钥，以JSON Web Key格式编码",
    "JSON Web Key public": "JSON Web Key 公钥",
    "Public key in JSON Web Key format": "公钥，以JSON Web Key格式编码",
    "Common": "常规",
    "Please enter the password to encrypt the key of certificate &apos;%1&apos; in the PKCS#12 file: %2": "请输入密码，用于在PKCS#12文件 %2 中加密证书 &apos;%1&apos; 的密钥",
    "Successfully imported the PKCS#10 certificate request &apos;%1&apos;": "成功导入PKCS#10证书请求 &apos;%1&apos;",
    "Successfully created the PKCS#10 certificate request &apos;%1&apos;": "成功创建PKCS#10证书请求 &apos;%1&apos;",
    "Create": "创建",
    "Directory": "目录"
}

count = 0

for src, trans in translations.items():
    pattern = re.compile(
        r'(<source>' + re.escape(src) + r'</source>[\s\S]*?<translation) type="unfinished">.*?(</translation>)'
    )
    content, n = pattern.subn(r'\1>' + trans + r'\2', content)
    count += n

# 复数形式（numerusform）的翻译映射
plurals = {
    "Please enter the password to encrypt all %n exported private key(s) in: %1": "请输入密码，用于加密 %1 中的全部 %n 个导出私钥",
    "Delete the %n %1 public key(s) &apos;%2&apos;?": "删除 %n 个%1公钥 &apos;%2&apos;?",
    "Delete the %n %1 private key(s) &apos;%2&apos;?": "删除 %n 个%1私钥 &apos;%2&apos;?",
    "Delete the %n token key(s): &apos;%1&apos;?": "删除 %n 个令牌密钥: &apos;%1&apos;?",
    "Delete the %n XCA template(s): &apos;%1&apos;?": "删除 %n 个XCA模板: &apos;%1&apos;?",
    "Delete the %n certificate(s): &apos;%1&apos;?": "删除 %n 个证书: &apos;%1&apos;?",
    "Delete the %n revocation list(s): &apos;%1&apos;?": "删除 %n 个吊销列表: &apos;%1&apos;?",
    "Delete the %n PKCS#10 certificate request(s): &apos;%1&apos;?": "删除 %n 个PKCS#10证书请求: &apos;%1&apos;?"
}

for src, trans in plurals.items():
    pattern = re.compile(
        r'(<source>' + re.escape(src) + r'</source>[\s\S]*?<translation) type="unfinished" numerus="yes">[\s\S]*?<numerusform>.*?</numerusform>[\s\S]*?(</translation>)'
    )
    replacement = r'\1 numerus="yes">\n            <numerusform>' + trans + r'</numerusform>\n        \2'
    content, n = pattern.subn(replacement, content)
    count += n

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"修补完成！共更新了 {count} 处未翻译条目。")
