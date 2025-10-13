from multiprocessing import Manager, Process
import time

def worker1(shared_list, shared_dict):
    for i in range(5):
        shared_list.append(i)
        shared_dict[f'key_{i}'] = i * 2
        time.sleep(0.1)

def worker2(shared_list, shared_dict):
    for i in range(5, 10):
        shared_list.append(i)
        shared_dict[f'key_{i}'] = i * 3
        time.sleep(0.1)

if __name__ == "__main__":
    with Manager() as manager:
        shared_list = manager.list()
        shared_dict = manager.dict()
        
        p1 = Process(target=worker1, args=(shared_list, shared_dict))
        p2 = Process(target=worker2, args=(shared_list, shared_dict))
        
        p1.start()
        p2.start()
        
        p1.join()
        p2.join()
        
        print("Shared list:", list(shared_list))
        print("Shared dict:", dict(shared_dict))