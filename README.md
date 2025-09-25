# Fake News App Via Docker

## Requisitos
- Docker instalado

## Como rodar
Abra o terminal e execute:

```bash
git clone https://github.com/seu-usuario/fake-and-real-news-dataset.git
cd fake-and-real-news-dataset
docker build -t fake-news-app .
docker run -p 8000:8000 fake-news-app

Depois abra no navegador: http://127.0.0.1:8000/docs
```


# Fake News App Via Local 

## Requesitos
- pip install -r requirements.txt

## Como rodar
No arquivo main.py execute:
uvicorn api.main:app --reload

Depois
Abra o arquivo HTML e pode colar as noticias
