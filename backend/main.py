from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple
from pathlib import Path
import os

app = FastAPI(title="新闻处理API", version="1.0.0")

# 配置CORS，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

# 新闻分类编号到文件名的映射表
NAME_MAP = {
    1: "1.语音·音频识别与合成-非商业项目",
    2: "2.计算机视觉分析-生成模型不算入其中-非商业",
    3: "3.大语言模型，agent智能体-非商业",
    4: "4.图片生成模型-非商业",
    5: "5.音频生成模型-非商业",
    6: "6.视频生成模型-非商业",
    7: "7.3d人物物品生成模型-非商业",
    8: "8.3D环境生成模型-世界模型-非商业",
    9: "9.多模态ai模型相关-非商业",
    10: "10.AI 终端技术或项目",
    11: "11.模型记忆相关",
    12: "12.AI安全与对齐",
    13: "13.Extended Reality和脑机接口",
    14: "14.科技趋势分析以及名人言论",
    15: "15.评测基准与比赛",
    16: "16.ai软件创业项目-商业项目",
    17: "17.其他"
}







# 实际仓库路径：/media/bill/新加卷/Users/Bill Chou/Documents/Obsidian Vault/ubuntu/学习笔记合集1/科技新闻收集与观察/ai技术的突破进展
# 测试路径：/home/bill/桌面/ai技术的进展突破
# 确保data目录存在
DATA_DIR = Path("/media/bill/新加卷/Users/Bill Chou/Documents/Obsidian Vault/ubuntu/学习笔记合集1/科技新闻收集与观察/ai技术的突破进展")
DATA_DIR.mkdir(exist_ok=True)


class NewsItem(BaseModel):
    """单个新闻项模型"""
    category_id: int  # 新闻分类编号
    content: str      # 新闻内容


class NewsListRequest(BaseModel):
    """新闻列表请求模型"""
    news_list: List[List]  # 二维列表，格式: [[分类编号, 新闻内容], ...]


@app.post("/api/save-news")
async def save_news(request: NewsListRequest):
    """
    保存新闻到本地文件
    
    接收一个二维列表，格式: [[分类编号, 新闻内容], ...]
    根据分类编号将新闻内容写入对应的文件
    """
    try:
        saved_count = 0
        errors = []
        
        for item in request.news_list:
            if not isinstance(item, list) or len(item) < 2:
                errors.append(f"无效的数据项: {item}")
                continue
            
            num = item[0]
            text = item[1]
            
            # 验证分类编号
            if not isinstance(num, int) or num < 1 or num > 19:
                errors.append(f"无效的分类编号: {num}")
                continue
            
            # 验证新闻内容
            if not isinstance(text, str) or not text.strip():
                errors.append(f"分类编号 {num} 的新闻内容为空")
                continue
            
            # 获取文件名
            file_name = NAME_MAP.get(num) or f"{num}.未知分类"
            
            # 构建文件路径
            file_path = DATA_DIR / f"{file_name}.md"
            
            # 写入文件（追加模式）
            try:
                with file_path.open("a", encoding="utf8") as f:
                    f.write(f"\n{text}\n")
                saved_count += 1
            except Exception as e:
                errors.append(f"写入文件 {file_name}.md 时出错: {str(e)}")
        
        # 返回结果
        result = {
            "success": True,
            "saved_count": saved_count,
            "total_count": len(request.news_list),
            "errors": errors if errors else None
        }
        
        if errors:
            result["message"] = f"成功保存 {saved_count} 条新闻，但有 {len(errors)} 个错误"
        else:
            result["message"] = f"成功保存 {saved_count} 条新闻"
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "message": "服务运行正常"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)

