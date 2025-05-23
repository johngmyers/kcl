# Copyright The KCL Authors. All rights reserved.

import sys
import unittest

import kclvm_runtime

dylib = kclvm_runtime.KclvmRuntimeDylib()

# https://github.com/python/cpython/blob/main/Lib/test/string_tests.py


class BaseTest(unittest.TestCase):

    # check that obj.method(*args) returns result
    def checkequal(self, result, obj, methodname, *args, **kwargs):
        realresult = dylib.Invoke(f"str.{methodname}", obj, *args, **kwargs)
        self.assertEqual(result, realresult)

    def test_chars(self):
        self.checkequal([], "", "chars")
        self.checkequal(["a"], "a", "chars")
        self.checkequal(["a", "b", "c"], "abc", "chars")
        self.checkequal(["一", "二", "三"], "一二三", "chars")

    def test_count(self):
        self.checkequal(3, "aaa", "count", "a")
        self.checkequal(0, "aaa", "count", "b")
        self.checkequal(3, "aaa", "count", "a")
        self.checkequal(0, "aaa", "count", "b")
        self.checkequal(3, "aaa", "count", "a")
        self.checkequal(0, "aaa", "count", "b")
        self.checkequal(0, "aaa", "count", "b")
        self.checkequal(2, "aaa", "count", "a", 1)
        self.checkequal(0, "aaa", "count", "a", 10)
        self.checkequal(1, "aaa", "count", "a", -1)
        self.checkequal(3, "aaa", "count", "a", -10)
        self.checkequal(1, "aaa", "count", "a", 0, 1)
        self.checkequal(3, "aaa", "count", "a", 0, 10)
        self.checkequal(2, "aaa", "count", "a", 0, -1)
        self.checkequal(0, "aaa", "count", "a", 0, -10)
        self.checkequal(3, "aaa", "count", "", 1)
        self.checkequal(1, "aaa", "count", "", 3)
        self.checkequal(0, "aaa", "count", "", 10)
        self.checkequal(2, "aaa", "count", "", -1)
        self.checkequal(4, "aaa", "count", "", -10)

        self.checkequal(1, "", "count", "")
        self.checkequal(0, "", "count", "", 1, 1)
        # self.checkequal(0, '', 'count', '', sys.maxsize, 0)

        self.checkequal(0, "", "count", "xx")
        self.checkequal(0, "", "count", "xx", 1, 1)
        # self.checkequal(0, '', 'count', 'xx', sys.maxsize, 0)

    def test_find(self):
        self.checkequal(0, "abcdefghiabc", "find", "abc")
        self.checkequal(9, "abcdefghiabc", "find", "abc", 1)
        self.checkequal(-1, "abcdefghiabc", "find", "def", 4)

        self.checkequal(0, "abc", "find", "", 0)
        self.checkequal(3, "abc", "find", "", 3)
        self.checkequal(-1, "abc", "find", "", 4)

        # to check the ability to pass None as defaults
        self.checkequal(2, "rrarrrrrrrrra", "find", "a")
        self.checkequal(12, "rrarrrrrrrrra", "find", "a", 4)
        self.checkequal(-1, "rrarrrrrrrrra", "find", "a", 4, 6)
        self.checkequal(12, "rrarrrrrrrrra", "find", "a", 4, None)
        self.checkequal(2, "rrarrrrrrrrra", "find", "a", None, 6)

        # self.checkraises(TypeError, 'hello', 'find')

        # if self.contains_bytes:
        #    self.checkequal(-1, "hello", "find", 42)
        # else:
        #    # self.checkraises(TypeError, 'hello', 'find', 42)
        #    pass

        self.checkequal(0, "", "find", "")
        self.checkequal(-1, "", "find", "", 1, 1)
        # self.checkequal(-1, '', 'find', '', sys.maxsize, 0)

        self.checkequal(-1, "", "find", "xx")
        self.checkequal(-1, "", "find", "xx", 1, 1)
        # self.checkequal(-1, '', 'find', 'xx', sys.maxsize, 0)

        # issue 7458
        # self.checkequal(-1, 'ab', 'find', 'xxx', sys.maxsize + 1, 0)

    def test_rfind(self):
        self.checkequal(9, "abcdefghiabc", "rfind", "abc")
        self.checkequal(12, "abcdefghiabc", "rfind", "")
        self.checkequal(0, "abcdefghiabc", "rfind", "abcd")
        self.checkequal(-1, "abcdefghiabc", "rfind", "abcz")

        self.checkequal(3, "abc", "rfind", "", 0)
        self.checkequal(3, "abc", "rfind", "", 3)
        self.checkequal(-1, "abc", "rfind", "", 4)

        # to check the ability to pass None as defaults
        self.checkequal(12, "rrarrrrrrrrra", "rfind", "a")
        self.checkequal(12, "rrarrrrrrrrra", "rfind", "a", 4)
        self.checkequal(-1, "rrarrrrrrrrra", "rfind", "a", 4, 6)
        self.checkequal(12, "rrarrrrrrrrra", "rfind", "a", 4, None)
        self.checkequal(2, "rrarrrrrrrrra", "rfind", "a", None, 6)

    def _test_index(self):
        self.checkequal(0, "abcdefghiabc", "index", "")
        self.checkequal(3, "abcdefghiabc", "index", "def")
        self.checkequal(0, "abcdefghiabc", "index", "abc")
        self.checkequal(9, "abcdefghiabc", "index", "abc", 1)

        # self.checkraises(ValueError, 'abcdefghiabc', 'index', 'hib')
        # self.checkraises(ValueError, 'abcdefghiab', 'index', 'abc', 1)
        # self.checkraises(ValueError, 'abcdefghi', 'index', 'ghi', 8)
        # self.checkraises(ValueError, 'abcdefghi', 'index', 'ghi', -1)

        # to check the ability to pass None as defaults
        self.checkequal(2, "rrarrrrrrrrra", "index", "a")
        self.checkequal(12, "rrarrrrrrrrra", "index", "a", 4)
        # self.checkraises(ValueError, 'rrarrrrrrrrra', 'index', 'a', 4, 6)
        self.checkequal(12, "rrarrrrrrrrra", "index", "a", 4, None)
        self.checkequal(2, "rrarrrrrrrrra", "index", "a", None, 6)

    def test_rindex(self):
        self.checkequal(12, "abcdefghiabc", "rindex", "")
        self.checkequal(3, "abcdefghiabc", "rindex", "def")
        self.checkequal(9, "abcdefghiabc", "rindex", "abc")
        self.checkequal(0, "abcdefghiabc", "rindex", "abc", 0, -1)

        # self.checkraises(ValueError, 'abcdefghiabc', 'rindex', 'hib')
        # self.checkraises(ValueError, 'defghiabc', 'rindex', 'def', 1)
        # self.checkraises(ValueError, 'defghiabc', 'rindex', 'abc', 0, -1)
        # self.checkraises(ValueError, 'abcdefghi', 'rindex', 'ghi', 0, 8)
        # self.checkraises(ValueError, 'abcdefghi', 'rindex', 'ghi', 0, -1)

        # to check the ability to pass None as defaults
        self.checkequal(12, "rrarrrrrrrrra", "rindex", "a")
        self.checkequal(12, "rrarrrrrrrrra", "rindex", "a", 4)
        # self.checkraises(ValueError, 'rrarrrrrrrrra', 'rindex', 'a', 4, 6)
        self.checkequal(12, "rrarrrrrrrrra", "rindex", "a", 4, None)
        self.checkequal(2, "rrarrrrrrrrra", "rindex", "a", None, 6)

    def test_lower(self):
        self.checkequal("hello", "HeLLo", "lower")
        self.checkequal("hello", "hello", "lower")
        # self.checkraises(TypeError, 'hello', 'lower', 42)

    def test_upper(self):
        self.checkequal("HELLO", "HeLLo", "upper")
        self.checkequal("HELLO", "HELLO", "upper")
        # self.checkraises(TypeError, 'hello', 'upper', 42)

    def test_split(self):
        # by a char
        self.checkequal(["a", "b", "c", "d"], "a|b|c|d", "split", "|")
        self.checkequal(["a|b|c|d"], "a|b|c|d", "split", "|", 0)
        self.checkequal(["a", "b|c|d"], "a|b|c|d", "split", "|", 1)
        self.checkequal(["a", "b", "c|d"], "a|b|c|d", "split", "|", 2)
        self.checkequal(["a", "b", "c", "d"], "a|b|c|d", "split", "|", 3)
        self.checkequal(["a", "b", "c", "d"], "a|b|c|d", "split", "|", 4)
        # self.checkequal(['a', 'b', 'c', 'd'], 'a|b|c|d', 'split', '|', sys.maxsize-2)
        self.checkequal(["a|b|c|d"], "a|b|c|d", "split", "|", 0)
        self.checkequal(["a", "", "b||c||d"], "a||b||c||d", "split", "|", 2)
        self.checkequal(["abcd"], "abcd", "split", "|")
        self.checkequal([""], "", "split", "|")
        self.checkequal(["endcase ", ""], "endcase |", "split", "|")
        self.checkequal(["", " startcase"], "| startcase", "split", "|")
        self.checkequal(["", "bothcase", ""], "|bothcase|", "split", "|")
        self.checkequal(
            ["a", "", "b\x00c\x00d"], "a\x00\x00b\x00c\x00d", "split", "\x00", 2
        )

        self.checkequal(["a"] * 20, ("a|" * 20)[:-1], "split", "|")
        self.checkequal(["a"] * 15 + ["a|a|a|a|a"], ("a|" * 20)[:-1], "split", "|", 15)

        # by string
        self.checkequal(["a", "b", "c", "d"], "a//b//c//d", "split", "//")
        self.checkequal(["a", "b//c//d"], "a//b//c//d", "split", "//", 1)
        self.checkequal(["a", "b", "c//d"], "a//b//c//d", "split", "//", 2)
        self.checkequal(["a", "b", "c", "d"], "a//b//c//d", "split", "//", 3)
        self.checkequal(["a", "b", "c", "d"], "a//b//c//d", "split", "//", 4)
        # self.checkequal(['a', 'b', 'c', 'd'], 'a//b//c//d', 'split', '//', sys.maxsize-10)
        self.checkequal(["a//b//c//d"], "a//b//c//d", "split", "//", 0)
        self.checkequal(["a", "", "b////c////d"], "a////b////c////d", "split", "//", 2)
        self.checkequal(["endcase ", ""], "endcase test", "split", "test")
        self.checkequal(["", " begincase"], "test begincase", "split", "test")
        self.checkequal(["", " bothcase ", ""], "test bothcase test", "split", "test")
        self.checkequal(["a", "bc"], "abbbc", "split", "bb")
        self.checkequal(["", ""], "aaa", "split", "aaa")
        self.checkequal(["aaa"], "aaa", "split", "aaa", 0)
        self.checkequal(["ab", "ab"], "abbaab", "split", "ba")
        self.checkequal(["aaaa"], "aaaa", "split", "aab")
        self.checkequal([""], "", "split", "aaa")
        self.checkequal(["aa"], "aa", "split", "aaa")
        self.checkequal(["A", "bobb"], "Abbobbbobb", "split", "bbobb")
        self.checkequal(["A", "B", ""], "AbbobbBbbobb", "split", "bbobb")

        self.checkequal(["a"] * 20, ("aBLAH" * 20)[:-4], "split", "BLAH")
        self.checkequal(["a"] * 20, ("aBLAH" * 20)[:-4], "split", "BLAH", 19)
        self.checkequal(
            ["a"] * 18 + ["aBLAHa"], ("aBLAH" * 20)[:-4], "split", "BLAH", 18
        )

        # with keyword args
        self.checkequal(["a", "b", "c", "d"], "a|b|c|d", "split", sep="|")
        self.checkequal(["a", "b|c|d"], "a|b|c|d", "split", "|", maxsplit=1)
        self.checkequal(["a", "b|c|d"], "a|b|c|d", "split", sep="|", maxsplit=1)
        self.checkequal(["a", "b|c|d"], "a|b|c|d", "split", maxsplit=1, sep="|")
        self.checkequal(["a", "b c d"], "a b c d", "split", maxsplit=1)

        # argument type
        # self.checkraises(TypeError, 'hello', 'split', 42, 42, 42)

        # null case
        # self.checkraises(ValueError, 'hello', 'split', '')
        # self.checkraises(ValueError, 'hello', 'split', '', 0)

    def test_rsplit(self):
        # by a char
        self.checkequal(["a", "b", "c", "d"], "a|b|c|d", "rsplit", "|")
        self.checkequal(["a|b|c", "d"], "a|b|c|d", "rsplit", "|", 1)
        self.checkequal(["a|b", "c", "d"], "a|b|c|d", "rsplit", "|", 2)
        self.checkequal(["a", "b", "c", "d"], "a|b|c|d", "rsplit", "|", 3)
        self.checkequal(["a", "b", "c", "d"], "a|b|c|d", "rsplit", "|", 4)
        self.checkequal(
            ["a", "b", "c", "d"], "a|b|c|d", "rsplit", "|", sys.maxsize - 100
        )
        self.checkequal(["a|b|c|d"], "a|b|c|d", "rsplit", "|", 0)
        self.checkequal(["a||b||c", "", "d"], "a||b||c||d", "rsplit", "|", 2)
        self.checkequal(["abcd"], "abcd", "rsplit", "|")
        self.checkequal([""], "", "rsplit", "|")
        self.checkequal(["", " begincase"], "| begincase", "rsplit", "|")
        self.checkequal(["endcase ", ""], "endcase |", "rsplit", "|")
        self.checkequal(["", "bothcase", ""], "|bothcase|", "rsplit", "|")

        self.checkequal(
            ["a\x00\x00b", "c", "d"], "a\x00\x00b\x00c\x00d", "rsplit", "\x00", 2
        )

        self.checkequal(["a"] * 20, ("a|" * 20)[:-1], "rsplit", "|")
        self.checkequal(["a|a|a|a|a"] + ["a"] * 15, ("a|" * 20)[:-1], "rsplit", "|", 15)

        # by string
        self.checkequal(["a", "b", "c", "d"], "a//b//c//d", "rsplit", "//")
        self.checkequal(["a//b//c", "d"], "a//b//c//d", "rsplit", "//", 1)
        self.checkequal(["a//b", "c", "d"], "a//b//c//d", "rsplit", "//", 2)
        self.checkequal(["a", "b", "c", "d"], "a//b//c//d", "rsplit", "//", 3)
        self.checkequal(["a", "b", "c", "d"], "a//b//c//d", "rsplit", "//", 4)
        self.checkequal(
            ["a", "b", "c", "d"], "a//b//c//d", "rsplit", "//", sys.maxsize - 5
        )
        self.checkequal(["a//b//c//d"], "a//b//c//d", "rsplit", "//", 0)
        self.checkequal(["a////b////c", "", "d"], "a////b////c////d", "rsplit", "//", 2)
        self.checkequal(["", " begincase"], "test begincase", "rsplit", "test")
        self.checkequal(["endcase ", ""], "endcase test", "rsplit", "test")
        self.checkequal(["", " bothcase ", ""], "test bothcase test", "rsplit", "test")
        self.checkequal(["ab", "c"], "abbbc", "rsplit", "bb")
        self.checkequal(["", ""], "aaa", "rsplit", "aaa")
        self.checkequal(["aaa"], "aaa", "rsplit", "aaa", 0)
        self.checkequal(["ab", "ab"], "abbaab", "rsplit", "ba")
        self.checkequal(["aaaa"], "aaaa", "rsplit", "aab")
        self.checkequal([""], "", "rsplit", "aaa")
        self.checkequal(["aa"], "aa", "rsplit", "aaa")
        self.checkequal(["bbob", "A"], "bbobbbobbA", "rsplit", "bbobb")
        self.checkequal(["", "B", "A"], "bbobbBbbobbA", "rsplit", "bbobb")

        self.checkequal(["a"] * 20, ("aBLAH" * 20)[:-4], "rsplit", "BLAH")
        self.checkequal(["a"] * 20, ("aBLAH" * 20)[:-4], "rsplit", "BLAH", 19)
        self.checkequal(
            ["aBLAHa"] + ["a"] * 18, ("aBLAH" * 20)[:-4], "rsplit", "BLAH", 18
        )

        # with keyword args
        self.checkequal(["a", "b", "c", "d"], "a|b|c|d", "rsplit", sep="|")
        self.checkequal(["a|b|c", "d"], "a|b|c|d", "rsplit", "|", maxsplit=1)
        self.checkequal(["a|b|c", "d"], "a|b|c|d", "rsplit", sep="|", maxsplit=1)
        self.checkequal(["a|b|c", "d"], "a|b|c|d", "rsplit", maxsplit=1, sep="|")
        self.checkequal(["a b c", "d"], "a b c d", "rsplit", maxsplit=1)

        # argument type
        # self.checkraises(TypeError, 'hello', 'rsplit', 42, 42, 42)

        # null case
        # self.checkraises(ValueError, 'hello', 'rsplit', '')
        # self.checkraises(ValueError, 'hello', 'rsplit', '', 0)

    def test_replace(self):
        EQ = self.checkequal

        # Operations on the empty string
        EQ("", "", "replace", "", "")
        EQ("A", "", "replace", "", "A")
        EQ("", "", "replace", "A", "")
        EQ("", "", "replace", "A", "A")
        EQ("", "", "replace", "", "", 100)
        EQ("A", "", "replace", "", "A", 100)
        EQ("", "", "replace", "", "", sys.maxsize)

        # interleave (from=="", 'to' gets inserted everywhere)
        EQ("A", "A", "replace", "", "")
        EQ("*A*", "A", "replace", "", "*")
        EQ("*1A*1", "A", "replace", "", "*1")
        EQ("*-#A*-#", "A", "replace", "", "*-#")
        EQ("*-A*-A*-", "AA", "replace", "", "*-")
        EQ("*-A*-A*-", "AA", "replace", "", "*-", -1)
        EQ("*-A*-A*-", "AA", "replace", "", "*-", sys.maxsize)
        EQ("*-A*-A*-", "AA", "replace", "", "*-", 4)
        EQ("*-A*-A*-", "AA", "replace", "", "*-", 3)
        EQ("*-A*-A", "AA", "replace", "", "*-", 2)
        EQ("*-AA", "AA", "replace", "", "*-", 1)
        EQ("AA", "AA", "replace", "", "*-", 0)

        # single character deletion (from=="A", to=="")
        EQ("", "A", "replace", "A", "")
        EQ("", "AAA", "replace", "A", "")
        EQ("", "AAA", "replace", "A", "", -1)
        EQ("", "AAA", "replace", "A", "", sys.maxsize)
        EQ("", "AAA", "replace", "A", "", 4)
        EQ("", "AAA", "replace", "A", "", 3)
        EQ("A", "AAA", "replace", "A", "", 2)
        EQ("AA", "AAA", "replace", "A", "", 1)
        EQ("AAA", "AAA", "replace", "A", "", 0)
        EQ("", "AAAAAAAAAA", "replace", "A", "")
        EQ("BCD", "ABACADA", "replace", "A", "")
        EQ("BCD", "ABACADA", "replace", "A", "", -1)
        EQ("BCD", "ABACADA", "replace", "A", "", sys.maxsize)
        EQ("BCD", "ABACADA", "replace", "A", "", 5)
        EQ("BCD", "ABACADA", "replace", "A", "", 4)
        EQ("BCDA", "ABACADA", "replace", "A", "", 3)
        EQ("BCADA", "ABACADA", "replace", "A", "", 2)
        EQ("BACADA", "ABACADA", "replace", "A", "", 1)
        EQ("ABACADA", "ABACADA", "replace", "A", "", 0)
        EQ("BCD", "ABCAD", "replace", "A", "")
        EQ("BCD", "ABCADAA", "replace", "A", "")
        EQ("BCD", "BCD", "replace", "A", "")
        EQ("*************", "*************", "replace", "A", "")
        EQ("^A^", "^" + "A" * 1000 + "^", "replace", "A", "", 999)

        # substring deletion (from=="the", to=="")
        EQ("", "the", "replace", "the", "")
        EQ("ater", "theater", "replace", "the", "")
        EQ("", "thethe", "replace", "the", "")
        EQ("", "thethethethe", "replace", "the", "")
        EQ("aaaa", "theatheatheathea", "replace", "the", "")
        EQ("that", "that", "replace", "the", "")
        EQ("thaet", "thaet", "replace", "the", "")
        EQ("here and re", "here and there", "replace", "the", "")
        EQ(
            "here and re and re",
            "here and there and there",
            "replace",
            "the",
            "",
            sys.maxsize,
        )
        EQ("here and re and re", "here and there and there", "replace", "the", "", -1)
        EQ("here and re and re", "here and there and there", "replace", "the", "", 3)
        EQ("here and re and re", "here and there and there", "replace", "the", "", 2)
        EQ("here and re and there", "here and there and there", "replace", "the", "", 1)
        EQ(
            "here and there and there",
            "here and there and there",
            "replace",
            "the",
            "",
            0,
        )
        EQ("here and re and re", "here and there and there", "replace", "the", "")

        EQ("abc", "abc", "replace", "the", "")
        EQ("abcdefg", "abcdefg", "replace", "the", "")

        # substring deletion (from=="bob", to=="")
        EQ("bob", "bbobob", "replace", "bob", "")
        EQ("bobXbob", "bbobobXbbobob", "replace", "bob", "")
        EQ("aaaaaaa", "aaaaaaabob", "replace", "bob", "")
        EQ("aaaaaaa", "aaaaaaa", "replace", "bob", "")

        # single character replace in place (len(from)==len(to)==1)
        EQ("Who goes there?", "Who goes there?", "replace", "o", "o")
        EQ("WhO gOes there?", "Who goes there?", "replace", "o", "O")
        EQ("WhO gOes there?", "Who goes there?", "replace", "o", "O", sys.maxsize)
        EQ("WhO gOes there?", "Who goes there?", "replace", "o", "O", -1)
        EQ("WhO gOes there?", "Who goes there?", "replace", "o", "O", 3)
        EQ("WhO gOes there?", "Who goes there?", "replace", "o", "O", 2)
        EQ("WhO goes there?", "Who goes there?", "replace", "o", "O", 1)
        EQ("Who goes there?", "Who goes there?", "replace", "o", "O", 0)

        EQ("Who goes there?", "Who goes there?", "replace", "a", "q")
        EQ("who goes there?", "Who goes there?", "replace", "W", "w")
        EQ("wwho goes there?ww", "WWho goes there?WW", "replace", "W", "w")
        EQ("Who goes there!", "Who goes there?", "replace", "?", "!")
        EQ("Who goes there!!", "Who goes there??", "replace", "?", "!")

        EQ("Who goes there?", "Who goes there?", "replace", ".", "!")

        # substring replace in place (len(from)==len(to) > 1)
        EQ("Th** ** a t**sue", "This is a tissue", "replace", "is", "**")
        EQ("Th** ** a t**sue", "This is a tissue", "replace", "is", "**", sys.maxsize)
        EQ("Th** ** a t**sue", "This is a tissue", "replace", "is", "**", -1)
        EQ("Th** ** a t**sue", "This is a tissue", "replace", "is", "**", 4)
        EQ("Th** ** a t**sue", "This is a tissue", "replace", "is", "**", 3)
        EQ("Th** ** a tissue", "This is a tissue", "replace", "is", "**", 2)
        EQ("Th** is a tissue", "This is a tissue", "replace", "is", "**", 1)
        EQ("This is a tissue", "This is a tissue", "replace", "is", "**", 0)
        EQ("cobob", "bobob", "replace", "bob", "cob")
        EQ("cobobXcobocob", "bobobXbobobob", "replace", "bob", "cob")
        EQ("bobob", "bobob", "replace", "bot", "bot")

        # replace single character (len(from)==1, len(to)>1)
        EQ("ReyKKjaviKK", "Reykjavik", "replace", "k", "KK")
        EQ("ReyKKjaviKK", "Reykjavik", "replace", "k", "KK", -1)
        EQ("ReyKKjaviKK", "Reykjavik", "replace", "k", "KK", sys.maxsize)
        EQ("ReyKKjaviKK", "Reykjavik", "replace", "k", "KK", 2)
        EQ("ReyKKjavik", "Reykjavik", "replace", "k", "KK", 1)
        EQ("Reykjavik", "Reykjavik", "replace", "k", "KK", 0)
        EQ("A----B----C----", "A.B.C.", "replace", ".", "----")
        # issue #15534
        EQ("...\u043c......&lt;", "...\u043c......<", "replace", "<", "&lt;")

        EQ("Reykjavik", "Reykjavik", "replace", "q", "KK")

        # replace substring (len(from)>1, len(to)!=len(from))
        EQ(
            "ham, ham, eggs and ham",
            "spam, spam, eggs and spam",
            "replace",
            "spam",
            "ham",
        )
        EQ(
            "ham, ham, eggs and ham",
            "spam, spam, eggs and spam",
            "replace",
            "spam",
            "ham",
            sys.maxsize,
        )
        EQ(
            "ham, ham, eggs and ham",
            "spam, spam, eggs and spam",
            "replace",
            "spam",
            "ham",
            -1,
        )
        EQ(
            "ham, ham, eggs and ham",
            "spam, spam, eggs and spam",
            "replace",
            "spam",
            "ham",
            4,
        )
        EQ(
            "ham, ham, eggs and ham",
            "spam, spam, eggs and spam",
            "replace",
            "spam",
            "ham",
            3,
        )
        EQ(
            "ham, ham, eggs and spam",
            "spam, spam, eggs and spam",
            "replace",
            "spam",
            "ham",
            2,
        )
        EQ(
            "ham, spam, eggs and spam",
            "spam, spam, eggs and spam",
            "replace",
            "spam",
            "ham",
            1,
        )
        EQ(
            "spam, spam, eggs and spam",
            "spam, spam, eggs and spam",
            "replace",
            "spam",
            "ham",
            0,
        )

        EQ("bobob", "bobobob", "replace", "bobob", "bob")
        EQ("bobobXbobob", "bobobobXbobobob", "replace", "bobob", "bob")
        EQ("BOBOBOB", "BOBOBOB", "replace", "bob", "bobby")

        self.checkequal("one@two!three!", "one!two!three!", "replace", "!", "@", 1)
        self.checkequal("onetwothree", "one!two!three!", "replace", "!", "")
        self.checkequal("one@two@three!", "one!two!three!", "replace", "!", "@", 2)
        self.checkequal("one@two@three@", "one!two!three!", "replace", "!", "@", 3)
        self.checkequal("one@two@three@", "one!two!three!", "replace", "!", "@", 4)
        self.checkequal("one!two!three!", "one!two!three!", "replace", "!", "@", 0)
        self.checkequal("one@two@three@", "one!two!three!", "replace", "!", "@")
        self.checkequal("one!two!three!", "one!two!three!", "replace", "x", "@")
        self.checkequal("one!two!three!", "one!two!three!", "replace", "x", "@", 2)
        self.checkequal("-a-b-c-", "abc", "replace", "", "-")
        self.checkequal("-a-b-c", "abc", "replace", "", "-", 3)
        self.checkequal("abc", "abc", "replace", "", "-", 0)
        self.checkequal("", "", "replace", "", "")
        self.checkequal("abc", "abc", "replace", "ab", "--", 0)
        self.checkequal("abc", "abc", "replace", "xy", "--")
        # Next three for SF bug 422088: [OSF1 alpha] string.replace(); died with
        # MemoryError due to empty result (platform malloc issue when requesting
        # 0 bytes).
        self.checkequal("", "123", "replace", "123", "")
        self.checkequal("", "123123", "replace", "123", "")
        self.checkequal("x", "123x123", "replace", "123", "")

        # self.checkraises(TypeError, 'hello', 'replace')
        # self.checkraises(TypeError, 'hello', 'replace', 42)
        # self.checkraises(TypeError, 'hello', 'replace', 42, 'h')
        # self.checkraises(TypeError, 'hello', 'replace', 'h', 42)

    def test_capitalize(self):
        self.checkequal(" hello ", " hello ", "capitalize")
        self.checkequal("Hello ", "Hello ", "capitalize")
        self.checkequal("Hello ", "hello ", "capitalize")
        self.checkequal("Aaaa", "aaaa", "capitalize")
        self.checkequal("Aaaa", "AaAa", "capitalize")

        # self.checkraises(TypeError, 'hello', 'capitalize', 42)

    def test_removeprefix(self):
        self.checkequal("a ", " aa ", "removeprefix", " a")
        self.checkequal(" ", " aa ", "removeprefix", " aa")
        self.checkequal("", " aa ", "removeprefix", " aa ")

        s = 'foobarfoo'
        s_ref='foobarfoo'

        self.checkequal(s_ref[1:], s, "removeprefix", "f")
        self.checkequal(s_ref[2:], s, "removeprefix", "fo")
        self.checkequal(s_ref[3:], s, "removeprefix", "foo")

        self.checkequal(s_ref, s, "removeprefix", "")
        self.checkequal(s_ref, s, "removeprefix", "bar")
        self.checkequal(s_ref, s, "removeprefix", "lol")
        self.checkequal(s_ref, s, "removeprefix", "_foo")
        self.checkequal(s_ref, s, "removeprefix", "-foo")
        self.checkequal(s_ref, s, "removeprefix", "afoo")
        self.checkequal(s_ref, s, "removeprefix", "*foo")

        s_uc = '😱foobarfoo🖖'
        s_ref_uc = '😱foobarfoo🖖'

        self.checkequal(s_ref_uc[1:], s_uc, "removeprefix", "😱")
        self.checkequal(s_ref_uc[3:], s_uc, "removeprefix", "😱fo")
        self.checkequal(s_ref_uc[4:], s_uc, "removeprefix", "😱foo")

        self.checkequal(s_ref_uc, s_uc, "removeprefix", "🖖")
        self.checkequal(s_ref_uc, s_uc, "removeprefix", "foo")
        self.checkequal(s_ref_uc, s_uc, "removeprefix", " ")
        self.checkequal(s_ref_uc, s_uc, "removeprefix", "_😱")
        self.checkequal(s_ref_uc, s_uc, "removeprefix", " 😱")
        self.checkequal(s_ref_uc, s_uc, "removeprefix", "-😱")
        self.checkequal(s_ref_uc, s_uc, "removeprefix", "#😱")

    def test_removesuffix(self):
        self.checkequal(" a", " aa ", "removesuffix", "a ")
        self.checkequal(" ", " aa ", "removesuffix", "aa ")
        self.checkequal("", " aa ", "removesuffix", " aa ")

        s = 'foobarfoo'
        s_ref='foobarfoo'

        self.checkequal(s_ref[:-1], s, "removesuffix", "o")
        self.checkequal(s_ref[:-2], s, "removesuffix", "oo")
        self.checkequal(s_ref[:-3], s, "removesuffix", "foo")

        self.checkequal(s_ref, s, "removesuffix", "")
        self.checkequal(s_ref, s, "removesuffix", "bar")
        self.checkequal(s_ref, s, "removesuffix", "lol")
        self.checkequal(s_ref, s, "removesuffix", "_foo")
        self.checkequal(s_ref, s, "removesuffix", "-foo")
        self.checkequal(s_ref, s, "removesuffix", "afoo")
        self.checkequal(s_ref, s, "removesuffix", "*foo")

        s_uc = '😱foobarfoo🖖'
        s_ref_uc = '😱foobarfoo🖖'

        self.checkequal(s_ref_uc[:-1], s_uc, "removesuffix", "🖖")
        self.checkequal(s_ref_uc[:-3], s_uc, "removesuffix", "oo🖖")
        self.checkequal(s_ref_uc[:-4], s_uc, "removesuffix", "foo🖖")

        self.checkequal(s_ref_uc, s_uc, "removesuffix", "😱")
        self.checkequal(s_ref_uc, s_uc, "removesuffix", "foo")
        self.checkequal(s_ref_uc, s_uc, "removesuffix", " ")
        self.checkequal(s_ref_uc, s_uc, "removesuffix", "🖖_")
        self.checkequal(s_ref_uc, s_uc, "removesuffix", "🖖 ")
        self.checkequal(s_ref_uc, s_uc, "removesuffix", "🖖-")
        self.checkequal(s_ref_uc, s_uc, "removesuffix", "🖖#")

    def test_additional_split(self):
        self.checkequal(
            ["this", "is", "the", "split", "function"],
            "this is the split function",
            "split",
        )

        # by whitespace
        self.checkequal(["a", "b", "c", "d"], "a b c d ", "split")
        self.checkequal(["a", "b c d"], "a b c d", "split", None, 1)
        self.checkequal(["a", "b", "c d"], "a b c d", "split", None, 2)
        self.checkequal(["a", "b", "c", "d"], "a b c d", "split", None, 3)
        self.checkequal(["a", "b", "c", "d"], "a b c d", "split", None, 4)
        self.checkequal(["a", "b", "c", "d"], "a b c d", "split", None, sys.maxsize - 1)
        self.checkequal(["a b c d"], "a b c d", "split", None, 0)
        self.checkequal(["a b c d"], "  a b c d", "split", None, 0)
        self.checkequal(["a", "b", "c  d"], "a  b  c  d", "split", None, 2)

        self.checkequal([], "         ", "split")
        self.checkequal(["a"], "  a    ", "split")
        self.checkequal(["a", "b"], "  a    b   ", "split")
        self.checkequal(["a", "b   "], "  a    b   ", "split", None, 1)
        self.checkequal(["a    b   c   "], "  a    b   c   ", "split", None, 0)
        self.checkequal(["a", "b   c   "], "  a    b   c   ", "split", None, 1)
        self.checkequal(["a", "b", "c   "], "  a    b   c   ", "split", None, 2)
        self.checkequal(["a", "b", "c"], "  a    b   c   ", "split", None, 3)
        self.checkequal(["a", "b"], "\n\ta \t\r b \v ", "split")
        aaa = " a " * 20
        self.checkequal(["a"] * 20, aaa, "split")
        self.checkequal(["a"] + [aaa[4:]], aaa, "split", None, 1)
        self.checkequal(["a"] * 19 + ["a "], aaa, "split", None, 19)

        for b in ("arf\tbarf", "arf\nbarf", "arf\rbarf", "arf\fbarf", "arf\vbarf"):
            self.checkequal(["arf", "barf"], b, "split")
            self.checkequal(["arf", "barf"], b, "split", None)
            self.checkequal(["arf", "barf"], b, "split", None, 2)

    def test_additional_rsplit(self):
        self.checkequal(
            ["this", "is", "the", "rsplit", "function"],
            "this is the rsplit function",
            "rsplit",
        )

        # by whitespace
        self.checkequal(["a", "b", "c", "d"], "a b c d ", "rsplit")
        self.checkequal(["a b c", "d"], "a b c d", "rsplit", None, 1)
        self.checkequal(["a b", "c", "d"], "a b c d", "rsplit", None, 2)
        self.checkequal(["a", "b", "c", "d"], "a b c d", "rsplit", None, 3)
        self.checkequal(["a", "b", "c", "d"], "a b c d", "rsplit", None, 4)
        self.checkequal(
            ["a", "b", "c", "d"], "a b c d", "rsplit", None, sys.maxsize - 20
        )
        self.checkequal(["a b c d"], "a b c d", "rsplit", None, 0)
        self.checkequal(["a b c d"], "a b c d  ", "rsplit", None, 0)
        self.checkequal(["a  b", "c", "d"], "a  b  c  d", "rsplit", None, 2)

        self.checkequal([], "         ", "rsplit")
        self.checkequal(["a"], "  a    ", "rsplit")
        self.checkequal(["a", "b"], "  a    b   ", "rsplit")
        self.checkequal(["  a", "b"], "  a    b   ", "rsplit", None, 1)
        self.checkequal(["  a    b   c"], "  a    b   c   ", "rsplit", None, 0)
        self.checkequal(["  a    b", "c"], "  a    b   c   ", "rsplit", None, 1)
        self.checkequal(["  a", "b", "c"], "  a    b   c   ", "rsplit", None, 2)
        self.checkequal(["a", "b", "c"], "  a    b   c   ", "rsplit", None, 3)
        self.checkequal(["a", "b"], "\n\ta \t\r b \v ", "rsplit", None, 88)
        aaa = " a " * 20
        self.checkequal(["a"] * 20, aaa, "rsplit")
        self.checkequal([aaa[:-4]] + ["a"], aaa, "rsplit", None, 1)
        self.checkequal([" a  a"] + ["a"] * 18, aaa, "rsplit", None, 18)

        for b in ("arf\tbarf", "arf\nbarf", "arf\rbarf", "arf\fbarf", "arf\vbarf"):
            self.checkequal(["arf", "barf"], b, "rsplit")
            self.checkequal(["arf", "barf"], b, "rsplit", None)
            self.checkequal(["arf", "barf"], b, "rsplit", None, 2)

    def test_strip_whitespace(self):
        self.checkequal("hello", "   hello   ", "strip")
        self.checkequal("hello   ", "   hello   ", "lstrip")
        self.checkequal("   hello", "   hello   ", "rstrip")
        self.checkequal("hello", "hello", "strip")

        b = " \t\n\r\f\vabc \t\n\r\f\v"
        self.checkequal("abc", b, "strip")
        self.checkequal("abc \t\n\r\f\v", b, "lstrip")
        self.checkequal(" \t\n\r\f\vabc", b, "rstrip")

        # strip/lstrip/rstrip with None arg
        self.checkequal("hello", "   hello   ", "strip", None)
        self.checkequal("hello   ", "   hello   ", "lstrip", None)
        self.checkequal("   hello", "   hello   ", "rstrip", None)
        self.checkequal("hello", "hello", "strip", None)

    def test_strip(self):
        # strip/lstrip/rstrip with str arg
        self.checkequal("hello", "xyzzyhelloxyzzy", "strip", "xyz")
        self.checkequal("helloxyzzy", "xyzzyhelloxyzzy", "lstrip", "xyz")
        self.checkequal("xyzzyhello", "xyzzyhelloxyzzy", "rstrip", "xyz")
        self.checkequal("hello", "hello", "strip", "xyz")
        self.checkequal("", "mississippi", "strip", "mississippi")

        # only trim the start and end; does not strip internal characters
        self.checkequal("mississipp", "mississippi", "strip", "i")

        # self.checkraises(TypeError, 'hello', 'strip', 42, 42)
        # self.checkraises(TypeError, 'hello', 'lstrip', 42, 42)
        # self.checkraises(TypeError, 'hello', 'rstrip', 42, 42)

    def test_islower(self):
        self.checkequal(False, "", "islower")
        self.checkequal(True, "a", "islower")
        self.checkequal(False, "A", "islower")
        self.checkequal(False, "\n", "islower")
        self.checkequal(True, "abc", "islower")
        self.checkequal(False, "aBc", "islower")
        self.checkequal(True, "abc\n", "islower")
        # self.checkraises(TypeError, 'abc', 'islower', 42)

    def test_isupper(self):
        self.checkequal(False, "", "isupper")
        self.checkequal(False, "a", "isupper")
        self.checkequal(True, "A", "isupper")
        self.checkequal(False, "\n", "isupper")
        self.checkequal(True, "ABC", "isupper")
        self.checkequal(False, "AbC", "isupper")
        self.checkequal(True, "ABC\n", "isupper")
        # self.checkraises(TypeError, 'abc', 'isupper', 42)

    def test_istitle(self):
        self.checkequal(False, "", "istitle")
        self.checkequal(False, "a", "istitle")
        self.checkequal(True, "A", "istitle")
        self.checkequal(False, "\n", "istitle")
        self.checkequal(True, "A Titlecased Line", "istitle")
        self.checkequal(True, "A\nTitlecased Line", "istitle")
        self.checkequal(True, "A Titlecased, Line", "istitle")
        self.checkequal(False, "Not a capitalized String", "istitle")
        self.checkequal(False, "Not\ta Titlecase String", "istitle")
        self.checkequal(False, "Not--a Titlecase String", "istitle")
        self.checkequal(False, "NOT", "istitle")
        # self.checkraises(TypeError, 'abc', 'istitle', 42)

    def test_isspace(self):
        self.checkequal(False, "", "isspace")
        self.checkequal(False, "a", "isspace")
        self.checkequal(True, " ", "isspace")
        self.checkequal(True, "\t", "isspace")
        self.checkequal(True, "\r", "isspace")
        self.checkequal(True, "\n", "isspace")
        self.checkequal(True, " \t\r\n", "isspace")
        self.checkequal(False, " \t\r\na", "isspace")
        # self.checkraises(TypeError, 'abc', 'isspace', 42)

    def test_isalpha(self):
        self.checkequal(False, "", "isalpha")
        self.checkequal(True, "a", "isalpha")
        self.checkequal(True, "A", "isalpha")
        self.checkequal(False, "\n", "isalpha")
        self.checkequal(True, "abc", "isalpha")
        self.checkequal(False, "aBc123", "isalpha")
        self.checkequal(False, "abc\n", "isalpha")
        # self.checkraises(TypeError, 'abc', 'isalpha', 42)

    def test_isalnum(self):
        self.checkequal(False, "", "isalnum")
        self.checkequal(True, "a", "isalnum")
        self.checkequal(True, "A", "isalnum")
        self.checkequal(False, "\n", "isalnum")
        self.checkequal(True, "123abc456", "isalnum")
        self.checkequal(True, "a1b3c", "isalnum")
        self.checkequal(False, "aBc000 ", "isalnum")
        self.checkequal(False, "abc\n", "isalnum")
        # self.checkraises(TypeError, 'abc', 'isalnum', 42)

    def test_isdigit(self):
        self.checkequal(False, "", "isdigit")
        self.checkequal(False, "a", "isdigit")
        self.checkequal(True, "0", "isdigit")
        self.checkequal(True, "0123456789", "isdigit")
        self.checkequal(False, "0123456789a", "isdigit")

        # self.checkraises(TypeError, 'abc', 'isdigit', 42)

    def test_title(self):
        self.checkequal(" Hello ", " hello ", "title")
        self.checkequal("Hello ", "hello ", "title")
        self.checkequal("Hello ", "Hello ", "title")
        self.checkequal(
            "Format This As Title String", "fOrMaT thIs aS titLe String", "title"
        )
        self.checkequal(
            "Format,This-As*Title;String",
            "fOrMaT,thIs-aS*titLe;String",
            "title",
        )
        self.checkequal("Getint", "getInt", "title")
        # self.checkraises(TypeError, 'hello', 'title', 42)

    def test_splitlines(self):
        self.checkequal(["abc", "def", "", "ghi"], "abc\ndef\n\rghi", "splitlines")
        self.checkequal(["abc", "def", "", "ghi"], "abc\ndef\n\r\nghi", "splitlines")
        self.checkequal(["abc", "def", "ghi"], "abc\ndef\r\nghi", "splitlines")
        self.checkequal(["abc", "def", "ghi"], "abc\ndef\r\nghi\n", "splitlines")
        self.checkequal(["abc", "def", "ghi", ""], "abc\ndef\r\nghi\n\r", "splitlines")
        self.checkequal(
            ["", "abc", "def", "ghi", ""], "\nabc\ndef\r\nghi\n\r", "splitlines"
        )
        self.checkequal(
            ["", "abc", "def", "ghi", ""], "\nabc\ndef\r\nghi\n\r", "splitlines", False
        )
        self.checkequal(
            ["\n", "abc\n", "def\r\n", "ghi\n", "\r"],
            "\nabc\ndef\r\nghi\n\r",
            "splitlines",
            True,
        )
        self.checkequal(
            ["", "abc", "def", "ghi", ""],
            "\nabc\ndef\r\nghi\n\r",
            "splitlines",
            keepends=False,
        )
        self.checkequal(
            ["\n", "abc\n", "def\r\n", "ghi\n", "\r"],
            "\nabc\ndef\r\nghi\n\r",
            "splitlines",
            keepends=True,
        )

        # self.checkraises(TypeError, 'abc', 'splitlines', 42, 42)


