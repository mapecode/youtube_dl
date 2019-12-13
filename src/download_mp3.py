# pylint: disable=C0114
import os
import sys

try:
    import youtube_dl
except ImportError:
    print('ERROR: do you have installed youtube-dl library?')
    sys.exit()


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
