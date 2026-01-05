"""
认证相关 API 路由

包含功能：
- Token 验证
"""

import logging
from flask import Blueprint, request, jsonify
from backend.services.user import get_user_service

logger = logging.getLogger(__name__)


def create_auth_blueprint():
    """创建认证路由蓝图"""
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/auth/validate', methods=['GET', 'POST'])
    def validate_token():
        """
        验证 Token 是否有效

        请求头：
        - Authorization: Bearer <token>
        - 或 X-Access-Token: <token>

        返回：
        - success: 是否有效
        - user: 用户信息（有效时）
        """
        # 提取 Token
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
        else:
            token = request.headers.get('X-Access-Token', '')

        if not token:
            return jsonify({
                'success': False,
                'error': '未提供访问令牌'
            }), 401

        user_service = get_user_service()
        user = user_service.validate_token(token)

        if user:
            return jsonify({
                'success': True,
                'user': user
            })
        else:
            return jsonify({
                'success': False,
                'error': '访问令牌无效或已禁用'
            }), 401

    return auth_bp
