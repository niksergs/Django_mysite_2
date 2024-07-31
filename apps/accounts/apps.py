from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Аккаунты'

    def ready(self):
        """Переопределили метод конфигурации пользовательского приложения для выполнения задачи инициализации,
        которая регистрирует сигналы."""
        import apps.accounts.signals
