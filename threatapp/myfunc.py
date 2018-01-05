from datetime import datetime
from datetime import timedelta


def sanitize_text(intxt):
	#convert from byte data to text
	
	# replace Unicode for the single left and right quote characters with the ACSII equivalent
	text = intxt.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201C", '"').replace(u"\u201D", '"')
	#convert whitespace characters(defined in string.whitespace) to a single space
	text = text.translate(str.maketrans("\t\n\r\x0b\x0c", "     "))
	return text

"""
 period == 0  for date within a day; (default if it is not 0,1,or 2)
 period == 1 for date within a week; 
 period == 2 for date within four weeks; 

"""
def filter_by_period(periodtype,list_data):
	js_data = []
	cur_date = datetime.now()
	if periodtype == "1":
		start_week = cur_date - timedelta(7)
		js_data = list(filter(lambda record: datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') > start_week and datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') < cur_date, list_data))
	elif periodtype == "2":
		start_four_weeks = cur_date - timedelta(28)
		js_data = list(filter(lambda record: datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') > start_four_weeks and datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') < cur_date, list_data))
	else:
		start_today = cur_date - timedelta(1)
		js_data = list(filter(lambda record: datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') > start_today and datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') < cur_date, list_data))
	return js_data