from src.preprocessing.preprocessing import Preprocessor


class IndexConfig:
    """
    Configuration for the index object
    """

    def __init__(self, name, preprocessor: Preprocessor):
        """
        Constructor for the IndexConfig object
        :param name: name of the index
        :param preprocessor: preprocessor to use
        """
        self.name = name
        self.preprocessor = preprocessor
