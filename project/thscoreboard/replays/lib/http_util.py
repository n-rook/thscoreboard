"""Contains utility functions to deal with HTTP."""

from urllib import parse


def GetDownloadFileHeaders(ascii_filename: str, full_filename: str):
    """Returns file headers (as a dict) to suggest downloading a file.
    
    Args:
        ascii_filename: An ASCII-only filename. Used by ancient browsers.
        full_filename: A UTF-8 filename.
    
    Returns:
        A dict defining the "Content-Type" and "Content-Disposition"
        headers.
    """

    # See https://datatracker.ietf.org/doc/html/rfc5987
    content_disposition = 'attachment; filename="{ascii_filename}"; filename*=utf-8\'\'{utf8_filename}'.format(
        ascii_filename=ascii_filename,
        utf8_filename=parse.quote_plus(full_filename, encoding='UTF-8'))
    
    return {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': content_disposition
    }
