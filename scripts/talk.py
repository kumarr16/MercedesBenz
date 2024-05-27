import random


class Talk:
    """ GrandPy can talk! """

    def __init__(self):
        """ List of sentences """

        self.sentences = {
            "OK": ["Oui, je me souviens de cet endroit !",
                   "Je connais bien cet endroit !",
                   "J'adore ce lieu !"],

            "Map Error": ["Désolé, je ne peux rien t'indiquer.",
                          "Euh... je ne connais pas.",
                          "Je ne sais pas de quoi tu parles."],

            "Place Error": ["Désolé, je ne sais rien.",
                            "Je ne connais pas, désolé !",
                            "Je n'en ai jamais entendu parler."]
        }

    def sentence(self, key):
        """ Return a random sentence. """
        return self.sentences[key][random.randint(0, 2)]
