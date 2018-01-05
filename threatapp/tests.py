from django.test import TestCase
from . import myfunc
from datetime import datetime
from datetime import timedelta


# Create your tests here.
class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_single_left_quote_unicode_is_valid(self):
        print("test_single_left_quote_unicode_is_valid")
        self.assertEqual(myfunc.sanitize_text("‘"),"'")

    def test_single_right_quote_unicode_is_valid(self):
        print("test_single_right_quote_unicode_is_valid")
        self.assertEqual(myfunc.sanitize_text("’"),"'")

    def test_double_left_quote_unicode_is_valid(self):
        print("test_double_left_quote_unicode_is_valid")
        self.assertEqual(myfunc.sanitize_text("“"),'"')
        
    def test_double_right_quote_unicode_is_valid(self):
        print("test_double_right_quote_unicode_is_valid")
        self.assertEqual(myfunc.sanitize_text("”"),'"')

    def test_filter__300secs_date_within_one_day_ago_use(self):
        t = datetime.now() - timedelta(0,300)
        sample = [{"date": t.strftime('%b %d, %Y %H:%M:%S')}]
        self.assertEqual(myfunc.filter_by_period("0",sample),sample)

    def test_filter_19hours_date_within_one_day_ago_use(self):
        t = datetime.now() - timedelta(0,0,0,0,0,19)
        sample = [{"date": t.strftime('%b %d, %Y %H:%M:%S')}]
        self.assertEqual(myfunc.filter_by_period("0",sample),sample)

    def test_filter_3days_date_in_one_day_ago(self):
        t = datetime.now() - timedelta(3)
        sample = [{"date": t.strftime('%b %d, %Y %H:%M:%S')}]
        self.assertEqual(myfunc.filter_by_period("1",sample),sample)


    def test_filter_8days_date_outof_one_day_ago(self):
        t = datetime.now() - timedelta(8)
        sample = [{"date": t.strftime('%b %d, %Y %H:%M:%S')}]
        self.assertNotEqual(myfunc.filter_by_period("1",sample),sample)

    def test_filter_23days_date_within_four_weeks_ago(self):
        t = datetime.now() - timedelta(23)
        sample = [{"date": t.strftime('%b %d, %Y %H:%M:%S')}]
        self.assertEqual(myfunc.filter_by_period("2",sample),sample)