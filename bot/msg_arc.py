import requests


class MessageArchiver(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    def save_file(self, file_id, file_name):
        if not self.bot:
            return
        download_url = self.bot.getFile(file_id)

        if not download_url:
            return
        
        print("downloading...")
        res = requests.get('https://api.telegram.org/file/bot%s/%s' % 
            (self.config.BOT_TOKEN, download_url['file_path']))
        ext = download_url['file_path'].split('.')[-1]
        if res.status_code == 200:
            fp = open('%s/%s.%s' % (self.config.STORAGE_BASE_PATH, file_name, ext), 'wb')
            fp.write(res.content)
            fp.close()

        return ext




