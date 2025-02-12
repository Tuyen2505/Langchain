from transformers import pipeline
import torch
import os

def process_prompt(text_input_prompt):
    
    model_id = "meta-llama/Llama-3.2-3B-Instruct"
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map= torch.device("cuda:0"),
    )

    def rewrite_prompt(prompt):
        messages = [
            # {"role": "system", "content": "tôi là một nhân viên viết lại prompt bằng tiếng việt cho lãnh đạo, viết lại ngắn gọn súc tích nhưng không thêm bớt nội dung và tóm tắt mọi thứ trong 1 câu. viết lại prompt dành cho báo cáo"},
            {"role": "system", "content": "Tôi chỉ viết lại và nâng cao prompt bằng tiếng Việt, không trả lời bất kỳ câu hỏi nào, chỉ trong 1 câu"},
            ]
        prompt_template = f"Viết lại & nâng cao & không cần trả lời & chỉ trong 1 câu & không thêm nội dung ngoài:viết lại {prompt}"
        messages.append({"role": "user", "content": prompt_template})
        # messages = [
        #     {"role": "system", "content": "tôi là thư ký của Hoàng Thành Đạt, trả lời bằng tiếng việt"},
        #     ]
        # prompt_template = f"Tôi cần :{prompt}"
        # messages.append({"role": "user", "content": prompt_template})

        outputs = pipe(
        messages,
        temperature=0.8,
        # max_new_tokens=256,
        max_new_tokens=512,
        )
        text = (outputs[0]["generated_text"][-1])
        print(text)
        return text


    # while True:
    text_input = input(text_input_prompt)
    # if text_input.lower() == 'exit':
    #     break
    result = rewrite_prompt(text_input)

    return result



# while True:
#     text_input_prompt = "Nhập prompt (hoặc gõ 'exit' để thoát): "
#     result = process_prompt(text_input_prompt)
#     print(result)
#     if result.lower() == 'exit':
#         break
#     print(result)
#     # print("")