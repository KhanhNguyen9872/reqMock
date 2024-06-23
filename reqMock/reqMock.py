
class function:
	def __init__(self, Session):
		self.__Session = Session()
		self.__request = Session.request
		self.__urlparse = __import__('urllib').parse
		self.__showQuery = False
		# for hide
		try:
			self.__inspect = __import__('inspect')
		except Exception:
			print("WARNING: hide feature not working due to 'inspect' library not found!")
			self.__inspect = None

		self.__mockData = {
			"host": [
       
       		],
			"url": [
				
			],
			"match": [
				
			],
			"text": [
				
			]
		}
		return
	
	@property
	def __name__(self):
		return self.__request.__name__

	@property
	def __module__(self):
		return self.__request.__module__

	@property
	def __dict__(self):
		return self.__request.__dict__

	@property
	def __dir__(self):
		return self.__request.__dir__

	def __repr__(self):
		return "<function Session.request at {}>".format(hex(id(self)))

	def __check(self):
		if self.__inspect:
			stack = self.__inspect.stack()
			# caller_frame = stack[2]
			# caller_info = (caller_frame.function, caller_frame.lineno)
			return stack
		return True

	def __add(self, url, method, mock, to, headers = None, data = None, status_code = 200):
		try:
			tmp = self.__urlparse.urlparse(url)
			if url and all([tmp.scheme, tmp.netloc]):
				pass
			else:
				raise ValueError
		except ValueError:
			raise ValueError("add(): [url] must be a url")

		if (not method) and (not method.lower() in ["get", "post", "delete", "put", "patch", "options", "head"]):
			raise TypeError("add(): invalid [method]")

		if not mock in self.__mockData:
			raise TypeError("add(): [mock] must be a {text}. Found '{found}'".format(text = ", ".join([("'" + x + "'") for x in self.__mockData]), found = mock))

		if mock in ["url", "host", "match"]:
			try:
				tmp = self.__urlparse.urlparse(to)
				if to and all([tmp.scheme, tmp.netloc]):
					pass
				else:
					raise ValueError
			except ValueError:
				raise ValueError("add(): In mock ('url', 'host', 'match'), [to] must is a url")

		try:
			if len(str(status_code)) == 3:
				int(status_code)
			else:
				raise ValueError
		except ValueError:
			raise ValueError("add(): [status_code] must be a integer, and from 000 to 999")

		if mock == "text":
			if type(to) != type(b''):
				to = str(to).encode('utf8')
    
		data = {
			'url': url,
			'method': method.lower(),
			'to': to,
			'headers': headers,
			'data': data,
			'status_code': status_code
		}
		self.__mockData[mock].append(data)
		return

	def __remove(self, url):
		for type in self.__mockData:
			for i in range(0, len(self.__mockData[type]), 1):
				if (self.__mockData[type][i]['url'] == url):
					del self.__mockData[type][i]
		return

	def __call__(self, method, url, **kwargs):
		isBreak = False
		isText = None
		status_code = None
		url = self.__urlparse.urlparse(url)

		for _type in self.__mockData:
			for i in range(0, len(self.__mockData[_type]), 1):
				if (self.__mockData[_type][i]['method'] == method):
					if _type == "text":
						if (self.__mockData[_type][i]['url'] == self.__urlparse.urlunparse(url)):
							isBreak = True

							url = "http://google.com"
							isText = self.__mockData[_type][i]['to']
							status_code = self.__mockData[_type][i]['status_code']
							break
	
					elif _type == "url":
						if (self.__mockData[_type][i]['url'] == self.__urlparse.urlunparse(url)):
							isBreak = True

							url = self.__mockData[_type][i]['to']
							if self.__mockData[_type][i]['headers']:
								kwargs['headers'] = self.__mockData[_type][i]['headers']
							if self.__mockData[_type][i]['data']:
								kwargs['data'] = self.__mockData[_type][i]['data']
							status_code = self.__mockData[_type][i]['status_code']
							
							break
					
					elif _type == "host":
						if (self.__mockData[_type][i]['url'] == "{scheme}://{netloc}".format(scheme = url.scheme, netloc = url.netloc)):
							isBreak = True
							
							url = "{host}{path}".format(host = self.__mockData[_type][i]['to'], path = url.query if url.query else url.path)
							if self.__mockData[_type][i]['headers']:
								kwargs['headers'] = self.__mockData[_type][i]['headers']
							if self.__mockData[_type][i]['data']:
								kwargs['data'] = self.__mockData[_type][i]['data']
							status_code = self.__mockData[_type][i]['status_code']
							break
	
					elif _type == "match":
						if (self.__mockData[_type][i]['url'] in self.__urlparse.urlunparse(url)):
							isBreak = True
		
							url = self.__mockData[_type][i]['to']
							if self.__mockData[_type][i]['headers']:
								kwargs['headers'] = self.__mockData[_type][i]['headers']
							if self.__mockData[_type][i]['data']:
								kwargs['data'] = self.__mockData[_type][i]['data']
							status_code = self.__mockData[_type][i]['status_code']
							break
				
			if isBreak:
				break

		if (type(url) != type("")):
			url = self.__urlparse.urlunparse(url)

		if (self.__showQuery):
			text = ">> requests: {method}: {url}".format(method = method.upper(), url = url)
			if (kwargs) and (len(kwargs) > 0):
				count = 0
				text = text + " ("
				for i in kwargs:
					text = text + "{key}={value}".format(key = i, value = kwargs[i])
					if (len(kwargs) > 1) and (count != len(kwargs) - 1):
						text = text + ", "
					count = count + 1
				text = text + ")"
			
			print(text)
		result = self.__request(self.__Session, method=method, url=url, **kwargs)
		if isText:
			result._content = isText
		if status_code:
			result.status_code = status_code

		return result
	
	def add(self, url, **kwargs):
		if self.__check():
			return self.__add(url, **kwargs)
		else:
			raise AttributeError("'function' object has no attribute 'add'")

	def remove(self, url):
		if self.__check():
			return self.__remove(url)
		else:
			raise AttributeError("'function' object has no attribute 'remove'")

	def set(self, **kwargs):
		if kwargs:
			for i in kwargs:
				if i == "showQuery":
					self.__showQuery = bool(kwargs[i])
				else:
					raise TypeError("config '{name}' not found!".format(name = i))
		return

mockControl = function(__import__('requests').Session)

try:
	del function
except:
    pass

try:
	__import__('requests').Session.request = mockControl
except Exception as e:
	raise e
