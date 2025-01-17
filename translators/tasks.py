from .models import Translator
from translate.models import Word
from datetime import datetime
import requests

def send_words():
  now = datetime.now()
  # users = Translator.objects.filter(send_time=f"{now.hour}:{now.minute}")
  users = Translator.objects.all()
  print(f'Sending for {users.count()} users')
  for user in users:
    words: list[Word] = Word.objects.exclude(translators__in=[user]).order_by('word')[:user.number_of_words]
    if words.count() < 1: continue
    for platform in user.platform_set.filter(is_active=True):
      data = {
            'uuid': str(user.uuid),
            'words': [
              {
                'word': word.word,
                'translates': word.get_translates()
              }
              for word in words
            ]
          }
      res = requests.post(
          f'{platform.base_url}/get_words',
          json=data 
      )
