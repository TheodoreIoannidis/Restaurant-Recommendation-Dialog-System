from models.preprocessor import Preprocessor
from Levenshtein import distance
class SystemInfoRetriever:
    def __init__(self, info_dict, restaurant_info_df, caps= False):
        self.preprocessor = Preprocessor()
        self.restaurant_info_df = restaurant_info_df.copy()
        self.info_dict = info_dict
        self.caps = caps

    def _get_column_by_word(self, word, dataframe):
        for column in ["pricerange", "area", "food"]:
            for item in dataframe[column].values:
                try:
                    stemmed_item = self.preprocessor.stem_word(item)
                    # compare stem Levenstein distance
                    if distance(word, stemmed_item) <=1 :
                        return column, item
                except:
                    pass
        return None

    def get_info_from_input(self, user_input):
        """
        Method to find preferences in user input and fill in the info dict
        """
        tokens = self.preprocessor.preprocess_sentence(user_input)

        for token in tokens:
            info = self._get_column_by_word(token, self.restaurant_info_df)
            if info is not None:
                column, word = info
                if self.info_dict[column] is None:
                    self.info_dict[column] = word
                    print(f"{column} = {word}" if not self.caps else f"{column} = {word}".upper())
            

        if "any" in user_input:
            for column, value in self.info_dict.items():
                if self.info_dict[column] is None:
                    self.info_dict[column] = "dontcare"
                    print(f"{column} = dontcare" if not self.caps else f"{column} = dontcare".upper())
                    break
