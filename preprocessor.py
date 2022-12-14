import os
import re
from helpers import pymongo_get_database
from helpers import ini_config_reader


class Preprocessor:
    def clean(self, tweet):
        tweet = self._removeTwitterSymbols(tweet)
        tweet = self._demojize(tweet)
        tweet = self._removeQuotationMarks(tweet)
        tweet = self._removePunctuations(tweet)
        tweet = self._mergeWhiteSpaces(tweet)
        return tweet

    def _removeTwitterSymbols(self, tweet):
        """ This function is intended to clean tweets further for passing
        for sentiment classification task
        """
        # tweet = tweet.lower()
        # remove retweets and their original_users
        tweet = re.sub(r'^rt', " ", tweet)
        # remove user_mentions
        tweet = re.sub(r'@\w{1,15}[.]*', " ", tweet)
        # remove hash tags
        tweet = re.sub(r'#(\w)*[.]*', " ", tweet)
        # remove url links and use keyword URL
        tweet = re.sub(r'(https://)[\S]*', " ", tweet)
        tweet = re.sub(r'(http://)[\S]*', " ", tweet)

        # remove inverted commas like “ ” and ‘ ’
        tweet = re.sub(r'“|”', " ", tweet)
        tweet = re.sub(r'‘|’', " ", tweet)

        # remove dots and ellipses(...)
        tweet = re.sub(r'\.{2,}', '', tweet)

        return tweet

    def _removeUnicodeEmojis(self, tweet):
        '''
        remove all the emojis and graphical symbols
        '''
        # convert emoji like 😀 to '\U0001f600' string
        u_text = tweet.encode("unicode_escape")

        u_text = u_text.decode("utf-8", "replace")

        # 0x1F600...0x1F64F, // Emoticons
        emoticons_regex = r"\s*\\U0001f6[0-4][0-9a-f]\s*"
        # 0x1F300...0x1F5FF, // Misc Symbols and Pictographs
        pictoGraphs_regex = r"\s*\\U0001f[3-5][0-9a-f][0-9a-f]\s*"
        # 0x1F680...0x1F6FF, // Transport and Map
        map_regex = r"\s*\\U0001f6[8-9a-f][0-9a-f]\s*"
        # 0x2600...0x26FF,   // Misc symbols
        misc_symbols_regex = r"\s*\\U000026[0-9a-f][0-9a-f]\s*"
        # 0x2700...0x27BF,   // Dingbats
        dingbats_regex = r"\s*\\U000027[0-9a-b][0-9a-f]\s*"
        # 0xFE00...0xFE0F,   // Variation Selectors
        variation_selectors_regex = r"\s*\\U0000fe0[0-9a-f]\s*"
        # 0x1F900...0x1F9FF, // Supplemental Symbols and Pictographs
        supplimental_symbols_regex = r"\s*\\U0001f9[0-9a-f][0-9a-f]\s*"
        # 0x1F1E6...0x1F1FF: // Flags
        flags_regex = r"\s*\\U0001f1[e-f][6-9a-f]\s*"
        random_regex = r"\s*\\U0001f[1-9]f[1-9]\s*"

        other_regex = r'\\(n|x..)'
        regex = r'\s*\\(u|U)*[0-9a-z]*'

        u_text = re.sub(emoticons_regex, " ", u_text)
        u_text = re.sub(pictoGraphs_regex, " ", u_text)
        u_text = re.sub(map_regex, " ", u_text)
        u_text = re.sub(misc_symbols_regex, " ", u_text)
        u_text = re.sub(dingbats_regex, " ", u_text)
        u_text = re.sub(variation_selectors_regex, " ", u_text)
        u_text = re.sub(supplimental_symbols_regex, " ", u_text)
        u_text = re.sub(flags_regex, " ", u_text)
        u_text = re.sub(random_regex, " ", u_text)
        u_text = re.sub(other_regex, " ", u_text)
        u_text = re.sub(regex, " ", u_text)

        return u_text

    def _demojize(self, tweet):
        emoticons_happy = set([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
            '<3'])
        emoticons_sad = set([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
            ':c', ':{', '>:\\', ';('])
        emoji_happy = set(
            ['😋', '😊', '😉', '😌', '😚', '😀', '😀', '😁', '😂', '😃', '😄', '🤣', '😅', '😆', '😉', '🙂', '🙃', '😌', '🤪', '😜', '😝',
             '😛', '🤑', '😎', '🤓', '🤗', '😏', '😺', '😸', '😹', '😻', '😈', '🤠'])
        emoji_sad = set(
            ['☹', '🙁', '😕', '😔', '🤬', '😡', '😠', '😟', '😞', '😒', '😣', '😖', '😫', '😩', '😤', '😱', '😨', '😰', '😧', '😢', '😥',
             '😪', '😓', '😿', '😾'])

        # escape special regex characters
        happy_patterns = set([
            '\:-\)', '\:\)', ';\)', '\:o\)', '\:]', '\:3', '\:c\)', '\:>', '=]', '8\)', '=\)', '\:}',
            '\:\^\)', '\:-D', '\:D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', '\:-\)\)', "\:'-\)", "\:'\)", '\:\*', '\:\^\*', '>\:P', '\:-P', '\:P', 'X-P',
            'x-p', 'xp', 'XP', '\:-p', '\:p', '=p', '\:-b', '\:b', '>\:\)', '>;\)', '>\:-\)',
            '<3']).union(emoji_happy)

        sad_patterns = set([
            '\:L', '\:-/', '>\:/', '\:S', '>\:\[', '\:@', '\:-\(', '\:\[', '\:-\|\|', '=L', '\:<',
            '\:-\[', '\:-<', '=\\\\', '=/', '>\:\(', '\:\(', '>.<', "\:'-\(", "\:'\(", '\:\\\\', '\:-c',
            '\:c', '\:{', '>\:\\\\', ';\(']).union(emoji_sad)

        emo_pos_regex = r'\s*(?:' + r'|'.join(list(happy_patterns)) + r')\s*'
        emo_neg_regex = r'\s*(?:' + r'|'.join(list(sad_patterns)) + r')\s*'

        tweet = re.sub(emo_pos_regex, " EMO_POS ", tweet)
        tweet = re.sub(emo_neg_regex, " EMO_NEG ", tweet)

        tweet = self._removeUnicodeEmojis(tweet)

        return tweet

    def _removeQuotationMarks(self, tweet):
        regex = r"(?:^\'|^\"|\'$|\"$|\'\s*\'|\'\s*\'|\'\s*\"|\"\s*\'|\"\s*\"|\s+\"|\s+\'|\'\s+|\"\s)"
        tweet = re.sub(regex, ' ', tweet)
        return tweet

    def _removePunctuations(self, tweet):
        punctuations = ['!', '#', '\$', '%', '&', '\\\\', '\*', '\+', '/', ':', ';', '<', '=', '>', '\?', '\|', '\~',
                        '\^', '\`', '\(', '\{', '\[', '\)', '\}', '\]']
        regex = r'\s*(?:' + r'|'.join(punctuations) + r')\s*'
        tweet = re.sub(regex, ' ', tweet)
        return tweet

    def _mergeWhiteSpaces(self, tweet):
        tweet = re.sub(r'[\s]+', ' ', tweet)
        return tweet


if __name__ == "__main__":
    config = ini_config_reader.read_config()
    tweet_topic = config['topic_config']['topic_title']
    preprocessor = Preprocessor()
    db = pymongo_get_database.get_database()
    collection = db[f'tweet_extract_{tweet_topic}']
    extracted_tweet = collection.find()
    cleaned_tweets = []
    for item in extracted_tweet:
        clean_tweet = preprocessor.clean(item['tweet_text'])
        cleaned_tweets.append({'_id': item['_id'], 'cleaned_tweet_text': clean_tweet})
    clean_tweet_collection = db[f'cleaned_tweet_{tweet_topic}']
    clean_tweet_collection.insert_many(cleaned_tweets)
