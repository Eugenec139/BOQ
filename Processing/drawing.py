import io
from io import StringIO
from xml.etree.ElementTree import Element, fromstring

from bs4 import BeautifulSoup
from pdfminer.converter import XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from utility import Utility


class Drawing:
    # filename the name of the pdf file to read from
    def __init__(self, filename):
        self.filename = filename

    # converts the pdf into xml structure which a computer can deal with
    # returns str
    def __get_xml_from_pdf(self):
        resource_manager: PDFResourceManager = PDFResourceManager(caching=True)
        la_params = LAParams()
        la_params.all_texts = True
        la_params.detect_vertical = True
        rotation = 0
        output_xml: StringIO = io.StringIO()
        device: XMLConverter = XMLConverter(
            resource_manager, output_xml, laparams=la_params, stripcontrol=True
        )

        with open(self.filename, "rb") as pdf_file:
            interpreter = PDFPageInterpreter(resource_manager, device)
            for page in PDFPage.get_pages(pdf_file, check_extractable=True):
                page.rotate = (page.rotate + rotation) % 360
                interpreter.process_page(page)

        device.close()
        output_value: str = output_xml.getvalue()
        output_xml.close()

        return output_value

    # extracts all text from the pdf and returns it with bbox's
    # returns a mixed array with bbox and the text in the line
    def get_text(self):
        xml_file = self.__get_xml_from_pdf()
        soup: BeautifulSoup = BeautifulSoup(xml_file, features="xml")
        tags = "textline"
        text_lines = soup.find_all(tags)
        output = []

        for group_lines in text_lines:
            assert isinstance(group_lines, object)
            single_line: Element = fromstring(str(group_lines))
            characters = []

            for letter in single_line:
                characters.append(letter.text)

            full_line = "".join(map(str, characters))
            if not Utility.is_number(full_line):
                continue

            line_bounding_box = group_lines.get("bbox")
            output.append([full_line, line_bounding_box])

        return output
