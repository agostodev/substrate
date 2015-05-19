from string import maketrans
def sanitize_app_id(name):
    """
    Remove unsafe characters from a app ID. Right now this just translates _ to -.
    """

    # TODO: validate against this valid app_id regexp?
    # ^(?:[a-z\d\-]{1,100}\~)?(?:(?!\-)[a-z\d\-\.]{1,100}:)?(?!-)[a-z\d\-]{1,100}$
    
    table = maketrans("_", "-")

    return name.translate(table)

from commands import *
from _version import __version__
