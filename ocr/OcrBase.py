import cv2
import pytesseract


class OcrBase:
    def __init__(self, img):
        """
        Must initialize with an image that has to be parsed
        :param img: Image which represents an openCV Image Object
        """
        self.img = img
        self.img_str = None
        self.errors = []

    def basic_preprocess(self):
        # Step 1: Grayscale
        # Step 2: Threshold
        # Step 3: Remove horizontal lines
        # Step 4: Remove vertical lines
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        thresh_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Length of contour
        L = 15
        # Thickness of the contour
        T = 1
        # Iterations
        I = 2

        # Remove horizontal
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (L, T))
        detected_lines = cv2.morphologyEx(thresh_inv, cv2.MORPH_OPEN, kernel, iterations=I)
        h_cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        h_cnts = h_cnts[0] if len(h_cnts) == 2 else h_cnts[1]

        # Remove vertical
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (T, L))
        detected_lines = cv2.morphologyEx(thresh_inv, cv2.MORPH_OPEN, kernel, iterations=I)
        v_cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        v_cnts = v_cnts[0] if len(v_cnts) == 2 else v_cnts[1]

        for c in h_cnts + v_cnts:
            cv2.drawContours(self.img, [c], -1, (255, 255, 255), 4)

        # cv2.imshow('Pre Processed', self.img)
        # cv2.waitKey(0)
        # at this point the image must have the horizontal and vertical lines stripped

    def _ocr(self):
        custom_oem_psm_config = r'--oem 3 --psm 6'
        self.img_str = pytesseract.image_to_string(self.img, config=custom_oem_psm_config)

    def process_ocr_text(self):
        pass

    def parse(self):
        """
        Define a function that can parse a given image and return a json object
        that has atleast:
            - Date of the report
            - Array of district objects
            - Totals
        :return: string representing csv of the parsed data
        """
        self.basic_preprocess()
        self._ocr()
        return self.process_ocr_text()