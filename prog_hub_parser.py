from excel import Table
from model import Question
from selenium.common.exceptions import NoSuchElementException

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class ProhHubParser(object):

  def __init__(self, driver, lang):
    self.driver = driver
    self.lang = lang
    self.question_arr = []
    self.by_add = False

  def parse(self):
    self.go_to_tests_page()
    for i in range(200):
      try:
        time.sleep(0.1)
        self.by_add = False
        question = self.parse_question_page()
        question_start_link = self.driver.find_elements_by_class_name("btn-cyan")[0].get_attribute('href')
        self.driver.get(question_start_link)
        if self.by_add:
          continue
        else:
          self.question_arr.append(question)
          print(i)
      except Exception as err:
        print(err)


    self.driver.close()
    table = Table()
    table.create_table(self.question_arr)

  def go_to_tests_page(self):
    self.driver.get("https://proghub.ru/tests")
    slide_elems = self.driver.find_elements_by_class_name("carousel__card")

    for elem in slide_elems:
      lang_link = elem.get_attribute('href')

      if self.lang in lang_link:
        language = lang_link.split("/")[-1]
        self.driver.get("https://proghub.ru/t/" + language)
        question_start_link = self.driver.find_elements_by_class_name("btn-cyan")[0].get_attribute('href')
        self.driver.get(question_start_link)
        break

  def parse_question_page(self):
    question = Question()
    self.fill_question_text(question)
    self.fill_question_code(question)
    self.fill_question_answers(question)
    return question

  def fill_question_text(self, question):
    try:
      question_text_elm = self.driver.find_element_by_class_name("question__title")
      question.text = question_text_elm.text
      print(question.text)
    except NoSuchElementException:
      print("Question text missing")

  def fill_question_code(self, question):
    try:
      code_elm = self.driver.find_element_by_tag_name("code")
      question.code = code_elm.text
      print(question.code)
    except NoSuchElementException:
      pass

  def fill_question_answers(self, question):
    try:
      if self.fill_question_answers_check():
        self.driver.find_element_by_class_name("question__answer_item").click()
        self.driver.find_element_by_class_name("btn-primary").click()
        WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CLASS_NAME, "correct")))
        for elem in self.driver.find_elements_by_class_name("correct"):
          question.answers.append(elem.text)
        print(question.answers)
    except NoSuchElementException:
      print("Answer missing")

  def fill_question_answers_check(self):
    try:
      self.driver.find_element_by_class_name("correct")
      self.by_add = True
      return False
    except NoSuchElementException:
      return True
