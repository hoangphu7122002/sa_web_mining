import json
import re
import string
from underthesea import text_normalize

# Dictionary definitions
dict_symbol = {
  "-_- ": "chán",
  "8-)": "vui",
  ":$": "thường",
  "=(" : "buồn",
  ":(" : "buồn",
  ":+": "giận",
  ":-(": "khóc",
  ":-H": "giận",
  ":3": "vui",
  ":<": "buồn",
  ":>": "vui",
  ":B": "thường",
  ":D": "vui",
  ":L": "mệt",
  ":P": "vui",
  ":Q": "bực",
  ":T": "bực",
  ":Z": "thường",
  ":o": "thường",
  ":V": "thường",
  ":v": "thường",
  ":|": "thường",
  ":~": "lo",
  ";-X": "bực",
  ";D": "vui",
  ";G": "buồn",
  ";O": "thường",
  ";P": "vui",
  "=)": "vui",
  ":)": "vui",
  ";)" : "vui",
  "=.=": "chán",
  "@@": "chán",
  "B-)": "vui",
  "P-(": "khóc",
  "^^": "vui",
  "T_T" : "buồn",
  "T.T" : "buồn",
  ":-O" : "ngờ",
  ":3" : "vui"
}

dict_symbol.update({key.lower(): value for key, value in dict_symbol.items()})

