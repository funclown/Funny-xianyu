# 闲鱼爬虫管理系统 - 完整版

一个功能完整的闲鱼爬虫系统，具备强大的爬虫能力、多渠道通知系统、Web可视化管理界面和灵活的任务调度功能。

## ✨ 核心功能

### 1. 强大的爬虫能力
- ✅ 商品搜索和筛选（关键词、价格区间、个人闲置）
- ✅ 商品详细信息采集
- ✅ 卖家完整信息采集（包括信用评价、历史商品）
- ✅ 自动去重机制
- ✅ 数据保存为JSONL格式
- ✅ 反爬虫策略（随机延迟、真实浏览器行为）
- ✅ 支持登录状态，可爬取更完整的数据

### 2. 多渠道通知系统
支持8种通知渠道，可同时配置多个：
- 📱 **企业微信机器人** - 支持Markdown格式
- 📱 **钉钉机器人** - 支持Markdown格式
- 📱 **飞书机器人** - 富文本卡片消息
- 🍎 **Bark** - iOS推送通知
- 📢 **Gotify** - 自托管通知服务
- ✈️ **Telegram** - 机器人推送
- 🔔 **ntfy.sh** - 简单HTTP推送
- 🔗 **通用Webhook** - 支持自定义Webhook

### 3. Web可视化管理界面
- 🎨 现代化的响应式设计
- 📊 任务管理（创建、编辑、删除、启动）
- 📈 爬取结果查看和浏览
- 🔧 系统状态监控
- 🔒 Basic认证保护

### 4. 灵活的任务调度
- ⏰ 支持Cron表达式定时执行
- 🔄 后台独立进程运行
- 📝 任务状态实时更新

## 📁 项目结构

```
闲鱼爬虫测试/
├── src/
│   ├── __init__.py
│   ├── config.py           # 配置管理
│   ├── scraper.py          # 核心爬虫逻辑
│   ├── parsers.py          # 数据解析模块
│   ├── utils.py            # 工具函数
│   └── notification.py     # 通知模块
├── templates/
│   └── index.html          # Web管理界面
├── jsonl/                   # 数据输出目录
├── logs/                    # 日志目录
├── images/                  # 图片临时目录
├── main.py                  # 命令行入口
├── web_server.py            # Web服务器
├── test_basic.py            # 测试脚本
├── .env                     # 环境配置
├── .env.example             # 环境配置示例
├── requirements.txt         # 依赖包列表
├── tasks.json               # 任务存储文件
├── README.md                # 项目说明
└── PROJECT_SUMMARY.md       # 开发指南
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd "C:\Users\Administrator\Desktop\闲鱼爬虫测试"
pip install -r requirements.txt
playwright install chromium
```

如果要使用 Edge 浏览器，还需安装：

```bash
playwright install msedge
```

### 2. 配置环境

复制环境变量示例文件：

```bash
copy .env.example .env
```

根据需要修改 `.env` 文件中的配置，特别是通知配置：

```env
# 企业微信通知
WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key

# 钉钉通知
DINGTALK_BOT_URL=https://oapi.dingtalk.com/robot/send?access_token=your-token

# 飞书通知
FEISHU_BOT_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your-hook
```

### 3. 准备登录状态（重要）

为了让爬虫能够访问需要登录才能看到的数据，需要提供登录状态文件。

#### 方法一：使用 Chrome 扩展（推荐）

