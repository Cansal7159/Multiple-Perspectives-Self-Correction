# 开发时间：2024/7/5 13:06
import json
from config import args
import openai
import logging
from utils import write_json, print_now, load_data, print_exp, mkpath
from prompt import get_prompt,construct_input,get_repair_prompt,repair_output
from prediction_answer import get_answer
from extracter import extract_answer,get_precision

#当前的日期
now = print_now(1).split(' ')[0].replace('/', '-')

#创建的文件夹
Result_Folder = 'result/{}'.format(now)
mkpath('result')
mkpath(Result_Folder)
mkpath(f'{Result_Folder}/{args.dataset}')

Log_Folder = 'log/{}'.format(now)
mkpath('log')
mkpath(Log_Folder)
mkpath(f'{Log_Folder}/{args.dataset}')

#定义文件夹路径
Decoder_Error_File = f'{Result_Folder}/{args.dataset}-{args.prompt_id}-{args.repair_prompt_id}-{args.engine}_deco.json'
Predict_File = f'{Result_Folder}/{args.dataset}/-{args.prompt_id}-{args.repair_prompt_id}-{args.engine}.json'
Log_File = f'{Log_Folder}/{args.dataset}/-{args.prompt_id}-{args.repair_prompt_id}-{args.engine}.log'

# Decoder_Error_File = f'{Result_Folder}/{args.dataset}-{args.prompt_id}-{args.engine}_deco.json'
# Predict_File = f'{Result_Folder}/{args.dataset}/-{args.prompt_id}-{args.engine}.json'
# Log_File = f'{Log_Folder}/{args.dataset}/-{args.prompt_id}-{args.engine}.log'
#设置日志
formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
sh = logging.StreamHandler()
fh = logging.FileHandler(filename=Log_File)
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(fh)
logger.addHandler(sh)

def zero_shot():
    # 设定正确的数量以及读apikey
    correct = 0

    # apikey_list = json.load(open('apikey.json','r',encoding='utf-8'))
    # apikey = apikey_list[0]

    # 读入训练集的数据跟prompt
    question, answer, ids = load_data(args)
    _, prompt = get_prompt()
    _, correction_prompt = get_repair_prompt()
    for idx, element in enumerate(question):

        # first
        inputs = construct_input(prompt,element)
        get_result,pred = get_answer(args,inputs)

        # repair
        inputs1 = repair_output(correction_prompt,element,pred)
        _, pred1 = get_answer(args,inputs1)


        if 'Therefore, the answer is' in pred1 or 'The answer is' in pred1:
            if 'The answer is' in pred1:
                # 取分隔后最后一个答案
                pred2 = pred1.split('The answer is')[-1]
            else:
                pred2 = pred1.split('the answer is')[-1]
            try:
                pred_answer = extract_answer(args, pred2)
            except:
                pred_answer = None
        # else:
        #     # 没有想要的提示词就强行加上去再问一次
        #     inputs2 = pred + ' ' + args.direct_answer_trigger_for_direct
        #     get_result, pred3 = get_answer(args, inputs2)
        #     try:
        #         pred_answer = extract_answer(args, pred3)
        #     except:
        #         pred_answer = None

        ans = False
        if pred_answer is not None:
            if args.dataset.lower() in ["svamp", "gsm8k", "multiarith", "addsub", "singleeq"]:
                ##表示两个答案之间的绝对差值，用于衡量模型预测答案 (pred_answer) 和真实答案 (answer[idx]) 之间的数值差异##
                if abs(pred_answer - answer[idx]) < 1e-3:
                    correct += 1
                    ans = True
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred1,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    print(json_data)
                    write_json(json_data, Predict_File)
                else:
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred1,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    print(json_data)
                    write_json(json_data, Predict_File)
            else:

                '''
                isinstance 是 Python 内置的一个函数，用于检查一个对象是否是指定的类型或类型元组。它的语法为：
                 isinstance(object, classinfo)

                 参数
                 object：要检查的对象。

                 classinfo：可以是单个类型，也可以是类型构成的元组。如果 object 是 classinfo 中的一个实例或子类实例，则返回 True，否则返回 False。

                 作用
                 isinstance 用于类型检查，可以确保代码在处理数据时是类型安全的。它通常用于验证函数参数或变量是否为预期的类型。


                '''
            if isinstance(pred_answer, float) and isinstance(answer[idx], float):
                precision = min(get_precision(pred_answer), get_precision(answer[idx]))
                if round(pred_answer, precision) == round(answer[idx], precision):
                    correct += 1
                    ans = True
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred1,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    print(json_data)
                    write_json(json_data, Predict_File)
                else:
                    ans = False
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred1,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    print(json_data)
                    write_json(json_data, Predict_File)
            else:
                if pred_answer == answer[idx]:
                    correct += 1
                    ans = True
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred1,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    print(json_data)
                    write_json(json_data, Predict_File)
                else:
                    json_data = {
                        "ID": ids[idx],
                        "question": question[idx],
                        "chain-of-thought": pred1,
                        "pred": pred_answer,
                        "answer": answer[idx],
                        "ans": ans
                    }
                    print(json_data)
                    write_json(json_data, Predict_File)
        else:
            json_data = {
                "ID": ids[idx],
                "question": question[idx],
                "chain-of-thought": pred1,
                "pred": pred_answer,
                "answer": answer[idx],
                "ans": ans
            }
            print(json_data)
            write_json(json_data, Predict_File)
    return correct

if __name__ == '__main__':
    print_exp(args)
    alls = zero_shot()
    print("数量为:%d" %
          alls)
    logger.info(f"correct num: {alls}")




