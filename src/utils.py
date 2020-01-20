import IceStorm
import os
import sys

try:
    import youtube_dl
except ImportError:
    print('ERROR: do you have installed youtube-dl library?')
    sys.exit()


# DOWNLOADER

# pylint: disable=C0115
class NullLogger:
    # pylint: disable=C0116
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


_YOUTUBEDL_OPTS_ = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}


def download_mp3(url, destination='./'):
    '''
    Synchronous download from YouTube
    '''
    options = {}
    task_status = {}

    def progress_hook(status):
        task_status.update(status)

    options.update(_YOUTUBEDL_OPTS_)
    options['progress_hooks'] = [progress_hook]
    options['outtmpl'] = os.path.join(destination, '%(title)s.%(ext)s')
    with youtube_dl.YoutubeDL(options) as youtube:
        youtube.download([url])
    filename = task_status['filename']
    # BUG: filename extension is wrong, it must be mp3
    filename = filename[:filename.rindex('.') + 1]
    return filename + options['postprocessors'][0]['preferredcodec']


def generate_id(url):
    """
    Generate id for a video
    @param url:
    @return:
    """
    with youtube_dl.YoutubeDL(_YOUTUBEDL_OPTS_) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    return info_dict['id']


def supported(url):
    """ source: https://github.com/ytdl-org/youtube-dl/issues/4503
    Check the url
    @param url:
    @return:
    """
    # pylint: disable=C0103
    ies = youtube_dl.extractor.gen_extractors()
    for ie in ies:
        if ie.suitable(url) and ie.IE_NAME != 'generic':
            # Site has dedicated extractor
            return True
    return False


def download_mp3_with_id(url, destination='./'):
    """
    Download the video generating the id
    @param url:
    @param destination:
    @return: file, id
    """
    options = {}
    task_status = {}

    def progress_hook(status):
        task_status.update(status)

    options.update(_YOUTUBEDL_OPTS_)
    options['progress_hooks'] = [progress_hook]
    options['outtmpl'] = os.path.join(destination, '%(title)s.%(ext)s')
    with youtube_dl.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
    filename = task_status['filename']
    # BUG: filename extension is wrong, it must be mp3
    filename = filename[:filename.rindex('.') + 1]
    return (filename + options['postprocessors'][0]['preferredcodec']), info_dict['id']


# MY STORM

ORCHESTRATOR_TOPIC_NAME = 'OrchestratorSync'
DOWNLOADER_TOPIC_NAME = 'UpdateEvents'


def get_topic_manager(broker):
    """
    Function for create a topic manager
    @param broker:
    @return: topic manager
    """
    key = 'IceStorm.TopicManager.Proxy'

    topic_manager_proxy = broker.stringToProxy('YoutubeDownloaderApp.IceStorm/TopicManager')

    if topic_manager_proxy is None:
        raise ValueError("property {} not set".format(key))
    # pylint: disable=E1101
    topic_manager = IceStorm.TopicManagerPrx.checkedCast(topic_manager_proxy)

    if not topic_manager:
        raise ValueError(Color.BOLD + Color.RED + 'Invalid proxy in topic manager' + Color.END)

    return topic_manager


def get_topic(topic_manager, topic_name):
    """
    Function for generate the topic
    @param topic_manager: the topic manager for create the topic
    @param topic_name: the topic name
    @return: topic
    """
    try:
        return topic_manager.retrieve(topic_name)
    # pylint: disable=E1101
    except IceStorm.NoSuchTopic:
        return topic_manager.create(topic_name)


# COLOR PRINT

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
