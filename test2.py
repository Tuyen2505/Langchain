def get_hf_llm(model_name: str = "gemini-2.0-pro-exp-02-05",
             max_new_token = 1024,
             **kwargs):
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=nf4_config,
        low_cpu_mem_usage=True
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_token,
        pad_token_id=tokenizer.eos_token_id,
        device_map="auto"
    )

    llm = HuggingFacePipeline(
        pipeline=model_pipeline,
        model_kwargs=kwargs
    )

    return llm
