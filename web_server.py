"""
闲鱼爬虫 Web 管理界面
提供任务管理、日志查看、结果浏览等功能
"""
import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import secrets

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel

from src.config import (
    SERVER_PORT,
    WEB_USERNAME,
    WEB_PASSWORD,
    STATE_FILE,
    JSONL_OUTPUT_DIR,
    LOG_DIR,
    TASKS_FILE,
    get_notification_config,
)

# ==================== FastAPI应用 ====================
app = FastAPI(title="闲鱼爬虫管理系统", version="1.0.0")

# Session 管理
app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_urlsafe(32),
    max_age=3600 * 24 * 7,  # 7天
    session_cookie="session_id",
    same_site="lax",
)

# Basic认证（保留用于API兼容）
security = HTTPBasic()

# ==================== 数据模型 ====================
class TaskCreate(BaseModel):
    task_name: str
    keyword: str
    max_pages: int = 1
    personal_only: bool = False
    min_price: str = None
    max_price: str = None
    cron_expression: str = None
    enabled: bool = True
    auto_push: bool = False  # 默认不开启自动推送


class TaskUpdate(BaseModel):
    task_name: str = None
    keyword: str = None
    max_pages: int = None
    personal_only: bool = None
    min_price: str = None
    max_price: str = None
    cron_expression: str = None
    enabled: bool = None
    auto_push: bool = None  # 支持更新自动推送设置


class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: bool = False


# ==================== 辅助函数 ====================
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """验证Web界面登录凭据（Basic认证，用于API兼容）"""
    correct_username = WEB_USERNAME
    correct_password = WEB_PASSWORD
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


def verify_session(request: Request):
    """验证Session认证（用于Web界面）"""
    if not request.session.get("logged_in"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录，请先登录"
        )
    return request.session


