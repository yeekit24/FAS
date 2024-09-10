"""Faust app module.

Faust commands can be executed either by directly executing this file or
by running faust -A config.queue.faust_app

"""
import os
import ssl
import sys
from pathlib import Path

# mypy: ignore-errors
import faust

# make sure the event loop is used as early as possible.
os.environ.setdefault("FAUST_LOOP", "eventlet")

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR))

# set the default Django settings module for the 'faust' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
app = faust.App(
    os.environp["APP_UID"],
    autodiscover=["src.queues.agents"],
)


@app.on_configured.connect
def configure_from_settings(app, conf, **kwargs):
    """Setup faust app based off Django settings."""
    from django.conf import settings

    if settings.QUEUE_ENABLE_SSL:
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH,
            cafile=settings.QUEUE_SSL_CA,
        )
        if settings.QUEUE_CERT_CHAIN:
            ssl_context.load_cert_chain(
                settings.QUEUE_CERT_CHAIN,
                password=settings.QUEUE_CERT_CHAIN_PASSWORD,
            )
        ssl_context.check_hostname = settings.QUEUE_ENABLE_SSL_HOSTNAME_CHECK
        if not settings.QUEUE_ENABLE_SSL_VERIFY:
            ssl_context.verify_mode = ssl.CERT_NONE
        conf.broker_credentials = ssl_context

    conf.broker = settings.QUEUE_BROKER
    conf.store = settings.QUEUE_STORE


def main():
    app.main()


if __name__ == "__main__":
    main()
