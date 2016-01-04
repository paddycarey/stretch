

class StretchException(Exception):
    """Common base class for all exceptions raised explicitly by stretch.

    Exceptions which are subclasses of this type will be handled nicely by
    stretch and will not cause the program to exit. Any exceptions raised
    which are not a subclass of this type will exit(1) and print a traceback
    to stdout.
    """
    level = "error"

    def __init__(self, message, **kwargs):
        Exception.__init__(self, message)
        self.message = message
        self.kwargs = kwargs

    def format_message(self):
        return self.message

    def __unicode__(self):
        return self.message

    def __str__(self):
        return self.message.encode('utf-8')
