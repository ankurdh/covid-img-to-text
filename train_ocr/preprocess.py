import cv2
import logging
import os

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class Preprocessor:
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

        Step 1: Convert image to grayscale
        Step 2: Threshold image to remove random jitter
        Step 3: Remove vertical and horizontal lines

        Write the image
        :param path: path to the image file
        :return: N/A
        """
        img = cv2.imread(path)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # adaptive gaussian much clearer, better details, than adaptive mean

        # tested adaptive threshold with box size: 11, 25, 33, 39, 41, 51
        # quality increases between 11-33, and decreases from 33-51
        # decided to go with adaptive thresholding; compared with linear thresholding
        # compared with tozero and otsu filters
        # vertical and horizontal lines appear clearer with adaptive thresholding

        # for the c-value, we tried: -7, 0, 1, 2, 3, 8, 10, 13
        # 1, 2 were yielding best results, most amount of detail

        thresh_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 33, 1)

        # Length of contour
        L = 15
        # Thickness of the contour
        T = 1
        # Iterations
        I = 2

        # Remove horizontal
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (L, T))
        detected_lines = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel, iterations=I)
        h_cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        h_cnts = h_cnts[0] if len(h_cnts) == 2 else h_cnts[1]

        # Remove vertical
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (T, L))
        detected_lines = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel, iterations=I)
        v_cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        v_cnts = v_cnts[0] if len(v_cnts) == 2 else v_cnts[1]

        for c in h_cnts + v_cnts:
            cv2.drawContours(img, [c], -1, (255, 255, 255), 4)

        d_name = os.path.dirname(path)
        f_name = os.path.basename(path).replace('.jpg', '_processed.jpg')
        f_name = os.path.join(d_name, f_name)
        print("Saving: ", f_name)
        cv2.imwrite(f_name, img)

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
