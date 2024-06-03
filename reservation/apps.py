from django.apps import AppConfig


class ReservationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reservation"

    def ready(self):
        import reservation.signals  # noqa