class CommonTest(BaseTest):
    def test_capitalize_nonascii(self):
        # check that titlecased chars are lowered correctly
        # \u1ffc is the titlecased char
        # self.checkequal(
        #    "\u1ffc\u1ff3\u1ff3\u1ff3", "\u1ff3\u1ff3\u1ffc\u1ffc", "capitalize"
        # )
        # check with cased non-letter chars
        self.checkequal(
            "\u24c5\u24e8\u24e3\u24d7\u24de\u24dd",
            "\u24c5\u24ce\u24c9\u24bd\u24c4\u24c3",
            "capitalize",
        )
        self.checkequal(
            "\u24c5\u24e8\u24e3\u24d7\u24de\u24dd",
            "\u24df\u24e8\u24e3\u24d7\u24de\u24dd",
            "capitalize",
        )
        self.checkequal("\u2160\u2171\u2172", "\u2160\u2161\u2162", "capitalize")
        self.checkequal("\u2160\u2171\u2172", "\u2170\u2171\u2172", "capitalize")
        # check with Ll chars with no upper - nothing changes here
        # self.checkequal(
        #    "\u019b\u1d00\u1d86\u0221\u1fb7",
        #    "\u019b\u1d00\u1d86\u0221\u1fb7",
        #    "capitalize",
        # )


