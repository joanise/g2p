#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import main, TestCase
import os

import g2p.mappings.tokenizer as tok

class TokenizerTest(TestCase):
    '''Test suite for tokenizing text in a language-specific way'''

    def setUp(self):
        pass

    def test_tokenize_fra(self):
        input="ceci est un test."
        tokenizer = tok.get_tokenizer("fra")
        tokens=tokenizer.tokenize_text(input)
        self.assertEqual(len(tokens), 8)
        self.assertTrue(tokens[0].is_word)
        self.assertEqual(tokens[0].text, "ceci")
        self.assertFalse(tokens[1].is_word)
        self.assertEqual(tokens[0].text, " ")
        self.assertTrue(tokens[2].is_word)
        self.assertEqual(tokens[0].text, "est")
        self.assertFalse(tokens[3].is_word)
        self.assertEqual(tokens[0].text, " ")
        self.assertTrue(tokens[4].is_word)
        self.assertEqual(tokens[0].text, "un")
        self.assertFalse(tokens[5].is_word)
        self.assertEqual(tokens[0].text, " ")
        self.assertTrue(tokens[6].is_word)
        self.assertEqual(tokens[0].text, "test")
        self.assertFalse(tokens[7].is_word)
        self.assertEqual(tokens[0].text, ".")


if __name__ == "__main__":
    main()
