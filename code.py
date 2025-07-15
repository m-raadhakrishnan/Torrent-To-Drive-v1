import libtorrent as lt
import time
import os
from google.colab import drive, files

drive.mount('/content/drive')
print("Upload your .torrent file:")
uploaded = files.upload()
torrent_file_path = list(uploaded.keys())[0]
save_path = '/content/drive/MyDrive/TorrentDownloads'
os.makedirs(save_path, exist_ok=True)
session = lt.session()
session.listen_on(50000, 60000)

settings = session.get_settings()
settings.update({
    'download_rate_limit': 0,  # No download limit
    'upload_rate_limit': 0,    # No upload limit
    'connections_limit': 2000, # Max peers
    'active_downloads': 50,
    'active_seeds': 50,
    'request_timeout': 10,
    'piece_timeout': 5,
    'enable_dht': True,
    'enable_lsd': True,
})
session.apply_settings(settings)
info = lt.torrent_info(torrent_file_path)
h = session.add_torrent({'ti': info, 'save_path': save_path})
h.set_sequential_download(True)  # Prioritize sequential download
print(f"\nDownloading {info.name()} to {save_path}")
while not h.is_seed():
    s = h.status()
    print(f"Progress: {s.progress * 100:.2f}% | Down: {s.download_rate / 1024:.2f} kB/s | Up: {s.upload_rate / 1024:.2f} kB/s | Peers: {s.num_peers}")
    time.sleep(5)

print("✅ Download complete!")
print(f"File saved to: {save_path}")
