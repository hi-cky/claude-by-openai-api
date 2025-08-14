<p align="center">
  <a href="README.md">English</a> | <strong>中文</strong>
</p>

# Claude OpenAI代理服务

用OpenAI接口的方式使用Claude模型

## 🗂️ 项目说明
这是一个FastAPI服务，把OpenAI的请求格式转译成Claude格式，让你不用改现有使用OpenAI的代码，直接用Claude的接口。

## 🚀 启动

```bash
# 克隆/下载后进入目录
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的配置

# 启动
python main.py

# 访问 http://localhost:8000
```

## ⚙️ 环境变量

```bash
# 二选一
ANTHROPIC_API_KEY=你的API密钥
ANTHROPIC_AUTH_TOKEN=你的认证令牌  

# 模型
DEFAULT_MODEL=你的模型名称

# 其他
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

## 🔧 用到的项目
- **FastAPI** - Web框架
- **Anthropic SDK** - Claude官方Python包
- **Uvicorn** - ASGI服务器
- **Pydantic** - 数据验证

## 📊 用法
启动后访问 http://localhost:8000/docs 查看API文档