"""Manejadores de errores HTTP - punto de entrada centralizado."""

from api.error_handlers.not_found_handler import handle_not_found
from api.error_handlers.internal_error_handler import handle_internal_error
from api.error_handlers.method_not_allowed_handler import handle_method_not_allowed
from api.error_handlers.bad_request_handler import handle_bad_request

__all__ = [
    'handle_not_found',
    'handle_internal_error',
    'handle_method_not_allowed',
    'handle_bad_request',
]
