# -*- coding: utf-8 -*-
from multiprocessing import Pool
import time
# 训练过程
def worker(start,end):
    # 载入预处理过得文件和模型、向量
    print range(5)
    time.sleep(5)
if __name__ == '__main__':
    # 分五个进程
    pool=Pool(processes=5)
    for i in range(0, 20000, 4000):
        result = pool.apply_async(worker, (i,i+4000))
    pool.close()
    pool.join()
    if result.successful():
        print 'successful'