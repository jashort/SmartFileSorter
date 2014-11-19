import unittest
import smartfilesorter
import os
import tempfile
import shutil

class TestIntegrationTests(unittest.TestCase):
    """
    Broader test cases
    """
    def setUp(self):
        self.source_dir = tempfile.mkdtemp()
        self.dest_dir = os.path.join(self.source_dir, 'dest/')
        os.mkdir(self.dest_dir)

        self.test_filename = "test.txt"
        self.source_file = os.path.join(self.source_dir, self.test_filename)
        self.dest_file = os.path.join(self.dest_dir, self.test_filename)

        with open(self.source_file, 'w') as output:
            output.write("This is a test file.")

        self.s = smartfilesorter.SmartFileSorter()

    def tearDown(self):
        #shutil.rmtree(self.source_dir)
        pass

    def test_file_matches_multiple_rulesets(self):
        test_path = os.path.dirname(__file__)
        test_file = os.path.join(test_path, 'match_multiple_rulesets.yml')
        self.s.args = self.s.parse_arguments([test_file, self.source_dir])
        self.s.create_logger(self.s.args)
        self.s.run(self.s.args)



