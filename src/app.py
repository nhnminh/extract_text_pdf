# ==================================================
# This small application is to: 
# - Extract text from pdf
# - Attach text with their position 
# - Export to a dataframe, then a csv file
# 
# Library pdfminer is required to run this script
# Python3 is required either 
# @author: NGUYEN Hoang Nhat Minh
# 2020-11-01
# ================================================== 

from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import pandas as pd
import numpy as np

def extractTextAndPosition(pdfFileName, outputName):
    print('Open and initialize the object ... ')
    fp = open(pdfFileName + '.pdf', 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)

    df = pd.DataFrame(columns=['page', 'text', 'x', 'y'])
    nbPage = 0
    for page in pages:
        nbPage += 1
        print('Processing page ' + str(nbPage))
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                # print('At %r is text: %s' % ((x, y), text))
                df.loc[len(df)] = {
                    'page': nbPage,
                    'text':lobj.get_text(),
                    'x': lobj.bbox[0],
                    'y': lobj.bbox[3]
                }
    df.to_csv(outputName + ".csv", index = False)


if __name__ == "__main__":
    extractTextAndPosition("data/file", "out/title_2")