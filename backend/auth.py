import hashlib
import os
import jwt
import datetime
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from Crypto.Random import get_random_bytes
import base64

# 修改存储路径到 backend/user_data/profile.json
USER_DATA_DIR = os.path.join(os.path.dirname(__file__), 'user_data')
PROFILE_FILE = os.path.join(USER_DATA_DIR, 'profile.json')
# Token 过期时间（小时）
TOKEN_EXPIRE_HOURS = 24
# JWT 密钥
JWT_SECRET_KEY = 'SteamGamePriceSpiderJWTSecret2026!'
ALGORITHM = 'HS256'

# 固定的 AES 加密密钥和 IV (32 字节密钥，16 字节 IV)
SECRET_KEY = '7A4B2C9D8E1F6G3H5I0J2K4L8M6N0O2P'
IV = '1A2B3C4D5E6F7G8H'

def decrypt_data(encrypted_data):
    """AES 解密数据 (CBC 模式)"""
    try:
        cipher_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_CBC, IV.encode('utf-8'))
        decrypted = unpad(cipher.decrypt(cipher_bytes), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        raise ValueError(f"解密失败：{str(e)}")

def hash_password(password):
    """对密码进行 SHA256 哈希"""
    return hashlib.sha256(password.encode()).hexdigest()

def is_password_initialized():
    """检查是否已初始化密码"""
    return os.path.exists(PROFILE_FILE)

def init_password(password):
    """初始化管理员密码"""
    if is_password_initialized():
        return False, "密码已存在，无需重复初始化"
    
    # 确保 user_data 目录存在
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    
    hashed = hash_password(password)
    profile_data = {
        "password": hashed,
        "settings": {
            "language": "zh-CN",
            "theme": "dark"
        }
    }
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(profile_data, f, indent=2, ensure_ascii=False)
    return True, "密码初始化成功"

def verify_password(password):
    """验证密码"""
    if not is_password_initialized():
        return False, "密码未初始化"
    
    with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    hashed = hash_password(password)
    if hashed == data["password"]:
        return True, "验证成功"
    else:
        return False, "密码错误"

def change_password(old_password, new_password):
    """修改密码"""
    if not is_password_initialized():
        return False, "密码未初始化"
    
    # 验证旧密码
    success, message = verify_password(old_password)
    if not success:
        return False, message
    
    # 更新为新密码
    hashed = hash_password(new_password)
    with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    
    profile["password"] = hashed
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    return True, "密码修改成功"

def generate_token():
    """生成 JWT token"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRE_HOURS),
        'iat': datetime.datetime.utcnow(),
        'type': 'auth'
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, "Token 已过期"
    except jwt.InvalidTokenError:
        return False, "无效的 Token"

def get_profile():
    """获取用户配置"""
    if not is_password_initialized():
        return None
    
    with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_profile(updates):
    """更新用户配置"""
    if not is_password_initialized():
        return False, "密码未初始化"
    
    with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    
    # 更新配置
    if 'settings' in updates:
        if 'settings' not in profile:
            profile['settings'] = {}
        profile['settings'].update(updates['settings'])
    
    # 更新 API KEY
    if 'api_key' in updates:
        profile['api_key'] = updates['api_key']
    
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    return True, "配置更新成功"

def get_api_key():
    """获取 API KEY"""
    if not is_password_initialized():
        return None
    
    with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    
    return profile.get('api_key')

def set_api_key(api_key):
    """设置 API KEY"""
    return update_profile({'api_key': api_key})