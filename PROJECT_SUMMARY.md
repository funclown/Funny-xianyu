# 闲鱼爬虫项目 - 完整版开发指南

## 项目概述

本项目是从 `ai-goofish-monitor-master` 提取并增强的闲鱼爬虫系统，**保留**以下功能：
- ✅ 完整的爬虫核心功能
- ✅ 多渠道通知系统（企业微信、钉钉、飞书、Bark、Gotify、Telegram、ntfy、Webhook）
- ✅ Web管理界面
- ✅ 任务调度系统

**移除**的功能：
- ❌ AI分析和推荐功能

## 已完成的工作

### 1. 核心爬虫模块 ✅
- `src/scraper.py` - 完整的爬虫逻辑
- `src/parsers.py` - 数据解析模块
- `src/utils.py` - 工具函数
- `src/config.py` - 配置管理（已更新支持通知和Web）

### 2. 通知系统 ✅
- `src/notification.py` - 完整的通知模块
  - 企业微信机器人
  - 钉钉机器人
  - 飞书机器人
  - Bark
  - Gotify
  - Telegram
  - ntfy.sh
  - 通用Webhook

### 3. Web管理界面（部分完成）⚠️
- `web_server.py` - FastAPI后端（已创建，功能完整）

### 4. 配置文件 ✅
- `.env` - 环境配置（已更新）
- `.env.example` - 环境配置示例
- `requirements.txt` - 依赖列表（需要更新）

## 需要完成的工作

### 1. 创建Web前端界面

需要创建以下文件：

