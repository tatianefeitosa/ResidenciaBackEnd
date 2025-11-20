import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busca_api.settings')

app = Celery('busca_api')

# Carrega configurações do Django, com prefixo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Detecta tasks automaticamente em apps instalados
app.autodiscover_tasks()

# configuração útil
app.conf.task_track_started = True
app.conf.task_time_limit = 60 * 60  # 1 hora por task 
