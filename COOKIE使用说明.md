# Cookie 登录使用说明

## 🎯 为什么推荐使用 Cookie？

相比使用 `xianyu_state.json` 状态文件，使用 Cookie 方式有以下优势：

1. **更轻量**：只需要一行文本，不需要整个状态文件
2. **更灵活**：可以随时从浏览器复制新的 Cookie
3. **更安全**：Cookie 失效后可以快速更换，不需要重新生成状态文件
4. **更隐蔽**：某些情况下不容易被反爬虫检测

## 📝 如何获取 Cookie？

### 方法 1：使用浏览器开发者工具（推荐）

1. **打开闲鱼网站**
   - 访问 https://www.goofish.com
   - 确保已经登录

2. **打开开发者工具**
   - 按 **F12** 键
   - 或右键点击页面 → 检查

3. **切换到网络标签**
   - 点击顶部的 **网络 (Network)** 标签
   - 如果看不到请求，刷新页面（F5）

4. **找到 Cookie**
   - 点击任意一个请求（推荐选择主页面请求，如 `www.goofish.com`）
   - 在右侧找到 **请求标头 (Request Headers)**
   - 向下滚动找到 **Cookie:** 字段
   - 复制整个 Cookie 值（很长的字符串，包含多个 `cookie=value;` 对）

5. **复制 Cookie**
   ```
   示例格式：
   isg=xxxxx; cookie2=xxxxx; sgcookie=xxxxx; unb=xxxxx; uc1=xxxxx; cna=xxxxx
   ```

### 方法 2：使用浏览器扩展

也可以使用 "EditThisCookie" 或 "Cookie-Editor" 等浏览器扩展导出 Cookie。

## 🔧 配置 Cookie

### 方式 1：修改 .env 文件

打开 `.env` 文件，找到 `XIANYU_COOKIE=` 这一行，粘贴你的 Cookie：

```env
XIANYU_COOKIE=isg=xxxxx; cookie2=xxxxx; sgcookie=xxxxx; unb=xxxxx; uc1=xxxxx; cna=xxxxx
```

**注意**：
- Cookie 值不需要引号
- 确保整行都在，不要有换行
- 保存文件后重启程序

### 方式 2：环境变量（Linux/Mac）

```bash
export XIANYU_COOKIE="isg=xxxxx; cookie2=xxxxx; sgcookie=xxxxx"
```

## 🔄 Cookie 失效怎么办？

Cookie 通常有以下几种失效情况：

1. **过期失效**：重新获取 Cookie 即可
2. **登出失效**：重新登录并获取新 Cookie
3. **IP 变化**：某些 Cookie 绑定 IP，需要重新获取

**失效迹象**：
- 任务启动后很快被要求登录
- 无法获取到商品数据
- 出现登录验证

**解决方法**：重复上面的获取步骤，更新 `.env` 文件中的 Cookie 即可。

## 💡 使用建议

1. **定期更新**：建议每周更新一次 Cookie
2. **保持登录**：获取 Cookie 前确保在浏览器中正常登录
3. **完整复制**：确保复制了完整的 Cookie 字符串
4. **测试验证**：更新 Cookie 后先测试一下任务是否能正常运行

## 🆚 Cookie vs State 文件对比

| 特性 | Cookie | State 文件 |
|------|--------|-----------|
| 配置复杂度 | ⭐ 简单 | ⭐⭐ 复杂 |
| 文件大小 | ⭐ 极小（几KB） | ⭐⭐⭐ 较大（几十KB） |
| 更新难度 | ⭐ 简单（复制粘贴） | ⭐⭐⭐ 需要重新生成 |
| 反爬风险 | ⭐⭐ 较低 | ⭐⭐⭐ 较高 |
| 适用场景 | 日常使用 | 长期稳定运行 |

## 📚 相关 Cookie 字段说明

闲鱼登录相关的重要 Cookie 字段：

- `cookie2` / `sgcookie`：会话标识
- `unb` / `uc1`：用户标识
- `isg`：安全网关标识
- `cna`：客户端标识
- `_m_h5_tk` / `_m_h5_tk_enc`：加密令牌

**注意**：不需要理解每个字段的作用，只需要复制完整的 Cookie 字符串即可。

## ❓ 常见问题

**Q: Cookie 会泄露我的账号吗？**
A: Cookie 包含登录信息，请勿分享给他人。建议定期更换。

**Q: 可以用多个账号的 Cookie 吗？**
A: 可以通过修改 `.env` 文件切换不同账号的 Cookie。

**Q: Cookie 有效期是多久？**
A: 通常 1-2 周，但也可能随时失效，取决于闲鱼的安全策略。

**Q: 为什么配置了 Cookie 还是无法登录？**
A: 可能是：
   - Cookie 不完整（请确认复制了整个 Cookie 字符串）
   - Cookie 已过期（重新获取）
   - 浏览器环境不一致（确保使用相同浏览器获取）

---

如有问题，请检查程序日志中的错误信息进行排查。
