from django.apps import AppConfig


class UsersAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users_account'

    def ready(self):
        import users_account.signals
