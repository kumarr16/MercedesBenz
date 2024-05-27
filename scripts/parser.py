import re

from .stopwords import STOPWORDS


class Parser:
    """ Try to extract a place from a question. """

    def __init__(self):
        """ The attribute that must be returned. """
        self.place = str()

    def extract(self, string):
        """ Extract words that are not in a list (stopwords). """

        # lowercase
        string = string.lower()

        # no symbols
        string = re.sub("[,-?@#!&.<>^\"""]", " ", string)

        # extract words
        generator = " ".join((word for word in string.split()
                              if word not in STOPWORDS))

        for word in generator:
            self.place += word

        return self.place
