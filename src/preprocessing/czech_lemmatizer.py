import simplemma


class CzechLemmatizer:
    langdata = simplemma.load_data('cs')

    def lemmatize(self, word):
        return simplemma.lemmatize(word, self.langdata)
