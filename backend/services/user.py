"""
用户服务模块

提供用户管理和 Token 认证功能：
- 用户 CRUD 操作
- Token 验证
- 管理员密码验证
"""

import json
import secrets
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / 'data'
USERS_FILE = DATA_DIR / 'users.json'

# 默认管理员密码（首次启动时使用，建议立即修改）
DEFAULT_ADMIN_PASSWORD = 'redink2025'


def _ensure_data_file():
    """确保数据文件存在，不存在则创建默认结构"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not USERS_FILE.exists():
        default_data = {
            'users': [],
            'admin_password_hash': generate_password_hash(DEFAULT_ADMIN_PASSWORD)
        }
        _write_data(default_data)
        logger.info(f"已创建用户数据文件: {USERS_FILE}")
        logger.warning(f"默认管理员密码为: {DEFAULT_ADMIN_PASSWORD}，请尽快修改！")


def _read_data() -> dict:
    """读取用户数据"""
    _ensure_data_file()
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _write_data(data: dict):
    """写入用户数据（原子写入）"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = USERS_FILE.with_suffix('.tmp')
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temp_file.replace(USERS_FILE)


class UserService:
    """用户服务类"""

    @staticmethod
    def verify_admin_password(password: str) -> bool:
        """验证管理员密码"""
        data = _read_data()
        return check_password_hash(data.get('admin_password_hash', ''), password)

    @staticmethod
    def change_admin_password(old_password: str, new_password: str) -> bool:
        """修改管理员密码"""
        if not UserService.verify_admin_password(old_password):
            return False

        data = _read_data()
        data['admin_password_hash'] = generate_password_hash(new_password)
        _write_data(data)
        logger.info("管理员密码已修改")
        return True

    @staticmethod
    def get_all_users() -> List[Dict]:
        """获取所有用户列表（不含 token）"""
        data = _read_data()
        users = []
        for user in data.get('users', []):
            users.append({
                'id': user['id'],
                'username': user['username'],
                'enabled': user['enabled'],
                'created_at': user['created_at'],
                'last_used': user.get('last_used')
            })
        return users

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict]:
        """根据 ID 获取用户"""
        data = _read_data()
        for user in data.get('users', []):
            if user['id'] == user_id:
                return user
        return None

    @staticmethod
    def get_user_by_token(token: str) -> Optional[Dict]:
        """根据 Token 获取用户"""
        if not token:
            return None
        data = _read_data()
        for user in data.get('users', []):
            if user.get('access_token') == token and user.get('enabled', True):
                return user
        return None

    @staticmethod
    def validate_token(token: str) -> Optional[Dict]:
        """验证 Token 并更新最后使用时间"""
        user = UserService.get_user_by_token(token)
        if user:
            UserService._update_last_used(user['id'])
            return {
                'id': user['id'],
                'username': user['username']
            }
        return None

    @staticmethod
    def _update_last_used(user_id: str):
        """更新用户最后使用时间"""
        data = _read_data()
        for user in data.get('users', []):
            if user['id'] == user_id:
                user['last_used'] = datetime.now().isoformat()
                _write_data(data)
                break

    @staticmethod
    def create_user(username: str) -> Dict:
        """创建新用户"""
        data = _read_data()

        # 检查用户名是否已存在
        for user in data.get('users', []):
            if user['username'] == username:
                raise ValueError(f"用户名 '{username}' 已存在")

        # 生成新用户
        new_user = {
            'id': secrets.token_hex(8),
            'username': username,
            'access_token': secrets.token_urlsafe(32),
            'enabled': True,
            'created_at': datetime.now().isoformat(),
            'last_used': None
        }

        data.setdefault('users', []).append(new_user)
        _write_data(data)
        logger.info(f"已创建用户: {username}")

        return new_user

    @staticmethod
    def regenerate_token(user_id: str) -> Optional[str]:
        """重新生成用户 Token"""
        data = _read_data()
        for user in data.get('users', []):
            if user['id'] == user_id:
                new_token = secrets.token_urlsafe(32)
                user['access_token'] = new_token
                _write_data(data)
                logger.info(f"已重新生成用户 Token: {user['username']}")
                return new_token
        return None

    @staticmethod
    def toggle_user(user_id: str) -> Optional[bool]:
        """切换用户启用/禁用状态"""
        data = _read_data()
        for user in data.get('users', []):
            if user['id'] == user_id:
                user['enabled'] = not user.get('enabled', True)
                _write_data(data)
                status = "启用" if user['enabled'] else "禁用"
                logger.info(f"用户 {user['username']} 已{status}")
                return user['enabled']
        return None

    @staticmethod
    def delete_user(user_id: str) -> bool:
        """删除用户"""
        data = _read_data()
        users = data.get('users', [])
        for i, user in enumerate(users):
            if user['id'] == user_id:
                deleted_user = users.pop(i)
                _write_data(data)
                logger.info(f"已删除用户: {deleted_user['username']}")
                return True
        return False


# 单例实例
_user_service = None


def get_user_service() -> UserService:
    """获取用户服务单例"""
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service
