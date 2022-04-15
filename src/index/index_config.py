from src.preprocessing.preprocessing import Preprocessor

# Default search
default_models = ['tf_idf', 'boolean']

# Additional search that can be added to the default search
additional_models = ['transformers', 'doc2vec']


class IndexConfig:
    """
    Configuration for the index object
    """

    def __init__(self, name, models, preprocessor: Preprocessor):
        """
        Constructor for the IndexConfig object
        :param name: name of the index
        :param models: list of search models to use
        :param preprocessor: preprocessor to use
        """
        for model in models:
            if model not in additional_models:
                raise ValueError(f'{model} is not a valid model')

        self.name = name
        self.models = models + default_models
        self.preprocessor = preprocessor