def load_tasks():
    """从文件加载任务列表"""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_tasks(tasks):
    """保存任务列表到文件"""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def get_results_list():
    """获取所有结果文件列表"""
    results = []
    if os.path.exists(JSONL_OUTPUT_DIR):
        for filename in os.listdir(JSONL_OUTPUT_DIR):
            if filename.endswith('_full_data.jsonl'):
                filepath = os.path.join(JSONL_OUTPUT_DIR, filename)
                # 获取文件信息
                stat = os.stat(filepath)
                keyword = filename.replace('_full_data.jsonl', '')

                # 统计记录数
                count = 0
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        count = sum(1 for _ in f)
                except:
                    pass

                results.append({
                    'filename': filename,
                    'keyword': keyword,
                    'count': count,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
    # 按修改时间倒序排列
    results.sort(key=lambda x: x['modified'], reverse=True)
    return results


def read_jsonl_file(filename, limit=50):
    """读取JSONL文件的内容"""
    filepath = os.path.join(JSONL_OUTPUT_DIR, filename)
    records = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except:
                        continue
                if len(records) >= limit:
                    break
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return records


# ==================== 认证路由 ====================
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """显示登录页面"""
    html_path = Path(__file__).parent / "templates" / "login.html"
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>登录页面未找到</h1>"


@app.post("/api/auth/login")
async def login(login_data: LoginRequest, request: Request):
    """处理登录请求"""
    if login_data.username == WEB_USERNAME and login_data.password == WEB_PASSWORD:
        request.session["logged_in"] = True
        request.session["username"] = login_data.username
        if login_data.remember_me:
            request.session["remember_me"] = True
        return {"success": True, "message": "登录成功"}
    else:
        return {"success": False, "message": "用户名或密码错误"}


@app.post("/api/auth/logout")
async def logout(request: Request):
    """处理退出登录"""
    request.session.clear()
    return {"success": True, "message": "已退出登录"}


@app.get("/api/auth/status")
async def auth_status(request: Request):
    """检查登录状态"""
    logged_in = request.session.get("logged_in", False)
    username = request.session.get("username", "")
    return {"logged_in": logged_in, "username": username}


# ==================== 主页路由（需要登录）====================
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """返回Web界面首页（需要登录）"""
    # 检查是否已登录
    if not request.session.get("logged_in"):
        # 未登录，重定向到登录页
        return RedirectResponse(url="/login", status_code=302)

    html_path = Path(__file__).parent / "templates" / "index.html"
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    return """
    <html>
    <head><title>闲鱼爬虫管理系统</title></head>
    <body>
        <h1>闲鱼爬虫管理系统</h1>
        <p>Web界面文件未找到，请检查 templates/index.html 是否存在。</p>
    </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    """健康检查端点（无需认证）"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/tasks")
async def get_tasks(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """获取所有任务"""
    tasks = load_tasks()
    return {"tasks": tasks}


@app.post("/api/tasks")
async def create_task(task: TaskCreate, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """创建新任务"""
    tasks = load_tasks()

    # 检查任务名是否已存在
    for existing_task in tasks:
        if existing_task['task_name'] == task.task_name:
            raise HTTPException(status_code=400, detail=f"任务名 '{task.task_name}' 已存在")

    # 创建新任务
    new_task = {
        "id": str(len(tasks) + 1),
        "task_name": task.task_name,
        "keyword": task.keyword,
        "max_pages": task.max_pages,
        "personal_only": task.personal_only,
        "min_price": task.min_price,
        "max_price": task.max_price,
        "cron_expression": task.cron_expression,
        "enabled": task.enabled,
        "auto_push": task.auto_push,  # 添加自动推送设置
        "created_at": datetime.now().isoformat(),
        "last_run": None,
        "status": "idle"
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return {"message": "任务创建成功", "task": new_task}


@app.put("/api/tasks/{task_id}")
async def update_task(task_id: str, task: TaskUpdate, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """更新任务"""
    tasks = load_tasks()

    for existing_task in tasks:
        if existing_task['id'] == task_id:
            # 更新字段
            if task.task_name is not None:
                existing_task['task_name'] = task.task_name
            if task.keyword is not None:
                existing_task['keyword'] = task.keyword
            if task.max_pages is not None:
                existing_task['max_pages'] = task.max_pages
            if task.personal_only is not None:
                existing_task['personal_only'] = task.personal_only
            if task.min_price is not None:
                existing_task['min_price'] = task.min_price
            if task.max_price is not None:
                existing_task['max_price'] = task.max_price
            if task.cron_expression is not None:
                existing_task['cron_expression'] = task.cron_expression
            if task.enabled is not None:
                existing_task['enabled'] = task.enabled
            if task.auto_push is not None:
                existing_task['auto_push'] = task.auto_push

            save_tasks(tasks)
            return {"message": "任务更新成功", "task": existing_task}

    raise HTTPException(status_code=404, detail="任务未找到")


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """删除任务"""
    tasks = load_tasks()

    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            deleted_task = tasks.pop(i)
            save_tasks(tasks)
            return {"message": "任务删除成功", "task": deleted_task}

    raise HTTPException(status_code=404, detail="任务未找到")


@app.post("/api/tasks/{task_id}/start")
async def start_task(task_id: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """手动启动任务"""
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            # 在后台启动爬虫任务
            try:
                # 启动独立进程运行爬虫，使用--task-id参数
                # 添加 -u 参数禁用Python输出缓冲，确保日志实时写入
                cmd = [sys.executable, "-u", "main.py", "--task-id", task_id]

                # 设置工作目录和创建日志文件
                work_dir = os.path.dirname(os.path.abspath(__file__))
                log_file = os.path.join(work_dir, LOG_DIR, f"task_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

                # 打开日志文件以记录输出，使用行缓冲
                log_handle = open(log_file, 'w', encoding='utf-8', buffering=1)

                # 启动进程
                process = subprocess.Popen(
                    cmd,
                    cwd=work_dir,
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )

                task['status'] = 'running'
                task['last_run'] = datetime.now().isoformat()
                task['pid'] = process.pid
                task['log_file'] = os.path.basename(log_file)
                save_tasks(tasks)

                return {
                    "message": f"任务 '{task['task_name']}' 已启动",
                    "task_id": task_id,
                    "log_file": task['log_file']
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"启动任务失败: {str(e)}")

    raise HTTPException(status_code=404, detail="任务未找到")


@app.post("/api/tasks/{task_id}/stop")
async def stop_task(task_id: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """手动停止任务"""
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            # 检查任务是否正在运行
            if task.get('status') != 'running':
                raise HTTPException(status_code=400, detail=f"任务 '{task['task_name']}' 当前未在运行")

            # 获取进程ID
            pid = task.get('pid')
            if not pid:
                raise HTTPException(status_code=400, detail="任务进程ID不存在，无法停止")

            try:
                # 尝试终止进程
                if sys.platform == 'win32':
                    # Windows系统使用taskkill命令
                    import subprocess
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)],
                                 capture_output=True,
                                 timeout=5)
                else:
                    # Linux/Mac系统使用os.kill
                    import signal
                    os.kill(pid, signal.SIGTERM)

                # 更新任务状态
                task['status'] = 'stopped'
                save_tasks(tasks)

                return {
                    "message": f"任务 '{task['task_name']}' 已停止",
                    "task_id": task_id,
                    "pid": pid
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"停止任务失败: {str(e)}")

    raise HTTPException(status_code=404, detail="任务未找到")


@app.post("/api/tasks/restart-all-running")
async def restart_all_running_tasks(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """重启所有正在运行的任务（用于配置变更后）"""
    tasks = load_tasks()
    running_tasks = [task for task in tasks if task.get('status') == 'running']

    if not running_tasks:
        return {
            "success": True,
            "message": "当前没有正在运行的任务",
            "restarted_count": 0
        }

    restarted_tasks = []
    failed_tasks = []

    for task in running_tasks:
        task_id = task['id']
        task_name = task['task_name']
        pid = task.get('pid')

        try:
            # 1. 停止任务
            if pid:
                if sys.platform == 'win32':
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)],
                                 capture_output=True, timeout=5)
                else:
                    import signal
                    os.kill(pid, signal.SIGTERM)

            # 等待进程结束
            import time
            time.sleep(1)

            # 2. 重新启动任务
            cmd = [sys.executable, "-u", "main.py", "--task-id", task_id]
            work_dir = os.path.dirname(os.path.abspath(__file__))
            log_file = os.path.join(work_dir, LOG_DIR, f"task_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            log_handle = open(log_file, 'w', encoding='utf-8', buffering=1)

            process = subprocess.Popen(
                cmd,
                cwd=work_dir,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            # 更新任务信息
            task['status'] = 'running'
            task['last_run'] = datetime.now().isoformat()
            task['pid'] = process.pid
            task['log_file'] = os.path.basename(log_file)

            restarted_tasks.append({
                'task_id': task_id,
                'task_name': task_name,
                'new_pid': process.pid
            })

        except Exception as e:
            failed_tasks.append({
                'task_id': task_id,
                'task_name': task_name,
                'error': str(e)
            })

    # 保存更新后的任务列表
    save_tasks(tasks)

    return {
        "success": True,
        "message": f"已重启 {len(restarted_tasks)} 个任务",
        "restarted_count": len(restarted_tasks),
        "failed_count": len(failed_tasks),
        "restarted_tasks": restarted_tasks,
        "failed_tasks": failed_tasks
    }


@app.get("/api/results")
async def get_results(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """获取所有结果文件列表"""
    results = get_results_list()
    return {"results": results}


@app.get("/api/results/{filename}")
async def get_result_detail(filename: str, limit: int = 50, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """获取特定结果的详细数据"""
    # 安全检查：确保文件名合法
    if not filename.endswith('_full_data.jsonl'):
        raise HTTPException(status_code=400, detail="无效的文件名")

    records = read_jsonl_file(filename, limit)
    return {"filename": filename, "count": len(records), "records": records}


@app.delete("/api/results/{filename}")
async def delete_result(filename: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """删除指定的结果文件"""
    # 安全检查：确保文件名合法
    if not filename.endswith('_full_data.jsonl'):
        raise HTTPException(status_code=400, detail="无效的文件名")

    # 构建文件路径
    filepath = os.path.join(JSONL_OUTPUT_DIR, filename)

    # 检查文件是否存在
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="文件不存在")

    try:
        # 删除文件
        os.remove(filepath)
        return {"message": f"文件 '{filename}' 已成功删除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")


def get_current_cookie():
    """动态读取 .env 文件中的当前 Cookie 值"""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        return ""
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("XIANYU_COOKIE="):
                    cookie = line.split("=", 1)[1].strip()
                    return cookie
    except Exception as e:
        print(f"读取 Cookie 失败: {e}")
    return ""


@app.get("/api/system/status")
async def get_system_status(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """获取系统状态"""
    # 动态读取最新的 Cookie 值
    current_cookie = get_current_cookie()

    status = {
        "login_state_exists": os.path.exists(STATE_FILE),
        "tasks_file_exists": os.path.exists(TASKS_FILE),
        "output_dir_exists": os.path.exists(JSONL_OUTPUT_DIR),
        "results_count": len(get_results_list()),
        "tasks_count": len(load_tasks()),
        "notification_configured": bool(get_notification_config().get('wx_bot_url') or
                                       get_notification_config().get('dingtalk_bot_url') or
                                       get_notification_config().get('feishu_bot_url')),
        "cookie_configured": bool(current_cookie),
        "cookie_preview": current_cookie[:50] + "..." if len(current_cookie) > 50 else current_cookie if current_cookie else ""
    }
    return status


@app.post("/api/system/cookie")
async def update_cookie(request: dict, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """更新 Cookie 配置"""
    new_cookie = request.get("cookie", "").strip()

    if not new_cookie:
        raise HTTPException(status_code=400, detail="Cookie 不能为空")

    try:
        # 读取 .env 文件
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

        if not os.path.exists(env_path):
            raise HTTPException(status_code=404, detail=".env 文件不存在")

        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 查找并更新 XIANYU_COOKIE 行
        updated = False
        for i, line in enumerate(lines):
            if line.startswith("XIANYU_COOKIE="):
                lines[i] = f"XIANYU_COOKIE={new_cookie}\n"
                updated = True
                break

        # 如果没有找到 XIANYU_COOKIE 行，添加新行
        if not updated:
            # 在文件末尾添加
            lines.append(f"\nXIANYU_COOKIE={new_cookie}\n")

        # 写回文件
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return {
            "message": "Cookie 更新成功",
            "cookie_preview": new_cookie[:50] + "..." if len(new_cookie) > 50 else new_cookie
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新 Cookie 失败: {str(e)}")


@app.get("/api/browser-mode")
async def get_browser_mode(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """获取浏览器模式设置"""
    try:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

        if not os.path.exists(env_path):
            # 如果 .env 文件不存在，返回默认值（无头模式）
            return {"success": True, "headless": True}

        # 读取 .env 文件
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 查找 RUN_HEADLESS 行
        for line in lines:
            if line.startswith("RUN_HEADLESS="):
                value = line.split("=")[1].strip().lower()
                headless = value in ['true', '1', 'yes']
                return {"success": True, "headless": headless}

        # 如果没有找到，返回默认值（无头模式）
        return {"success": True, "headless": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取浏览器模式失败: {str(e)}")


@app.post("/api/browser-mode")
async def update_browser_mode(request: dict, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """更新浏览器模式设置，并自动重启正在运行的任务"""
    headless = request.get("headless", True)
    auto_restart = request.get("auto_restart", True)  # 默认自动重启

    try:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

        if not os.path.exists(env_path):
            raise HTTPException(status_code=404, detail=".env 文件不存在")

        # 读取 .env 文件
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 查找并更新 RUN_HEADLESS 行
        updated = False
        for i, line in enumerate(lines):
            if line.startswith("RUN_HEADLESS="):
                lines[i] = f"RUN_HEADLESS={'true' if headless else 'false'}\n"
                updated = True
                break

        # 如果没有找到 RUN_HEADLESS 行，添加新行
        if not updated:
            lines.append(f"\nRUN_HEADLESS={'true' if headless else 'false'}\n")

        # 写回文件
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"[浏览器模式] 设置已更新为: {'无头模式' if headless else '有头模式'}")

        result = {
            "success": True,
            "headless": headless,
            "auto_restarted": False,
            "restarted_info": None
        }

        # 自动重启正在运行的任务
        if auto_restart:
            tasks = load_tasks()
            running_tasks = [task for task in tasks if task.get('status') == 'running']

            if running_tasks:
                print(f"[浏览器模式] 检测到 {len(running_tasks)} 个正在运行的任务，准备自动重启...")

                restarted_tasks = []
                for task in running_tasks:
                    task_id = task['id']
                    task_name = task['task_name']
                    pid = task.get('pid')

                    try:
                        # 1. 停止任务
                        if pid:
                            if sys.platform == 'win32':
                                subprocess.run(['taskkill', '/F', '/PID', str(pid)],
                                             capture_output=True, timeout=5)
                            else:
                                import signal
                                os.kill(pid, signal.SIGTERM)

                        # 等待进程结束
                        import time
                        time.sleep(1)

                        # 2. 重新启动任务
                        cmd = [sys.executable, "-u", "main.py", "--task-id", task_id]
                        work_dir = os.path.dirname(os.path.abspath(__file__))
                        log_file = os.path.join(work_dir, LOG_DIR, f"task_{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
                        log_handle = open(log_file, 'w', encoding='utf-8', buffering=1)

                        process = subprocess.Popen(
                            cmd,
                            cwd=work_dir,
                            stdout=log_handle,
                            stderr=subprocess.STDOUT,
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                        )

                        # 更新任务信息
                        task['status'] = 'running'
                        task['last_run'] = datetime.now().isoformat()
                        task['pid'] = process.pid
                        task['log_file'] = os.path.basename(log_file)

                        restarted_tasks.append({
                            'task_id': task_id,
                            'task_name': task_name,
                            'new_pid': process.pid
                        })

                        print(f"[浏览器模式] 任务 '{task_name}' 已重启 (PID: {process.pid})")

                    except Exception as e:
                        print(f"[浏览器模式] 任务 '{task_name}' 重启失败: {e}")

                # 保存更新后的任务列表
                save_tasks(tasks)

                if restarted_tasks:
                    result["auto_restarted"] = True
                    result["restarted_info"] = {
                        "count": len(restarted_tasks),
                        "tasks": restarted_tasks
                    }

                    message = f"浏览器模式已设置为: {'无头模式' if headless else '有头模式'}，已自动重启 {len(restarted_tasks)} 个任务"
                else:
                    message = f"浏览器模式已设置为: {'无头模式' if headless else '有头模式'}，但重启任务失败"
            else:
                message = f"浏览器模式已设置为: {'无头模式' if headless else '有头模式'}，当前没有运行中的任务"

        result["message"] = message
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新浏览器模式失败: {str(e)}")


@app.get("/api/tasks/{task_id}/logs")
async def get_task_logs(task_id: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """获取任务日志"""
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            log_file = task.get('log_file')
            if not log_file:
                return {"error": "任务尚未运行或日志文件不存在"}

            log_path = os.path.join(LOG_DIR, log_file)
            if not os.path.exists(log_path):
                return {"error": "日志文件不存在"}

            try:
                # 尝试多种编码方式读取日志文件
                log_content = None
                for encoding in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
                    try:
                        with open(log_path, 'r', encoding=encoding) as f:
                            log_content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue

                if log_content is None:
                    return {"error": "无法读取日志文件（编码问题）"}

                return {
                    "task_id": task_id,
                    "log_file": log_file,
                    "log_content": log_content,
                    "log_lines": len(log_content.split('\n'))
                }
            except Exception as e:
                return {"error": f"读取日志文件失败: {str(e)}"}

    raise HTTPException(status_code=404, detail="任务未找到")


@app.get("/api/system/notification")
async def get_notification_config_api(request: Request):
    """获取通知配置"""
    # Session 认证
    if not request.session.get("logged_in"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录，请先登录"
        )

    try:
        config = get_notification_config()
        # 只返回三个通知渠道的配置状态
        result = {}
        for key in ['wx_bot_url', 'dingtalk_bot_url', 'feishu_bot_url']:
            value = config.get(key, '')
            if value and isinstance(value, str) and value.strip():
                # 如果有值，显示前30个字符
                result[key] = {
                    'configured': True,
                    'preview': value[:30] + '...' if len(value) > 30 else value
                }
            else:
                result[key] = {'configured': False, 'preview': ''}

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取通知配置失败: {str(e)}")


@app.post("/api/system/notification")
async def update_notification_config(request_req: Request, request: dict):
    """更新通知配置"""
    # Session 认证
    if not request_req.session.get("logged_in"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录，请先登录"
        )

    try:
        # 读取 .env 文件
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

        if not os.path.exists(env_path):
            raise HTTPException(status_code=404, detail=".env 文件不存在")

        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 定义环境变量映射 - 只处理三个通知渠道
        env_mapping = {
            'wx_bot_url': 'WX_BOT_URL',
            'dingtalk_bot_url': 'DINGTALK_BOT_URL',
            'feishu_bot_url': 'FEISHU_BOT_URL'
        }

        # 更新配置
        updated_fields = []
        for field_key, env_var in env_mapping.items():
            new_value = request.get(field_key, "").strip()

            # 查找并更新对应的行
            found = False
            for i, line in enumerate(lines):
                # 跳过注释行
                if line.strip().startswith('#'):
                    continue
                if line.startswith(f"{env_var}="):
                    if new_value:
                        lines[i] = f"{env_var}={new_value}\n"
                        updated_fields.append(env_var)
                    else:
                        # 如果值为空，注释掉这一行
                        lines[i] = f"# {env_var}=\n"
                        updated_fields.append(f"{env_var}(已清空)")
                    found = True
                    break

            # 如果没有找到且新值不为空，添加新行
            if not found and new_value:
                lines.append(f"\n{env_var}={new_value}\n")
                updated_fields.append(env_var)

        # 写回文件
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return {
            "message": "通知配置更新成功",
            "updated_fields": updated_fields,
            "note": "配置已保存，下次任务执行时会自动使用新的通知设置"
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"更新通知配置失败: {str(e)}")


@app.post("/api/notify-products")
async def notify_products(request: Request, product_ids: list = None, message: str = None):
    """
    批量推送指定商品到通知渠道

    参数:
    - product_ids: 商品ID列表
    - message: 推送消息（可选）
    """
    try:
        # 解析请求体
        print(f"\n[DEBUG] 收到推送请求...")
        body = await request.json()
        product_ids = body.get('product_ids', [])
        message = body.get('message', '批量推送商品')
        print(f"[DEBUG] 请求参数: product_ids数量={len(product_ids)}, message={message}")
        if product_ids:
            print(f"[DEBUG] 前3个商品ID: {product_ids[:3]}")

        # 验证参数
        if not product_ids or not isinstance(product_ids, list):
            raise HTTPException(status_code=400, detail="商品ID列表不能为空")

        if len(product_ids) == 0:
            raise HTTPException(status_code=400, detail="商品ID列表不能为空")

        # 检查通知配置
        notify_config = get_notification_config()
        has_notification = any([
            notify_config.get('ntfy_topic_url'),
            notify_config.get('gotify_url'),
            notify_config.get('bark_url'),
            notify_config.get('wx_bot_url'),
            notify_config.get('dingtalk_bot_url'),
            notify_config.get('feishu_bot_url'),
            notify_config.get('telegram_bot_token'),
            notify_config.get('webhook_url')
        ])

        if not has_notification:
            raise HTTPException(status_code=400, detail="未配置任何通知渠道，请先在系统设置中配置通知渠道")

        # 在所有JSONL文件中查找指定商品
        found_products = []
        jsonl_dir = Path(JSONL_OUTPUT_DIR)

        if not jsonl_dir.exists():
            raise HTTPException(status_code=404, detail="数据目录不存在")

        print(f"[DEBUG] 开始在JSONL文件中查找商品...")
        # 遍历所有_full_data.jsonl文件
        for jsonl_file in jsonl_dir.glob("*_full_data.jsonl"):
            print(f"[DEBUG] 检查文件: {jsonl_file.name}")
            try:
                with open(jsonl_file, 'r', encoding='utf-8', errors='replace') as f:
                    line_count = 0
                    for line in f:
                        if not line.strip():
                            continue
                        line_count += 1
                        try:
                            product = json.loads(line)
                            # 商品ID在"商品信息"字段内
                            product_id = product.get('商品信息', {}).get('商品ID', '')

                            if product_id in product_ids:
                                found_products.append(product)
                                print(f"[DEBUG] 找到商品: {product_id}")
                                # 如果找到了所有商品，可以提前退出
                                if len(found_products) == len(product_ids):
                                    break
                        except json.JSONDecodeError:
                            continue
                    print(f"[DEBUG] 文件 {jsonl_file.name} 处理了 {line_count} 行")
            except Exception as e:
                print(f"读取文件 {jsonl_file} 时出错: {e}")
                continue

        print(f"[DEBUG] 查找完成: 共找到 {len(found_products)} 个商品")

        # 发送通知
        print(f"[DEBUG] 开始导入 send_notification...")
        try:
            from src.notification import send_notification
            print(f"[DEBUG] 导入 send_notification 成功")
        except Exception as import_error:
            print(f"[ERROR] 导入 send_notification 失败: {import_error}")
            import traceback
            traceback.print_exc()
            raise

        print(f"[DEBUG] 准备发送 {len(found_products)} 个商品的通知...")
        sent_count = 0
        for idx, product in enumerate(found_products):
            try:
                # 从商品信息中提取数据
                product_info = product.get('商品信息', {})
                seller_info = product.get('卖家信息', {})

                print(f"[DEBUG] 正在处理第 {idx+1}/{len(found_products)} 个商品: {product_info.get('商品ID', 'unknown')}")

                # 构建扁平化的商品数据，用于send_notification
                flat_product_data = {
                    '商品标题': product_info.get('商品标题', '未知商品'),
                    '当前售价': product_info.get('当前售价', 'N/A'),
                    '商品链接': product_info.get('商品链接', '#'),
                    '商品主图链接': product_info.get('商品主图链接', ''),
                    '商品图片列表': product_info.get('商品图片列表', []),
                    '商品ID': product_info.get('商品ID', ''),
                    '卖家昵称': product_info.get('卖家昵称', seller_info.get('卖家昵称', '未知'))
                }

                # 构建通知消息（精简以符合企业微信4096字节限制）
                title = product_info.get('商品标题', '未知商品')
                price = product_info.get('当前售价', '未知')
                link = product_info.get('商品链接', '#')
                seller = product_info.get('卖家昵称', seller_info.get('卖家昵称', '未知'))

                # 限制标题长度，避免消息过长
                if len(title) > 50:
                    title = title[:50] + '...'

                content = f"{message}\n\n商品: {title}\n价格: {price}\n卖家: {seller}\n链接: {link}"

                print(f"[DEBUG] 调用 send_notification 函数...")
                # 发送通知 - 注意参数顺序：(product_data, reason, notification_config)
                await send_notification(flat_product_data, content, notify_config)
                sent_count += 1
                print(f"[DEBUG] 成功发送商品 {product_info.get('商品ID', 'unknown')} 的通知")
            except Exception as e:
                print(f"[ERROR] 发送商品 {product.get('商品信息', {}).get('商品ID', 'unknown')} 通知失败: {e}")
                import traceback
                traceback.print_exc()
                continue

        print(f"[DEBUG] 推送完成: 成功发送 {sent_count}/{len(found_products)} 个商品")

        return {
            "message": f"推送完成",
            "sent_count": sent_count,
            "total_requested": len(product_ids),
            "total_found": len(found_products),
            "not_found_count": len(product_ids) - len(found_products)
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"推送商品时发生错误: {str(e)}")


# ==================== 主程序入口 ====================
if __name__ == "__main__":
    import uvicorn

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              闲鱼爬虫管理系统 Web 服务                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

服务地址: http://127.0.0.1:{SERVER_PORT}
用户名: {WEB_USERNAME}
密码: {WEB_PASSWORD}

按 Ctrl+C 停止服务
    """)

    # 创建必要的目录
    os.makedirs(JSONL_OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)

    uvicorn.run(app, host="127.0.0.1", port=SERVER_PORT, log_level="info")
