# JaNLP 内存管理和不足应对策略

## 内存使用分析

### 基础内存需求

1. **jamdict 数据库文件**：~300MB
2. **每个线程的 jamdict 实例**：~50-100MB
3. **SQLite 缓存**：10MB (PRAGMA cache_size=10000)
4. **内存映射**：256MB (PRAGMA mmap_size=268435456)
5. **Python 运行时**：~50-100MB
6. **FastAPI 框架**：~20-50MB

### 总内存估算

- **单线程最小**：~400MB
- **5个并发线程**：~800MB-1.2GB
- **10个并发线程**：~1.5GB-2GB

## 内存不足的影响

### 1. SQLite 性能下降

```python
# 当内存不足时，SQLite 会：
conn.execute("PRAGMA cache_size=10000")  # 缓存可能被强制减小
conn.execute("PRAGMA mmap_size=268435456")  # 内存映射失败
```

**症状**：
- 查询速度显著下降
- 磁盘 I/O 增加
- 响应时间从 50ms 增加到 500ms+

### 2. 系统级内存压力

**可能发生**：
- 操作系统开始使用 swap
- 进程被 OOM Killer 终止
- 容器被 Kubernetes 重启

### 3. 线程初始化失败

```python
def _get_jamdict():
    try:
        conn = sqlite3.connect(_db_path, check_same_thread=True)
        _optimize_sqlite_connection(conn)  # 可能失败
        _thread_local.jam = Jamdict(db_conn=conn)
    except MemoryError:
        logger.error("Memory allocation failed for jamdict connection")
        raise
```

## 内存监控和预警

让我添加内存监控功能： 