# Character lists setup
list_chr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
list_dau = 'á, é, í, ó, ú, ý, ắ, ế, ố, ớ, ứ, ử, ấ, ề, ồ, ờ, ừ, ử, ứ'.split(', ')
list_dau += 'à, è, ì, ò, ù, ỳ, ằ, ề, ồ, ờ, ừ, ỳ, ằ, ề, ồ, ờ, ừ, ỳ'.split(', ')
list_dau += 'ã, ẽ, ĩ, ỉ, õ, ũ, ỹ, ẵ, ễ, ỗ, ỡ, ữ, ỷ, ẵ, ễ, ỗ, ỡ, ữ, ỷ'.split(', ')
list_dau += 'ã, ẽ, ĩ, ỉ, õ, ũ, ỹ, ẵ, ễ, ỗ, ỡ, ữ, ỷ, ẵ, ễ, ỗ, ỡ, ữ, ỷ'.split(', ')
list_dau += ['ả', 'ẩ', 'ẳ', 'ẻ', 'ế', 'ể', 'ỉ', 'ị', 'ỏ', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ']
list_dau = list(set(list_dau))

# Combine and extend character lists
list_chr = list_chr + list_dau
list_chr = list_chr + [ele.upper() for ele in list_chr]
list_chr = list_chr + list(range(0,10))

# Generate punctuation-character combinations
punctuation = string.punctuation
list_punc_chr = []
for punc in punctuation:
    for chr in list_chr:
        if (punc in '.,/%|') and isinstance(chr, int):
            continue
        list_punc_chr.append(str(chr) + str(punc))

class TextProcessor:
    """A class for processing Vietnamese text with various cleaning and normalization methods.
    
    This class provides methods to clean, normalize and transform Vietnamese text including:
    - URL removal
    - Special character handling
    - Punctuation normalization
    - Emoji/symbol conversion
    - Vietnamese diacritics handling
    - Text case normalization
    
    Attributes:
        teencode_dict (dict): Dictionary for mapping teencode to standard words
        stopwords (set): Set of Vietnamese stopwords
        tu_dien (set): Dictionary of valid Vietnamese words
    """
    
    def __init__(self, teencode_path=None, tudien_path=None, single_word_dict_path=None):
        """Initialize the TextProcessor with paths to required dictionary files.
        
        Args:
            teencode_path (str): Path to teencode dictionary file
            tudien_path (str): Path to main dictionary file
            single_word_dict_path (str): Path to single word dictionary file
        """
        self.teencode = self._load_teencode(teencode_path) if teencode_path else []
        self.tu_dien = self._load_dictionaries(tudien_path, single_word_dict_path) if tudien_path and single_word_dict_path else set()

    def _load_teencode(self, path):
        """Load teencode dictionary from file.
        
        Args:
            path (str): Path to teencode file
            
        Returns:
            list: List of [teencode, standard_word] pairs
        """
        try:
            with open(path, "r", encoding='utf-8') as f:
                teencode = f.read().split('\n')
            return [pair.split("\t") for pair in teencode if pair]
        except Exception as e:
            print(f"Warning: Could not load teencode file: {e}")
            return []

    def _load_dictionaries(self, tudien_path, single_word_path):
        """Load and combine dictionaries from files.
        
        Args:
            tudien_path (str): Path to main dictionary file
            single_word_path (str): Path to single word dictionary file
            
        Returns:
            set: Combined set of dictionary words
        """
        tu_dien = set()
        try:
            # Load main dictionary
            with open(tudien_path, 'r', encoding='utf-8') as f:
                tu_dien.update(json.load(f).keys())
                
            # Load single word dictionary
            with open(single_word_path, 'r', encoding='utf-8') as f:
                tu_dien.update(json.load(f).keys())
                
            # Remove single characters
            tu_dien = {word for word in tu_dien if word not in list_chr}
            
            return tu_dien
        except Exception as e:
            print(f"Warning: Could not load dictionary files: {e}")
            return set()

    def remove_acronyms(self, text):
        """Replace Vietnamese internet acronyms with their standard forms.
        
        Args:
            text (str): Input text containing acronyms
            
        Returns:
            str: Text with acronyms replaced by standard words
            
        Example:
            >>> processor.remove_acronyms("k thể tin nổi")
            "không thể tin nổi"
        """
        for x in self.teencode:
            text = re.sub(fr' {x[0]} |^{x[0]} | {x[0]}$', fr' {x[1]} ', text)
        return text

    def remove_diacritics(self, text):
        """Remove Vietnamese diacritics from text.
        
        Args:
            text (str): Input text with diacritics
            
        Returns:
            str: Text with diacritics removed
            
        Example:
            >>> processor.remove_diacritics("Xin chào thế giới")
            "Xin chao the gioi"
        """
        diacritics_map = {
            'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
            'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
            'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
            'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
            'ê': 'e', 'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
            'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
            'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
            'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
            'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
            'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
            'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
            'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
            'đ': 'd',
        }
        
        result = text
        for diacritic, plain in diacritics_map.items():
            result = result.replace(diacritic, plain)
            result = result.replace(diacritic.upper(), plain.upper())
        return result

    def normalize_whitespace(self, text):
        """Normalize whitespace in text by removing extra spaces and standardizing line endings.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Remove spaces at the beginning and end of lines
        text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
        return text.strip()

    def remove_repeated_words(self, text):
        """Remove immediately repeated words in text.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with repeated words removed
            
        Example:
            >>> processor.remove_repeated_words("xin xin chào chào bạn bạn")
            "xin chào bạn"
        """
        words = text.split()
        result = []
        for i, word in enumerate(words):
            if i == 0 or word != words[i-1]:
                result.append(word)
        return ' '.join(result)

    def normalize_numbers(self, text):
        """Standardize number formats in text.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with standardized number formats
            
        Example:
            >>> processor.normalize_numbers("giá 15,000,000đ và 98k")
            "giá 15000000 đồng và 98000"
        """
        # Convert k/K format (e.g., 98k -> 98000)
        text = re.sub(r'(\d+)[kK]\b', lambda m: str(int(m.group(1)) * 1000), text)
        
        # Remove commas in numbers
        text = re.sub(r'(\d+),(\d{3})', r'\1\2', text)
        
        # Standardize currency
        text = re.sub(r'(\d+)đ\b', r'\1 đồng', text)
        
        return text

    def remove_url(self, text):
        """Remove URLs from text.
        
        Args:
            text (str): Input text containing URLs
            
        Returns:
            str: Text with URLs removed
        """
        text = re.sub(r'(http\S+)?(\w+\.)+\S+', '', text)
        return text

    def convert_upper_to_lower(self, text):
        """Convert text to lowercase.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text converted to lowercase
            
        Example:
            >>> processor.convert_upper_to_lower("Xin Chào")
            "xin chào"
        """
        return text.lower()

    def remove_special_character(self, text):
        """Remove special characters while preserving Vietnamese characters.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with special characters removed
            
        Example:
            >>> processor.remove_special_character("Xin chào! @#$%")
            "Xin chào "
        """
        text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]', ' ', text)
        return text

    def remove_duplicate_character(self, text):
        """Remove repeated characters and whitespace, preserving numbers.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with repeated characters removed
            
        Example:
            >>> processor.remove_duplicate_character("helloooo    world!!! 98000")
            "hello world! 98000"
        """
        # Split text into words to preserve numbers
        words = text.split()
        processed_words = []
        
        for word in words:
            # Skip processing if word is a number
            if word.isdigit():
                processed_words.append(word)
            else:
                # Remove repeated characters for non-numeric words
                word = re.sub(r'(.)\1{2,}', r'\1', word)
                processed_words.append(word)
        
        # Join words and normalize spaces
        text = ' '.join(processed_words)
        text = re.sub(r'(\s)\1+', r'\1', text)
        return text

    def replace_double_punc(self, text):
        """Replace repeated punctuation marks with single ones.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized punctuation
            
        Example:
            >>> processor.replace_double_punc("hello!!! world...")
            "hello! world"
        """
        text = text.replace('...', '')
        for punc in punctuation:
            double_punc = punc + punc
            while double_punc in text:
                text = text.replace(double_punc, punc)
            double_punc_2 = punc + ' ' + punc
            while double_punc_2 in text:
                text = text.replace(double_punc_2, punc)
        return text

    def add_space_punc(self, text):
        """Add spaces around punctuation marks for better tokenization.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with spaces added around punctuation
            
        Example:
            >>> processor.add_space_punc("hello,world")
            "hello , world"
        """
        for punc_chr in list_punc_chr:
            punc, chr = punc_chr[-1], punc_chr[0]
            text = text.replace(punc_chr, chr + ' ' + punc)
            text = text.replace(punc+chr, punc + ' ' + chr)
        return text

    def fix_symbol(self, text):
        """Convert emoticons and symbols to their text representation.
        
        Args:
            text (str): Input text containing emoticons/symbols
            
        Returns:
            str: Text with emoticons replaced by their meanings
            
        Example:
            >>> processor.fix_symbol("hello :D")
            "hello vui"
        """
        output = ""
        words = text.split(" ")
        for word in words:
            symbol_found = False
            for key in dict_symbol:
                if key in word:
                    output += dict_symbol[key] + " "
                    symbol_found = True
                    break
            if not symbol_found:
                output += word + " "
        return output.strip()

    def replace_word(self, text):
        """Clean up text by removing redundant punctuation and spaces.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Cleaned text with normalized punctuation and spacing
            
        Example:
            >>> processor.replace_word("hello , world . ")
            "hello world"
        """
        text = re.sub(r"\s+", " ", text)
        replacements = [
            (' , ', ' '), (' . ', ' '), (' " ', ' '), (' ! ', ' '),
            (' ( ', ' '), (' ) ', ' '), (' = ', ' '), (' ? ', ' '),
            (' ,', ' '), (' .', ' '), (' "', ' '), (' !', ' '),
            (' (', ' '), (' )', ' '), (' =', ' '), (' ?', ' '),
            (', ', ' '), ('. ', ' '), ('" ', ' '), ('! ', ' '),
            ('( ', ' '), (') ', ' '), ('= ', ' '), ('? ', ' ')
        ]
        
        for old, new in replacements:
            text = text.replace(old, new)
            
        # Remove trailing punctuation
        idx = len(text) - 1
        while idx >= 0 and text[idx] in punctuation:
            idx -= 1
        return text[:idx + 1]

    def _debug_print(self, step_name, text, print_debug):
        """Helper function to print debug information.
        
        Args:
            step_name (str): Name of the processing step
            text (str): Current text state
            print_debug (bool): Whether to print debug info
        """
        if print_debug:
            print(f"{step_name}: {text}")

    def process_text(self, text, remove_diacritics=False, print_debug=False):
        """Process Vietnamese text with comprehensive cleaning and normalization.
        
        Args:
            text (str): Input text to process
            remove_diacritics (bool): Whether to remove Vietnamese diacritics
            print_debug (bool): Whether to print intermediate results
            
        Returns:
            str: Processed text
        """
        # Normalize text
        
        text = self.normalize_numbers(text)
        self._debug_print("normalize_numbers", text, print_debug)
        
        text = text_normalize(text)
        self._debug_print("text_normalize", text, print_debug)
        
        # Basic cleaning
        text = self.remove_url(text)
        self._debug_print("remove_url", text, print_debug)
        
        text = self.convert_upper_to_lower(text)
        self._debug_print("convert_upper_to_lower", text, print_debug)
        
        text = self.remove_duplicate_character(text)
        self._debug_print("remove_duplicate_character", text, print_debug)
        
        text = self.normalize_whitespace(text)
        self._debug_print("normalize_whitespace", text, print_debug)
        
        
        text = self.remove_repeated_words(text)
        self._debug_print("remove_repeated_words", text, print_debug)
        
        # Advanced processing
        text = self.replace_double_punc(text)
        self._debug_print("replace_double_punc", text, print_debug)
        
        text = self.fix_symbol(text)
        self._debug_print("fix_symbol", text, print_debug)
        
        text = self.add_space_punc(text)
        self._debug_print("add_space_punc", text, print_debug)
        
        text = self.remove_acronyms(text)
        self._debug_print("remove_acronyms", text, print_debug)
        
        text = self.replace_word(text)
        self._debug_print("replace_word", text, print_debug)
        
        text = self.remove_special_character(text)
        self._debug_print("remove_special_character", text, print_debug)
        
        if remove_diacritics:
            text = self.remove_diacritics(text)
            self._debug_print("remove_diacritics", text, print_debug)

        return text.strip() 