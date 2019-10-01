# -*- coding: utf-8 -*-

import os
from unittest import main, TestCase
import json

from g2p.tests.private.git_data_wrangler import returnLinesFromDocuments
from g2p.tests.private import __file__ as private_dir_f
from g2p.log import LOGGER


class Story:
    '''
    Initialize class with path (json,data,word document).
    Access story data.
    '''
    def __init__(self, path: str):
        '''
        The path should be to one of the three:
        - a word document containing the data
        - a json file containing the data
        - add actual data, not sure of file type?
        '''
        self.path = path
        
        if self.path.lower().endswith('.docx'):
            self.data = self.parse_word(self.path)
       
        elif self.path.lower().endswith('.json'):
            self.data = self.parse_json(self.path)
        
        else:
            raise TypeError("Not a supported file type")

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def parse_word(self, path: str):
        '''
        Takes the path to a word document.
        Returns returnLinesFromDocuments.
        '''
        return returnLinesFromDocuments([self.path])

    def parse_json(self, path: str):
        '''
        Takes the path to a JSON file.
        Returns the lines as strings.
        '''
        with open(self.path, 'r') as f:
            json_data = json.load(f)
        return json_data

class Stats:
    def __init__(self, s1: str, s2: str):
        if len(s1) == len(s2):
            self.base_string = s1
            self.compare_string = s2
        else:
            # Assign longest string as base, shorter as compare
            self.base_string = max(s1, s2)
            self.compare_string = min(s1, s2)
      
    def compare_words(self):
        '''
        Count the number of words in a line and count the number of words which do not match between two lists.
        Print the percentage of words which do not match.
        '''
        #breaks line into words
        base_words = self.base_string.split()
        compare_words = self.compare_string.split()
        print(base_words)
        print(compare_words)

        #counts the number of words that don't match and prints the percentage error rate
        mismatched_words = []
        for index, word in enumerate(base_words):
            try:
                if word != compare_words[index]:
                    mismatched_words.append((word, compare_words[index]))
            except IndexError:
                mismatched_words.append((word, None))
        mismatch_percentage = (len(mismatched_words) / len(base_words)) * 100
        LOGGER.info("The word error rate is " + str(round(mismatch_percentage, 2)) + "%")
        return mismatch_percentage

    def compare_characters(self):
        ''' TODO: Add docstring
        '''
        
       #breaks line into words
        base_words = self.base_string.split()
        compare_words = self.compare_string.split()
        
        #TODO: write a unit test
        
        #turns base_word string into an indexed list of words
        mismatch_words = []
        #unequal_words contains words that are not exact matches
        unequal_words = []
        # threshold for deciding what is a g2p error and what is a offset error
        threshold = 75
        under_threshold_mismatch_words = [] # these are words that are under the threshold
        char_mismatch_percentage = 0
        #sets count for indexes in compare_words
        offset = 0
        for word_index, word in enumerate(base_words):
            try:
                while offset <= 1:
                    #identifies mismatches
                    if word != compare_words[word_index+offset]:
                        #adds mismatched words to unequal_words
                        unequal_words.append(compare_words[word_index+offset])
                        #split words into characters and stores them in lists
                        base_chars = [char for char in word]
                        compare_chars = [char for char in compare_words[word_index+offset]]                    
                        
                        #turns base_chars in to an indexed list of characters
                        mismatch_chars = []
                        for char_index, char in enumerate(base_chars):
                            try:
                                #compares with compare_chars by index
                                if char != compare_chars[char_index]:
                                    #add mismatched word with compare word to new list
                                    mismatch_chars.append((char, compare_chars[char_index]))
                                    
                            except IndexError:
                                LOGGER.info('The indexes for chars were not able to be compared.Check for irregular formatting of input data.')
                        #calculates the character mismatch percentage
                        char_mismatch_percentage = int((len(mismatch_chars) / len(base_chars)) * 100)
                        #for a character error rate of less than or equal to 75%
                        if char_mismatch_percentage <= threshold:
                            LOGGER.info('mismatch words: {}'.format(mismatch_words))
                            #add mismatched word with compare word to new list
                            under_threshold_mismatch_words.append((word, compare_words[word_index+offset]))
                            break
                        #otherwise if more than 75% of the word is wrong, add one to the offset and try again
                        else:
                            offset += 1
                            break
                    else:
                        break

            except IndexError:
                LOGGER.info('The words were not able to be split into characters. Check for irregular formatting of input data.')
                
            
        # LOGGER.info('Word percentage error rate was not calculated correctly. Check that counter is functioning as expected.')
        print("The character error rate is " + str(char_mismatch_percentage) + "%")
        mismatch_percentage = int((len(under_threshold_mismatch_words) / len(base_words)) * 100)
        LOGGER.info("The word error rate is " + str(round(mismatch_percentage, 2)) + "%")
        return char_mismatch_percentage, under_threshold_mismatch_words, mismatch_percentage

