import requests
import hashlib
import subprocess
import os

def get_expected_hash(url):
    resp_msg = requests.get(url)
    if resp_msg.status_code == requests.codes.ok:
        return resp_msg.text.strip()
    else:
        raise Exception("Failed to download the hash value file.")

def download_file(url):
    resp_msg = requests.get(url)
    if resp_msg.status_code == requests.codes.ok:
        return resp_msg.content
    else:
        raise Exception("Failed to download the file.")

def compute_hash(content):
    return hashlib.sha256(content).hexdigest()

def save_file(content, path):
    with open(path, 'wb') as file:
        file.write(content)

def run_installer(path):
    subprocess.run([path, '/S'])

def delete_file(path):
    os.remove(path)

def main():
    hash_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    installer_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    installer_path = r'C:\temp\vlc-3.0.11.1-win64.exe'
    
    expected_hash = get_expected_hash(hash_url)
    installer_content = download_file(installer_url)
    computed_hash = compute_hash(installer_content)
    
    if computed_hash == expected_hash:
        print("Hash value verified. The file is valid.")
        save_file(installer_content, installer_path)
        run_installer(installer_path)
        delete_file(installer_path)
    else:
        print("Hash value mismatch. The file may be corrupted.")

if __name__ == "__main__":
    main()
