"""
Utility module for the solid_integration classes.
"""
import urllib

PREFERRED_SIGNING_ALG = ["ES256"]

def normalize_htu(audience: str) -> str:
    """
    Normalizes a URL to generate a DPoP token based on a consistent scheme.

    :param audience: The URL to normalize.
    :return: The normalized URL as a string.
    """
    audience_url = urllib.parse.urlparse(audience)
    return urllib.parse.urlunparse((audience_url.scheme,
                                    audience_url.netloc,
                                    audience_url.path,
                                    '', '', ''))
