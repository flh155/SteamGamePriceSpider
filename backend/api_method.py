import requests
import json
import os
import logging

from backend.api_url import GET_UPDATE_SHOPS_URL, GET_SEARCH_GAME_INFO_URL, POST_GET_GAME_INFO_URL, POST_GET_GAME_PRICE_URL, POST_GET_DEAL_GAME_LIST_URL

# 获取日志记录器
logger = logging.getLogger(__name__)

# 从 profile.json 中读取 API_KEY
def get_api_key():
    """从 user_data/profile.json 中读取 API Key"""
    profile_path = os.path.join(os.path.dirname(__file__), 'user_data', 'profile.json')
    
    if not os.path.exists(profile_path):
        return None
    
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile = json.load(f)
        return profile.get('api_key')
    except Exception:
        return None


def update_shop_info():
    url = GET_UPDATE_SHOPS_URL
    params = {"country": "CN"}
    response = requests.get(url,params=params)
    shop_info_list = response.json()
    shop_info_dict = {}
    for shop_info in shop_info_list:
        shop_id = shop_info["id"]
        shop_name = shop_info["title"]
        update_time = shop_info["update"]
        shop_info_dict[shop_id] = {"name": shop_name,"update_time": update_time}
    with open("shop_info.json", "w") as f:
        json.dump(shop_info_dict, f, indent=4)


def get_one_game_price(game_name):
    logger.info(f"开始查询游戏价格：{game_name}")
    API_KEY = get_api_key()
    
    # 检查 API Key 是否存在
    if not API_KEY:
        logger.warning("API Key 未配置")
        return {
            "game_name": "请先在设置页面配置 API Key",
            "game_id": -1,
            "best_price_shop_name": None,
            "best_price": None,
            "lowest_shop_name": None,
            "lowest_price": None,
            "now_steam_price": None,
            "currency": None,
            "pic_url": {
                "600x344": None,
                "400x187": None,
                "300x140": None,
                "145x68": None,
                "boxart": None
            }
        }
    
    search_url = GET_SEARCH_GAME_INFO_URL
    search_params = {"key": API_KEY,"title": game_name}
    logger.debug(f"搜索游戏 API：{search_url}, 参数：{search_params}")
    
    try:
        response = requests.get(search_url, params=search_params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"搜索游戏 API 请求失败：{str(e)}")
        raise
    
    return_json = response.json()
    logger.debug(f"搜索游戏返回数据：{len(return_json) if isinstance(return_json, list) else 'dict'}")
    
    if len(return_json) == 0:
        logger.info(f"未找到游戏：{game_name}")
        game_id = -1
        game_origin_name = "未查询到该游戏，请尝试使用英文名或其它别称"
        current_shop_name = None
        current_price = None 
        lowest_shop_name = None
        lowest_price = None
        now_steam_price = None
        current_currency = None
        return_dict = {"game_name":game_origin_name,"game_id":game_id,"best_price_shop_name": current_shop_name,"best_price": current_price,"lowest_shop_name":lowest_shop_name,"lowest_price": lowest_price,"now_steam_price":now_steam_price,"currency": current_currency,"pic_url":{"600x344":None,"400x187":None,"300x140":None,"145x68":None,"boxart":None}}
        return return_dict
    
    if isinstance(return_json, dict):
        logger.error(f"搜索游戏 API 返回字典而非列表：{return_json}")
        game_id = -1
        game_origin_name = "查询 API 报错，请检查后端"
        current_shop_name = None
        current_price = None 
        lowest_shop_name = None
        lowest_price = None
        now_steam_price = None
        current_currency = None
        return_dict = {"game_name":game_origin_name,"game_id":game_id,"best_price_shop_name": current_shop_name,"best_price": current_price,"lowest_shop_name":lowest_shop_name,"lowest_price": lowest_price,"now_steam_price":now_steam_price,"currency": current_currency,"pic_url":{"600x344":None,"400x187":None,"300x140":None,"145x68":None,"boxart":None}}
        return return_dict

    game_id = return_json[0]["id"]
    game_origin_name = return_json[0]["title"]
    logger.info(f"找到游戏：{game_origin_name} (ID: {game_id})")
    
    get_game_info_url = POST_GET_GAME_INFO_URL
    get_game_info_params = {"key": API_KEY,"title": game_origin_name}

    get_game_best_price_url = POST_GET_GAME_PRICE_URL
    get_game_best_price_params = {"key": API_KEY,"country": "CN","shops":"16,35,36,37,61,62"}

    get_game_steam_price_url = POST_GET_GAME_PRICE_URL
    get_game_steam_price_params = {"key": API_KEY,"country": "CN","shops": "61"}
    
    logger.debug("开始并发请求游戏详情、最佳价格和 Steam 价格")
    
    try:
        game_info_response = requests.get(get_game_info_url,params=get_game_info_params, timeout=10)
        best_price_response = requests.post(get_game_best_price_url, json=[game_id],params=get_game_best_price_params, timeout=10)
        steam_price_response = requests.post(get_game_steam_price_url, json=[game_id],params=get_game_steam_price_params, timeout=10)
        
        game_info_response.raise_for_status()
        best_price_response.raise_for_status()
        steam_price_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"获取游戏详细信息失败：{str(e)}")
        raise

    game_info_json = game_info_response.json()
    game_pic_url_dict = game_info_json[0]["assets"]
    game_pic_600_344_url = game_pic_url_dict.get("banner600")
    game_pic_400_187_url = game_pic_url_dict.get("banner400")
    game_pic_300_140_url = game_pic_url_dict.get("banner300")
    game_pic_145_68_url = game_pic_url_dict.get("banner145")
    game_pic_boxart_url = game_pic_url_dict.get("boxart")   # 300x450

    best_price_json = best_price_response.json()
    logger.debug(f"best_price_json：{best_price_json}")
    if len(best_price_json["prices"]) == 0:
        logger.warning(f"未找到游戏:{game_origin_name}")
        current_shop_name = "无"
        current_price = -1
        lowest_price = -1
        lowest_shop_name = "无"
        current_currency = "CNY"
        now_steam_price = -1
        return_dict = {"game_name":game_origin_name,"game_id":game_id,"best_price_shop_name": current_shop_name,"best_price": current_price,"lowest_shop_name":lowest_shop_name,"lowest_price": lowest_price,"now_steam_price":now_steam_price,"currency": current_currency,"pic_url":{"600x344":game_pic_600_344_url,"400x187":game_pic_400_187_url,"300x140":game_pic_300_140_url,"145x68":game_pic_145_68_url,"boxart":game_pic_boxart_url}}
        return return_dict
    prices_list = best_price_json["prices"][0]
    current_shop_name = prices_list["current"]["shop"]["name"]
    current_price = prices_list["current"]["price"]["amount"]
    current_currency = prices_list["current"]["price"]["currency"]
    lowest_price = prices_list["lowest"]["price"]["amount"]
    lowest_shop_name = prices_list["lowest"]["shop"]["name"]
    # lowest_currency = prices_list["lowest"]["price"]["currency"]

    steam_price_json = steam_price_response.json()
    now_steam_price = steam_price_json["prices"][0]["current"]["price"]["amount"]

    logger.info(f"游戏价格查询完成：{game_origin_name}, 当前价格：{current_price}, 最低价格：{lowest_price}")
    
    return_dict = {"game_name":game_origin_name,"game_id":game_id,"best_price_shop_name": current_shop_name,"best_price": current_price,"lowest_shop_name":lowest_shop_name,"lowest_price": lowest_price,"now_steam_price":now_steam_price,"currency": current_currency,"pic_url":{"600x344":game_pic_600_344_url,"400x187":game_pic_400_187_url,"300x140":game_pic_300_140_url,"145x68":game_pic_145_68_url,"boxart":game_pic_boxart_url}}
    return return_dict