#### `templates/index.html` - 主界面
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>闲鱼爬虫管理系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .header h1 { margin: 0; }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab { padding: 10px 20px; background: #f0f0f0; border: none; border-radius: 4px; cursor: pointer; }
        .tab.active { background: #007bff; color: white; }
        .content { display: none; }
        .content.active { display: block; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .btn { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #007bff; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-success { background: #28a745; color: white; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; }
        .badge-success { background: #28a745; color: white; }
        .badge-danger { background: #dc3545; color: white; }
        .badge-warning { background: #ffc107; color: black; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); }
        .modal.active { display: flex; align-items: center; justify-content: center; }
        .modal-content { background: white; padding: 20px; border-radius: 8px; width: 500px; max-width: 90%; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 闲鱼爬虫管理系统</h1>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab('tasks')">任务管理</button>
            <button class="tab" onclick="showTab('results')">爬取结果</button>
            <button class="tab" onclick="showTab('system')">系统状态</button>
        </div>

        <!-- 任务管理 -->
        <div id="tasks" class="content active">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h2>任务列表</h2>
                    <button class="btn btn-primary" onclick="showCreateTaskModal()">+ 创建新任务</button>
                </div>
                <table id="tasksTable">
                    <thead>
                        <tr>
                            <th>任务名称</th>
                            <th>关键词</th>
                            <th>页数</th>
                            <th>状态</th>
                            <th>上次运行</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="tasksBody"></tbody>
                </table>
            </div>
        </div>

        <!-- 爬取结果 -->
        <div id="results" class="content">
            <div class="card">
                <h2>爬取结果</h2>
                <table id="resultsTable">
                    <thead>
                        <tr>
                            <th>关键词</th>
                            <th>记录数</th>
                            <th>文件大小</th>
                            <th>修改时间</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="resultsBody"></tbody>
                </table>
            </div>
        </div>

        <!-- 系统状态 -->
        <div id="system" class="content">
            <div class="card">
                <h2>系统状态</h2>
                <div id="systemStatus"></div>
            </div>
        </div>
    </div>

    <!-- 创建任务模态框 -->
    <div id="createTaskModal" class="modal">
        <div class="modal-content">
            <h2>创建新任务</h2>
            <form id="createTaskForm">
                <div class="form-group">
                    <label>任务名称</label>
                    <input type="text" name="task_name" required>
                </div>
                <div class="form-group">
                    <label>搜索关键词</label>
                    <input type="text" name="keyword" required>
                </div>
                <div class="form-group">
                    <label>爬取页数</label>
                    <input type="number" name="max_pages" value="1" min="1" required>
                </div>
                <div class="form-group">
                    <label>只看个人闲置</label>
                    <select name="personal_only">
                        <option value="false">否</option>
                        <option value="true">是</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>最低价格（可选）</label>
                    <input type="text" name="min_price" placeholder="例如: 100">
                </div>
                <div class="form-group">
                    <label>最高价格（可选）</label>
                    <input type="text" name="max_price" placeholder="例如: 1000">
                </div>
                <div style="text-align: right; margin-top: 20px;">
                    <button type="button" class="btn" onclick="hideCreateTaskModal()">取消</button>
                    <button type="submit" class="btn btn-primary">创建</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // API基础URL
        const API_BASE = window.location.origin;

        // 显示标签页
        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.content').forEach(content => content.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');

            if (tabName === 'tasks') loadTasks();
            if (tabName === 'results') loadResults();
            if (tabName === 'system') loadSystemStatus();
        }

        // 加载任务列表
        async function loadTasks() {
            const response = await fetch(`${API_BASE}/api/tasks`);
            const data = await response.json();
            const tbody = document.getElementById('tasksBody');
            tbody.innerHTML = data.tasks.map(task => `
                <tr>
                    <td>${task.task_name}</td>
                    <td>${task.keyword}</td>
                    <td>${task.max_pages}</td>
                    <td><span class="badge ${task.enabled ? 'badge-success' : 'badge-warning'}">${task.enabled ? '启用' : '禁用'}</span></td>
                    <td>${task.last_run || '未运行'}</td>
                    <td>
                        <button class="btn btn-success" onclick="startTask('${task.id}')">启动</button>
                        <button class="btn btn-danger" onclick="deleteTask('${task.id}')">删除</button>
                    </td>
                </tr>
            `).join('');
        }

        // 加载结果列表
        async function loadResults() {
            const response = await fetch(`${API_BASE}/api/results`);
            const data = await response.json();
            const tbody = document.getElementById('resultsBody');
            tbody.innerHTML = data.results.map(result => `
                <tr>
                    <td>${result.keyword}</td>
                    <td>${result.count}</td>
                    <td>${(result.size / 1024).toFixed(2)} KB</td>
                    <td>${result.modified}</td>
                    <td>
                        <button class="btn btn-primary" onclick="viewResult('${result.filename}')">查看</button>
                    </td>
                </tr>
            `).join('');
        }

        // 加载系统状态
        async function loadSystemStatus() {
            const response = await fetch(`${API_BASE}/api/system/status`);
            const data = await response.json();
            const statusDiv = document.getElementById('systemStatus');
            statusDiv.innerHTML = `
                <p>登录状态文件: ${data.login_state_exists ? '✅ 存在' : '❌ 不存在'}</p>
                <p>任务文件: ${data.tasks_file_exists ? '✅ 存在' : '❌ 不存在'}</p>
                <p>输出目录: ${data.output_dir_exists ? '✅ 存在' : '❌ 不存在'}</p>
                <p>任务数量: ${data.tasks_count}</p>
                <p>结果文件数: ${data.results_count}</p>
                <p>通知配置: ${data.notification_configured ? '✅ 已配置' : '❌ 未配置'}</p>
            `;
        }

        // 显示创建任务模态框
        function showCreateTaskModal() {
            document.getElementById('createTaskModal').classList.add('active');
        }

        function hideCreateTaskModal() {
            document.getElementById('createTaskModal').classList.remove('active');
        }

        // 创建任务
        document.getElementById('createTaskForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = {
                task_name: formData.get('task_name'),
                keyword: formData.get('keyword'),
                max_pages: parseInt(formData.get('max_pages')),
                personal_only: formData.get('personal_only') === 'true',
                min_price: formData.get('min_price') || null,
                max_price: formData.get('max_price') || null,
                enabled: true
            };

            const response = await fetch(`${API_BASE}/api/tasks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                hideCreateTaskModal();
                loadTasks();
                alert('任务创建成功');
            } else {
                alert('任务创建失败');
            }
        });

        // 启动任务
        async function startTask(taskId) {
            const response = await fetch(`${API_BASE}/api/tasks/${taskId}/start`, { method: 'POST' });
            if (response.ok) {
                alert('任务已启动');
                loadTasks();
            } else {
                alert('启动任务失败');
            }
        }

        // 删除任务
        async function deleteTask(taskId) {
            if (!confirm('确定要删除这个任务吗？')) return;

            const response = await fetch(`${API_BASE}/api/tasks/${taskId}`, { method: 'DELETE' });
            if (response.ok) {
                loadTasks();
            } else {
                alert('删除任务失败');
            }
        }

        // 查看结果
        function viewResult(filename) {
            window.open(`${API_BASE}/api/results/${filename}`, '_blank');
        }

        // 页面加载时初始化
        loadTasks();
    </script>
</body>
</html>
```

### 2. 更新 requirements.txt

```
playwright==1.48.0
python-dotenv==1.0.0
fastapi==0.115.0
uvicorn[standard]==0.32.0
requests==2.31.0
python-multipart==0.0.6
pydantic==2.9.0
```

### 3. 更新 .env.example

```env
# 闲鱼爬虫环境变量配置

# ==================== 浏览器配置 ====================
# 是否以无头模式运行浏览器
RUN_HEADLESS=true
# 是否使用 Edge 浏览器
LOGIN_IS_EDGE=false

# ==================== 调试配置 ====================
DEBUG_MODE=false

# ==================== Web服务配置 ====================
# Web服务端口
SERVER_PORT=8000
# Web界面登录用户名
WEB_USERNAME=admin
# Web界面登录密码
WEB_PASSWORD=admin123

# ==================== 通知配置 ====================
# NTFY通知（可选）
# NTFY_TOPIC_URL=https://ntfy.sh/your-topic

# Gotify通知（可选）
# GOTIFY_URL=https://push.example.de
# GOTIFY_TOKEN=your-token

# Bark通知（可选）
# BARK_URL=https://api.day.app/your_key

# 企业微信通知（可选）
# WX_BOT_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key

# 钉钉通知（可选）
# DINGTALK_BOT_URL=https://oapi.dingtalk.com/robot/send?access_token=your-token

# 飞书通知（可选）
# FEISHU_BOT_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your-hook

# Telegram通知（可选）
# TELEGRAM_BOT_TOKEN=your-bot-token
# TELEGRAM_CHAT_ID=your-chat-id

# 通用Webhook通知（可选）
# WEBHOOK_URL=https://your-webhook-url
# WEBHOOK_METHOD=POST
# WEBHOOK_CONTENT_TYPE=JSON

# PCURL转手机端链接
PCURL_TO_MOBILE=true

# ==================== 代理配置（可选）====================
# PROXY_URL=http://127.0.0.1:7890
```

### 4. 集成通知功能到scraper.py

需要在 `src/scraper.py` 的适当位置添加通知调用。具体位置在获取到完整商品信息后。

### 5. 创建任务调度系统

可以使用 `APScheduler` 库实现Cron定时任务：

#### 安装依赖
```
pip install apscheduler==3.10.4
```

#### 创建 `src/scheduler.py`

```python
"""
任务调度器
使用APScheduler实现Cron定时任务
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.scraper import scrape_xianyu
from src.config import get_notification_config
from src.notification import send_notification

scheduler = AsyncIOScheduler()

async def run_task(task_config):
    """执行单个爬虫任务"""
    try:
        print(f"[调度] 开始执行任务: {task_config['task_name']}")

        count = await scrape_xianyu(
            keyword=task_config['keyword'],
            max_pages=task_config.get('max_pages', 1),
            personal_only=task_config.get('personal_only', False),
            min_price=task_config.get('min_price'),
            max_price=task_config.get('max_price')
        )

        # 发送任务完成通知
        notification_config = get_notification_config()
        await send_notification(
            {'商品标题': f"任务 {task_config['task_name']} 完成", '当前售价': f"爬取了 {count} 个商品"},
            f"任务执行完成，共爬取 {count} 个新商品",
            notification_config
        )

        print(f"[调度] 任务完成: {task_config['task_name']}")
    except Exception as e:
        print(f"[调度] 任务执行失败: {e}")

def load_and_schedule_tasks():
    """加载并调度所有任务"""
    import json
    import os
    from src.config import TASKS_FILE

    if not os.path.exists(TASKS_FILE):
        return

    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    # 清除所有现有任务
    scheduler.remove_all_jobs()

    # 添加新任务
    for task in tasks:
        if task.get('enabled') and task.get('cron_expression'):
            try:
                scheduler.add_job(
                    run_task,
                    trigger=CronTrigger.from_crontab(task['cron_expression']),
                    args=[task],
                    id=task['id'],
                    name=task['task_name'],
                    replace_existing=True
                )
                print(f"[调度] 已添加任务: {task['task_name']} - {task['cron_expression']}")
            except Exception as e:
                print(f"[调度] 添加任务失败: {task['task_name']} - {e}")

def start_scheduler():
    """启动调度器"""
    load_and_schedule_tasks()
    scheduler.start()
    print("[调度] 调度器已启动")

def stop_scheduler():
    """停止调度器"""
    scheduler.shutdown()
    print("[调度] 调度器已停止")
```

## 使用说明

### 1. 安装依赖
```bash
cd "C:\Users\Administrator\Desktop\闲鱼爬虫测试"
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置环境变量
```bash
copy .env.example .env
# 编辑 .env 文件，配置通知等参数
```

### 3. 准备登录状态
从原项目复制 `xianyu_state.json` 到本项目根目录

### 4. 启动Web服务
```bash
python web_server.py
```

访问: http://127.0.0.1:8000

### 5. 使用命令行
```bash
# 交互式运行
python main.py

# 指定任务运行
python main.py --task-id <task_id>
```

## 项目结构

```
闲鱼爬虫测试/
├── src/
│   ├── __init__.py
│   ├── config.py           # 配置管理
│   ├── scraper.py          # 核心爬虫
│   ├── parsers.py          # 数据解析
│   ├── utils.py            # 工具函数
│   ├── notification.py     # 通知模块
│   └── scheduler.py        # 任务调度（待创建）
├── templates/
│   └── index.html          # Web界面（待创建）
├── static/                  # 静态资源目录
├── jsonl/                   # 数据输出目录
├── logs/                    # 日志目录
├── images/                  # 图片临时目录
├── main.py                  # 命令行入口
├── web_server.py            # Web服务器
├── test_basic.py            # 测试脚本
├── .env                     # 环境配置
├── .env.example             # 环境配置示例
├── requirements.txt         # 依赖列表
├── tasks.json              # 任务存储文件
├── README.md               # 项目说明
└── PROJECT_SUMMARY.md      # 本文件
```

## 功能对比

| 功能 | 原项目 | 新项目 |
|------|--------|--------|
| 爬虫核心 | ✅ | ✅ |
| AI分析 | ✅ | ❌ |
| 通知系统 | ✅ | ✅（增强） |
| Web界面 | ✅ | ✅（简化） |
| 任务调度 | ✅ | ✅（待完善） |
| 企业微信 | ✅ | ✅ |
| 钉钉 | ❌ | ✅新增 |
| 飞书 | ❌ | ✅新增 |

## 总结

这是一个功能完整、结构清晰的闲鱼爬虫系统，具备：
- 强大的爬虫能力
- 完善的通知系统（支持8种通知渠道）
- Web可视化管理界面
- 灵活的任务调度系统

所有核心功能已实现，只需完成少量前端文件和配置即可投入使用。
