import itchat
import json
import logging
import threading
import time
import os
import webbrowser

from flask_cors import CORS
from openai import OpenAI
from itchat.content import TEXT
from flask import Flask, render_template
from models import Session, ChatMessage

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 读取配置文件
with open('config.json', 'r') as f:
    config = json.load(f)

# 配置常量
API_KEY = config['LLM_API']['api_key']
BASE_URL = config['LLM_API']['base_url']
MODEL = config['LLM_API']['model']
SYSTEM_PROMPT = config['LLM_API']['system_prompt']
MAX_CONTEXT_WINDOW = config['CHAT_CONFIG']['max_context_window']

# Flask 配置
FLASK_CONFIG = config['FLASK_CONFIG']
SECRET_KEY = FLASK_CONFIG['SECRET_KEY']
TEMPLATES_AUTO_RELOAD = FLASK_CONFIG['TEMPLATES_AUTO_RELOAD']
HOST = FLASK_CONFIG['HOST']
PORT = FLASK_CONFIG['PORT']

# 创建Flask应用
app = Flask(__name__, static_folder='static')
CORS(app)

# 全局变量存储上下文
chat_contexts = {}


# 保存消息到数据库
def save_message(sender_id, sender_name, message, reply):
    """
    保存聊天记录到数据库
    :param sender_id: 发送者ID
    :param sender_name: 发送者姓名
    :param message: 用户消息
    :param reply: 机器人回复
    """
    try:
        session = Session()
        chat_message = ChatMessage(
            sender_id=sender_id,
            sender_name=sender_name,
            message=message,
            reply=reply
        )
        session.add(chat_message)
        session.commit()
        session.close()
    except Exception as e:
        logger.error(f"保存消息失败: {str(e)}")


# 获取LLM的回复
def get_llm_response(user_id):
    """
    调用大模型生成回复
    :param user_id: 用户ID
    :return: 生成的回复
    """
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *chat_contexts[user_id]]
    )
    return resp.choices[0].message.content


# 获取回复
def get_response(message, user_id):
    """
    调用 API获取回复
    :param message: 用户消息
    :param user_id: 用户ID
    :return: 机器人回复
    """
    try:
        # 获取用户上下文
        if user_id not in chat_contexts:
            chat_contexts[user_id] = []

        # 添加新消息到上下文
        chat_contexts[user_id].append({"role": "user", "content": message})

        # 保持上下文长度不超过最大限制
        if len(chat_contexts[user_id]) > MAX_CONTEXT_WINDOW:
            chat_contexts[user_id] = chat_contexts[user_id][-MAX_CONTEXT_WINDOW:]

        # 获取回复
        reply = get_llm_response(user_id)

        # 添加回复到上下文
        chat_contexts[user_id].append({"role": "assistant", "content": reply})

        return reply
    except Exception as e:
        logger.error(f"调用DeepSeek API失败: {str(e)}")
        return "抱歉，我现在无法回复，请稍后再试。"


# 处理微信文本消息
@itchat.msg_register([TEXT])
def handle_text(msg):
    """
    处理接收到的微信文本消息
    :param msg: 消息内容
    :return: 机器人回复
    """
    try:
        # 获取发送者信息
        username = msg['FromUserName']
        content = msg['Text']

        # 获取发送者昵称
        sender = itchat.search_friends(userName=username)
        sender_name = sender['NickName'] if sender else username

        logger.info(f"收到消息 - 发送者: {sender_name}, 内容: {content}")

        # 获取机器人回复
        reply = get_deepseek_response(content, username)

        # 保存消息记录
        save_message(username, sender_name, content, reply)

        # 发送回复
        logger.info(f"回复 {sender_name}: {reply}")
        return reply

    except Exception as e:
        logger.error(f"处理消息失败: {str(e)}")
        return "抱歉，我遇到了一些问题，请稍后再试。"


# Flask路由 - 首页
@app.route('/')
def index():
    """渲染监控页面"""
    return render_template('index.html')


# Flask路由 - 获取聊天记录
@app.route('/messages')
def get_messages():
    """获取所有聊天记录"""
    session = Session()
    messages = session.query(ChatMessage).order_by(ChatMessage.created_at.desc()).all()
    result = [{
        'id': msg.id,
        'sender_name': msg.sender_name,
        'message': msg.message,
        'reply': msg.reply,
        'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for msg in messages]
    session.close()
    return {'messages': result}


# 运行Flask服务器
def run_flask():
    """运行Flask应用"""
    app.config['SECRET_KEY'] = SECRET_KEY  # 从配置文件获取密钥
    app.config['TEMPLATES_AUTO_RELOAD'] = TEMPLATES_AUTO_RELOAD  # 启用模板自动重载
    app.run(
        host=HOST,  # 从配置文件获取地址
        port=PORT,  # 从配置文件获取端口
        debug=False,  # 关闭调试模式
        threaded=True
    )


# 打开监控面板
def open_dashboard():
    """打开监控页面"""
    time.sleep(2)  # 等待Flask服务器启动
    webbrowser.open(f'http://{HOST}:{PORT}')


# 微信登录
def login_wechat():
    """微信登录函数"""
    try:
        # 删除旧的登录状态文件
        if os.path.exists('itchat.pkl'):
            os.remove('itchat.pkl')
            logger.info("删除旧的登录状态文件")

        # 尝试登录
        itchat.auto_login(
            hotReload=False,
            enableCmdQR=0,  # 使用图片二维码
            statusStorageDir='itchat.pkl',
            loginCallback=lambda: logger.info("登录成功"),
            exitCallback=lambda: logger.info("微信退出")
        )

        # 等待登录完成
        time.sleep(3)

        # 验证登录状态
        friends = itchat.get_friends()
        if friends:
            logger.info(f"登录验证成功，共有 {len(friends)} 个好友")
            open_dashboard()
            return True

        logger.error("登录验证失败")
        return False

    except Exception as e:
        logger.error(f"登录过程出错: {str(e)}")
        return False


# 主函数
def main():
    """程序主入口"""
    try:
        # 启动Flask线程
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info("监控服务器已启动")

        # 尝试登录微信
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                if login_wechat():  # 登录成功后会自动打开监控页面
                    # 注册消息处理函数
                    @itchat.msg_register([TEXT])
                    def text_reply(msg):
                        return handle_text(msg)

                    # 运行微信机器人
                    logger.info("开始运行微信机器人...")
                    itchat.run(debug=True)
                    break
                else:
                    retry_count += 1
                    if retry_count < max_retries:
                        logger.info(f"等待 10 秒后进行第 {retry_count + 1} 次重试")
                        time.sleep(10)
            except Exception as e:
                logger.error(f"运行出错: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    logger.info(f"等待 10 秒后进行第 {retry_count + 1} 次重试")
                    time.sleep(10)

        if retry_count >= max_retries:
            logger.error("多次尝试登录失败，程序退出")

    except Exception as e:
        logger.error(f"程序运行错误: {str(e)}")
    finally:
        logger.info("程序退出")


if __name__ == '__main__':
    try:
        # 确保使用最新版本的 itchat-uos
        if not hasattr(itchat, '__version__') or itchat.__version__ < '1.5.0':
            logger.warning("建议更新 itchat-uos 到最新版本")
        main()
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {str(e)}")
