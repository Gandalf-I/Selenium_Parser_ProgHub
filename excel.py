from openpyxl import Workbook


class Table(object):
  workbook = Workbook()
  sheet = workbook.active

  def create_table(self, question_arr):
    for i, question in enumerate(question_arr):
      self.sheet["A" + str(i + 1)] = question.text
      self.sheet["B" + str(i + 1)] = question.code
      box_answers = ""
      for answers in question.answers:
        box_answers += answers + "\n"
      self.sheet["C" + str(i + 1)] = box_answers

    self.workbook.save(filename="123.xlsx")
