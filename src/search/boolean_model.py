from typing import List

from src.index.document import Document
from src.index.index import Index
from src.preprocessing.preprocessing import Preprocessor
from src.search.search_model import SearchModel


class BooleanModel(SearchModel):

    def __init__(self, index: Index, preprocessor: Preprocessor):
        super().__init__(index)
        self.preprocessor = preprocessor

    def search(self, query: str, n_items=None) -> List[Document]:
        query_terms = self.preprocessor.get_tokens(query)

        # TODO evaluate boolean expression
