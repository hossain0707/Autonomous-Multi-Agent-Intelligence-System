import sqlite3, json, threading
from pathlib import Path
from datetime import datetime, timezone

class Store:
    def __init__(self, path="data/agents.db"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.path=path; self.lock=threading.Lock()
        with self._db() as c:
            c.executescript("""CREATE TABLE IF NOT EXISTS events(
              id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, agent TEXT,
              summary TEXT, importance INTEGER, payload TEXT, created_at TEXT);
            CREATE TABLE IF NOT EXISTS approvals(
              id TEXT PRIMARY KEY, agent TEXT, tool TEXT, arguments TEXT, reason TEXT,
              status TEXT, created_at TEXT, decided_at TEXT);
            CREATE TABLE IF NOT EXISTS schedules(
              id TEXT PRIMARY KEY, name TEXT, target TEXT, objective TEXT, payload TEXT,
              priority INTEGER, interval_seconds INTEGER, enabled INTEGER, next_run TEXT, last_run TEXT);""")
    def _db(self): return sqlite3.connect(self.path)
    def add(self,kind,agent,summary,importance=0,payload=None):
        with self.lock, self._db() as c:
            c.execute("INSERT INTO events(kind,agent,summary,importance,payload,created_at) VALUES(?,?,?,?,?,?)",
              (kind,agent,summary,importance,json.dumps(payload or {}),datetime.now(timezone.utc).isoformat()))
    def recent(self,limit=100):
        with self._db() as c:
            rows=c.execute("SELECT id,kind,agent,summary,importance,payload,created_at FROM events ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
        return [{"id":r[0],"kind":r[1],"agent":r[2],"summary":r[3],"importance":r[4],"payload":json.loads(r[5]),"created_at":r[6]} for r in rows]
    def create_approval(self, item):
        with self.lock, self._db() as c:
            c.execute("INSERT INTO approvals VALUES(?,?,?,?,?,?,?,?)",(item["id"],item["agent"],item["tool"],json.dumps(item["arguments"]),item["reason"],"pending",item["created_at"],None))
    def approvals(self,status="pending"):
        with self._db() as c:
            rows=c.execute("SELECT id,agent,tool,arguments,reason,status,created_at,decided_at FROM approvals WHERE status=? ORDER BY created_at DESC",(status,)).fetchall()
        return [{"id":r[0],"agent":r[1],"tool":r[2],"arguments":json.loads(r[3]),"reason":r[4],"status":r[5],"created_at":r[6],"decided_at":r[7]} for r in rows]
    def decide_approval(self, approval_id, status):
        now=datetime.now(timezone.utc).isoformat()
        with self.lock, self._db() as c:
            cur=c.execute("UPDATE approvals SET status=?,decided_at=? WHERE id=? AND status='pending'",(status,now,approval_id))
            return cur.rowcount == 1
    def add_schedule(self,item):
        with self.lock, self._db() as c:
            c.execute("INSERT INTO schedules VALUES(?,?,?,?,?,?,?,?,?,?)",(item["id"],item["name"],item["target"],item["objective"],json.dumps(item["payload"]),item["priority"],item["interval_seconds"],1,item["next_run"],None))
    def schedules(self,enabled_only=False):
        q="SELECT id,name,target,objective,payload,priority,interval_seconds,enabled,next_run,last_run FROM schedules"
        if enabled_only: q+=" WHERE enabled=1"
        with self._db() as c: rows=c.execute(q).fetchall()
        return [{"id":r[0],"name":r[1],"target":r[2],"objective":r[3],"payload":json.loads(r[4]),"priority":r[5],"interval_seconds":r[6],"enabled":bool(r[7]),"next_run":r[8],"last_run":r[9]} for r in rows]
    def mark_schedule_run(self,sid,next_run):
        now=datetime.now(timezone.utc).isoformat()
        with self.lock, self._db() as c: c.execute("UPDATE schedules SET last_run=?,next_run=? WHERE id=?",(now,next_run,sid))
store=Store()
