# -*- coding: utf-8 -*-

import os
import json
from g2p.tests.private.git_data_wrangler import returnLinesFromDocuments
from g2p.tests.private import __file__ as private_dir_f
from g2p.mappings import Mapping
from g2p.transducer import CompositeTransducer, Transducer
from typing import List, Union

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

class Stats(Story):
    def __init__(self, base_string: str, compare_string: str): 
        self.base_string = base_string
        self.compare_string = compare_string
      
    def test_words(self):
        '''
        Count the number of words in a line and count the number of words which do not match between two lists.
        Print the percentage of words which do not match.
        '''
        #breaks line into words
        base_words = self.base_string.split()
        compare_words = self.compare_string.split()

        #counts the number of words that don't match and prints the percentage error rate
        word_mismatch_count = 0
        for index, word in enumerate(base_words):
            try:
                if word != compare_words[index]:
                    word_mismatch_count += 1
            except IndexError:
                #TODO: put log message here
                pass
        
        mismatch_percentage = (word_mismatch_count / len(base_words)) * 100
        # TODO: log this as INFO
        print("The word error rate is" + str(mismatch_percentage) + "%")
        return mismatch_percentage

    def test_characters(self, base_string: str, compare_string: str):
        '''
        Calculates the number of characters per word in a line.

        '''
        
       #breaks line into words
        base_words = self.base_string.split()
        compare_words = self.compare_string.split()
        
        #turns the words into a list and compares two lists by index
        #identifies mismatches and splits mismatched words into characters
        for index, word in enumerate(base_words):
            try:
                if word != compare_words[index]:
                    base_chars = base_words.split()
                    compare_chars = compare_chars.split()

            except IndexError:
                #TODO: put log message here
                pass
            
            #counts the number of words that don't match and prints the percentage error rate
            char_mismatch_count = 0
            for index,char in enumerate(base_chars):
                try:
                    if char != compare_chars[index]:
                        char_mismatch_count += 1
               
                except IndexError:
                    #TODO: put log message here
                    pass
        
        char_mismatch_percentage = (char_mismatch_count / len(base_chars)) * 100
        # TODO: log this as INFO
        print("The word error rate is" + str(char_mismatch_percentage) + "%")
        return char_mismatch_percentage



    

if __name__ == '__main__':
    orth_to_ipa_mapping = Mapping(
            language={"lang": "git", "table": "Orthography (Deterministic)"})
    ipa_to_apa_mapping = Mapping(
            language={"lang": "git", "table": "APA"}, reverse=True)
    orth_to_apa_transducer = CompositeTransducer([orth_to_ipa_mapping, ipa_to_apa_mapping])
    mapping = Mapping(language={"lang": "git", "table": "Orthography (Deterministic)"}, case_sensitive=False)
    transducer = Transducer(mapping)
    private_dir = os.path.dirname(private_dir_f)
    story_json = Story(os.path.join(private_dir, 'BS - Dihlxw', 'Dihlxw Story 2013-04-29 for HD copy - clean.json'))  
    story_docx = Story(os.path.join(private_dir, 'BS - Dihlxw', 'Dihlxw Story 2013-04-29 for HD copy - clean.docx')) 
    breakpoint()