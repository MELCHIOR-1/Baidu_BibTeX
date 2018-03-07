# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 00:28:43 2018

@author: x
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
#from selenium.webdriver.common.proxy import ProxyType
import sys
from selenium.webdriver.chrome.options import Options
#from bs4 import  BeautifulSoup
#import bibtexparser
#from bibtexparser.bparser import BibTexParser


class SelectDialog(QDialog):
    def __init__(self, parent=None):
        super(SelectDialog, self).__init__(parent)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.initUI()
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("查找文献引用bibtex")
        self.resize(800, 400)
    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(QLabel("题目："), 0, 0)
        self.pathLineEdit = QLineEdit()
        grid.addWidget(self.pathLineEdit, 0, 1, 1, 6)
        button = QPushButton("查找")
        button.clicked.connect(self.process)
        grid.addWidget(button, 0, 7)
        self.listWidget = QListWidget()
        self.listWidget.setWordWrap(True)
        grid.addWidget(self.listWidget, 1, 0, 1, 8)
        self.setLayout(grid)


    def process(self):
        key = str(self.pathLineEdit.text())
        res = []
        res = self.fetch_bibtex(self.driver,key)
        self.listWidget.clear()
        self.listWidget.addItems(res)
        
        
        
    def fetch_bibtex(self,driver,key):
#        key = '航空电磁勘查技术发展现状及展望'
        driver.get('http://xueshu.baidu.com/s?wd=%s&ie=utf-8&pn=00'%key)
        elems = driver.find_elements_by_class_name('sc_q')
        hrefs = []
        for elem in elems:
            elem.click()
            quot = driver.find_element_by_class_name('sc_quote_content')
            cls_btn = driver.find_element_by_class_name('sc_md_cls')
            WebDriverWait(quot, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[data-type='BibTeX']")))
            hrefs.append(quot.find_element_by_css_selector("[data-type='BibTeX']").get_attribute('href'))
            cls_btn.click()
        bibs = []
        for href in hrefs:
            driver.get(href)
            bibs.append( driver.find_element_by_tag_name('pre').text )
        return bibs
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = SelectDialog()
    if dialog.exec_():
        pass