import cv2
import pytesseract
from PIL import Image
import os, subprocess
import re
import glob
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'A:\full\path\to\tesseract.exe'
popplerpath = r'B:\full\path\to\pdftoppm.exe'

pdf_dir = input("Enter full path to folder containing the pdfs: ")
os.chdir(pdf_dir)

def file_list():
    """Lists all the file in the desired directory containing 
    the pdfs to be converted"""
    pdfs = []
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            pdfs.append(file)
    return pdfs

def pdf_to_img(file):
    """Uses poppler to convert each page of the pdf file 
    to a jpeg for a more accurate text extraction as 
    compared to directly extracting text from the pdf"""
    filename = file[:-4]
    proc = subprocess.Popen('"%s" -jpeg %s %s' %(popplerpath, file, filename), \
        stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    proc.communicate()
    print(f"Done converting {file} to Image")

def img_to_txt(pdffile):
    """Creates a text file containing all the text extracted
    from each jpeg extracted from the original pdf file"""
    filename = pdffile[:-4]
    txtfile = open('%s.txt' %(filename), 'a')
    for file in os.listdir(pdf_dir):
        if file.endswith(".jpg"):
            img = cv2.imread(file)
            text = pytesseract.image_to_string(img)
            txtfile.write(text)
    txtfile.close()
    print(f"Done converting {filename} image to Text")

def text_process(pdffile):
    """Creates a csv file containing all the names
    in the extracted text from the pdf file. Names
    are expected to be in the form of Last Name,
    Given Name Middle Name"""
    filename = pdffile[:-4] + ".txt"
    processedfile = pdffile[:-4] + ".csv"
    file = open(filename, 'r')
    text = file.readlines()
    file.close()
    df = pd.DataFrame(text, columns = ["Name"])
    df = df[df["Name"].str.contains(',')]
    df["Name"] = df["Name"].str.strip('\n, *, .')
    # Removes "Page x of x" from text extracted
    df["Name"] = df["Name"].apply(lambda x: re.sub(r"^Page\s+\d+\s+of\s+\d+", '', x))
    # Removes "x." from text extracted
    df["Name"] = df["Name"].apply(lambda x: re.sub(r"\d+\.\s?", '', x))
    # Names are expected to be formatted using uppercase letters
    # This line removes the paragraph on every first page of each file
    df = df[df["Name"] == df["Name"].str.upper()]
    df = df["Name"].str.split(',', 1, expand = True)
    df.columns = ["Last Name", "First Name"]
    # Year and Scholarship type are extracted from the file name
    year, scholartype = pdffile[:-4].split('_')
    if scholartype == "ug":
        scholartype = "Merit/ RA"
    df["Year"] = year
    df["Scholarship Type"] = scholartype
    df.to_csv(processedfile, encoding = 'utf-8', index = False)
    print(f"Done creating {processedfile}")

def delete_imgs():
    """Deletes ALL jpeg files in the directory containing the
    pdf files to be converted. This assumes that the only jpeg files
    in the folder are the ones created during the run of this program"""
    pics = glob.glob('*.jpg')
    for pic in pics:
        try:
            os.unlink(pic)
        except:
            pass
    print("Done deleting converted images")

def delete_txt():
    """Deletes ALL txt files in the directory containing the
    pdf files to be converted. This assumes that the only txt files
    in the folder are the ones created during the run of this program"""
    txts = glob.glob('*.txt')
    for txt in txts:
        try:
            os.unlink(txt)
        except:
            pass
    print("Done deleting text files")

def combine_sources():
    """Creates a csv file containing all the entries
    of the csv files created before"""
    srcs = glob.glob('*.csv')
    for src in srcs:
        tmp = pd.read_csv(src, )
        tmp["Source"] = src
        try:
            final_df = pd.read_csv("combinedsources.csv", encoding = 'utf-8')
            final_df = pd.concat([final_df, tmp], ignore_index = True)
            final_df.to_csv("combinedsources.csv", index = False, encoding = 'utf-8')
        except FileNotFoundError:
            tmp.to_csv("combinedsources.csv", index = False, encoding = 'utf-8')
    print("Done combining sources")

if __name__ == "__main__":
    PDFS = file_list()
    for pdf in PDFS:
        pdfstart = time.time()
        print(f"Processing {pdf}")
        pdf_to_img(pdf)
        print(f"Started converting {pdf[:-4]} image to text")
        img_to_txt(pdf)
        text_process(pdf)
        delete_imgs()
        delete_txt()
    print("Done extracting all names from pdfs")
    combine_sources()