import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from googletrans import Translator
import datetime
import os
import requests

tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
#####################
ultimo_mensaje = ""

#Logs
carpeta = "memory_log" #ubicacion de donde guarda y carga la memoria
memoria = "" #inicia la memoria para su escritura


tiempo_log= datetime.datetime.now()
log_name = tiempo_log.strftime("(%H-%M-%S)-%d-%m-%Y")
print(log_name)


def log_create(texto_log):
    with open(f"memory_log/{log_name}", 'a', encoding="utf-8") as archivo:
        # Escribir el texto en el archivo
        archivo.write(texto_log)


def agregar_texto_archivo(nombre_archivo, texto):
    with open(nombre_archivo, 'a', encoding="utf-8") as archivo:
        archivo.write('\n' + texto)



#memoria
def listar_archivos_en_carpeta(ruta_carpeta):
    try:
        # Obtener la lista de archivos en la carpeta
        archivos = os.listdir(ruta_carpeta)
        #print("Archivos:", ruta_carpeta, ":")
        for archivo in archivos:
            print(archivo)
            with open(f"{carpeta}/" + str(archivo), 'r', encoding="utf-8") as archivo:
                info_texto = archivo.read()
            global memoria
            memoria = memoria + "\n" + info_texto
    except:
        print("error en archivos")


######################

def chat_Twitch():
    try:
        #Pide info al Node.js
        #response = requests.get('http://127.0.0.1:8080/obtener_ultimo_mensaje')
        response = requests.get('http://127.0.0.1:3000/obtener_ultimo_mensaje')
        response.encoding = "utf-8"
        global ultimo_mensaje
        ultimo_mensaje = response.text
    except:
        pass


#Traduccion español a ingles
def traducir_en(texto):
    translator = Translator()
    traduccion = translator.translate(texto, src='es', dest='en')
    return traduccion.text

#Traduccion ingles a español
def traducir_es(texto):
    translator = Translator()
    traduccion = translator.translate(texto, src='en', dest='es')
    return traduccion.text




#Silv model here
def generate_response(prompt, max_new_tokens=100, num_beams=1, early_stopping=False, repetition_penalty=2.0):
    prompt = f"{prompt}\n'Silv': "
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)

    output = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        num_beams=num_beams,
        early_stopping=early_stopping,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        top_k=80,
        top_p=0.95,
    )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    try:
        return response.split("'Silv':")[1].strip()
    except:
        print("error")


chat_Twitch()
print(ultimo_mensaje)
valor_anterior = ultimo_mensaje
while True:
    chat_Twitch()
    if ultimo_mensaje != valor_anterior:  # recibe el mensaje de twitch si es diferente al anterior

        listar_archivos_en_carpeta(carpeta)

        print(f"chat:{ultimo_mensaje}")
        chat_en = traducir_en(ultimo_mensaje)
        Silv_rpta = generate_response(f"{memoria}\n{chat_en}")
        print(f"Original: {Silv_rpta} \n \n")
        Silv_ES = traducir_es(Silv_rpta)
        print(Silv_ES)
        agregar_texto_archivo(f"{carpeta}/{log_name}", f"{chat_en}\nSilv: {Silv_rpta}")
        valor_anterior = ultimo_mensaje #Guarda el ultimo mensaje

