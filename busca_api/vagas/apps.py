from django.apps import AppConfig


class VagasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vagas'

    def ready(self):
        # importa signals para registro
        import vagas.signals  # noqa: F401
