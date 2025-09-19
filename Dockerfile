# Imagem base Python
FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Flask
EXPOSE 5000

# Comando para iniciar o Flask
CMD ["python", "run.py"]
