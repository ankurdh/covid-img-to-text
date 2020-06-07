import os
import unittest
from train_ocr.preprocess import Preprocessor

class TestPreprocessor(unittest.TestCase):
    test_path = '../../data/test_state'

    def __init__(self):
        super().__init__()
        self.preprocessor = Preprocessor()

    def setUpClass(cls):
        # create a dir
        os.makedirs(TestPreprocessor.test_path, exist_ok=True)

        # create a sample file
        filename = os.path.join(TestPreprocessor.test_path, 'sample1.jpg')
        with open(filename, 'wb') as temp_file:
            temp_file.write(bytearray(b'0'))

    def tearDownClass(cls):
        filename = os.path.join(TestPreprocessor.test_path, 'sample1.jpg')
        os.unlink(filename)
        os.rmdir(TestPreprocessor.test_path)

    def test_do(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()