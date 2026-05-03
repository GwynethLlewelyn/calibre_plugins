"""Utilities for certificate management."""

import os

certifi_where = None
try:
    from certifi import where as certifi_where
except (ImportError, AttributeError) as e:
    print(f"[DEBUG] Mozilla certificates not found; error was: {e}")
    pass

custom_ca_locater_where = None
try:
    from ca_certs_locater import get as custom_ca_locater_where
except (ImportError, AttributeError) as e:
    print(f"[DEBUG] Custom certificate locator not found on path (error: {e}); trying local...")
    try:
        from .ca_certs_locater import get as custom_ca_locater_where
    except (ImportError, AttributeError) as e:
        print(f"[DEBUG] Custom certificate locator not found locally, error was: {e} — aborting, using built-in certs")
        pass

"""
Internal path for certificates, if all else fails
"""
BUILTIN_CA_CERTS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "cacerts.txt"
)


def where():
    """
    Returns path to certificate file, with several fallbacks
    """
    env = os.environ.get("HTTPLIB2_CA_CERTS")
    if env is not None:
        if os.path.isfile(env):
            return env
        else:
            raise RuntimeError("[ERROR] Environment variable HTTPLIB2_CA_CERTS is not a valid file")
    if custom_ca_locater_where is not None:
        return custom_ca_locater_where()
    if certifi_where is not None:
        return certifi_where()
    return BUILTIN_CA_CERTS

print(f"[DEBUG] Getting certificates... {where()}")
