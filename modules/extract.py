import wget
import os
import subprocess
import requests

def download_file_wget(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.basename(url)
    filepath = os.path.join(output_folder, filename)
    
    # overskriv eksisterende fil
    if os.path.exists(filepath):
        os.remove(filepath)
    
    wget.download(url, out=filepath, bar=False)
    print(f"File downloaded to {filepath}")

def download_file_subprocess(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.basename(url)
    
    with subprocess.Popen(['wget', url, '-q', '-O', '-'], stdout=subprocess.PIPE) as wget_pipe:
        with open(os.path.join(output_folder, filename), 'wb') as output_file:
            for chunk in iter(lambda: wget_pipe.stdout.read(1024), b""):
                output_file.write(chunk)

    print(f"File downloaded with wget-subproc to {os.path.join(output_folder, filename)}")

def download_file_requests(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)    
    filepath = os.path.join(output_folder, url.split("/")[-1])

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Download with requests to {filepath} complete.")
    return filepath

def extract_iris(url, output_folder):
    print(f"Extracting data")

    

if __name__ == "__main__":
    pass
    # IRIS_DOWNLOAD_URL = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv'
    # INPUT_FOLDER = 'input_data'
    # OUTPUT_FOLDER = 'output_data'
    # download_file_wget(IRIS_DOWNLOAD_URL, output_folder = INPUT_FOLDER)