# 开发时间：2024/7/5 20:41
import re
from typing import Union
import numpy as np
import random
def extract_number(args, text: str) -> Union[float, None]:
    text = text.replace(',', '')
    pred = [s for s in re.findall(r'-?\d+\.?\d*', text)]
    if pred:
        pred_answer = float(pred[-1])
    else:
        pred_answer = None
    return pred_answer

def extract_answer(args, text):
    dataset = args.dataset.lower()
    if dataset in ["svamp", "gsm8k", "multiarith", "addsub", "singleeq"]:
        pred_answer = extract_number(args, text)
    elif dataset == "commonsenseqa":
        pred = text.strip()
        pred = re.sub("\(|\)|\:|\.|\,", "", pred)
        pred = pred.split()
        pred_answer = [i for i in pred if i in ('A|B|C|D|E')][-1]
        # pred_answer = re.findall(r'A|B|C|D|E', pred)[0]
        return pred_answer
    elif dataset == "aqua":
        pred = text.strip()
        pred_answer = re.findall(r'A|B|C|D|E', pred)[0]
        return pred_answer
    elif dataset == "strategyqa" or dataset == 'coin_flip':
        pred = text.lower()
        pred = re.sub("\"|\'|\n|\.|\s|\:|\,", " ", pred)
        pred = pred.split()
        pred_answer = [i for i in pred if i in ("yes", "no")][-1]
        return pred_answer
    elif dataset == "last_letters":
        pred = re.sub("\"|\'|\n|\.|\s", "", text)
        pred_answer = pred
        return pred_answer
    else:
        raise NotImplementedError(' not support dataset: {}'.format(dataset))
    if isinstance(pred_answer, str):
        try:
            pred_answer = float(pred_answer)
        except ValueError as e:
            pred_answer = float('inf')
    return pred_answer


def get_precision(gt_ans: float) -> int:
    precision = 5
    if '.' in str(gt_ans):
        precision = len(str(gt_ans).split('.')[-1])
    return precision

# 基于索引分配权重
def assign_index_weight(sentences, index_list):
    max_weight = 100
    n = len(sentences)

    # 按照 index_list 中的顺序分配权重
    weights = [0] * len(sentences)
    for rank, idx in enumerate(index_list):
        weights[idx] = max_weight - (rank * max_weight // (n - 1))

    return weights

def count_numbers(sentence):
    return len(re.findall(r'\d+', sentence))

# 基于句子中的数字个数分配权重
def assign_number_weight(sentences):
    number_counts = [count_numbers(sentence) for sentence in sentences]
    max_count = max(number_counts) if (max(number_counts)!=0)else 1  # 防止除零
    max_weight = 100
    return [(count / max_count) * max_weight for count in number_counts]

# 结合两种权重（可以通过加权平均或乘积等方式组合）
def combine_weights(index_weights, number_weights, alpha=0.3):
    # alpha 控制两种权重的相对重要性
    return [(alpha * i_w + (1 - alpha) * n_w) for i_w, n_w in zip(index_weights, number_weights)]


def reduce_max_weight(weights, decrement_range=(2, 4)):
    # 找到最大权重的索引和值
    max_weight_index = np.argmax(weights)
    max_weight = weights[max_weight_index]

    # 生成一个指定范围内的随机值
    random_decrement = random.uniform(*decrement_range)

    # 减少最大权重，并确保其不小于 0
    weights[max_weight_index] = max(max_weight - random_decrement, 0)

    return weights

def filter_answer(out):
    n_list = re.split(r'[,\.]', out)
    n_list = [item for item in n_list if item]
    num = len(n_list)
    print(n_list)
    print(num)
    if (num > 3):
        pass  # 进入fiter阶段
        # fileter 阶段
        # 我们从num个句子中选择n/3个元素,这里选择n/3是因为我们理论上不能
        # 超过n个而我们每个被选中的元素都要选上下那个元素捆版，所以为了有随机性,我们选择n/4
        #

        subset = random.sample(n_list
                               , num // 4)
        # 把subset元素对应的上下的句子拿出来
        print(subset)
        print(len(subset))
        nested_list = []
        index_set = []
        for element in subset:
            # 某个特定元素的索引
            index = n_list.index(element)
            index_set.append(index)
            # 假如刚好取到最后一个跟第一个
            if index == (len(n_list) - 1):
                nested_list.append((n_list[index], n_list[index - 1], n_list[index - 2]))
            elif index == 0:
                nested_list.append((n_list[index],n_list[index + 1],n_list[index+2]))
            else:
                nested_list.append((n_list[index - 1], n_list[index], n_list[index + 1]))
        print(nested_list)
        print(len(nested_list))
        print(index_set)
        print(len(index_set))
        # 1. 基于索引分配权重
        index_weights = assign_index_weight(n_list, index_set)

        # 2. 基于句子中的数字数量分配权重
        number_weights = assign_number_weight(subset)

        # 3. 结合两种权重
        combined_weights = combine_weights(index_weights, number_weights, alpha=0.3)

        # 4. 减少权重列表中最大值的函数
        modified_weights = reduce_max_weight(combined_weights)

        weighted_nested_list = []
        for sentence, weight in zip(nested_list, modified_weights):
            # 将每个元组(sentence)和对应的权重(weight)打包成新的元组
            weighted_nested_list.append((f"Sentence: '{sentence}', Weight: {weight:.4f}"))
            # 打印每个句子和对应的权重
            print(f"Sentence: '{sentence}', Weight: {weight:.4f}")
        print(weighted_nested_list)
    else:
        pass
        # 直接进入supervisor阶段