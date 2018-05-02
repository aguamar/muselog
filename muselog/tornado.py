"""
Helpers to log tornado request information.
"""

import logging

import tornado
from tornado import escape

logger = logging.getLogger(__name__)


def log_request(handler):
    """Log the request information with extra context for use w/ Graylog-enabled apps."""

    response_status = handler.get_status()
    request_time = 1000.0 * handler.request.request_time()
    request_summary = handler._request_summary()

    if response_status < 400:
        log_method = logger.info
    elif response_status < 500:
        log_method = logger.warning
    else:
        log_method = logger.error

    try:
        req_body = escape.json_decode(handler.request.body)
    except:
        req_body = {}

    log_method("%d %s %.2fms", response_status, request_summary, request_time,
               extra={"request_duration": request_time,
                      "request_body": handler.request.body,
                      "request_method": handler.request.method,
                      "request_path": handler.request.path,
                      "request_query": handler.request.query,
                      "request_remote_ip": handler.request.remote_ip,
                      "response_status": response_status,
                      "request_summary": request_summary})
