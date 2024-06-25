from reqMock import mockControl as mock

mock.add(
	url = "https://google.com",
	method = "GET",
	mockCheck = "url",
	mockMethod = "text",
	to = "Hello World!",
	status_code = 404
)

mock.set(enable = True)

import requests
a = requests.get("https://google.com")
print(a)
print(a.text)