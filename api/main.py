from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import re
import pickle
from newspaper import Article
from tensorflow.keras.preprocessing.sequence import pad_sequences

# --- CARREGA MODELO E TOKENIZER ---
modelo = tf.keras.models.load_model("models/modelo_fake_news.h5")

with open("models/tokenizer.pkl", "rb") as handle:
    tokenizer = pickle.load(handle)

MAXLEN = 300  # Mesmo valor usado no treino

# --- FASTAPI ---
app = FastAPI()

# --- MIDDLEWARE CORS ---
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem (teste local)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoticiaInput(BaseModel):
    url: str

# --- FUNÇÃO DE LIMPEZA ---
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\W', ' ', text)
    return text

# --- ENDPOINT DE PREDIÇÃO ---
@app.post("/predict")
def predict(noticia: NoticiaInput):
    try:
        artigo = Article(noticia.url)
        artigo.download()
        artigo.parse()
    except:
        return {"erro": "URL inválida ou artigo não pôde ser lido"}

    texto = (artigo.title or "") + " " + (artigo.text or "")
    texto_limpo = clean_text(texto)

    sequencia = tokenizer.texts_to_sequences([texto_limpo])
    sequencia = pad_sequences(sequencia, maxlen=MAXLEN)

    prob = modelo.predict(sequencia)[0][0]
    resultado = "FAKE" if prob > 0.5 else "REAL"
    confianca = prob if prob > 0.5 else 1 - prob  # Ajuste aqui

    return {"resultado": resultado, "probabilidade": float(confianca)}

# Para rodar: uvicorn api.main:app --reload
