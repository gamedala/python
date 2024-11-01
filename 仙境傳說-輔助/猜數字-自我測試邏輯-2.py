import itertools
import random
import math
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

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

def 機率計算(高概率數字清單):
    # 計算每個數字的出現次數
    counter = Counter(高概率數字清單)
    
    # 取得出現次數最多的前十個三位數
    top_10 = [num for num, _ in counter.most_common(20)]  # most_common返回出現次數最多的前N個
    return top_10

# 猜數字遊戲主循環
def guess_number_game(高概率數字清單):
    all_possible = generate_all_possible()  # 所有可能的解
    錯誤 = 0
    正確 = 0
    for i in range(100):
        answer = random.choice(all_possible)  # 隨機選擇一個初始猜測數字
        possible_list = all_possible[:]  # 可能的解空间
        all_candidates = all_possible[:]  # 候选猜测集合
        guess_count = 0  # 猜測次數
        高概率數字 = 機率計算(高概率數字清單)
        while guess_count != 5:  # 保證在5次內猜中
            guess_count += 1
            if guess_count == 1:
                # if 高概率數字清單:
                #     guess = random.choice(高概率數字)  # 優先從高概率數字清單中選擇猜測
                # else:
                    guess = random.choice(all_possible)  # 否則隨機選擇一個初始猜測數字
            elif len(possible_list) == 1:  # 如果只剩下一個可能的選擇，直接猜測
                guess = possible_list[0]
            else:
                guess = select_next_guess(possible_list, all_candidates)  # 使用熵策略選擇下一次猜測
            A, B = get_feedback(guess, answer)  # 根據猜測結果獲取反饋

            if A == 3:
                正確 += 1
                高概率數字清單.append(guess)  # 猜中後將該數字加入高概率清單
                break

            possible_list = filter_possible(possible_list, guess, A, B)  # 更新剩余的可能解
            if guess_count == 5 and A != 3:
                錯誤 += 1
                break
    return 正確, 錯誤

# 多進程猜數字遊戲
def multi_process_guess_game(thread_id, 高概率數字清單):
    global 淨賺
    正確, 錯誤 = guess_number_game(高概率數字清單)
    賺 = (正確*4) - (錯誤*16)
    return f" 正確 {正確} 錯誤 {錯誤} 賺多少 {賺}",賺

# 設置共享變量
淨賺 = 0
高概率數字清單 = []  # 用於存放高概率正確數字的清單

# 使用 ProcessPoolExecutor 创建多进程任务
if __name__ == '__main__':
    manager = multiprocessing.Manager()  # 創建一個Manager來管理共享變量
    高概率數字清單 = manager.list()  # 共享的高概率數字清單
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(multi_process_guess_game, i, 高概率數字清單) for i in range(30)]
        for future in as_completed(futures):
            result,賺 = future.result()
            淨賺 += 賺
            print(result)
    print(f"最終淨賺 {淨賺}")