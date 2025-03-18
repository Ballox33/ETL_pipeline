# Usa un'immagine Python leggera
FROM python:3.11-slim

# Imposta la working directory
WORKDIR /app

# Copia i file del progetto nella working directory
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Comando di esecuzione dello script
CMD ["python", "Job_csv_update.py"]
