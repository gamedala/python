import threading
import itertools
import random
import math

# 生成所有可能的三位數字組合
def generate_all_possible():
    return [''.join(p) for p in itertools.permutations('123456789', 3)]

def get_feedback(guess, answer):
    A = sum(1 for g, a in zip(guess, answer) if g == a)
    B = sum(1 for g in guess if g in answer) - A
    return A, B

def filter_possible(possible_list, guess, A, B):
    return [p for p in possible_list if get_feedback(guess, p) == (A, B)]

def entropy(feedback_counts):
    total = sum(feedback_counts.values())
    return -sum((count/total) * math.log2(count/total) for count in feedback_counts.values())

# 選擇下一次猜測，使用期望值策略
def select_next_guess(possible_list, all_candidates):
    best_guess = None
    max_entropy = None
    for guess in all_candidates:
        feedback_counts = {}
        for answer in possible_list:
            feedback = get_feedback(guess, answer)
            feedback_counts[feedback] = feedback_counts.get(feedback, 0) + 1
        current_entropy = entropy(feedback_counts)  # 計算該猜測的熵值
        if max_entropy is None or current_entropy > max_entropy:  # 找到熵值最大化的猜測
            max_entropy = current_entropy
            best_guess = guess
    return best_guess

# 猜數字遊戲主循環
def guess_number_game():
    all_possible = generate_all_possible()  # 所有可能的解
    錯誤 = 0
    正確 = 0
    for i in range(100):
        answer = random.choice(all_possible)  # 隨機選擇一個初始猜測數字
        possible_list = all_possible[:]  # 可能的解空间
        all_candidates = all_possible[:]  # 候选猜测集合
        guess_count = 0  # 猜測次數

        while guess_count != 5:  # 保證在5次內猜中
            guess_count += 1
            if guess_count == 1:
                guess = random.choice(all_possible)  # 隨機選擇一個初始猜測數字
            elif len(possible_list) == 1:  # 如果只剩下一個可能的選擇，直接猜測
                guess = possible_list[0]
            else:
                guess = select_next_guess(possible_list, all_candidates)  # 使用熵策略選擇下一次猜測
            A, B = get_feedback(guess, answer)  # 根據猜測結果獲取反饋

            if A == 3:
                正確 += 1
                break

            possible_list = filter_possible(possible_list, guess, A, B)  # 更新剩余的可能解
            if guess_count == 5 and A != 3:
                錯誤 += 1
                break
    return 正確, 錯誤

# 多線程猜數字遊戲
def thread_guess_game(thread_id, lock):
    global 淨賺
    正確, 錯誤 = guess_number_game()
    賺 = (正確*4) - (錯誤*16)
    with lock:  # 使用鎖來確保對共享變量的安全操作
        淨賺 += 賺
        print(f"Thread-{thread_id}: 正確 {正確} 錯誤 {錯誤} 機率 {正確/100*100}% 賺多少: {賺} 淨賺多少: {淨賺}")

# 設置共享變量
淨賺 = 0
lock = threading.Lock()

# 創建多個線程
threads = []
for i in range(20):  # 創建10個線程
    thread = threading.Thread(target=thread_guess_game, args=(i, lock))
    threads.append(thread)
    thread.start()

# 等待所有線程完成
for thread in threads:
    thread.join()

print(f"最終淨賺: {淨賺}")
