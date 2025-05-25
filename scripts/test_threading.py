#!/usr/bin/env python3
"""
测试线程本地存储的 jamdict 实现
"""
import sys
import threading
import time
sys.path.append('janlp')

from janlp import utils

def test_lookup():
    thread_id = threading.current_thread().ident
    print(f'Thread {thread_id}: Starting lookup')
    start = time.time()
    result = utils.lookup_word(lemma='こんにちは')
    end = time.time()
    print(f'Thread {thread_id}: Lookup completed in {end-start:.3f}s, found {len(result.meanings)} meanings')

if __name__ == "__main__":
    print('Testing thread-local jamdict...')
    utils.init_jamdict()
    
    # Test with multiple threads
    threads = []
    for i in range(3):
        t = threading.Thread(target=test_lookup)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print('All tests completed successfully!') 