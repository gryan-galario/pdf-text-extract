# pdf-text-extract

This python script uses poppler and pytesseract to extract names from PDFs in the format LAST NAME, GIVEN NAME then saves the output to a csv file

Simply enter the full path to the folder containing all the PDFs to be extracted and wait for the program to finish

Sample outputs are shown in the Outputs folder. As for the input, the path to the PDF folder is used as the input. However, for user visibility purposes, the outputs were shown in a different folder. If you run the script with the path to the PDF folder as the input, the outputs would also be shown in the same directory.

The time it took for my computer to process through the file is written in the timing.txt.

The PDFs are taken from [DOST SEI Scholarship Results](http://www.sei.dost.gov.ph/index.php/scholarships).

**IMPORTANT:**
The script must be edited first in your computer before running, specifically **lines 10 and 11**.

Requirements:
Poppler: [Poppler Download Link](https://poppler.freedesktop.org/)
PyTesseract: [tesseract-ocr GitHub Link](https://github.com/tesseract-ocr/tesseract)
