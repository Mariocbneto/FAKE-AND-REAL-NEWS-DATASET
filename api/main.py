from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import re
import pickle
from newspaper import Article
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
from fastapi.middleware.cors import CORSMiddleware

# --- CARREGA MODELO E TOKENIZER ---
modelo = tf.keras.models.load_model("models/modelo_fake_news.h5")
with open("models/tokenizer.pkl", "rb") as handle:
    tokenizer = pickle.load(handle)
MAXLEN = 300

# --- FASTAPI ---
app = FastAPI()

origins = ["*"]  # "*" permite qualquer origem, ideal pra teste local

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # permite POST, GET, OPTIONS...
    allow_headers=["*"],
)


# Servir arquivos estáticos (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

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
        return {"erro": "Não foi possível baixar ou ler a notícia"}

    texto = (artigo.title or "") + " " + (artigo.text or "")
    texto_limpo = clean_text(texto)

    sequencia = tokenizer.texts_to_sequences([texto_limpo])
    sequencia = pad_sequences(sequencia, maxlen=MAXLEN)

    prob = modelo.predict(sequencia)[0][0]
    resultado = "FAKE" if prob > 0.5 else "REAL"

    return {"resultado": resultado, "probabilidade": float(prob)}
