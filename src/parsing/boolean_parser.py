# Simple parser module for boolean expressions used in search queries

# Grammar:
# Terms - any word that does not contain "AND" or "NOT" or "OR"
# Operators - "AND", "OR", "NOT"

# Tokens
AND, OR, NOT = "AND", "OR", "NOT"
LPAREN, RPAREN = "(", ")"


# Rules
# Expression -> LPAREN Expression RPAREN | Expression AND Expression | Expression OR Expression | NOT Expression | Term

class ParseError(Exception):
    """
    Exception raised when the parser fails to parse the input.
    """

    def __init__(self, position, message, *args):
        self.position = position
        self.message = message
        self.args = args

    def __str__(self):
        return f'${self.message} at position {self.position}'


class Parser:
    def __init__(self):
        self.cache = {}
        self.text, self.position, self.max_idx = None, None, None

    def parse(self, text: str):
        """
        Parses the given text and return a list of tokens or throws a ParseError exception if the text is invalid
        :param text: The text to parse
        :return: A list of tokens
        """
        self.text = text
        self.position = -1  # Set position to -1 since we have not started parsing yet
        self.max_idx = len(text) - 1  # Store the maximum index of the text
        result = self._parse()  # Parse the text
        self._validate_end()  # Validate that the text has been parsed correctly
        return result

    def _validate_end(self):
        """
        Validate that the text has been parsed correctly. If not the parser will raise a ParseError exception.
        :return:
        """
        if self.position < self.max_idx:
            raise ParseError(self.position + 1, f'Unexpected end of input instead of {self.text[self.position + 1]}')

    def _consume_whitespace(self):
        """
        Consume whitespace characters from the input.
        :return:
        """
        while self.position < self.max_idx and self.text[self.position].isspace():
            self.position += 1

    def _extract_char(self, chars=None):
        if self.position >= self.max_idx:
            raise ParseError(self.position + 1,
                             f'Unexpected end of input instead of {chars if chars is not None else "character"}')
        next_char = self.text[self.position + 1]
        if chars is None:
            self.position += 1
            return next_char

        
