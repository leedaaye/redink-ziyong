"""
管理面板模块

提供后台管理功能：
- 管理员登录/登出
- 用户管理（CRUD）
- API 配置管理
"""

from flask import Blueprint
from pathlib import Path

# 创建 Admin Blueprint
admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder=str(Path(__file__).parent / 'templates')
)

# 导入路由（必须在 Blueprint 创建后导入）
from . import routes  # noqa: F401, E402

__all__ = ['admin_bp']