def get_deal_game_list(get_num = 20):
    logger.info(f"开始获取热门游戏，数量：{get_num}")
    API_KEY = get_api_key()
    
    # 检查 API Key 是否存在
    if not API_KEY:
        logger.warning("API Key 未配置")
        return []
    
    if get_num < 1 or get_num > 200:
        logger.error(f"get_num 参数超出范围：{get_num}")
        assert False, "get_num must be between 1 and 200"
    
    url = POST_GET_DEAL_GAME_LIST_URL
    params = {"key": API_KEY,"country": "CN","sort": "-hot","limit": get_num}
    logger.debug(f"热门游戏 API：{url}, 参数：{params}")
    
    try:
        response = requests.get(url,params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"获取热门游戏失败：{str(e)}")
        raise
    
    return_json = response.json()
    game_list = return_json["list"]
    logger.debug(f"获取到 {len(game_list)} 个游戏")
    
    now_deal_game_list = []
    for game_info_dict in game_list:
        if game_info_dict["type"] != "game":
            continue
        for drm_info in game_info_dict["deal"]["drm"]:
            if drm_info["id"] not in [61,62,16]:    # STEAM, Epic, Ubisoft Store
                continue
        
        game_id = game_info_dict["id"]
        game_name = game_info_dict["title"]
        game_deal_info_dict = game_info_dict["deal"]
        now_best_shop_name = game_deal_info_dict["shop"]["name"]
        now_best_price = game_deal_info_dict["price"]["amount"]
        price_currency = game_deal_info_dict["price"]["currency"]
        deal_info_dict = {"game_id":game_id,"game_name":game_name,"best_shop_name":now_best_shop_name,"best_price":now_best_price,"currency":price_currency}
        now_deal_game_list.append(deal_info_dict)

    logger.info(f"热门游戏筛选完成，最终数量：{len(now_deal_game_list)}")
    return now_deal_game_list
