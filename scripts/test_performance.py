#!/usr/bin/env python3
"""
性能测试脚本：测试 jamdict 连接池的性能改进
"""
import time
import threading
import concurrent.futures
from janlp import utils

def test_lookup_performance(test_name: str, num_threads: int = 5, num_requests: int = 10):
    """测试字典查找性能"""
    print(f"\n=== {test_name} ===")
    
    # 初始化
    utils.init_tagger()
    utils.init_jamdict()
    
    def single_lookup():
        start_time = time.time()
        result = utils.lookup_word(lemma="こんにちは")
        end_time = time.time()
        return end_time - start_time
    
    # 预热
    print("预热中...")
    single_lookup()
    
    # 并发测试
    print(f"开始并发测试：{num_threads} 个线程，每个线程 {num_requests} 次请求")
    
    all_times = []
    start_total = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_threads):
            for _ in range(num_requests):
                futures.append(executor.submit(single_lookup))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                lookup_time = future.result()
                all_times.append(lookup_time)
            except Exception as e:
                print(f"请求失败: {e}")
    
    end_total = time.time()
    
    # 统计结果
    if all_times:
        avg_time = sum(all_times) / len(all_times)
        min_time = min(all_times)
        max_time = max(all_times)
        total_time = end_total - start_total
        
        print(f"总请求数: {len(all_times)}")
        print(f"总耗时: {total_time:.3f}s")
        print(f"平均响应时间: {avg_time:.3f}s")
        print(f"最快响应时间: {min_time:.3f}s")
        print(f"最慢响应时间: {max_time:.3f}s")
        print(f"QPS: {len(all_times) / total_time:.2f}")
    else:
        print("没有成功的请求")

if __name__ == "__main__":
    test_lookup_performance("连接池性能测试", num_threads=10, num_requests=5) 