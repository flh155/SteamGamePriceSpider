import flask
from flask_cors import CORS
from backend.api_method import get_one_game_price, get_deal_game_list
from backend.auth import (
    is_password_initialized, 
    init_password, 
    verify_password, 
    generate_token, 
    verify_token,
    change_password,
    get_api_key,
    set_api_key,
    decrypt_data,
    SECRET_KEY,
    IV
)
import logging
import os
from datetime import datetime

app = flask.Flask(__name__)

# ===== 使用 CORS 配置 =====
CORS(app, 
     resources={r"/*": {"origins": "*"}},
     supports_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     expose_headers=["*"],
     max_age=600)
# ===========================

# 公开接口列表（不需要认证的接口）
PUBLIC_PATHS = [
    '/api/auth/init',
    '/api/auth/login',
    '/api/auth/check',
    '/api/auth/check-init',
    '/api/auth/logout',
    '/api/settings/api-key',
]

# 认证中间件
@app.before_request
def check_auth():
    """在每次请求前检查认证（排除公开接口和 OPTIONS 预检）"""
    start_time = datetime.now()
    flask.g.start_time = start_time
    
    # 所有 OPTIONS 预检请求直接放行
    if flask.request.method == 'OPTIONS':
        return '', 200
    
    # 如果是公开接口，跳过认证检查
    if flask.request.path in PUBLIC_PATHS:
        logger.info(f"{flask.request.method} {flask.request.path} - 公开接口")
        return None
    
    # 获取 Authorization header
    auth_header = flask.request.headers.get('Authorization')
    if not auth_header:
        logger.warning(f"{flask.request.method} {flask.request.path} - 缺少认证信息")
        return flask.jsonify({"code": 401, "message": "缺少认证信息", "data": None}), 401
    
    # 提取 token
    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != 'Bearer':
        logger.warning(f"{flask.request.method} {flask.request.path} - 认证格式错误")
        return flask.jsonify({"code": 401, "message": "认证格式错误", "data": None}), 401
    
    token = parts[1]
    valid, result = verify_token(token)
    if not valid:
        logger.warning(f"{flask.request.method} {flask.request.path} - Token 验证失败：{result}")
        return flask.jsonify({"code": 401, "message": result, "data": None}), 401
    
    return None

@app.after_request
def log_response(response):
    """记录每个请求的响应日志"""
    if hasattr(flask.g, 'start_time'):
        duration = (datetime.now() - flask.g.start_time).total_seconds()
        logger.info(
            f"{flask.request.method} {flask.request.path} - "
            f"Status: {response.status_code}, Duration: {duration:.3f}s"
        )
    return response

