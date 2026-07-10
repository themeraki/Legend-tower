import requests
import os
import sys

# Configuration from environment variables for security
URL = os.environ.get('https://silent-fire-c8c7.jobifezu.workers.dev/download?token=B_96nwN7qyCCZWCABS25N_whLH8OVKEn3TbuF_Ps55vyh8b4_XVk0xdR8mB0-0KUdSIZRk4_SLOPmzSFJz_ZVyiiRQMskqG4GH9UJ6M9MfPxRFpfNyFpumeLg4ecAXwAAiyIh9kD5WfTP5n_7dACboK1k2zZtaJNS_hd8Qhj490E39ucA_syssaZuAfHQadUZrIZobGNQN22t9vHSfGfZrZvNZzPIE8EGk8OrfePSAiICM2eXuPBLoJmoboRPB6zrwUnaH8dXJTDHYtVek7qzJORl578tpNSezdCrDUf9HReJsU&file_name=users_data.zip')
TOKEN = os.environ.get('8495831796:AAFj0VIS6iZqI9J1BbK8x11hIaAuJnSgBfM')
CHAT_ID = os.environ.get('-1004371967621')
CHUNK_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB

def upload_to_telegram(file_path, part_num):
    print(f"Uploading part {part_num}...")
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(file_path, 'rb') as f:
        # Telegram API call
        response = requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f})
    if response.status_code == 200:
        print(f"Part {part_num} uploaded successfully.")
    else:
        print(f"Failed to upload part {part_num}: {response.text}")
    os.remove(file_path) # Delete file to free space!

def stream_and_split():
    part_num = 1
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        
        while True:
            file_name = f"part_{part_num}.tmp"
            bytes_written = 0
            
            with open(file_name, 'wb') as f:
                # Read in small blocks to keep RAM usage low
                for chunk in r.iter_content(chunk_size=1024*1024): 
                    f.write(chunk)
                    bytes_written += len(chunk)
                    if bytes_written >= CHUNK_SIZE:
                        break
            
            if bytes_written == 0:
                os.remove(file_name)
                break
                
            upload_to_telegram(file_name, part_num)
            part_num += 1

if __name__ == "__main__":
    stream_and_split()
