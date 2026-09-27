import sqlite3, json, threading
from pathlib import Path
from datetime import datetime, timezone

class Store:
    def __init__(self, path="data/agents.db"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.path=path; self.lock=threading.Lock()
        with self._db() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS events(
              id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, agent TEXT,
              summary TEXT, importance INTEGER, payload TEXT, created_at TEXT)""")
    def _db(self): return sqlite3.connect(self.path)
    def add(self,kind,agent,summary,importance=0,payload=None):
        with self.lock, self._db() as c:
            c.execute("INSERT INTO events(kind,agent,summary,importance,payload,created_at) VALUES(?,?,?,?,?,?)",
              (kind,agent,summary,importance,json.dumps(payload or {}),datetime.now(timezone.utc).isoformat()))
    def recent(self,limit=100):
        with self._db() as c:
            rows=c.execute("SELECT id,kind,agent,summary,importance,payload,created_at FROM events ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
        return [{"id":r[0],"kind":r[1],"agent":r[2],"summary":r[3],"importance":r[4],"payload":json.loads(r[5]),"created_at":r[6]} for r in rows]
store=Store()
