# 存在依赖冲突：crawl4ai 0.7.6 requires anyio>=4.0.0, but you have anyio 3.7.1(this project needs this version) which is incompatible.

# 新闻处理后端 API

## 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 运行服务

```bash
python main.py
```

或者使用 uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
```

## API 接口

### 1. 保存新闻接口

**POST** `/api/save-news`

**请求体：**

```json
{
  "news_list": [
    [1, "新闻内容1"],
    [2, "新闻内容2"],
    ...
  ]
}
```

**响应：**

```json
{
  "success": true,
  "saved_count": 2,
  "total_count": 2,
  "message": "成功保存 2 条新闻",
  "errors": null
}
```

### 2. 健康检查接口

**GET** `/api/health`

**响应：**

```json
{
  "status": "ok",
  "message": "服务运行正常"
}
```

## 新闻分类映射

新闻分类编号 1-19 对应的文件名：

1. 1.语音模型
2. 2.计算机视觉模型
3. 3.自然语言处理模型
4. 4.多模态模型
5. 5.强化学习模型
6. 6.生成式AI模型
7. 7.推荐系统模型
8. 8.知识图谱模型
9. 9.图神经网络模型
10. 10.时间序列模型
11. 11.异常检测模型
12. 12.联邦学习模型
13. 13.迁移学习模型
14. 14.元学习模型
15. 15.自监督学习模型
16. 16.对比学习模型
17. 17.可解释AI模型
18. 18.边缘计算模型
19. 19.其他

文件保存在 `backend/data/` 目录下，格式为 `{分类名称}.md`

## 注意事项

- 文件路径和文件名可以在 `main.py` 中的 `NAME_MAP` 和 `DATA_DIR` 变量中修改
- 默认文件保存路径为 `backend/data/`
- 文件以追加模式写入，不会覆盖已有内容
