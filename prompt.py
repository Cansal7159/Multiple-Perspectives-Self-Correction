# 开发时间：2024/7/5 16:27
import json
from config import args

prompt_101 = "Let's think step by step."
repair_prompt_201 = \
'''
Now, you should determine whether the given solution is correct. If there are errors in the intermediate steps of the solution, you should point them out and correct them.
The answer can only be one of the following: a number, an option(like A,B,C,D), a string, or Yes/No.
You need to analyze from the following three prompts and cannot skip any prompt when analyzing.
Prompt1：You are a brilliant mathematician, and you have an important task ahead. You are to use all your computational power to determine whether the given solution to the problem is correct.You should analyze from the perspective of a professional mathematician. While solving this problem.You must go step by step, without skipping any steps, and you must enumerate all the reasoning involving numbers. In the end, you are to provide your answer and judge whether the original answer is correct. 
Prompt2：You are a Google coder, and you have an important task ahead. You are to use all your computational power to determine whether the given solution to the problem is correc. You must use code to solve this problem, and provide detailed code,  also provide the result after running this code. You should analyze from the perspective of a Google programmer.Without skipping any steps, you must solve this problem using code(Python). In the end, you are to provide your answer and judge whether the original answer is correct.
Prompt3：You are an empathetic educator, and you have an important task ahead. You are to use all your computational power to determine whether the given solution to the problem is correct. You should analyze it in detail, much like how an MIT professor would dissect the problem and  explain each step in simple terms.You must go step by step, without skipping any steps, and you must enumerate all the reasoning involving numbers. In the end, you are to provide your answer and judge whether the original answer is correct.
When you complete the task of analyzing from these three respective prompts.Your have to make a judgment.If more than half of these respective prompts think the original answer is correct, it is considered that this answer is correct and  response with  'The orginal answer is true. Therefore, the answer is'+ your correct answer . If the number of votes does not exceed half, answer 'The orginal answer is wrong. Therefore, the answer is' + your  correct answer.
'''
def get_prompt():
    demos = None
    return demos, eval('prompt_{}'.format(args.prompt_id))

def get_repair_prompt():
    demos = None
    return demos, eval('repair_prompt_{}'.format(args.repair_prompt_id))
def construct_input(prompt, text):
    inputs = [
        {"role": "user",
         "content": 'Q:'+text+'You must response with this sentence pattern "Therefore, the answer is" '
         },
        {"role": "system",
         "content": 'A: '+prompt
         }
    ]
    return inputs

def repair_output(prompt, text1,text2):
    inputs = [
        {"role": "user",
         "content": 'Q:' + text1+'A:'+text2
         },
        {"role": "system",
         "content": prompt
         }
    ]
    return inputs
