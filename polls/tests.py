from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Question,Choice

def create_question(question_text, choice_list):
    """
    Creates a question with the given `question_text` and choices in 'choice_list'
    in database
    """
    ques_in_db = Question(question=question_text)
    ques_in_db.save()
    for ch in choice_list:
    	ques_in_db.choice_set.create(choice=ch)
    return ques_in_db.id

class IndexViewTest(TestCase):

	def test_for_latest_question(self):

		question_text = "latest question"
		choice_list = ["ch1","ch2","ch3"]
		create_question(question_text,choice_list)

		response = self.client.get(reverse('index'))
		self.assertContains(response, "latest question",
                            status_code=200)