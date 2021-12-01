from typing import Type, Optional


def exception_raiser(exception_class: Type[Exception], msg: Optional[str] = None) -> None:
    """
    @param exception_class: Any exception class
    @param msg: Exception message. Optional. By default False.
    @return: None
    @raise: exception_class with msg if msg passed.
    """
    raise exception_class(msg) if msg is not None else exception_class()