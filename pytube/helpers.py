# -*- coding: utf-8 -*-
"""Various helper functions implemented by pytube."""

import logging
import pprint
import re
from typing import Optional

from pytube.exceptions import RegexMatchError


logger = logging.getLogger(__name__)


def regex_search(
    pattern: str, string: str, groups: bool = False, group: Optional[int] = None,
):
    """Shortcut method to search a string for a given pattern.

    :param str pattern:
        A regular expression pattern.
    :param str string:
        A target string to search.
    :param bool groups:
        Should the return value be ``.groups()``.
    :param int group:
        Index of group to return.
    :rtype:
        str or tuple
    :returns:
        Substring pattern matches.
    """
    regex = re.compile(pattern)
    results = regex.search(string)
    if not results:
        raise RegexMatchError(
            "regex pattern ({pattern}) had zero matches".format(pattern=pattern),
        )
    else:
        logger.debug(
            "finished regex search: %s",
            pprint.pformat(
                {"pattern": pattern, "results": results.group(0),}, indent=2,
            ),
        )
        if groups:
            return results.groups()
        elif group is not None:
            return results.group(group)
        else:
            return results


def apply_mixin(dct, key, func, *args, **kwargs):
    r"""Apply in-place data mutation to a dictionary.

    :param dict dct:
        Dictionary to apply mixin function to.
    :param str key:
        Key within dictionary to apply mixin function to.
    :param callable func:
        Transform function to apply to ``dct[key]``.
    :param \*args:
        (optional) positional arguments that ``func`` takes.
    :param \*\*kwargs:
        (optional) keyword arguments that ``func`` takes.
    :rtype:
        None
    """
    dct[key] = func(dct[key], *args, **kwargs)


def safe_filename(s: str, max_length: int = 255) -> str:
    """Sanitize a string making it safe to use as a filename.

    This function was based off the limitations outlined here:
    https://en.wikipedia.org/wiki/Filename.

    :param str s:
        A string to make safe for use as a file name.
    :param int max_length:
        The maximum filename character length.
    :rtype: str
    :returns:
        A sanitized string.
    """
    # Characters in range 0-31 (0x00-0x1F) are not allowed in ntfs filenames.
    ntfs_characters = [chr(i) for i in range(0, 31)]
    characters = [
        '"',
        "\#",
        "\$",
        "\%",
        "'",
        "\*",
        "\,",
        "\.",
        "\/",
        "\:",
        '"',
        "\;",
        "\<",
        "\>",
        "\?",
        "\\",
        "\^",
        "\|",
        "\~",
        "\\\\",
    ]
    pattern = "|".join(ntfs_characters + characters)
    regex = re.compile(pattern, re.UNICODE)
    filename = regex.sub("", s)
    return filename[:max_length].rsplit(" ", 0)[0]


def create_logger(level: int = logging.ERROR) -> logging.Logger:
    """Create a configured instance of logger.

    :param int level:
        Describe the severity level of the logs to handle.
    """
    fmt = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    date_fmt = "%H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # https://github.com/nficano/pytube/issues/163
    logger = logging.getLogger("pytube")
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
