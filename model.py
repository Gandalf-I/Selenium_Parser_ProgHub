class Question(object):

  def __init__(self, text="", code="", answers=None):
    self.text = text
    self.code = code
    self.answers = answers if answers else []

  def __str__(self):
    return f"{self.text} {self.code} {self.answers}"
