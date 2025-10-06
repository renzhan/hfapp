from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from typing import Optional

app = FastAPI(title="Hugging Face Callback API", version="1.0.0")

@app.get("/huggingface")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "Hugging Face Callback API",
        "version": "1.0.0",
        "endpoints": {
            "callback": "/huggingface/callback",
            "docs": "/docs"
        }
    }

@app.get("/huggingface/callback")
async def huggingface_callback(
    code: Optional[str] = Query(None, description="授权码"),
    state: Optional[str] = Query(None, description="状态参数"),
    error: Optional[str] = Query(None, description="错误信息"),
    error_description: Optional[str] = Query(None, description="错误描述")
):
    """
    处理 Hugging Face OAuth 回调
    
    参数:
    - code: 授权码，用于换取访问令牌
    - state: 状态参数，用于防止CSRF攻击
    - error: 错误代码（如果有错误）
    - error_description: 错误描述（如果有错误）
    """
    
    # 检查是否有错误
    if error:
        error_msg = f"OAuth错误: {error}"
        if error_description:
            error_msg += f" - {error_description}"
        raise HTTPException(status_code=400, detail=error_msg)
    
    # 检查是否收到授权码
    if not code:
        raise HTTPException(status_code=400, detail="缺少授权码参数")
    
    # 这里可以添加更多处理逻辑，比如：
    # 1. 验证state参数
    # 2. 使用code换取访问令牌
    # 3. 存储令牌到数据库
    # 4. 重定向到前端应用
    
    return {
        "message": "成功接收到Hugging Face回调",
        "code": code,
        "state": state,
        "next_steps": "可以使用此授权码换取访问令牌"
    }

@app.get("/huggingface/callback/html", response_class=HTMLResponse)
async def huggingface_callback_html(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    error_description: Optional[str] = Query(None)
):
    """
    处理 Hugging Face OAuth 回调，返回HTML页面
    适用于需要在浏览器中显示结果的场景
    """
    
    if error:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hugging Face 授权错误</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ color: red; background: #ffe6e6; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Hugging Face 授权失败</h1>
            <div class="error">
                <h3>错误: {error}</h3>
                <p>{error_description or '未知错误'}</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=400)
    
    if not code:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hugging Face 授权错误</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ color: red; background: #ffe6e6; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Hugging Face 授权失败</h1>
            <div class="error">
                <h3>错误: 缺少授权码</h3>
                <p>回调请求中没有包含授权码参数</p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=400)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hugging Face 授权成功</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .success {{ color: green; background: #e6ffe6; padding: 20px; border-radius: 5px; }}
            .code {{ background: #f0f0f0; padding: 10px; border-radius: 3px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <h1>Hugging Face 授权成功</h1>
        <div class="success">
            <h3>授权码已接收</h3>
            <p>授权码: <span class="code">{code}</span></p>
            {f'<p>状态参数: <span class="code">{state}</span></p>' if state else ''}
            <p>现在可以使用此授权码换取访问令牌</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
