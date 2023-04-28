
import sys
import traceback


def eprint(error: Exception) -> None:
    '''print exception traceback'''
    traceback.print_exception(error, limit=2, file=sys.stdout)
