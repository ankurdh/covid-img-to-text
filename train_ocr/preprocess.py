import cv2
import logging
import os

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Preprocessor():
    """
    Define a methodology to parse all the samples from the states.

    The class will read all the samples*.jpg files and prepare a set of
    sample*_preprocessed.jpg in the same directory.

    Few ways to preprocess images files are:
    * remove the colors from them
    * threshold images
    * remove tables (horizontal and vertical lines)
    * remove other irregularities like:
        * Images
        * Scan irregularities
        * Table Headers
    """

    def __init__(self):
        self.states = [
            'himachal',
            'jammukashmir',
            'punjab',
            'rajasthan',
            'karnataka',
            'maharashtra',
            'uttarpradesh'
        ]

        self.samples_path = 'data'

    def _preprocess_image(self, path):
        """
        Read the image

        Step 1: Convert image to grayscase
        Step 2: Threshold image to remove random jitter
        Step 3: Remove vertical and horizontal lines

        Write the image
        :param path: path to the image file
        :return: N/A
        """
        img = cv2.imread(path)
        pass

    def _process_state(self, state, path):
        logging.info('Processing state: %s' % state)
        samples = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for sample in samples:
            sample_path = os.path.join(path, sample)
            logging.warning('Processing: %s' % sample_path)
            self._preprocess_image(sample_path)

    def do(self):
        for state in self.states:
            path = os.path.join(self.samples_path, state)
            if not os.path.exists(path):
                logging.warning('No data for state: %s' % state)
                continue

            self._process_state(state, path)


if __name__ == '__main__':
    Preprocessor().do()