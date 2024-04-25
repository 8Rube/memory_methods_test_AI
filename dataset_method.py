import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from datasets import load_dataset

tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Cargar el dataset
conv_dataset = load_dataset("text", data_files="test_texto")
historial = []

def generate_response(prompt, historial, dataset, max_new_tokens=100, num_beams=5, early_stopping=False, repetition_penalty=2.0):
    prompt = f"humano: {prompt}\nSilv:"

    input_text = ""
    for entry in historial:
        input_text += entry + "\n"
    input_text += prompt

    print("Texto de entrada al modelo:")
    print(input_text)

    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
    model.config.pad_token_id = model.config.eos_token_id

    attention_mask = torch.ones_like(input_ids)

    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_new_tokens=max_new_tokens,
        num_beams=num_beams,
        early_stopping=early_stopping,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        top_k=110,
        top_p=0.95
    )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    try:
        return response.split("Silv:")[1].strip()
    except:
        print("error")

while True:
    prompt = input("Usuario: ")
    response = generate_response(prompt, historial, conv_dataset)
    historial.append(response)  # Agregar la respuesta al historial
    print(prompt)
    print(f"Chatbot: {response}")
