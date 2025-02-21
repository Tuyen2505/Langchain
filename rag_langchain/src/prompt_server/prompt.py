from transformers import pipeline
import torch

def process_prompt(prompt):
    
    model_id = "meta-llama/Llama-3.2-3B-Instruct"
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map=torch.device("cuda:0"),
    )

    def rewrite_prompt(prompt):
        messages = [
            {
                "role": "system", 
                "content": "Tôi chỉ viết lại và nâng cao prompt bằng tiếng việt cho ban lãnh đạo tại Việt Nam, tôi chỉ viết lại prompt, không trả lời bất gì câu hỏi nào, viết lại ngắn gọn súc tích nhưng không thêm bớt nội dung và tóm tắt mọi thứ trong 1 câu. viết lại prompt dành cho báo cáo"
            }
        ]
        prompt_template = f"Viết lại & nâng cao & không cần trả lời & chỉ trong 1 câu & không thêm nội dung ngoài: viết một báo cáo về {prompt}"
        messages.append({"role": "user", "content": prompt_template})
        outputs = pipe(
            messages,
            temperature=0.8,
            max_new_tokens=512,
        )
        text = outputs[0]["generated_text"][-1]
        print(text)
        return text

    result = rewrite_prompt(prompt)
    return result