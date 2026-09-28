import os


def get_env(name, default):
    """Devuelve una variable de entorno o el valor indicado por defecto."""
    return os.getenv(name, default)
