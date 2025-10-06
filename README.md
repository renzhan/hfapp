# Hugging Face Callback API

基于 FastAPI 的 Hugging Face OAuth 回调处理应用。

## 功能特性

- 处理 Hugging Face OAuth 授权回调
- 支持 JSON 和 HTML 两种响应格式
- 完整的错误处理机制
- 自动生成的 API 文档
- 支持状态参数验证（防止 CSRF 攻击）

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python main.py
```

或者使用 uvicorn 直接运行：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问应用

- API 根路径: http://localhost:8000/
- 回调端点: http://localhost:8000/huggingface-callback
- HTML 回调端点: http://localhost:8000/huggingface-callback/html
- API 文档: http://localhost:8000/docs

## API 端点

### GET /huggingface-callback

处理 Hugging Face OAuth 回调，返回 JSON 格式响应。

**查询参数:**
- `code` (可选): 授权码
- `state` (可选): 状态参数
- `error` (可选): 错误代码
- `error_description` (可选): 错误描述

**响应示例:**
```json
{
  "message": "成功接收到Hugging Face回调",
  "code": "your_auth_code",
  "state": "your_state",
  "next_steps": "可以使用此授权码换取访问令牌"
}
```

### GET /huggingface-callback/html

处理 Hugging Face OAuth 回调，返回 HTML 格式响应，适用于浏览器显示。

**查询参数:** 与 JSON 端点相同

## 使用示例

### 1. 在 Hugging Face 应用中配置回调 URL

```
http://localhost:8000/huggingface-callback
```

### 2. 处理回调响应

当用户完成授权后，Hugging Face 会重定向到您的回调 URL，并携带授权码：

```
http://localhost:8000/huggingface-callback?code=abc123&state=xyz789
```

### 3. 使用授权码换取访问令牌

收到授权码后，您可以使用它来换取访问令牌：

```python
import requests

def exchange_code_for_token(code, client_id, client_secret, redirect_uri):
    token_url = "https://huggingface.co/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }
    response = requests.post(token_url, data=data)
    return response.json()
```

## 错误处理

应用会自动处理以下错误情况：

- 缺少授权码参数
- OAuth 授权错误
- 无效的状态参数

## 开发说明

- 基于 FastAPI 框架构建
- 支持异步处理
- 自动生成 OpenAPI 文档
- 包含完整的类型提示
- 支持热重载开发模式

## 扩展功能

您可以根据需要扩展以下功能：

1. **数据库集成**: 存储用户令牌和会话信息
2. **令牌管理**: 自动刷新过期令牌
3. **用户管理**: 用户注册和登录功能
4. **安全增强**: 添加更多安全验证机制
5. **日志记录**: 添加详细的日志记录功能
