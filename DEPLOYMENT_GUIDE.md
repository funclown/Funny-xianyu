# 闲鱼爬虫系统部署指南

本文档提供详细的跨平台部署指南，帮助你在新电脑上快速部署和运行闲鱼爬虫管理系统。

## 📋 目录

- [系统要求](#系统要求)
- [快速部署（Windows）](#快速部署windows)
- [快速部署（Linux/macOS）](#快速部署linuxmacos)
- [详细配置说明](#详细配置说明)
- [首次运行设置](#首次运行设置)
- [常见问题](#常见问题)
- [维护和更新](#维护和更新)

---

## 系统要求

### 必需软件

- **Python**: 3.9 或更高版本
- **浏览器**: Google Chrome 或 Microsoft Edge
- **操作系统**: Windows 10/11, macOS 10.15+, 或 Linux (Ubuntu 20.04+)
- **内存**: 至少 4GB RAM
- **磁盘空间**: 至少 2GB 可用空间

### 可选软件

- Git（用于版本控制）
- 文本编辑器（VS Code, PyCharm 等）

---

## 快速部署（Windows）

### 方法一：完整打包部署（推荐）

#### 1. 准备部署包

在原电脑上将以下文件和文件夹打包：

```
闲鱼爬虫测试/
├── src/                    # 源代码目录
├── templates/              # HTML 模板
├── static/                 # 静态文件
├── prompts/                # AI 提示词文件
├── logs/                   # 日志文件（可选）
├── results/                # 爬取结果（可选）
├── main.py                 # 主程序
├── spider_v2.py           # 爬虫脚本
├── web_server.py          # Web 服务器
├── requirements.txt       # Python 依赖
├── .env                   # 环境配置
├── .env.example          # 配置示例
├── config.json           # 任务配置
├── xianyu_state.json     # 登录状态（如有）
└── *.md                  # 文档文件
```

**打包命令**（在 PowerShell 中）：
```powershell
# 压缩整个项目文件夹
Compress-Archive -Path "闲鱼爬虫测试\*" -DestinationPath "闲鱼爬虫部署包.zip"
```

#### 2. 在新电脑上解压

```powershell
# 解压到目标位置
Expand-Archive -Path "闲鱼爬虫部署包.zip" -DestinationPath "C:\"
```

#### 3. 安装 Python

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载 Python 3.9 或更高版本
3. 安装时**务必勾选 "Add Python to PATH"**

验证安装：
```powershell
python --version
# 应该显示: Python 3.x.x
```

#### 4. 安装依赖

打开 PowerShell，进入项目目录：

```powershell
cd C:\闲鱼爬虫测试

# 安装 Python 依赖包
pip install -r requirements.txt

# 安装 Playwright 浏览器驱动
playwright install chromium
```

#### 5. 配置环境变量

编辑 `.env` 文件，根据需要修改配置：

```bash
# 最小化配置（必须）
RUN_HEADLESS=false          # 首次运行建议 false，方便手动登录
WEB_USERNAME=admin          # Web 管理界面用户名
WEB_PASSWORD=admin123       # Web 管理界面密码

# 可选：配置通知
WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的key
```

#### 6. 启动系统

```powershell
# 启动 Web 服务器
python web_server.py
```

访问 `http://127.0.0.1:8000`，使用配置的用户名和密码登录。

---

## 快速部署（Linux/macOS）

### 1. 安装系统依赖

**Ubuntu/Debian:**
```bash
# 更新包列表
sudo apt update

# 安装 Python 和依赖
sudo apt install -y python3 python3-pip python3-venv

# 安装 Chrome 和依赖
sudo apt install -y chromium-browser
```

**macOS:**
```bash
# 使用 Homebrew 安装
brew install python@3.9 chromium

# 或者安装 Google Chrome
brew install --cask google-chrome
```

### 2. 克隆或解压项目

```bash
# 如果使用 Git
git clone <你的仓库地址> 闲鱼爬虫测试
cd 闲鱼爬虫测试

# 或解压压缩包
unzip 闲鱼爬虫部署包.zip -d ~/闲鱼爬虫测试
cd ~/闲鱼爬虫测试
```

### 3. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux:
source venv/bin/activate
# macOS:
source venv/bin/activate

# 升级 pip
pip install --upgrade pip
```

### 4. 安装依赖

```bash
# 安装 Python 包
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 5. 配置和启动

```bash
# 复制并编辑配置文件
cp .env.example .env
nano .env  # 或使用其他编辑器

# 启动 Web 服务器
python web_server.py
```

后台运行（使用 nohup）:
```bash
nohup python web_server.py > server.log 2>&1 &
```

使用 systemd 服务（推荐）:
```bash
# 创建服务文件
sudo nano /etc/systemd/system/xianyu-crawler.service
```

添加以下内容：
```ini
[Unit]
Description=闲鱼爬虫 Web 服务
After=network.target

[Service]
Type=simple
User=你的用户名
WorkingDirectory=/home/你的用户名/闲鱼爬虫测试
ExecStart=/home/你的用户名/闲鱼爬虫测试/venv/bin/python web_server.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable xianyu-crawler
sudo systemctl start xianyu-crawler
sudo systemctl status xianyu-crawler
```

---

## 详细配置说明

### 1. Cookie 配置（推荐）

Cookie 登录是最简单、最稳定的登录方式。

**获取 Cookie 步骤：**

1. 在 Chrome 浏览器中登录闲鱼：https://www.goofish.com
2. 按 `F12` 打开开发者工具
3. 切换到 "Network"（网络）标签
4. 刷新页面，点击任意请求
5. 在右侧 "Request Headers"（请求头）中找到 `Cookie:`
6. 复制整个 Cookie 值（很长的一串）

**配置到 .env 文件：**

```bash
# 将复制的 Cookie 粘贴到这里（去掉 "Cookie: " 前缀）
XIANYU_COOKIE=isg=xxxxx; cookie2=xxxxx; sgcookie=xxxxx; unb=xxxxx; uc1=xxxxx; cna=xxxxx; ...
```

### 2. 浏览器模式配置

```bash
# 无头模式（后台运行，不显示浏览器窗口）
RUN_HEADLESS=true

# 有头模式（显示浏览器窗口，首次登录或调试用）
RUN_HEADLESS=false
```

### 3. Web 服务配置

```bash
# 服务端口
SERVER_PORT=8000

# 登录凭据
WEB_USERNAME=admin
WEB_PASSWORD=admin123
```

### 4. 通知配置

支持多种通知方式，根据需要配置：

```bash
# 企业微信机器人
WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的key

# Telegram
TELEGRAM_BOT_TOKEN=你的bot_token
TELEGRAM_CHAT_ID=你的chat_id

# Bark (iOS)
BARK_URL=https://api.day.app/你的key

# ntfy
NTFY_TOPIC_URL=https://ntfy.sh/你的topic
```

### 5. AI 配置（可选）

如果需要使用 AI 分析功能，需要在 `.env` 中配置：

```bash
# OpenAI 格式 API
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.openai.com/v1  # 或其他兼容的 API

# 或者使用其他兼容 OpenAI 格式的 API
OPENAI_BASE_URL=https://your-custom-api.com/v1
```

---

## 首次运行设置

### 步骤 1: 验证环境

```bash
# 检查 Python 版本
python --version

# 检查已安装的包
pip list | grep playwright
pip list | grep fastapi
```

### 步骤 2: 测试浏览器驱动

```bash
# 测试 Playwright
python -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

### 步骤 3: 启动 Web 服务

```bash
python web_server.py
```

看到以下输出表示启动成功：

```
==========================================
  闲鱼爬虫监控系统 Web 服务器
==========================================

访问地址: http://127.0.0.1:8000
用户名: admin
密码: admin123

按 Ctrl+C 停止服务器
```

### 步骤 4: 首次登录

1. 在浏览器中访问 `http://127.0.0.1:8000`
2. 输入配置的用户名和密码
3. 首次运行建议设置 `RUN_HEADLESS=false`，方便观察浏览器行为

### 步骤 5: 创建任务

在 Web 界面中：

1. 点击 "新建任务"
2. 填写任务信息：
   - 任务名称：例如 "iPhone 监控"
   - 搜索关键词：例如 "iPhone 13 Pro"
   - 最高价格：可选
   - 最低价格：可选
   - 只看个人：勾选（过滤商家）
3. 配置 AI 提示词（可选）
4. 保存任务

### 步骤 6: 启动任务

1. 在任务列表中找到新建的任务
2. 点击 "启动" 按钮
3. 查看实时日志确认运行正常

---

## 常见问题

### Q1: 提示 "playwright 找不到浏览器"

**解决方案：**

```bash
# 重新安装浏览器驱动
playwright install chromium

# 如果还是不行，安装所有依赖
playwright install --with-deps chromium
```

### Q2: 提示 "Cookie 无效或已过期"

**解决方案：**

Cookie 会定期过期，需要重新获取：

1. 在浏览器中重新登录闲鱼
2. 按照 [Cookie 配置](#1-cookie-配置推荐) 的步骤重新获取
3. 更新 `.env` 文件中的 `XIANYU_COOKIE`
4. 重启 Web 服务

### Q3: 任务启动后没有反应

**排查步骤：**

1. 检查日志文件：
   ```bash
   # Linux/macOS
   tail -f logs/task_1_*.log

   # Windows PowerShell
   Get-Content logs\task_1_*.log -Wait
   ```

2. 检查浏览器模式：
   - 首次运行建议使用 `RUN_HEADLESS=false`
   - 观察浏览器是否正常打开和操作

3. 检查网络连接：
   - 确保能访问 www.goofish.com
   - 检查代理设置

### Q4: Web 服务无法访问

**解决方案：**

1. 检查端口是否被占用：
   ```bash
   # Windows
   netstat -ano | findstr :8000

   # Linux/macOS
   lsof -i :8000
   ```

2. 更换端口：
   ```bash
   # 修改 .env
   SERVER_PORT=8080
   ```

3. 检查防火墙设置：
   ```bash
   # Windows 允许端口
   netsh advfirewall firewall add rule name="Allow 8000" dir=in action=allow protocol=TCP localport=8000

   # Linux
   sudo ufw allow 8000
   ```

### Q5: 依赖安装失败

**解决方案：**

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者分别安装
pip install playwright==1.48.0
pip install python-dotenv==1.0.0
pip install fastapi==0.115.0
pip install uvicorn[standard]==0.32.0
```

### Q6: Linux 上提示 "DISPLAY" 错误

**解决方案：**

```bash
# 安装虚拟显示
sudo apt install xvfb

# 使用 xvfb-run 运行
xvfb-run python web_server.py
```

或者直接使用无头模式：
```bash
# 修改 .env
RUN_HEADLESS=true
```

---

## 维护和更新

### 日志管理

日志文件会不断增长，需要定期清理：

```bash
# Linux/macOS - 清理 7 天前的日志
find logs/ -name "*.log" -mtime +7 -delete

# Windows PowerShell
Get-ChildItem logs\ -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | Remove-Item
```

### 数据备份

定期备份重要文件：

```bash
# 备份配置和结果
tar -czf backup_$(date +%Y%m%d).tar.gz \
    .env \
    config.json \
    prompts/ \
    results/ \
    xianyu_state.json
```

### 更新项目

如果使用 Git：

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 更新浏览器驱动
playwright install chromium --with-deps
```

### 性能优化

1. **限制并发任务数**：同时运行过多任务可能导致性能问题
2. **定期清理日志**：避免磁盘空间不足
3. **使用无头模式**：生产环境建议 `RUN_HEADLESS=true`
4. **监控资源使用**：
   ```bash
   # Linux
   htop

   # Windows
   taskmgr
   ```

---

## 端口转发和远程访问

### 内网穿透（可选）

如果需要在外网访问：

#### 使用 frp

**服务端配置 (frps.ini):**
```ini
[common]
bind_port = 7000
vhost_http_port = 8080
```

**客户端配置 (frpc.ini):**
```ini
[common]
server_addr = 你的服务器IP
server_port = 7000

[web]
type = http
local_port = 8000
custom_domains = 你的域名.com
```

#### 使用 ngrok（测试用）

```bash
# 下载 ngrok
# 启动隧道
ngrok http 8000
```

### 安全建议

1. **修改默认密码**：更改 `.env` 中的 `WEB_USERNAME` 和 `WEB_PASSWORD`
2. **使用 HTTPS**：配置反向代理（Nginx/Apache）并启用 SSL
3. **限制访问**：配置防火墙规则，只允许可信 IP 访问
4. **定期更新**：保持依赖包和系统更新

---

## 联系支持

如遇到问题，请参考：

- 项目文档：`README.md`
- Cookie 使用说明：`COOKIE使用说明.md`
- 项目总结：`PROJECT_SUMMARY.md`
- 提交 Issue：在项目仓库提交问题

---

**祝部署顺利！**
