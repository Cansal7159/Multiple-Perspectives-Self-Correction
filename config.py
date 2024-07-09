# 开发时间：2024/7/5 13:11
import argparse

def parse_agruments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--dataset', default='gsm8k',
        help="dataset",
        choices=["SVAMP", "GSM8K", "AQuA", "MultiArith", "AddSub", "SingleEq", "CommonsenseQA", "coin_flip",
                 "last_letters", "FinQA", "TATQA", "ConvFinQA", "StrategyQA"]
    )
    parser.add_argument(
        "--prompt_id", default='101', help='string'
    )
    parser.add_argument(
        "--repair_prompt_id", default='201', help='string'
    )
    parser.add_argument(
        "--engine", default='gpt-3.5-turbo', help="gpt-3.5-turbo",
        choices=["gpt-3.5-turbo", "gpt-4o"]
    )
    parser.add_argument(
        "--datapath", default=None, type=str, help='file path'
    )
    parser.add_argument(
        "--test_end", default='full', help='string, number'
    )
    parser.add_argument(
        "--test_start", default='0', help='string, number'
    )

    parsed_args = parser.parse_args()

    parsed_args.direct_answer_trigger_for_zeroshot = "Let's think step by step."
    parsed_args.direct_answer_trigger_for_direct = "Therefore,the answer is"
    return parsed_args

args = parse_agruments()