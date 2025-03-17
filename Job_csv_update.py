import requests                   #libreria per effettuare richieste HTTP
from google.cloud import storage
import logging

# Configurazione del logging
logging.basicConfig(level=logging.INFO)

# URL del file CSV
file_url = "http://data.comune.fi.it/datastore/download.php?id=7752&type=99&format=url&file_format=csv&file_id=22717"

# Simulazione di un browser per evitare il blocco da parte del server
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

bucket_name = "dati_invaso_bilancino"
file_name = "livelli_bilancino_2025.csv"
project_id = "core-verbena-453916-t2"

# Inizializzazione client per GCS
client = storage.Client(project=project_id)
bucket = client.bucket(bucket_name)

# Funzione per scaricare e caricare il file
def download_and_upload():
    try:
        logging.info(f"Inizio download del file da: {file_url}")
        response = requests.get(file_url, timeout=30, headers=headers, allow_redirects=True)

        # Controllo se la richiesta è andata a buon fine
        if response.status_code == 200:
            logging.info(f"Il file è stato scaricato con successo da: {file_url}")
            
            # Controllo se il file esiste già su GCS
            blob = bucket.blob(file_name)
            if blob.exists():
                logging.warning(f"Il file {file_name} esiste già su GCS. Verrà sovrascritto.")
            
            # Caricamento del file su GCS
            blob.upload_from_string(response.content)
            logging.info(f"File caricato con successo su GCS come {file_name}")
        else:
            logging.error(f"Errore durante il download del file: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Errore durante la richiesta HTTP: {e}")
    except Exception as e:
        logging.error(f"Errore imprevisto: {e}")

if __name__ == "__main__":
    download_and_upload()
