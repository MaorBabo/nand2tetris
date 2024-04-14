# Signs And Chars
DOCUMENTATION_START = "/**"
MULTILINE_COMMENT_START = "/*"
MULTILINE_COMMENT_OR_DOC_END = "*/"
COMMENT = "//"
SPACE = " "
NEW_LINE = "\n"
TAB = "\t"
QUOTATION_MARK = '"'
UNDERSCORE = "_"
SEMICOLON = ";"

# Errors Messages - JackTokenizer
ERROR_NO_MORE_COMMAND = "No more command left"
ERROR_UNKNOWN_TOKEN = '"{}" is unknown token'
WRONG_CALL = 'Wrong call! called "{}" method called on "{}" token'

# Errors Messages - JackTokenizer
SYNTAX_ERROR = 'Excepted: {} but got: {}'

# Token Types
TOKEN_KEYWORD = "KEYWORD"
TOKEN_SYMBOL = "SYMBOL"
TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_INT_CONST = "INT_CONST"
TOKEN_STRING_CONST = "STRING_CONST"

# {Keyword/Symbol types}: Token type - dictionary
TOKEN_TYPE_DICT = {"class": TOKEN_KEYWORD,
                   "constructor": TOKEN_KEYWORD,
                   "function": TOKEN_KEYWORD,
                   "method": TOKEN_KEYWORD,
                   "field": TOKEN_KEYWORD,
                   "static": TOKEN_KEYWORD,
                   "var": TOKEN_KEYWORD,
                   "int": TOKEN_KEYWORD,
                   "char": TOKEN_KEYWORD,
                   "boolean": TOKEN_KEYWORD,
                   "void": TOKEN_KEYWORD,
                   "true": TOKEN_KEYWORD,
                   "false": TOKEN_KEYWORD,
                   "null": TOKEN_KEYWORD,
                   "this": TOKEN_KEYWORD,
                   "let": TOKEN_KEYWORD,
                   "do": TOKEN_KEYWORD,
                   "if": TOKEN_KEYWORD,
                   "else": TOKEN_KEYWORD,
                   "while": TOKEN_KEYWORD,
                   "return": TOKEN_KEYWORD,
                   '{': TOKEN_SYMBOL,
                   '}': TOKEN_SYMBOL,
                   '(': TOKEN_SYMBOL,
                   ')': TOKEN_SYMBOL,
                   '[': TOKEN_SYMBOL,
                   ']': TOKEN_SYMBOL,
                   '.': TOKEN_SYMBOL,
                   ',': TOKEN_SYMBOL,
                   ';': TOKEN_SYMBOL,
                   '+': TOKEN_SYMBOL,
                   '-': TOKEN_SYMBOL,
                   '*': TOKEN_SYMBOL,
                   '/': TOKEN_SYMBOL,
                   '&': TOKEN_SYMBOL,
                   '&amp;': TOKEN_SYMBOL,
                   '|': TOKEN_SYMBOL,
                   '<': TOKEN_SYMBOL,
                   '&lt;': TOKEN_SYMBOL,
                   '>': TOKEN_SYMBOL,
                   '&gt;': TOKEN_SYMBOL,
                   '=': TOKEN_SYMBOL,
                   '~': TOKEN_SYMBOL,
                   '^': TOKEN_SYMBOL,  # ShiftLeft
                   '#': TOKEN_SYMBOL}  # ShiftRight

SYMBOLS_AND_SPACE = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-',
                     '*', '/', '&', '|', '<', '>', '=', '~', '^', '#', " "]

LT = '&lt;'
GT = '&gt;'
QUOT = '&quot;'
AMP = '&amp;'

PROBLEMATIC_SYMBOLS_EXCHANGE = {'<': LT,
                                '>': GT,
                                '"': QUOT,
                                '&': AMP
                                }

INT_CONST_MIN_VAL = 0
INT_CONST_MAX_VAL = 32767

LET_STATEMENT = "let"
IF_STATEMENT = "if"
WHILE_STATEMENT = "while"
DO_STATEMENT = "do"
RETURN_STATEMENT = "return"
STATEMENT_TYPES = [LET_STATEMENT, IF_STATEMENT, WHILE_STATEMENT, DO_STATEMENT, RETURN_STATEMENT]

UNARY_OP_EXCEPT_MINUS = ["~", "#", "^"]
UNARY_OP = ["~", "-", "#", "^"]
CONSTANT_KEYWORDS = ["true", "false", "null", "this"]
TERMS_TOKENS = CONSTANT_KEYWORDS + ['('] + UNARY_OP_EXCEPT_MINUS
TERMS_TYPES = [TOKEN_INT_CONST, TOKEN_STRING_CONST, TOKEN_IDENTIFIER]
