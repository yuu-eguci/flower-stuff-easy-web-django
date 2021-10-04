"""
Python やるときにいつもあって欲しい自分用モジュールです。
おおよそどのプロジェクトでも使っている utility functions を定義しています。
"""

# Built-in modules.
import logging
import datetime

# Third-party modules.
import pytz

# User modules.


def get_my_logger(logger_name: str) -> logging.Logger:
    """モジュール用のロガーを作成します。
    logger = get_my_logger(__name__)

    Args:
        logger_name (str): getLogger にわたす名前。 __name__ を想定しています。

    Returns:
        logging.Logger: モジュール用のロガー。
    """

    # ルートロガーを作成します。ロガーはモジュールごとに分けるもの。
    logger = logging.getLogger(logger_name)
    # ルートロガーのログレベルは DEBUG。
    logger.setLevel(logging.DEBUG)
    # コンソールへ出力するハンドラを作成。
    handler = logging.StreamHandler()
    # ハンドラもログレベルを持ちます。
    handler.setLevel(logging.DEBUG)
    # ログフォーマットをハンドラに設定します。
    formatter = logging.Formatter(
        # NOTE: 改行は逆に見づらいので E501 を無視します。
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')  # noqa: E501
    handler.setFormatter(formatter)
    # ハンドラをロガーへセットします。
    logger.addHandler(handler)
    # 親ロガーへの伝播をオフにします。
    logger.propagate = False
    return logger


def get_now_jst() -> datetime.datetime:
    """datetime.datetime.now を日本時間で取得します。
    NOTE: フォーマットはいつも参照してしまうのでここに note しておきます %Y-%m-%d %H:%M:%S
          あるいは .isoformat() も良い。

    Returns:
        datetime.datetime: 日本時間
    """

    TZ_JAPAN = pytz.timezone('Asia/Tokyo')
    current_jst_time = datetime.datetime.now(tz=TZ_JAPAN)
    return current_jst_time


def get_beginning_of_month_utc(y: int, m: int) -> str:
    """与えた年月の月初を iso フォーマットで取得します。
    EXAMPLE: 2020-09-30T14:41:00Z

    Args:
        y (int): 年
        m (int): 月

    Returns:
        str: 月初
    """

    beginning_of_month = datetime.datetime(
        y, m, 1, 0, 0, 0, 0, pytz.timezone('Asia/Tokyo'))
    beginning_of_month_utc = pytz.utc.normalize(
        beginning_of_month.astimezone(pytz.utc))
    return beginning_of_month_utc.strftime('%Y-%m-%dT%H:%M:%SZ')


def yes_no_input(message="Please respond with 'yes' or 'no' [y/N]: ") -> bool:
    """y/N で返答する input です。

    Args:
        message (str, optional): [description].
                                 Defaults to "Please respond with 'yes' or 'no' [y/N]: ".

    Returns:
        bool: [description]
    """

    while True:
        choice = input(message).lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False


# utils モジュール用のロガーを作成します。
logger = get_my_logger(__name__)

if __name__ == '__main__':
    logger.debug('でばーぐ')
    logger.info('いんーふぉ')
    logger.warning('うぉーにん')
    logger.error('えろあ')
    logger.fatal('ふぇーたる(critical と同じっぽい)')
    logger.critical('くりてぃこぉ')
    logger.debug('get_now_jst -> ' + get_now_jst().isoformat())
    logger.info(get_beginning_of_month_utc(2020, 10))
