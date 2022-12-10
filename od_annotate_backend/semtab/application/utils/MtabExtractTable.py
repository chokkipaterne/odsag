import csv
import pathlib
from csv import reader
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import glob
from urllib.parse import unquote

from semtab.mantistable import views


class MtabAnnotationApi:
   #__list_CTA_Global = []
   #__list_CPA_Global = []
   #__list_CEA_Global = []

   def __init__(self, csv_files):
      self.csv_files = csv_files
      self.__list_CTA_Global = []
      self.__list_CPA_Global = []
      self.__list_CEA_Global = []
      self.__annotated_table = ""

   def __load_page(self,url):

      # open browser
      # L'option Headless permet d'éviter d'ouvrir une page web a chaque fois que l'algorithme est lancé. + performant
      options = Options()
      options.add_argument('--headless')


      #path = str(pathlib.Path().absolute())+'\plugin\geckodriver.exe'
      path = str(pathlib.Path(__file__).parent.resolve()).rsplit('\\', 1)[0]+'\plugin\geckodriver.exe'
      print(path)
      driver = webdriver.Firefox(options=options,executable_path=path)
      driver.set_window_size(2000, 1000)
      #driver = webdriver.Firefox(executable_path=path)

      # load page
      driver.get(url)
      return driver

   def __interactPage(self, driver, inputText, textElementId, buttonElementId,tableElementClass):
      #item = driver.find_element_by_id('table_text_content')
      item = driver.find_element_by_id(textElementId)

      # put text
      #driver.find_element_by_id('table_text_content').clear()
      driver.find_element_by_id(textElementId).clear()
      #item.send_keys('W. S. Coffin,Yale Divinity School,E. Rubinstein,"Strafford, Vermont",New York City\r W. Maclagan,"Peterhouse, Cambridge","William Barrington, 6th Viscount Barrington",London,Edinburgh')
      item.send_keys(inputText)

      # find button
      #item = driver.find_element_by_id('annotation1')
      item = driver.find_element_by_id(buttonElementId)

      # click button
      item.click()

      #J'ai mis un wait de 2 minutes sinon, l'algorithme ne laisse pas le temps au site de faire les annotations. La durée de 120 secondes peut être changée.
      wait = WebDriverWait(driver, 1200)
      #men_menu = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'table-info')))
      men_menu = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, tableElementClass)))
      ActionChains(driver).move_to_element(men_menu).perform()

   def getList_CTA_Global(self):
      return self.__list_CTA_Global

   def getList_CPA_Global(self):
      return self.__list_CPA_Global

   def getList_CEA_Global(self):
      return self.__list_CEA_Global

   def getAnnotated_table_Global(self):
      return self.__annotated_table

   def extractTableHTML(self):
      #url = 'https://dbpedia.mtab.app/mtab'
      url = 'https://mtab.app/'

      driver = self.__load_page(url)

      #Read csv
      # csv files in the path
      files = self.csv_files

      # checking all the csv files in the
      # specified path
      p = 1
      for filename in files:
         #print("Fichier"+str(p))
         #print(filename)
         # get subjectCOlumn index from semtab.mantistable
         subject_column_index = views.get_subject_index_mantistable(filename)

         print(filename)
         print(subject_column_index)

         p = p+1
         with open(filename, 'r', encoding='utf-8') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = csv.reader(read_obj, quotechar='\'', delimiter=',',
                                    quoting=csv.QUOTE_ALL, skipinitialspace=True)
            # Iterate over each row in the csv using reader object
            z = 0
            inputText =''
            colheader = list()
            for row in csv_reader:
               if z == 0:
                  colheader = row
                  z = 1
                  print(colheader)
               #print(row)
               # row variable is a list that represents a row in csv
               #print(row)
               #rowFinal = str(row)[1:]
               #rowFinal = rowFinal[:-1]
               #inputText = inputText + rowFinal + '\r'

               # rve: with mantistable move the subject column to first index
               if(len(row) > 1):
                  row.insert(0, row.pop(subject_column_index))

               firstWordLine = True
               for rowWord in row:
                  if firstWordLine == True:
                     inputText = inputText+'\r'+rowWord
                     firstWordLine = False
                     #print(inputText)
                  else:
                     inputText = inputText+','+rowWord
                     #print(inputText)


         self.__interactPage(driver,inputText,'table_text_content','annotation1','table-info')
         #print(inputText)
         #CTA
         listCTA = []
         self.__annotated_table = driver.find_element_by_class_name('table-responsive').get_attribute('innerHTML')
         #print(self.__annotated_table)

         table_class =  driver.find_element_by_class_name('table-info')
         rows = table_class.find_elements_by_tag_name("th") # get all of the rows in the table
         i = 0
         #print("CTA:\r")
         for row in rows:
            # Get the columns (all the column 2)
            links = row.find_elements_by_xpath("./a") #note: index start from 0, 1 is col 2
            ctaList = []
            for link in links:
               # print link href
               ctaList.append(link.text+"$"+unquote(link.get_attribute("href")).replace('"',''))
               #print(link.get_attribute("href")) #prints text from the element
            listCTA.insert(i,ctaList)
            i = i+1

         #print("self.__list_CTA_Global")
         #print(self.__list_CTA_Global)
         self.__list_CTA_Global.append(listCTA)
         #print("listCTA")
         #print(self.__list_CTA_Global)
         #print("end")


         #CPA
         listCPA = []
         table_class =  driver.find_element_by_class_name('table-success')
         rows = table_class.find_elements_by_tag_name("th") # get all of the rows in the table
         i = 0
         #print("CPA:\r")
         for row in rows:
            # Get the columns (all the column 2)
            links = row.find_elements_by_xpath("./a") #note: index start from 0, 1 is col 2
            if links == []:
               if(i > 0):
                  listCPA.insert(i-1,'')
                  listCPA[i-1] = ''
                  """if listCTA[i] != []:
                     #print(listCTA[i])
                     #listCPA[i-1] = ' '.join(listCTA[i])
                     listCPA[i-1] = listCTA[i][0].replace('"','')
                  else :
                     #listCPA[i-1] = filename[filename.rfind("\\")+1:]+"-COL"+str(i)
                     #listCPA[i-1] = filename[filename.rfind("\\")+1:]+"-"+colheader[i-1]
                     listCPA[i-1] = colheader[i-1].replace('"','')"""
               i = i+1
            else:
               #print('Col'+str(i))
               if(i > 0):
                  listCPA.insert(i-1,'')
                  for link in links:
                     # print link href
                     #print(link.get_attribute("href")) #prints text from the element
                     listCPA[i-1] = link.text+"$"+unquote(link.get_attribute("href")).replace('"','')
               i = i+1

         #listCPA[0] = listCTA[1][0]
         #listCPA[0] = 'Subject Column'
         self.__list_CPA_Global.append(listCPA)
         #print("listCPA")
         #print(listCPA)


         #CEA
         listCEA = []
         nbColumn = len(listCPA)
         table_class = driver.find_element_by_xpath('*//table[@class="table table-bordered"]/tbody')
         rows = table_class.find_elements_by_tag_name("td") # get all of the rows in the table
         i = 0
         #print("CEA:\r")
         for row in rows:
            # Get the columns (all the column 2)
            links = row.find_elements_by_xpath("./a") #note: index start from 0, 1 is col 2
            #print('Col'+str(i))
            listCEA.insert(i,'')
            if links == []:
               listCEA[i] = row.text+"$#"
            else :
               #print(links)
               for link in links:
                 # print(link)
                  #print(link.get_attribute("href")) #prints text from the element
                  #linkString = str(link.get_attribute("href"))
                  #linkString = linkString.encode('utf8')
                  if link.get_attribute("href") != None:
                      text = row.text
                      if "\n" in text:
                          text = text.replace("\n", '');
                          text = text.replace(link.text, '');

                      listCEA[i] = text+"$"+unquote(link.get_attribute("href")).replace('"','')
            i = i+1

         #Ca déconne
         nbRow = int(len(listCEA)/nbColumn)
         dataCEA = [[0 for x in range(int(nbColumn))] for y in range(int(nbRow))]

         #print("Begin")
         #print(nbColumn)
         #print(listCEA)
         #print(nbRow)
         #print("End")

         z = 0
         for i in range(0,nbRow,1):
            for j in range(0,nbColumn,1):
               dataCEA[i][j] = listCEA[z]
               z = z+1

         self.__list_CEA_Global.append(dataCEA)

         driver.get(url)
         driver.refresh()
      driver.close()