class MixinStrUnicodeUserStringTest(BaseTest):
    def test_startswith(self):
        self.checkequal(True, "hello", "startswith", "he")
        self.checkequal(True, "hello", "startswith", "hello")
        self.checkequal(False, "hello", "startswith", "hello world")
        self.checkequal(True, "hello", "startswith", "")
        self.checkequal(False, "hello", "startswith", "ello")
        self.checkequal(True, "hello", "startswith", "ello", 1)
        self.checkequal(True, "hello", "startswith", "o", 4)
        self.checkequal(False, "hello", "startswith", "o", 5)
        self.checkequal(True, "hello", "startswith", "", 5)
        self.checkequal(False, "hello", "startswith", "lo", 6)
        self.checkequal(True, "helloworld", "startswith", "lowo", 3)
        self.checkequal(True, "helloworld", "startswith", "lowo", 3, 7)
        self.checkequal(False, "helloworld", "startswith", "lowo", 3, 6)
        self.checkequal(True, "", "startswith", "", 0, 1)
        self.checkequal(True, "", "startswith", "", 0, 0)
        self.checkequal(False, "", "startswith", "", 1, 0)

        # test negative indices
        self.checkequal(True, "hello", "startswith", "he", 0, -1)
        self.checkequal(True, "hello", "startswith", "he", -53, -1)
        self.checkequal(False, "hello", "startswith", "hello", 0, -1)
        self.checkequal(False, "hello", "startswith", "hello world", -1, -10)
        self.checkequal(False, "hello", "startswith", "ello", -5)
        self.checkequal(True, "hello", "startswith", "ello", -4)
        self.checkequal(False, "hello", "startswith", "o", -2)
        self.checkequal(True, "hello", "startswith", "o", -1)
        self.checkequal(True, "hello", "startswith", "", -3, -3)
        self.checkequal(False, "hello", "startswith", "lo", -9)

        # self.checkraises(TypeError, 'hello', 'startswith')
        # self.checkraises(TypeError, 'hello', 'startswith', 42)

        # test tuple arguments
        # self.checkequal(True, "hello", "startswith", ("he", "ha"))
        # self.checkequal(False, "hello", "startswith", ("lo", "llo"))
        # self.checkequal(True, "hello", "startswith", ("hellox", "hello"))
        # self.checkequal(False, "hello", "startswith", ())
        # self.checkequal(True, "helloworld", "startswith", ("hellowo", "rld", "lowo"), 3)
        # self.checkequal(
        #    False, "helloworld", "startswith", ("hellowo", "ello", "rld"), 3
        # )
        # self.checkequal(True, "hello", "startswith", ("lo", "he"), 0, -1)
        # self.checkequal(False, "hello", "startswith", ("he", "hel"), 0, 1)
        # self.checkequal(True, "hello", "startswith", ("he", "hel"), 0, 2)

        # self.checkraises(TypeError, 'hello', 'startswith', (42,))

    def test_endswith(self):
        self.checkequal(True, "hello", "endswith", "lo")
        self.checkequal(False, "hello", "endswith", "he")
        self.checkequal(True, "hello", "endswith", "")
        self.checkequal(False, "hello", "endswith", "hello world")
        self.checkequal(False, "helloworld", "endswith", "worl")
        self.checkequal(True, "helloworld", "endswith", "worl", 3, 9)
        self.checkequal(True, "helloworld", "endswith", "world", 3, 12)
        self.checkequal(True, "helloworld", "endswith", "lowo", 1, 7)
        self.checkequal(True, "helloworld", "endswith", "lowo", 2, 7)
        self.checkequal(True, "helloworld", "endswith", "lowo", 3, 7)
        self.checkequal(False, "helloworld", "endswith", "lowo", 4, 7)
        self.checkequal(False, "helloworld", "endswith", "lowo", 3, 8)
        self.checkequal(False, "ab", "endswith", "ab", 0, 1)
        self.checkequal(False, "ab", "endswith", "ab", 0, 0)
        self.checkequal(True, "", "endswith", "", 0, 1)
        self.checkequal(True, "", "endswith", "", 0, 0)
        self.checkequal(False, "", "endswith", "", 1, 0)

        # test negative indices
        self.checkequal(True, "hello", "endswith", "lo", -2)
        self.checkequal(False, "hello", "endswith", "he", -2)
        self.checkequal(True, "hello", "endswith", "", -3, -3)
        self.checkequal(False, "hello", "endswith", "hello world", -10, -2)
        self.checkequal(False, "helloworld", "endswith", "worl", -6)
        self.checkequal(True, "helloworld", "endswith", "worl", -5, -1)
        self.checkequal(True, "helloworld", "endswith", "worl", -5, 9)
        self.checkequal(True, "helloworld", "endswith", "world", -7, 12)
        self.checkequal(True, "helloworld", "endswith", "lowo", -99, -3)
        self.checkequal(True, "helloworld", "endswith", "lowo", -8, -3)
        self.checkequal(True, "helloworld", "endswith", "lowo", -7, -3)
        self.checkequal(False, "helloworld", "endswith", "lowo", 3, -4)
        self.checkequal(False, "helloworld", "endswith", "lowo", -8, -2)

        # self.checkraises(TypeError, 'hello', 'endswith')
        # self.checkraises(TypeError, 'hello', 'endswith', 42)

        # test tuple arguments
        # self.checkequal(False, "hello", "endswith", ("he", "ha"))
        # self.checkequal(True, "hello", "endswith", ("lo", "llo"))
        # self.checkequal(True, "hello", "endswith", ("hellox", "hello"))
        # self.checkequal(False, "hello", "endswith", ())
        # self.checkequal(True, "helloworld", "endswith", ("hellowo", "rld", "lowo"), 3)
        # self.checkequal(
        #    False, "helloworld", "endswith", ("hellowo", "ello", "rld"), 3, -1
        # )
        # self.checkequal(True, "hello", "endswith", ("hell", "ell"), 0, -1)
        # self.checkequal(False, "hello", "endswith", ("he", "hel"), 0, 1)
        # self.checkequal(True, "hello", "endswith", ("he", "hell"), 0, 4)

        # self.checkraises(TypeError, 'hello', 'endswith', (42,))

    def test_join(self):
        # join now works with any sequence type
        # moved here, because the argument order is
        # different in string.join
        self.checkequal("a b c d", " ", "join", ["a", "b", "c", "d"])
        self.checkequal("abcd", "", "join", ("a", "b", "c", "d"))
        self.checkequal("bd", "", "join", ("", "b", "", "d"))
        self.checkequal("ac", "", "join", ("a", "", "c", ""))
        # self.checkequal('w x y z', ' ', 'join', Sequence())
        self.checkequal("abc", "a", "join", ("abc",))
        # self.checkequal('z', 'a', 'join', UserList(['z']))
        self.checkequal("a.b.c", ".", "join", ["a", "b", "c"])
        self.assertRaises(TypeError, ".".join, ["a", "b", 3])
        for i in [5, 25, 125]:
            self.checkequal(((("a" * i) + "-") * i)[:-1], "-", "join", ["a" * i] * i)
            self.checkequal(((("a" * i) + "-") * i)[:-1], "-", "join", ("a" * i,) * i)

        # self.checkequal(str(BadSeq1()), ' ', 'join', BadSeq1())
        # self.checkequal('a b c', ' ', 'join', BadSeq2())

    def _test_inplace_rewrites(self):
        # Check that strings don't copy and modify cached single-character strings
        self.checkequal("a", "A", "lower")
        self.checkequal(True, "A", "isupper")
        self.checkequal("A", "a", "upper")
        self.checkequal(True, "a", "islower")

        self.checkequal("a", "A", "replace", "A", "a")
        self.checkequal(True, "A", "isupper")

        self.checkequal("A", "a", "capitalize")
        self.checkequal(True, "a", "islower")

        self.checkequal("A", "a", "swapcase")
        self.checkequal(True, "a", "islower")

        self.checkequal("A", "a", "title")
        self.checkequal(True, "a", "islower")

    def test_none_arguments(self):
        # issue 11828
        s = "hello"
        self.checkequal(2, s, "find", "l", None)
        self.checkequal(3, s, "find", "l", -2, None)
        self.checkequal(2, s, "find", "l", None, -2)
        self.checkequal(0, s, "find", "h", None, None)

        self.checkequal(3, s, "rfind", "l", None)
        self.checkequal(3, s, "rfind", "l", -2, None)
        self.checkequal(2, s, "rfind", "l", None, -2)
        self.checkequal(0, s, "rfind", "h", None, None)

        self.checkequal(2, s, "index", "l", None)
        self.checkequal(3, s, "index", "l", -2, None)
        self.checkequal(2, s, "index", "l", None, -2)
        self.checkequal(0, s, "index", "h", None, None)

        self.checkequal(3, s, "rindex", "l", None)
        self.checkequal(3, s, "rindex", "l", -2, None)
        self.checkequal(2, s, "rindex", "l", None, -2)
        self.checkequal(0, s, "rindex", "h", None, None)

        self.checkequal(2, s, "count", "l", None)
        self.checkequal(1, s, "count", "l", -2, None)
        self.checkequal(1, s, "count", "l", None, -2)
        self.checkequal(0, s, "count", "x", None, None)

        self.checkequal(True, s, "endswith", "o", None)
        self.checkequal(True, s, "endswith", "lo", -2, None)
        self.checkequal(True, s, "endswith", "l", None, -2)
        self.checkequal(False, s, "endswith", "x", None, None)

        self.checkequal(True, s, "startswith", "h", None)
        self.checkequal(True, s, "startswith", "l", -2, None)
        self.checkequal(True, s, "startswith", "h", None, -2)
        self.checkequal(False, s, "startswith", "x", None, None)


if __name__ == "__main__":
    unittest.main()
