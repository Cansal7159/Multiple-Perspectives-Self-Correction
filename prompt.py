# 开发时间：2024/7/5 16:27
import json
from config import args

prompt_101 = "Let's think step by step."
repair_prompt_201 = \
'''
Your task is to meticulously evaluate the validity of a proposed solution to a given problem. This evaluation should be comprehensive, focusing on the accuracy of both the final result and the individual steps leading to it. It is imperative that you scrutinize each phase of the solution without omitting any details and provide a numerical breakdown where applicable. Your ultimate goal is to ascertain the correctness of the solution and render a judgment on its accuracy.

To accomplish this, you will analyze the solution from three distinct Perspectives: 

Perspective 1: Approach the problem methodically, ensuring that no steps are omitted. As you progress, meticulously document all numerical reasoning. Conclude by delivering your own answer and assessing whether the initial solution is accurate. 

Perspective 2: Identify the domain to which the problem pertains and employ domain-specific knowledge to evaluate the validity of the solution. If you detect an error, pinpoint the exact step where the mistake occurred, rectify it, and then present the corrected solution. 

Perspective 3: Conduct a detailed examination of the solution, akin to how an academic would deconstruct the problem and explain each step in layman's terms. Begin by gaining a clear understanding of the problem, then articulate it simply and clearly, identifying the crux of the solution. Conclude by providing your own answer and determining the correctness of the original solution.

After you have analyzed the solution from these three perspectives, you will render a verdict. If a majority of these perspectives conclude that the original answer is correct, you will state, "The original answer is true. Therefore, the answer is" followed by your verified answer. If the majority finds the original answer to be incorrect, you will respond with, "The original answer is wrong. Therefore, the answer is" followed by your corrected answer. When providing your answer, ensure that it matches the format of the original response, whether it be a number, a selection from multiple options, a string of text, or a yes/no response.
'''

repair_prompt_301 = \
'''
Your task is to meticulously evaluate the validity of a proposed solution to a given problem. This evaluation should be comprehensive, focusing on the accuracy of both the final result and the individual steps leading to it. It is imperative that you scrutinize each phase of the solution without omitting any details and provide a numerical breakdown where applicable. Your ultimate goal is to ascertain the correctness of the solution and render a judgment on its accuracy.

To accomplish this, you will analyze the solution from only one perspective: 

Perspective 1: Approach the problem methodically, ensuring that no steps are omitted. As you progress, meticulously document all numerical reasoning. Conclude by delivering your own answer and assessing whether the initial solution is accurate. 

If the majority finds the original answer to be incorrect, you will respond with, "The original answer is wrong. Therefore, the answer is" followed by your corrected answer. When providing your answer, ensure that it matches the format of the original response, whether it be a number, a selection from multiple options, a string of text, or a yes/no response.
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
         "content": 'Q:'+text+'the final response should be formatted as follows: "Therefore, the answer is"'
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
         "content": 'Your answer:'+prompt
         }
    ]
    return inputs
