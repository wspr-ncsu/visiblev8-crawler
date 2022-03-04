import unittest
import os.path
import web_server.vv8web.logParser
import filecmp


class LogParserTests(unittest.TestCase):
    def test_parser_accuracy(self):
        testPath = "C:\\Users\\qsd10\\PycharmProjects\\2022SpringTeam17-Kapravelos-LAS-1\\web_server\\logs\\testResult-https-__coinsbit.io.txt.json"
        absPath = "C:\\Users\\qsd10\\PycharmProjects\\2022SpringTeam17-Kapravelos-LAS-1\\web_server\\logs\\https-__coinsbit.io.txt.json"
        web_server.vv8web.logParser.main(absPath)
        self.assertTrue(os.path.exists(absPath))  # add assertion here
        self.assertTrue(filecmp.cmp(absPath, testPath, False))


if __name__ == '__main__':
    unittest.main()
