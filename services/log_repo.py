import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import aiosqlite


class SearchLogRepo:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS search_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    query_text TEXT NOT NULL,
                    top_k INTEGER NOT NULL,
                    latency_ms REAL,
                    requester_ip TEXT,
                    user_agent TEXT,
                    results_json TEXT
                )
                """
            )
            await db.commit()

    async def write_log(
        self,
        *,
        query_text: str,
        top_k: int,
        latency_ms: float,
        requester_ip: Optional[str],
        user_agent: Optional[str],
        results: List[Dict[str, Any]],
    ) -> None:
        payload = {
            "query_text": query_text,
            "top_k": top_k,
            "latency_ms": latency_ms,
            "requester_ip": requester_ip,
            "user_agent": user_agent,
            "results": results,
        }
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO search_logs (created_at, query_text, top_k, latency_ms, requester_ip, user_agent, results_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    query_text,
                    top_k,
                    latency_ms,
                    requester_ip,
                    user_agent,
                    json.dumps(payload, ensure_ascii=False),
                ),
            )
            await db.commit()

