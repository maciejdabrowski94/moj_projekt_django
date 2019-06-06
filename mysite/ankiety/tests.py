import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """
    Tworzy pytanie z 'question_text' i publikuje zadana liczbe z parametru 'days'
    liczac od timezone.now()
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() zwraca False dla ktorych pub_date
        jest w przyszlosci.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() zwraca False dla pytan ktorych pub_date
        jest starsze niz 1 dzien.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() zwraca True dla pytan ktorych pub_date
        jest w przedziale jednego dnia.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Jezeli nie ma ankiet - powinna zostac wyswietlona stosowna informacja
        """
        response = self.client.get(reverse('ankiety:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak ankiet do wyswietlenia.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Pytania ktore maja date publikacji ustawiona w przeszlosci powinny
        zostac wyswietlone
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('ankiety:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Pytania ktore maja date publikacji ustawiona w przyszlosci nie powinny
        zostac wyswietlone
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('ankiety:index'))
        self.assertContains(response, "Brak ankiet do wyswietlenia.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Jezeli istnieja pytania z przeszlosci i przyszlosci - tylko
        z data publikacji z przeszlosci powinny zostac wyswietlone
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('ankiety:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        Na stronie glownej moze zostac wyswietlone kilka testow
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('ankiety:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
