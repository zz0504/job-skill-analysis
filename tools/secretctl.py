#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
secretctl —— 仓库内敏感配置的加解密工具

用途：把 .env / deploy.config 这类含真实密码的文件加密后提交到公开仓库，
      明文永远不进版本库。口令（passphrase）自己保管，不写进任何文件。

用法：
    pip install cryptography

    # 加密（生成 xxx.enc，明文保留在本地但不提交）
    python tools/secretctl.py encrypt deploy/.env.production

    # 解密（生成明文 .env.production）
    python tools/secretctl.py decrypt deploy/.env.production.enc

    # 批量：加密 secrets.list 里列出的所有文件
    python tools/secretctl.py encrypt-all
    python tools/secretctl.py decrypt-all

口令来源（优先级从高到低）：
    1. 环境变量 SECRETS_PASSPHRASE
    2. 命令行参数 --passphrase
    3. 交互式输入（不回显）

文件格式：纯文本，便于 git diff
    SECF1:<base64( salt(16B) + Fernet token )>

安全说明：
    口令经 PBKDF2-HMAC-SHA256 派生密钥，480000 轮迭代，随机 16 字节盐。
    口令丢失 = 数据不可恢复，请自行备份到密码管理器。
"""

import argparse
import base64
import getpass
import os
import sys
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    sys.exit("缺少依赖，请先执行：pip install cryptography")

MAGIC = "SECF1:"
SALT_SIZE = 16
ITERATIONS = 480_000
LIST_FILE = "secrets.list"


def derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))


def get_passphrase(cli_value: str | None = None) -> str:
    if cli_value:
        return cli_value
    env_value = os.environ.get("SECRETS_PASSPHRASE")
    if env_value:
        return env_value
    value = getpass.getpass("口令：")
    if not value:
        sys.exit("口令不能为空")
    return value


def encrypt_file(src: Path, passphrase: str, keep_plain: bool = True) -> Path:
    if not src.exists():
        sys.exit(f"文件不存在：{src}")
    plaintext = src.read_bytes()
    salt = os.urandom(SALT_SIZE)
    token = Fernet(derive_key(passphrase, salt)).encrypt(plaintext)
    payload = base64.b64encode(salt + token).decode("ascii")
    dst = src.with_suffix(src.suffix + ".enc") if src.suffix else Path(str(src) + ".enc")
    dst.write_text(MAGIC + payload + "\n", encoding="utf-8")
    if not keep_plain:
        src.unlink()
    return dst


def decrypt_file(src: Path, passphrase: str, force: bool = False) -> Path:
    if not src.exists():
        sys.exit(f"文件不存在：{src}")
    raw = src.read_text(encoding="utf-8").strip()
    if not raw.startswith(MAGIC):
        sys.exit(f"不是有效的加密文件（缺少 {MAGIC} 头）：{src}")
    blob = base64.b64decode(raw[len(MAGIC):])
    salt, token = blob[:SALT_SIZE], blob[SALT_SIZE:]
    try:
        plaintext = Fernet(derive_key(passphrase, salt)).decrypt(token)
    except Exception:
        sys.exit("解密失败：口令错误或文件已损坏")
    dst = src.with_suffix("") if src.suffix == ".enc" else Path(str(src)[: -len(".enc")])
    if dst.exists() and not force:
        sys.exit(f"目标文件已存在，加 --force 覆盖：{dst}")
    dst.write_bytes(plaintext)
    return dst


def read_list() -> list[Path]:
    p = Path(LIST_FILE)
    if not p.exists():
        sys.exit(f"未找到 {LIST_FILE}")
    return [Path(line.strip()) for line in p.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")]


def main() -> None:
    ap = argparse.ArgumentParser(description="敏感配置加解密工具")
    ap.add_argument("action", choices=["encrypt", "decrypt", "encrypt-all", "decrypt-all"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--passphrase", help="不推荐用于命令行（会留在 shell 历史里）")
    ap.add_argument("--force", action="store_true", help="解密时覆盖已存在的明文")
    ap.add_argument("--drop-plain", action="store_true", help="加密后删除明文")
    args = ap.parse_args()

    if args.action.endswith("-all"):
        files = read_list()
    elif args.file:
        files = [Path(args.file)]
    else:
        sys.exit("请指定文件或使用 -all")

    pwd = get_passphrase(args.passphrase)

    for f in files:
        if args.action.startswith("encrypt"):
            if not f.exists():
                print(f"[跳过] 明文不存在：{f}")
                continue
            out = encrypt_file(f, pwd, keep_plain=not args.drop_plain)
            print(f"[加密] {f} -> {out}")
        else:
            target = f if f.suffix == ".enc" else Path(str(f) + ".enc")
            if not target.exists():
                print(f"[跳过] 加密文件不存在：{target}")
                continue
            out = decrypt_file(target, pwd, force=args.force)
            print(f"[解密] {target} -> {out}")


if __name__ == "__main__":
    main()
