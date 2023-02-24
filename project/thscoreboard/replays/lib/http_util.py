"""Contains utility functions to deal with HTTP."""


def GetDownloadFileHeaders(filename: str):
    """Returns file headers (as a dict) to suggest downloading a file.
    
    Args:
        filename: An ASCII-only filename.
    
    Returns:
        A dict defining the "Content-Type" and "Content-Disposition"
        headers.
    """

    # See https://datatracker.ietf.org/doc/html/rfc5987
    
    return {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