class StatsTest(TestCase):
    ''' Basic Test for Stats
    '''
    def setUp(self):
        # Any setup goes here
        pass

    def test_identical(self):
        ''' Test two identical strings
        '''
        print("test_identical")
        stats = Stats('test', 'test')
        print("stats")
        self.assertEqual(stats.compare_characters(),(0,[],0))

    def test_word_mismatch(self):
        ''' Test two non-identical words
        '''
        print("test_word_mismatch")
        stats = Stats('test', 'pest')
        self.assertEqual(stats.compare_characters(), (25, [('test', 'pest')], 100))

    def test_char_mismatch(self):
        ''' Test two strings differing by one character and by all characters
        '''
        print("test_char_mismatch1")
        stats_one_diff = Stats('test', 'pest')
        self.assertEqual(stats_one_diff.compare_characters(), (25, [('test', 'pest')],100))
        print("test_char_mismatch2")
        stats_all_diff = Stats('test', 'step')
        self.assertEqual(stats_all_diff.compare_characters(), (100, [('test', 'step')],100))

    def test_unequal_word_length(self):
        ''' Test two strings with differing numbers of words
        '''
        print("test_unequal_word_length1")
        stats_unequal_end = Stats('this is a test case', 'this is a test')
        self.assertEqual(stats_unequal_end.compare_characters(),(0, [], 20)) 
        print("test_unequal_word_length2")
        stats_unequal_mid = Stats('This test is mine', 'This test is not mine')
        self.assertEqual(stats_unequal_mid.compare_characters(), (0, [], 20)) 

    def test_unequal_char_length(self):
        '''Test two words with differing numbers of characters
        '''
        print("test_unequal_char_length1")
        stats_unequal_char_end = Stats('test', 'tests')
        self.assertEqual(stats_unequal_char_end.compare_characters(), (20, [('tests', 'test')], 100)) # TODO: This is producing 0 but should produce 1
        print("test_unequal_char_length2")
        stats_unequal_char_mid = Stats('test', 'teast')
        self.assertEqual(stats_unequal_char_mid.compare_characters(), (20, [('test', 'teast')],100)) # TODO: This is producing 50 but should produce 20
        

if __name__ == '__main__': 
    # orth_to_ipa_mapping = Mapping(
    #         language={"lang": "git", "table": "Orthography (Deterministic)"})
    # ipa_to_apa_mapping = Mapping(
    #         language={"lang": "git", "table": "APA"}, reverse=True)
    # orth_to_apa_transducer = CompositeTransducer([orth_to_ipa_mapping, ipa_to_apa_mapping])
    # mapping = Mapping(language={"lang": "git", "table": "Orthography (Deterministic)"}, case_sensitive=False)
    # transducer = Transducer(mapping)
    # private_dir = os.path.dirname(private_dir_f)
    # story_json = Story(os.path.join(private_dir, 'BS - Dihlxw', 'Dihlxw Story 2013-04-29 for HD copy - clean.json'))  
    # story_docx = Story(os.path.join(private_dir, 'BS - Dihlxw', 'Dihlxw Story 2013-04-29 for HD copy - clean.docx')) 
    main()