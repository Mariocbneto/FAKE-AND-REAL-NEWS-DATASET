# Base Python
FROM python:3.13-slim

# Configura diretório da aplicação
WORKDIR /app

# Copia arquivos do projeto
COPY . /app

# Atualiza pip e instala dependências
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir fastapi uvicorn tensorflow newspaper3k h5py numpy lxml[html_clean]

# Expõe porta
EXPOSE 8000

# Comando para rodar a API e servir o site
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


#docker build -t fake-news-app .

#docker run -p 8000:8000 fake-news-app
