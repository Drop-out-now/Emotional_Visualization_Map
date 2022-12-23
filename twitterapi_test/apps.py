from django.apps import AppConfig


class TwitterapiTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'twitterapi_test'

    def ready(self):
        from .views import task
        task()
