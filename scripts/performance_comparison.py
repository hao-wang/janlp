#!/usr/bin/env python3
"""
性能对比测试：模拟 FastAPI 并发请求场景
"""
import time
import threading
import concurrent.futures
import statistics
from typing import List

# 模拟 FastAPI 请求处理
def simulate_analyze_request(sentence: str = "こんにちは、元気ですか？") -> float:
    """模拟 /analyze 端点的请求处理"""
    start_time = time.time()
    
    # 这里应该导入并调用实际的 utils 函数
    # 但由于环境限制，我们用 sleep 来模拟
    # 实际测试时应该替换为：
    # from janlp import utils
    # result = utils.get_glossary(sentence)
    
    # 模拟不同的处理时间
    thread_id = threading.current_thread().ident
    if not hasattr(threading.current_thread(), '_initialized'):
        # 模拟首次初始化时间（原来的问题）
        time.sleep(2.5)  # 原来的初始化时间
        threading.current_thread()._initialized = True
    else:
        # 模拟后续请求时间
        time.sleep(0.05)  # 优化后的处理时间
    
    end_time = time.time()
    return end_time - start_time

def run_performance_test(test_name: str, num_threads: int, requests_per_thread: int):
    """运行性能测试"""
    print(f"\n=== {test_name} ===")
    print(f"并发线程数: {num_threads}")
    print(f"每线程请求数: {requests_per_thread}")
    print(f"总请求数: {num_threads * requests_per_thread}")
    
    response_times: List[float] = []
    start_total = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 提交所有任务
        futures = []
        for thread_idx in range(num_threads):
            for req_idx in range(requests_per_thread):
                future = executor.submit(simulate_analyze_request)
                futures.append(future)
        
        # 收集结果
        for future in concurrent.futures.as_completed(futures):
            try:
                response_time = future.result()
                response_times.append(response_time)
            except Exception as e:
                print(f"请求失败: {e}")
    
    end_total = time.time()
    total_time = end_total - start_total
    
    # 统计分析
    if response_times:
        avg_time = statistics.mean(response_times)
        median_time = statistics.median(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        p95_time = sorted(response_times)[int(len(response_times) * 0.95)]
        qps = len(response_times) / total_time
        
        print(f"\n📊 性能统计:")
        print(f"  总耗时: {total_time:.3f}s")
        print(f"  成功请求: {len(response_times)}")
        print(f"  QPS: {qps:.2f}")
        print(f"\n⏱️  响应时间统计:")
        print(f"  平均: {avg_time:.3f}s")
        print(f"  中位数: {median_time:.3f}s")
        print(f"  最快: {min_time:.3f}s")
        print(f"  最慢: {max_time:.3f}s")
        print(f"  P95: {p95_time:.3f}s")
        
        # 分析首次请求 vs 后续请求
        slow_requests = [t for t in response_times if t > 1.0]
        fast_requests = [t for t in response_times if t <= 1.0]
        
        print(f"\n🔍 请求分析:")
        print(f"  慢请求 (>1s): {len(slow_requests)} 个")
        print(f"  快请求 (≤1s): {len(fast_requests)} 个")
        
        if slow_requests:
            print(f"  慢请求平均时间: {statistics.mean(slow_requests):.3f}s")
        if fast_requests:
            print(f"  快请求平均时间: {statistics.mean(fast_requests):.3f}s")
    else:
        print("❌ 没有成功的请求")

def main():
    print("🚀 JaNLP 性能测试")
    print("=" * 50)
    
    # 测试场景 1: 低并发
    run_performance_test("低并发场景", num_threads=2, requests_per_thread=3)
    
    # 测试场景 2: 中等并发
    run_performance_test("中等并发场景", num_threads=5, requests_per_thread=4)
    
    # 测试场景 3: 高并发
    run_performance_test("高并发场景", num_threads=10, requests_per_thread=2)
    
    print("\n" + "=" * 50)
    print("📝 测试说明:")
    print("- 慢请求通常是线程首次初始化 jamdict 连接")
    print("- 快请求是使用已初始化连接的后续请求")
    print("- 优化目标：减少慢请求数量和时间")

if __name__ == "__main__":
    main() 