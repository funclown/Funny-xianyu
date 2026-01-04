# 闲鱼爬虫系统 - 快速入门指南

## 🚀 5分钟快速部署

### Windows 用户

```powershell
# 1. 进入项目目录
cd Desktop\闲鱼爬虫测试

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装浏览器驱动
playwright install chromium

# 4. 编辑配置文件
notepad .env
# 修改: RUN_HEADLESS=false (首次运行建议显示浏览器)
# 修改: WEB_USERNAME=admin
# 修改: WEB_PASSWORD=admin123

# 5. 启动服务
python web_server.py

# 6. 访问系统
# 在浏览器打开: http://127.0.0.1:8000
# 使用配置的用户名和密码登录
```

### Linux/macOS 用户

```bash
# 1. 进入项目目录
cd ~/闲鱼爬虫测试

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 安装浏览器驱动
playwright install chromium

# 4. 编辑配置文件
nano .env
# 修改: RUN_HEADLESS=false
# 修改: WEB_USERNAME=admin
# 修改: WEB_PASSWORD=admin123

# 5. 启动服务
python3 web_server.py

# 6. 访问系统
# 在浏览器打开: http://127.0.0.1:8000
```

---

## 📝 基础配置

### 1. 配置闲鱼 Cookie（重要！）

**为什么需要 Cookie？**
- 闲鱼需要登录才能访问商品信息
- Cookie 是保持登录状态的方式

**获取 Cookie 步骤：**

```
1. 在 Chrome 浏览器中打开 https://www.goofish.com 并登录
2. 按 F12 打开开发者工具
3. 点击 "Network"（网络）标签
4. 刷新页面，点击任意请求
5. 在右侧找到 "Request Headers"（请求头）
6. 找到 "Cookie:" 这一行
7. 复制 Cookie 后面的所有内容（很长的一串文本）
```

**配置到系统：**

编辑 `.env` 文件，粘贴复制的 Cookie：

```bash
# 将 Cookie 粘贴到这里
XIANYU_COOKIE=isg=xxxxx; cookie2=xxxxx; unb=xxxxx; ...
```

### 2. 配置通知（可选）

**企业微信机器人：**
```bash
WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的key
```

**其他通知方式请参考 DEPLOYMENT_GUIDE.md**

---

## 🎯 创建第一个监控任务

### Web 界面操作步骤

1. **登录系统**
   - 访问 http://127.0.0.1:8000
   - 输入用户名和密码

2. **创建任务**
   - 点击左上角 "新建任务"
   - 填写任务信息：
     ```
     任务名称: iPhone 13 监控
     搜索关键词: iPhone 13 128G
     最高价格: 3500
     最低价格: 2500
     只看个人: ✅ (勾选，过滤商家)
     最大页数: 3
     ```

3. **启动任务**
   - 在任务列表中找到新建的任务
   - 点击右侧的 "启动" 按钮
   - 查看实时日志，确认任务正常运行

4. **查看结果**
   - 点击 "结果" 标签页
   - 查看爬取到的商品信息
   - 可以下载或删除结果文件

---

## 🔧 常用设置

### 浏览器模式

```bash
# 显示浏览器窗口（首次运行或调试用）
RUN_HEADLESS=false

# 后台运行（生产环境推荐）
RUN_HEADLESS=true
```

### 服务端口

```bash
# 修改 Web 服务端口
SERVER_PORT=8000
```

### 登录凭据

```bash
# 修改 Web 管理界面的用户名和密码
WEB_USERNAME=admin
WEB_PASSWORD=your_secure_password
```

---

## ⚡ 常见问题快速解决

### 问题 1: "playwright 找不到浏览器"

```bash
# 重新安装浏览器驱动
playwright install chromium
```

### 问题 2: "Cookie 无效"

- Cookie 会定期过期，需要重新获取
- 按照 [配置闲鱼 Cookie](#1-配置闲鱼-cookie重要) 的步骤重新获取

### 问题 3: 任务启动但没有数据

```bash
# 1. 检查日志文件
# Windows: 在 Web 界面点击 "查看日志"
# Linux: tail -f logs/task_1_*.log

# 2. 确认 Cookie 配置正确
# 3. 首次运行建议设置 RUN_HEADLESS=false，观察浏览器行为
```

### 问题 4: 端口被占用

```bash
# Windows: 查找占用端口的进程
netstat -ano | findstr :8000
taskkill /F /PID <进程ID>

# Linux/macOS:
lsof -i :8000
kill -9 <进程ID>
```

---

## 📊 系统功能说明

### 任务管理

- **新建任务**: 创建新的监控任务
- **启动/停止**: 控制任务运行
- **编辑**: 修改任务配置
- **删除**: 删除不需要的任务
- **查看日志**: 实时查看任务运行日志

### 结果管理

- **浏览结果**: 查看爬取的商品数据
- **下载结果**: 下载 JSONL 格式的数据文件
- **删除结果**: 清理不需要的结果文件

### 系统设置

- **浏览器模式**: 切换有头/无头模式
- **Cookie 管理**: 更新闲鱼登录 Cookie
- **系统状态**: 查看系统运行状态

---

## 🎓 进阶使用

### AI 智能筛选（可选）

如果配置了 AI API，系统可以自动筛选符合条件的商品：

1. 在创建任务时点击 "配置 AI 提示词"
2. 填写筛选条件，例如：
   ```
   价格在 3000 元以下
   卖家信用等级优秀
   商品描述详细，图片清晰
   手机没有维修记录
   ```
3. 保存提示词
4. 启动任务，系统会自动筛选符合条件的商品

### 定时任务

系统支持定时自动运行任务：

1. 在 Web 界面创建任务
2. 编辑任务，设置定时规则（Cron 表达式）
3. 示例：
   - `0 */2 * * *` - 每 2 小时运行一次
   - `0 9,18 * * *` - 每天 9 点和 18 点运行

---

## 📞 获取帮助

- **完整文档**: 查看 `DEPLOYMENT_GUIDE.md`
- **Cookie 说明**: 查看 `COOKIE使用说明.md`
- **项目总结**: 查看 `PROJECT_SUMMARY.md`

---

## ✅ 部署检查清单

部署新环境时，请确认：

- [ ] Python 3.9+ 已安装
- [ ] 所有依赖已安装 (`pip install -r requirements.txt`)
- [ ] Playwright 浏览器驱动已安装 (`playwright install chromium`)
- [ ] `.env` 文件已配置
- [ ] 闲鱼 Cookie 已配置并有效
- [ ] Web 服务可以正常访问
- [ ] 可以成功登录系统
- [ ] 可以创建和启动任务
- [ ] 可以查看任务日志
- [ ] 通知配置正常（如果使用）

---

**开始使用吧！祝您监控愉快！** 🎉
