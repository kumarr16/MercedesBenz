import wikipedia


class ApiWikipedia:
    """ Request for information about a place. """

    def __init__(self):
        """ Wikipedia France """
        wikipedia.set_lang("fr")

    def find(self, keywords):
        """ Creation of a dictionary to keep the information found. """

        try:
            # Select the first element that corresponds to the keywords.
            page = wikipedia.search(keywords, results=1)[0]

        except IndexError:
            return False

        url = wikipedia.page(page).url
        summary = wikipedia.summary(page)

        return {
            "summary": summary,
            "url": url
        }
