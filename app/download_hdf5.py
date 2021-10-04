"""download_hdf5

トップディレクトリからの実行は
python ./app/download_hdf5.py

NOTE: HDF5 ファイルが Drive 上で変更された場合、
      環境変数の HDF5_DRIVE_ID を変更して対応します。
"""

# Built-in modules.
import os

# Third-party modules.
from google_drive_downloader import GoogleDriveDownloader

# User modules.
from utils import common_utils

# このモジュール用のロガーを作成します。
logger = common_utils.get_my_logger(__name__)

# hdf5 の情報を取得します。
HDF5 = dict(
    drive_id=os.environ['APP_HDF5_DRIVE_ID'],
    destination_path='./app/hdf5.hdf5',
)


def main():

    # すでにあるときは、再ダウンロードするかどうか確認します。
    if os.path.exists(HDF5['destination_path']):
        file_size_mb = round(os.path.getsize(HDF5['destination_path']) / 1000000, 3)
        input_message = (
            f'hdf5 already exists! File size {file_size_mb} MB.'
            ' Download and overwrite? [y/N]: '
        )
        if common_utils.yes_no_input(input_message):
            # ダウンロードへ進みます。
            pass
        else:
            # 処理を終了します。
            return

    # hdf5 をダウンロードします。
    logger.info('Download starting ...')
    GoogleDriveDownloader.download_file_from_google_drive(
        file_id=HDF5['drive_id'],
        dest_path=HDF5['destination_path'],
        unzip=False,  # zip ファイルではないので False
        showsize=True,
        overwrite=True,
    )


if __name__ == '__main__':
    logger.info('download_hdf5.py starting ...')
    main()
    logger.info('download_hdf5.py finished.')