1. 在 Chrome 浏览器中安装 [闲鱼登录状态提取扩展](https://chromewebstore.google.com/detail/xianyu-login-state-extrac/eidlpfjiodpigmfcahkmlenhppfklcoa)
2. 打开并登录闲鱼官网 (https://www.goofish.com)
3. 登录成功后，点击浏览器工具栏中的扩展图标
4. 点击"提取登录状态"按钮
5. 将复制的内容保存为 `xianyu_state.json` 文件，放在项目根目录

#### 方法二：从原项目复制

如果你在 `ai-goofish-monitor-master` 项目中已经有 `xianyu_state.json` 文件，直接复制到本项目根目录即可。

### 4. 启动Web服务

```bash
python web_server.py
```

然后在浏览器中访问: http://127.0.0.1:8000

**默认登录凭据：**
- 用户名：`admin`
- 密码：`admin123`

⚠️ **重要：生产环境请务必修改默认密码！**

### 5. 使用Web界面

1. **创建任务**
   - 点击"任务管理"标签
   - 点击"+ 创建新任务"按钮
   - 填写任务信息（任务名称、关键词、页数等）
   - 点击"创建"

2. **启动任务**
   - 在任务列表中找到要运行的任务
   - 点击"启动"按钮
   - 任务将在后台独立进程运行

3. **查看结果**
   - 点击"爬取结果"标签
   - 查看所有已爬取的数据
   - 点击"查看"按钮查看详细数据

4. **系统状态**
   - 点击"系统状态"标签
   - 查看系统整体运行状态

### 6. 使用命令行

```bash
# 交互式运行
python main.py

# 指定任务运行（需要先在Web界面创建任务）
python main.py --task-id <task_id>
```

## 📝 配置说明

### 环境变量 (.env)

#### 浏览器配置
| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `RUN_HEADLESS` | 是否无头模式运行 | `true` |
| `LOGIN_IS_EDGE` | 是否使用Edge浏览器 | `false` |

#### Web服务配置
| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SERVER_PORT` | Web服务端口 | `8000` |
| `WEB_USERNAME` | Web界面用户名 | `admin` |
| `WEB_PASSWORD` | Web界面密码 | `admin123` |

#### 通知配置

支持同时配置多个通知渠道，所有渠道都是可选的：

**企业微信：**
```env
WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
```

**钉钉：**
```env
DINGTALK_BOT_URL=https://oapi.dingtalk.com/robot/send?access_token=your-token
```

**飞书：**
```env
FEISHU_BOT_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your-hook
```

**Bark：**
```env
BARK_URL=https://api.day.app/your_key
```

**Gotify：**
```env
GOTIFY_URL=https://push.example.de
GOTIFY_TOKEN=your-token
```

**Telegram：**
```env
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

**ntfy.sh：**
```env
NTFY_TOPIC_URL=https://ntfy.sh/your-topic
```

**通用Webhook：**
```env
WEBHOOK_URL=https://your-webhook-url
WEBHOOK_METHOD=POST
WEBHOOK_CONTENT_TYPE=JSON
```

## 🔔 通知功能

通知会在以下情况触发：

1. **发现新商品时** - 每当爬虫发现符合条件的新商品时
2. **任务完成时** - 任务执行完毕后发送汇总通知

通知内容包含：
- 商品标题
- 当前价格
- 推荐原因/说明
- 商品链接（支持PC端和手机端）

## 📊 数据格式

爬取的数据保存在 `jsonl/` 目录下，文件名格式为 `{关键词}_full_data.jsonl`。

每条记录为一个 JSON 对象，包含：

```json
{
  "爬取时间": "2025-12-23T12:00:00",
  "搜索关键字": "iPhone 15",
  "商品信息": {
    "商品标题": "...",
    "当前售价": "¥4500",
    "商品图片列表": [...],
    "商品链接": "...",
    "想要人数": 10,
    "浏览量": 1523,
    ...
  },
  "卖家信息": {
    "卖家昵称": "...",
    "卖家信用等级": "...",
    "卖家芝麻信用": "...",
    "卖家在售/已售商品数": "...",
    "卖家收到的评价列表": [...],
    "卖家发布的商品列表": [...],
    ...
  }
}
```

## ⚠️ 注意事项

1. **反爬虫策略**：程序内置了多种反爬虫策略（随机延迟、真实用户行为模拟等），但仍建议：
   - 不要过于频繁地运行爬虫
   - 如果遇到验证码，可以设置 `RUN_HEADLESS=false` 手动处理
   - 定期更新登录状态文件

2. **法律合规**：
   - 仅用于个人学习和研究
   - 遵守闲鱼的用户协议
   - 不要用于商业用途或非法目的

3. **数据使用**：
   - 爬取的数据仅供个人分析使用
   - 不要恶意攻击或干扰闲鱼服务器

4. **安全性**：
   - 生产环境务必修改默认密码
   - 妥善保管登录状态文件，不要泄露
   - 使用HTTPS协议部署（生产环境）

## 🛠️ 故障排查

### 问题：无法启动浏览器

确保已安装 Playwright 浏览器：

```bash
playwright install chromium
```

### 问题：登录失败

检查 `xianyu_state.json` 文件是否存在且有效。可以尝试重新生成该文件。

### 问题：遇到验证码

1. 设置 `RUN_HEADLESS=false` 以非无头模式运行
2. 手动完成验证后继续

### 问题：通知未发送

检查 `.env` 文件中的通知配置是否正确，并测试通知渠道是否可用。

### 问题：Web界面无法访问

1. 检查端口 8000 是否被占用
2. 检查防火墙设置
3. 查看控制台错误信息

## 🆚 与原项目的对比

| 特性 | 原项目 | 新项目 |
|------|--------|--------|
| 核心爬虫功能 | ✅ | ✅ |
| AI分析和推荐 | ✅ | ❌ 已移除 |
| 通知系统 | ✅ 基础版 | ✅ 增强版（新增钉钉、飞书） |
| Web管理界面 | ✅ 完整版 | ✅ 简化版 |
| 任务调度 | ✅ 完整版 | ⚠️ 基础版（需完善） |
| 代码复杂度 | 高 | 中 |
| 学习曲线 | 陡峭 | 平缓 |
| 适用场景 | 生产监控 | 学习研究、轻度使用 |

## 📚 开发文档

详细的开发指南请参考：[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 🙏 致谢

本项目基于 [ai-goofish-monitor](https://github.com/Usagi-org/ai-goofish-monitor) 项目开发，感谢原作者的贡献。

## 📄 许可证

本项目遵循原项目的 MIT 许可证。

---

**祝你使用愉快！** 🎉

如有问题，请查看 `PROJECT_SUMMARY.md` 获取更多技术细节。
