# news-classification-ai
自动将以一段话为单位，换行符为分割的多段话自动分类并存放到对应类别txt文件的ai助手。An AI assistant that automatically classifies multi-paragraph texts—segmented by line breaks into individual paragraphs—and saves them into corresponding category-specific TXT files.


# 新闻处理代理 (news_process_agent)

一个基于 AI 的新闻自动分类与整理系统。用户粘贴多条 AI 相关新闻，AI 自动为每条新闻分配一个分类，系统按分类排序后，将新闻追加保存到对应的 Markdown 文件中。

## 功能特性

- **批量新闻分类**：输入多条新闻（每行一条），AI 自动识别每条新闻所属的 17 个分类之一
- **并发 AI 请求**：使用 `Promise.all` 并发处理所有新闻，提高处理效率
- **可视化展示**：分类结果以"分类编号 + 新闻内容"的长条形卡片形式展示，直观清晰
- **自动排序**：按分类编号对新闻进行重排，相同分类的新闻自动聚拢
- **自动归档**：按分类将新闻追加写入对应的 Markdown 文件（Obsidian 笔记库），不会覆盖已有内容

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 前端 | Vue 3 + TypeScript + Vite + Vue Router + Axios |
| 后端 | FastAPI (Python) |
| AI 服务 | SpringAI or Langchain（外部服务，不在本仓库内） |
| 数据存储 | 本地 Markdown 文件（Obsidian Vault） |

## 服务与端口

| 服务 | 端口 | 说明 |
| --- | --- | --- |
| Vite 开发服务器 | 5173 | 前端 |
| SpringAI or Langchain 服务 | 8081 | AI 聊天接口（需自行部署，不在本仓库） |
| FastAPI 服务 | 8083 | 后端保存接口 |

> **注意**：完整流程需要 LLM api 服务运行在 `localhost:8081`，否则 AI 分类步骤会失败。

## 系统架构与数据流程


用户输入新闻内容
    ↓
SearchPage.vue（文本预处理：合并换行、去尾空格）
    ↓ 路由跳转 /textbox?content=xxx
TextBoxPage.vue
    ↓ handleStart() 按换行分割 → newsList[]
    ↓ processNewsWithAI() 并发请求 AI（GET /ai/chat）
    ↓ SpringAI or Langchain 返回分类编号 → analysisList[]
    ↓ transformToNewsBars() 可视化展示
    ↓ sort() 排序 → finallist[[分类编号, 新闻内容]]
    ↓ append() → saveNews()
    ↓ POST /api/save-news (FastAPI, 8083)
    ↓ 验证 → 文件名映射 → 追加写入 Markdown 文件


## 目录结构
```

├── backend/                    # FastAPI 后端
│   ├── main.py                 # 后端主服务（保存新闻到 Markdown 文件）
│   ├── requirements.txt        # Python 依赖
│   └── README.md               # 后端说明（部分内容已过时，见"注意事项"）
├── src/
│   ├── api/
│   │   ├── api.js              # API 调用封装（LLM API + FastAPI）
│   │   └── api.d.ts            # 类型声明
│   ├── utils/
│   │   ├── prompts.js          # AI 提示词配置（17 个分类类目）
│   │   └── prompts.d.ts        # 类型声明
│   ├── views/
│   │   ├── SearchPage.vue      # 输入页面（首页）
│   │   └── TextBoxPage.vue     # 处理页面（分类、排序、保存）
│   ├── router/index.ts         # 路由配置
│   ├── App.vue
│   └── main.ts
└── 项目实现逻辑框架.md          # 详细实现逻辑设计文档
```

## 快速开始

### 前端

```bash
# 安装依赖
npm install

# 启动开发服务器（热更新）
npm run dev

# 构建生产版本（含类型检查）
npm run build

# 代码检查（自动修复）
npm run lint

# 代码格式化
npm run format
```

### 后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务（默认端口 8083）
python main.py
# 或使用 uvicorn 热重载模式：
uvicorn main:app --host 0.0.0.0 --port 8083 --reload
```

### SpringAI 服务

AI 服务为外部依赖，需自行部署并保证在 `localhost:8081` 提供服务，接口为 `GET /ai/chat?prompt=xxx&chatId=xxx`。

## API 接口

### 1. 保存新闻 `POST /api/save-news`

**请求体：**

```json
{
  "news_list": [
    [3, "- 新闻内容一"],
    [1, "- 新闻内容二"]
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

### 2. 健康检查 `GET /api/health`

```json
{
  "status": "ok",
  "message": "服务运行正常"
}
```

## 分类体系

系统使用 17 个分类类目，每个分类对应一个 Markdown 文件：

| 编号 | 分类名称 |
| --- | --- |
| 1 | 语音·音频识别与合成-非商业项目 |
| 2 | 计算机视觉分析-生成模型不算入其中-非商业 |
| 3 | 大语言模型，agent智能体-非商业 |
| 4 | 图片生成模型-非商业 |
| 5 | 音频生成模型-非商业 |
| 6 | 视频生成模型-非商业 |
| 7 | 3d人物物品生成模型-非商业 |
| 8 | 3D环境生成模型-世界模型-非商业 |
| 9 | 多模态ai模型相关-非商业 |
| 10 | AI 终端技术或项目 |
| 11 | 模型记忆相关 |
| 12 | AI安全与对齐 |
| 13 | Extended Reality和脑机接口 |
| 14 | 科技趋势分析以及名人言论 |
| 15 | 评测基准与比赛 |
| 16 | AI软件创业项目-商业项目 |
| 17 | 其他 |


## 文件保存位置

保存的目标目录在 `backend/main.py` 的 `DATA_DIR` 变量中配置，默认指向用户的 Obsidian 笔记库路径（`ai技术的突破进展` 目录），每个分类对应一个 `.md` 文件，以追加模式写入。

如需修改保存位置或分类映射，请修改 `backend/main.py` 中的 `DATA_DIR` 和 `NAME_MAP`。

## 注意事项

- **分类映射同步**：前端提示词（`src/utils/prompts.js`）与后端文件名映射（`backend/main.py` 的 `NAME_MAP`）中的分类列表需要保持一致
- **后端 README 已过时**：`backend/README.md` 中的端口号（写了 8081）和分类列表（写了 19 类）与当前代码不一致，请以本文档及实际代码为准
- **类型声明**：`api.js` 与 `prompts.js` 为纯 JS 文件，配有手写的 `.d.ts` 类型声明，修改 JS 时需同步更新声明文件
- **保存路径**：实际写入路径为 `DATA_DIR` 指定的绝对路径，而非 `backend/data/`

## 使用流程

1. 在首页输入框中粘贴多条新闻（每行一条），点击"发送"或按 `Shift + Enter` / `Ctrl + Enter`
2. 在处理页面点击"开始"，等待 AI 完成分类分析
3. 查看左侧的分类结果可视化展示
4. 点击"重排"按分类编号排序
5. 点击"追加"将新闻保存到对应的 Markdown 文件
6. 点击"返回"回到输入页面

### 主要改动总结

| 问题 | 修复 |
|------|------|
| 代码块没有语言标识 | 添加了 `bash`、`python`、`json` |
| 表格前缺少空行 | 每个表格前都加了空行 |
| 分类表格用字符画 | 改成标准 Markdown 表格 |
| 流程图用了缩进文本 | 用 ` ``` ` 代码块包裹 |
| 尾部有 `---` | 直接删掉（README 不需要） |
| 列表项有缩进不一致 | 统一成 2 空格缩进 |

