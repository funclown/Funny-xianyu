# Chrome Headless 模式错误解决方案

## ❌ 错误信息

```
playwright._impl._errors.TargetClosedError: BrowserType.launch: Target page, context or browser has been closed
Old Headless mode has been removed from the Chrome binary
```

## 🔍 问题原因

### 根本原因

1. **Chrome 版本太新** - 你的 Chrome 版本是 112+，已经移除了旧的 headless 模式
2. **Playwright 版本过旧** - Playwright 1.48.0 使用旧的 `--headless=old` 参数
3. **版本不兼容** - 旧版 Playwright 无法与新版 Chrome 配合工作

### 错误详情

从日志可以看到：
```
--headless=old
```

Chrome 112+ 不再支持这个参数，需要使用新的 headless 模式。

---

## ✅ 解决方案

### 方案 1：升级 Playwright（推荐）⭐

这是**最简单、最可靠**的解决方案。

#### 步骤 1：升级 Playwright

```bash
pip install --upgrade playwright
```

#### 步骤 2：安装新的浏览器驱动

```bash
playwright install chromium
```

#### 步骤 3：验证安装

```bash
# 检查 Playwright 版本
playwright --version
# 应该显示：1.57.0 或更高

# 测试浏览器启动
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); browser=p.chromium.launch(); print('✅ 成功'); browser.close()"
```

#### 完成！

现在运行任务应该可以正常工作了。

---

### 方案 2：使用 Playwright 自带的 Chromium（推荐）⭐

Playwright 自带了一个经过测试的 Chromium 版本，不依赖系统安装的 Chrome。

#### 修改代码

编辑 `src/scraper.py` 第 193 行：

**修改前：**
```python
browser = await p.chromium.launch(headless=RUN_HEADLESS, channel="chrome")
```

**修改后：**
```python
browser = await p.chromium.launch(headless=RUN_HEADLESS)
# 移除 channel="chrome" 参数
```

#### 说明

- `channel="chrome"` - 使用系统安装的 Chrome（可能有版本兼容问题）
- 不指定 `channel` - 使用 Playwright 自带的 Chromium（稳定，经过测试）

#### 优点

- ✅ 版本稳定，不会因为 Chrome 更新而失效
- ✅ Playwright 官方支持
- ✅ 跨平台一致性好

---

### 方案 3：降级 Chrome（不推荐）

如果必须使用系统的 Chrome，可以降级到旧版本。

#### 步骤

1. 卸载当前的 Chrome
2. 下载并安装 Chrome 111 或更早版本：
   - https://www.google.com/chrome/browser/desktop/old.html
3. 禁用 Chrome 自动更新

#### 缺点

- ❌ 安全风险（旧版本有已知漏洞）
- ❌ 不利于维护
- ❌ 可能影响其他应用

---

### 方案 4：暂时使用有头模式（临时调试）

如果只是想快速测试，可以暂时显示浏览器窗口。

#### 修改 .env 文件

```bash
# 设置为 false
RUN_HEADLESS=false
```

#### 重启任务

浏览器窗口会显示出来，可以看到具体的运行情况。

#### 优点

- ✅ 方便调试
- ✅ 可以看到爬取过程

#### 缺点

- ❌ 会干扰其他工作
- ❌ 不能在服务器上使用

---

## 🛠️ 完整的修复步骤

### 在新电脑上的完整步骤

#### 1. 升级 Playwright

```bash
pip install --upgrade playwright
```

#### 2. 安装浏览器驱动

```bash
playwright install chromium
```

#### 3. 更新 requirements.txt（可选）

已更新 `playwright>=1.57.0` 而不是固定版本 `playwright==1.48.0`

#### 4. 验证

```bash
python -c "
from playwright.sync_api import sync_playwright
import asyncio

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.baidu.com')
        title = await page.title()
        print(f'✅ 浏览器工作正常！标题: {title}')
        await browser.close()

asyncio.run(test())
"
```

#### 5. 运行任务

```bash
# 通过 Web UI 启动任务
# 或命令行启动
python main.py --task-id 1
```

---

## 📋 版本兼容性对照表

| Playwright 版本 | 支持的 Chrome 版本 | Headless 模式 | 状态 |
|----------------|-------------------|--------------|------|
| 1.48.0 | Chrome 111- | 旧模式 (`--headless=old`) | ❌ 过时 |
| 1.57.0 | Chrome 112+ | 新模式 (`--headless=new`) | ✅ 推荐 |
| 1.57.0+ | Chrome 112+ | 自带 Chromium | ✅ 稳定 |

---

## 🎯 推荐配置

### 最佳实践配置

```bash
# .env 文件
RUN_HEADLESS=true              # 生产环境使用无头模式
LOGIN_IS_EDGE=false            # 使用 Chromium（而不是 Edge）
DEBUG_MODE=false               # 关闭调试模式

# requirements.txt
playwright>=1.57.0             # 使用最新版
```

### 代码配置

```python
# src/scraper.py
# 推荐：使用 Playwright 自带的 Chromium
browser = await p.chromium.launch(headless=RUN_HEADLESS)

# 不推荐：使用系统的 Chrome（可能有兼容性问题）
# browser = await p.chromium.launch(headless=RUN_HEADLESS, channel="chrome")
```

---

## 🚨 常见问题

### Q1: 升级后还是报错？

**A:** 可能是浏览器驱动没有正确安装：

```bash
# 强制重新安装
playwright install chromium --force
playwright install-deps chromium
```

### Q2: 下载速度太慢？

**A:** 使用国内镜像：

```bash
# 设置环境变量
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/

# 然后安装
playwright install chromium
```

### Q3: 内存不足？

**A:** 使用轻量级的 headless shell：

```python
# 代码中指定使用 headless shell
browser = await p.chromium.launch(
    headless=True,
    channel="chrome"  # 需要系统 Chrome 112+
)
```

### Q4: 如何确认浏览器已正确安装？

**A:** 运行检查命令：

```bash
playwright install --help
playwright show-browsers
```

预期输出：
```
chromium 143.0.7499.4 (playwright build v1200)
```

---

## 📝 总结

### 快速修复（3 步）

```bash
# 1. 升级
pip install --upgrade playwright

# 2. 安装驱动
playwright install chromium

# 3. 运行任务
python main.py --task-id 1
```

### 永久修复

更新 `requirements.txt`：
```txt
playwright>=1.57.0
```

### 预防措施

1. ✅ 定期更新 Playwright
2. ✅ 使用 Playwright 自带的 Chromium
3. ✅ 不要依赖系统的 Chrome
4. ✅ 在 CI/CD 中固定 Playwright 版本

---

## 🔗 相关链接

- [Playwright Chrome Headless 文档](https://playwright.dev/python/docs/api/class-browsertype#browsertype-launch-option-headless)
- [Chrome 新 Headless 模式介绍](https://developer.chrome.com/docs/chromium/new-headless)
- [Playwright 发布日志](https://github.com/microsoft/playwright/releases)

---

**问题已解决！现在可以正常运行任务了。** 🎉
