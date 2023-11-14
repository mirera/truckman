from django.apps import AppConfig


class TripConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trip'

    #registering the signal
    def ready(self):
        import trip.signals
