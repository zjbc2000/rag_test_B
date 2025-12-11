# rag_test_B
构建了完整的 FastAPI 向量检索示例，包含文本切块、向量化入库、检索返回及异步 SQLite 日志记录，采用 Chroma 持久化向量存储与 sentence-transformers 预设模型。项目结构、依赖与运行说明写入 README.md
关键位置：
接口定义与逻辑：app/api/routes.py（/ingest 入库，/search 检索+异步日志）。
配置与依赖：app/config.py、app/dependencies.py。
组件：app/services/chunker.py（切块）、embedder.py（向量化）、vector_store.py（Chroma 封装）、log_repo.py（检索日志 SQLite）。
入口：main.py（启动、CORS、预热模型、路由挂载）。

