from typing import Type, Optional


def exception_raiser(exception_class: Type[Exception], msg: Optional[str] = None) -> None:
    """ The function to raise an exception """
    raise exception_class(msg) if msg is not None else exception_class()