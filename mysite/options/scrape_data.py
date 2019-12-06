from requests_html import HTMLSession
session = HTMLSession()

def has_option_decorator(func):
	def wrapper(*args, **kwargs):
		if args[0].has_options:
			return func(*args, **kwargs)
	return wrapper

class Yahoo_Option_Scraper():
	def __init__(self, ticker, date=None):
		self.ticker = ticker.upper()
		#base is the main url that won't be manipulated
		self.base = f'https://finance.yahoo.com/quote/{self.ticker}/options?p={self.ticker}'
		#url may be manipulated depending on values passed to the class constructor
		self.url = f'https://finance.yahoo.com/quote/{self.ticker}/options?p={self.ticker}'
		if date != None:
			self.url += f"&date={date}"
		self.response = self.get_response(self.url)
		self.exp_dates = self.get_exp_dates()
		if len(self.exp_dates.keys()) > 0:
			self.has_options = True
		else:
			self.has_options = False

	def get_response(self, url):
		return session.get(url)

	@has_option_decorator
	def get_company_name(self):
		return self.response.html.find(
				'div#quote-header-info > div > div > div > h1')[0].text

	def get_exp_dates(self):
		# <div class="Fl(start) Pend(18px) option-contract-control drop-down-selector">
		dates = {}
		html_dates = self.response.html.find('div.option-contract-control.drop-down-selector > select > option')
		for date in html_dates:
			#concatenates the base url with the appropriate date format
			dates[date.text] = date.attrs['value']
		return dates

	@has_option_decorator
	def get_stock_price(self):
		#used Chrome inspect tools to find what span to call
		# <span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="35">16.25</span>
		return self.response.html.find(
			'div#quote-header-info > div:nth-child(3) > div > div > span'
		)[0].text
		# return self.response.html.find('span[data-reactid="35"]')[0].text

	@has_option_decorator
	def get_option_table(self, call=True):
		#example from finance.yahoo.com/quote/{ticker}/options?p={ticker}
		#<table class="calls table-bordered W(100%) Pos(r) Bd(0) Pt(0) list-options" data-reactid="42">
		#<table class="puts table-bordered W(100%) Pos(r) list-options" data-reactid="343">
		opt_class = self.opt_class(call)
		#try and except because sometimes a compnay will just have calls or puts
		try:
			table = self.response.html.find(f'table.{opt_class}.list-options')[0]
			table_head = table.find('thead > tr')[0]
			data = {t_head.text:[] for t_head in table_head.find('th')}
			table_body = table.find('tbody')[0]
			for row in table_body.find('tr'):
				for i, col in enumerate(row.find('td')):
					data[list(data.keys())[i]].append(col.text)
			return data
		except Exception as e:
			return None


	def opt_class(self, value: bool):
		if value:
			return 'calls'
		return 'puts'