# 配置日志
def setup_logging():
    """配置日志系统"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'backend_{datetime.now().strftime("%Y%m%d")}.log')
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()

@app.route('/api/auth/check-init', methods=['GET', 'OPTIONS'])
def api_check_init():
    """检查是否已初始化密码"""
    try:
        logger.info("处理密码初始化检查请求")
        initialized = is_password_initialized()
        return flask.jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "initialized": initialized
            }
        })
    except Exception as e:
        logger.error(f"密码初始化检查失败：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

@app.route('/api/auth/init', methods=['POST', 'OPTIONS'])
def api_init_password():
    """初始化管理员密码"""
    try:
        if flask.request.method == 'OPTIONS':
            return '', 200
        
        logger.info("处理密码初始化请求")
        
        if is_password_initialized():
            logger.warning("密码已存在，拒绝重复初始化")
            return flask.jsonify({
                "code": 400,
                "message": "密码已初始化，无法重复设置",
                "data": None
            }), 400
        
        body = flask.request.get_json()
        if not body or 'password' not in body:
            logger.warning("密码初始化请求缺少参数")
            return flask.jsonify({
                "code": 400,
                "message": "缺少密码参数",
                "data": None
            }), 400
        
        # 检查是否加密
        is_encrypted = body.get('encrypted', False)
        password = body['password']
        
        # 如果加密了，先解密
        if is_encrypted:
            try:
                logger.debug(f"准备解密 - SECRET_KEY: {SECRET_KEY[:20]}..., IV: {IV[:20]}...")
                logger.debug(f"加密的密码：{password[:50]}...")
                password = decrypt_data(password)
                logger.info("密码已解密")
            except Exception as e:
                logger.error(f"密码解密失败：{str(e)}", exc_info=True)
                logger.error(f"当前使用的密钥 - SECRET_KEY length: {len(SECRET_KEY)}, IV length: {len(IV)}")
                return flask.jsonify({
                    "code": 400,
                    "message": "密码解密失败",
                    "data": None
                }), 400
        
        if len(password) < 8:
            logger.warning(f"密码长度不足：{len(password)}")
            return flask.jsonify({
                "code": 400,
                "message": "密码长度至少 8 位",
                "data": None
            }), 400
        
        success, message = init_password(password)
        if success:
            logger.info("密码初始化成功")
            return flask.jsonify({
                "code": 200,
                "message": message,
                "data": None
            })
        else:
            logger.warning(f"密码初始化失败：{message}")
            return flask.jsonify({
                "code": 400,
                "message": message,
                "data": None
            }), 400
    except Exception as e:
        logger.error(f"密码初始化异常：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def api_login():
    """管理员登录"""
    try:
        if flask.request.method == 'OPTIONS':
            return '', 200
        
        logger.info("处理登录请求")
        
        if not is_password_initialized():
            logger.warning("密码未初始化时的登录尝试")
            return flask.jsonify({
                "code": 400,
                "message": "密码未初始化，请先初始化密码",
                "data": None
            }), 400
        
        body = flask.request.get_json()
        if not body or 'password' not in body:
            logger.warning("登录请求缺少密码参数")
            return flask.jsonify({
                "code": 400,
                "message": "缺少密码参数",
                "data": None
            }), 400
        
        # 检查是否加密
        is_encrypted = body.get('encrypted', False)
        password = body['password']
        
        # 如果加密了，先解密
        if is_encrypted:
            try:
                password = decrypt_data(password)
                logger.info("密码已解密")
            except Exception as e:
                logger.error(f"密码解密失败：{str(e)}")
                return flask.jsonify({
                    "code": 400,
                    "message": "密码解密失败",
                    "data": None
                }), 400
        
        success, message = verify_password(password)
        
        if success:
            token = generate_token()
            logger.info("登录成功")
            return flask.jsonify({
                "code": 200,
                "message": message,
                "data": {
                    "token": token
                }
            })
        else:
            logger.warning(f"登录失败：{message}")
            return flask.jsonify({
                "code": 401,
                "message": message,
                "data": None
            }), 401
    except Exception as e:
        logger.error(f"登录异常：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

@app.route('/api/auth/check', methods=['GET', 'OPTIONS'])
def api_check_auth():
    """检查认证状态"""
    try:
        if flask.request.method == 'OPTIONS':
            return '', 200
        
        logger.info("处理认证检查请求")
        
        auth_header = flask.request.headers.get('Authorization')
        if not auth_header:
            logger.warning("认证检查：未授权")
            return flask.jsonify({
                "code": 401,
                "message": "未授权",
                "data": None
            }), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            logger.warning("认证检查：认证格式错误")
            return flask.jsonify({
                "code": 401,
                "message": "认证格式错误",
                "data": None
            }), 401
        
        token = parts[1]
        valid, result = verify_token(token)
        
        if valid:
            logger.info("认证检查：已授权")
            return flask.jsonify({
                "code": 200,
                "message": "已授权",
                "data": {
                    "authenticated": True
                }
            })
        else:
            logger.warning(f"认证检查：{result}")
            return flask.jsonify({
                "code": 401,
                "message": result,
                "data": None
            }), 401
    except Exception as e:
        logger.error(f"认证检查异常：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

@app.route('/api/auth/logout', methods=['POST', 'OPTIONS'])
def api_logout():
    """登出"""
    try:
        if flask.request.method == 'OPTIONS':
            return '', 200
        logger.info("处理登出请求")
        return flask.jsonify({
            "code": 200,
            "message": "已退出登录",
            "data": None
        })
    except Exception as e:
        logger.error(f"登出异常：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

# ========== 设置相关 API ==========

@app.route('/api/settings/api-key', methods=['GET', 'POST', 'OPTIONS'])
def api_settings_api_key():
    """获取或设置 API KEY"""
    try:
        if flask.request.method == 'OPTIONS':
            return '', 200
        elif flask.request.method == 'GET':
            logger.info("获取 API Key")
            api_key = get_api_key()
            return flask.jsonify({
                "code": 200,
                "message": "success",
                "data": {
                    "api_key": api_key or ""
                }
            })
        elif flask.request.method == 'POST':
            logger.info("设置 API Key")
            body = flask.request.get_json()
            if not body or 'api_key' not in body:
                logger.warning("设置 API Key 缺少参数")
                return flask.jsonify({
                    "code": 400,
                    "message": "缺少 API Key 参数",
                    "data": None
                }), 400
            
            # 检查是否加密
            is_encrypted = body.get('encrypted', False)
            api_key = body['api_key'].strip()
            
            # 如果加密了，先解密
            if is_encrypted:
                try:
                    api_key = decrypt_data(api_key)
                    logger.info("API Key 已解密")
                except Exception as e:
                    logger.error(f"API Key 解密失败：{str(e)}")
                    return flask.jsonify({
                        "code": 400,
                        "message": "API Key 解密失败",
                        "data": None
                    }), 400
            
            if not api_key:
                logger.warning("API Key 为空")
                return flask.jsonify({
                    "code": 400,
                    "message": "API Key 不能为空",
                    "data": None
                }), 400
            
            success, message = set_api_key(api_key)
            if success:
                logger.info("API Key 设置成功")
                return flask.jsonify({
                    "code": 200,
                    "message": "API Key 设置成功",
                    "data": None
                })
            else:
                logger.warning(f"API Key 设置失败：{message}")
                return flask.jsonify({
                    "code": 400,
                    "message": message,
                    "data": None
                }), 400
    except Exception as e:
        logger.error(f"API Key 操作异常：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

@app.route('/api/settings/change-password', methods=['POST', 'OPTIONS'])
def api_change_password():
    """修改密码"""
    try:
        if flask.request.method == 'OPTIONS':
            return '', 200
        
        logger.info("处理修改密码请求")
        
        body = flask.request.get_json()
        if not body:
            logger.warning("修改密码缺少参数")
            return flask.jsonify({
                "code": 400,
                "message": "缺少参数",
                "data": None
            }), 400
        
        # 检查是否加密
        is_encrypted = body.get('encrypted', False)
        
        old_password = body.get('old_password', '')
        new_password = body.get('new_password', '')
        confirm_password = body.get('confirm_password', '')
        
        # 如果加密了，先解密
        if is_encrypted:
            try:
                old_password = decrypt_data(old_password)
                new_password = decrypt_data(new_password)
                confirm_password = decrypt_data(confirm_password)
                logger.info("密码已解密")
            except Exception as e:
                logger.error(f"密码解密失败：{str(e)}")
                return flask.jsonify({
                    "code": 400,
                    "message": "密码解密失败",
                    "data": None
                }), 400
        
        if not old_password or not new_password or not confirm_password:
            logger.warning("修改密码：未填写所有字段")
            return flask.jsonify({
                "code": 400,
                "message": "请填写所有密码字段",
                "data": None
            }), 400
        
        if new_password != confirm_password:
            logger.warning("修改密码：两次新密码不一致")
            return flask.jsonify({
                "code": 400,
                "message": "两次输入的新密码不一致",
                "data": None
            }), 400
        
        if len(new_password) < 8:
            logger.warning(f"修改密码：新密码长度不足 {len(new_password)}")
            return flask.jsonify({
                "code": 400,
                "message": "新密码长度至少 8 位",
                "data": None
            }), 400
        
        success, message = change_password(old_password, new_password)
        if success:
            logger.info("密码修改成功")
            return flask.jsonify({
                "code": 200,
                "message": message,
                "data": None
            })
        else:
            logger.warning(f"密码修改失败：{message}")
            return flask.jsonify({
                "code": 400,
                "message": message,
                "data": None
            }), 400
    except Exception as e:
        logger.error(f"修改密码异常：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

# ========== 游戏相关 API ==========

@app.route('/api/game/search', methods=['GET', 'POST', 'OPTIONS'])
def api_game_search():
    """搜索游戏价格"""
    try:
        if flask.request.method == 'OPTIONS':
            return '', 200
        
        logger.info(f"处理游戏搜索请求：{flask.request.method}")
        
        if flask.request.method == 'GET':
            game_name = flask.request.args.get('game_name', '')
        elif flask.request.method == 'POST':
            body = flask.request.get_json()
            game_name = body.get('game_name', '') if body else ''
        else:
            logger.warning(f"不支持的请求方法：{flask.request.method}")
            return flask.jsonify({
                "code": 400,
                "message": "不支持的请求方法",
                "data": None
            }), 400
        
        if not game_name:
            logger.warning("游戏名称为空")
            return flask.jsonify({
                "code": 400,
                "message": "请输入游戏名称",
                "data": None
            }), 400
        
        logger.info(f"搜索游戏：{game_name}")
        price_info_dict = get_one_game_price(game_name)
        logger.info(f"游戏搜索完成：{game_name}")
        return flask.jsonify({
            "code": 200,
            "message": "success",
            "data": price_info_dict
        })
    except Exception as e:
        logger.error(f"游戏搜索异常：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

@app.route('/api/game/hot', methods=['GET', 'OPTIONS'])
def api_game_hot():
    """获取热门游戏"""
    try:
        if flask.request.method == 'OPTIONS':
            return '', 200
        
        limit = flask.request.args.get('num', 20, type=int)
        logger.info(f"获取热门游戏，数量：{limit}")
        
        if limit < 1 or limit > 200:
            logger.warning(f"热门游戏数量超出范围，重置为 20")
            limit = 20
        games_list = get_deal_game_list(get_num=limit)
        logger.info(f"热门游戏获取成功，共 {len(games_list)} 个")
        return flask.jsonify({
            "code": 200,
            "message": "success",
            "data": games_list
        })
    except Exception as e:
        logger.error(f"获取热门游戏异常：{str(e)}", exc_info=True)
        return flask.jsonify({
            "code": 500,
            "message": f"服务器错误：{str(e)}",
            "data": None
        }), 500

if __name__ == '__main__':
    logger.info("后端服务启动...")
    logger.info("运行模式：debug=True, host=0.0.0.0, port=5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
