# 闲鱼爬虫系统 - 部署指南总览

## 🎯 三种部署方式，任你选择！

### 🥇 方式一：一键安装脚本（最简单！）

**适合人群：** 新手、想要快速体验的用户

**Windows 用户：**
```
1. 双击运行：一键安装.bat
2. 双击运行：启动系统.bat
3. 浏览器自动打开，开始使用！
```

**Linux/macOS 用户：**
```bash
bash 一键安装.sh
bash 启动系统.sh
# 浏览器打开 http://127.0.0.1:8000
```

**优点：**
- ✅ 零技术门槛，双击即用
- ✅ 自动安装所有依赖
- ✅ 智能检测环境
- ✅ 只需配置 Cookie 即可使用

**时间：** 5 分钟完成

---

### 🥈 方式二：Docker 容器（推荐服务器）

**适合人群：** 服务器部署、需要环境隔离的用户

**使用步骤：**
```bash
# 1. 配置 .env 文件
cp .env.example .env
nano .env  # 修改 XIANYU_COOKIE

# 2. 启动容器
docker-compose up -d

# 3. 访问系统
# http://127.0.0.1:8000
```

**优点：**
- ✅ 完全隔离，不影响系统环境
- ✅ 一键启动、停止、更新
- ✅ 跨平台完全一致
- ✅ 方便迁移和备份

**时间：** 3 分钟完成（需要先安装 Docker）

---

### 🥉 方式三：手动部署（适合定制）

**适合人群：** 开发者、需要定制配置的用户

**基本步骤：**
```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 安装浏览器驱动
playwright install chromium

# 3. 配置环境
cp .env.example .env
nano .env

# 4. 启动
python web_server.py
```

**详细文档：** `DEPLOYMENT_GUIDE.md`

**优点：**
- ✅ 完全可控
- ✅ 适合深度定制
- ✅ 学习系统原理

**时间：** 10-15 分钟

---

## 📚 文档导航

| 文档名称 | 用途 | 适合人群 |
|---------|------|---------|
| **部署方式对比.md** | 对比三种部署方式，帮助你选择 | 所有用户 |
| **QUICKSTART.md** | 5 分钟快速入门 | 新手首选 |
| **DEPLOYMENT_GUIDE.md** | 完整部署指南 | 需要详细了解 |
| **COOKIE使用说明.md** | Cookie 获取详细教程 | 所有用户 |
| **PROJECT_SUMMARY.md** | 项目总结和技术文档 | 开发者 |

---

## 🚀 快速开始（推荐流程）

### 第一次使用？

1. **查看部署方式对比**
   ```
   打开：部署方式对比.md
   选择最适合你的方式
   ```

2. **运行一键安装**
   ```powershell
   # Windows
   双击 "一键安装.bat"

   # Linux/macOS
   bash 一键安装.sh
   ```

3. **配置 Cookie（必须）**
   ```powershell
   # 获取 Cookie 教程：COOKIE使用说明.md
   notepad .env  # 粘贴 Cookie
   ```

4. **启动系统**
   ```powershell
   # Windows
   双击 "启动系统.bat"

   # Linux/macOS
   bash 启动系统.sh
   ```

5. **开始使用**
   ```
   访问: http://127.0.0.1:8000
   登录: admin / admin123
   ```

---

## 🎓 部署方案选择指南

### 根据你的情况选择：

#### 我想快速体验，不想折腾
→ **一键安装脚本**
- Windows: 双击 `一键安装.bat`
- Linux/macOS: `bash 一键安装.sh`

#### 我要在服务器上长期运行
→ **Docker 容器**
```bash
docker-compose up -d
```

#### 我是开发者，想要定制
→ **手动部署**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python web_server.py
```

#### 我要在多台电脑上部署
→ **打包脚本 + 一键安装**
```powershell
# 1. 在配置好的电脑上打包
双击 "打包部署.bat"

# 2. 在新电脑上
双击 "一键安装.bat"
```

---

## 📋 必要配置

无论使用哪种部署方式，都需要配置：

### 1. 闲鱼 Cookie（必须！）

**为什么需要？**
- 闲鱼需要登录才能访问商品
- Cookie 是保持登录状态的凭证

**如何获取？**
```
1. 浏览器打开 https://www.goofish.com 并登录
2. 按 F12 打开开发者工具
3. 点击 "Network" 标签
4. 刷新页面，找到任意请求
5. 在 "Request Headers" 中复制 Cookie 值
6. 粘贴到 .env 文件的 XIANYU_COOKIE
```

详细教程：`COOKIE使用说明.md`

### 2. 浏览器模式（可选）

```bash
# 显示浏览器（首次运行建议）
RUN_HEADLESS=false

# 后台运行（生产环境推荐）
RUN_HEADLESS=true
```

### 3. 登录凭据（可选修改）

```bash
WEB_USERNAME=admin
WEB_PASSWORD=admin123
```

---

## 🛠️ 实用工具脚本

### Windows 脚本
| 脚本名称 | 功能 |
|---------|------|
| `一键安装.bat` | 自动安装所有依赖 |
| `启动系统.bat` | 启动 Web 服务 |
| `停止系统.bat` | 停止 Web 服务 |
| `打包部署.bat` | 打包整个项目用于部署 |

### Linux/macOS 脚本
| 脚本名称 | 功能 |
|---------|------|
| `一键安装.sh` | 自动安装所有依赖 |
| `启动系统.sh` | 启动 Web 服务 |
| `停止系统.sh` | 停止 Web 服务 |
| `打包部署.sh` | 打包整个项目用于部署 |

### Docker 配置
| 文件名称 | 功能 |
|---------|------|
| `Dockerfile` | Docker 镜像构建文件 |
| `docker-compose.yml` | Docker Compose 配置 |

---

## ⚡ 常见问题速查

### Q: 如何选择部署方式？
**A:** 参考 `部署方式对比.md`，新手推荐一键安装

### Q: 一键安装失败怎么办？
**A:**
1. 确认 Python 已安装
2. 以管理员身份运行
3. 检查网络连接
4. 查看 `DEPLOYMENT_GUIDE.md` 的[常见问题]章节

### Q: Cookie 配置后还是无法登录？
**A:**
1. 重新获取 Cookie（可能过期）
2. 确认复制了完整内容
3. 设置 `RUN_HEADLESS=false` 观察

### Q: 端口 8000 被占用？
**A:**
1. 运行 "停止系统" 脚本
2. 或修改 .env: `SERVER_PORT=8001`

### Q: 如何远程访问？
**A:**
1. 使用 Docker + 端口映射
2. 或配置内网穿透（frp/ngrok）
3. 参考 `DEPLOYMENT_GUIDE.md` 的[端口转发]章节

---

## 📞 获取帮助

遇到问题？按以下顺序查找：

1. **快速问题** → 查看本文档的[常见问题速查]
2. **详细说明** → 查看 `QUICKSTART.md`
3. **完整文档** → 查看 `DEPLOYMENT_GUIDE.md`
4. **Cookie 问题** → 查看 `COOKIE使用说明.md`
5. **技术细节** → 查看 `PROJECT_SUMMARY.md`

---

## 🎉 开始部署吧！

选择你的方式，立即开始：

### 新手推荐（最简单）
```powershell
# Windows
双击 "一键安装.bat" → 双击 "启动系统.bat" → 完成！

# Linux/macOS
bash 一键安装.sh → bash 启动系统.sh → 完成！
```

### 服务器推荐（最稳定）
```bash
docker-compose up -d → 完成！
```

---

**祝你部署顺利！🚀**

如有问题，请参考详细文档或提交 Issue。
