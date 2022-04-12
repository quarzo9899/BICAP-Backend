from django.apps import AppConfig


class BICAPwebConfig(AppConfig):
    name = 'BICAPweb'

    def ready(self):
        import  BICAPweb.signals
