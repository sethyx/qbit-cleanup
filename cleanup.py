import os, sys
import time
import datetime
import qbittorrentapi

HOST = os.environ.get("QBIT_HOST")
USER = os.environ.get("QBIT_USER")
PASSWORD = os.environ.get("QBIT_PASSWORD")
SEED_DAYS = os.environ.get("SEED_DAYS")
SEED_RATIO = os.environ.get("SEED_RATIO")

if (HOST is None or SEED_DAYS is None or SEED_RATIO is None):
    print("Please provide HOST, SEED_DAYS, SEED_RATIO in environment.")
    sys.exit(1)

while True:
    qbt_client = qbittorrentapi.Client(host=HOST, username=USER, password=PASSWORD)

    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    now = datetime.datetime.now()
    print("now: {}".format(now))

    for torrent in qbt_client.torrents_info():
        print(torrent.name)
        if (torrent.completion_on) > 0:
            complete_time = datetime.datetime.fromtimestamp( torrent.completion_on )
            print("completed: {}".format(complete_time))
            print("ratio: {}".format(torrent.ratio))
            xdaysago = now - datetime.timedelta(days = int(SEED_DAYS))
            if torrent.ratio > float(SEED_RATIO) or complete_time < xdaysago:
                print("torrent either above {} or completed {} days ago, removing".format(SEED_RATIO, SEED_DAYS))
                qbt_client.torrents_delete(delete_files=True, torrent_hashes=torrent.hash)
                qbt_client.torrents_delete(delete_files=True, torrent_hashes=torrent.hash)
        else:
            print("not completed yet")

        #print(f'{torrent.hash[-6:]}: {torrent.name} ({torrent.state})')
    time.sleep(3600)