# rag_test_B
构建了完整的 FastAPI 向量检索示例，包含文本切块、向量化入库、检索返回及异步 SQLite 日志记录，采用 Chroma 持久化向量存储与 sentence-transformers 预设模型。项目结构、依赖与运行说明写入 README.md，新增健康检查 /health。
关键位置：
接口定义与逻辑：app/api/routes.py（/ingest 入库，/search 检索+异步日志）。
配置与依赖：app/config.py、app/dependencies.py。
组件：app/services/chunker.py（切块）、embedder.py（向量化）、vector_store.py（Chroma 封装）、log_repo.py（检索日志 SQLite）。
入口：main.py（启动、CORS、预热模型、路由挂载）。
本地运行：
1) cd C:\Users\ASUS\Workspaces\fastapi-vector-demo
2) python -m venv .venv 并激活；pip install -r requirements.txt
3) uvicorn main:app --reload，访问 http://127.0.0.1:8000/docs
4) 示例：
入库：POST /ingest，body: {"text":"示例文本","source":"demo"}
检索：POST /search，body: {"query":"关键词","top_k":3}，日志写入 data/search_logs.db
向量模型首次运行会自动下载 all-MiniLM-L6-v2，请保持网络畅通。
关于仓库上传：当前环境无法直接替你推送，请在目录内执行 git init && git add . && git commit -m "Add FastAPI vector demo"，然后 git remote add origin <你的GitHub/Gitee仓库URL> 并 git push -u origin master/main 完成公开托管。
如需改用其他向量模型/库，可在 .env 或 app/config.py 中调整相关配置。
