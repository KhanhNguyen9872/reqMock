from reqMock import mockControl as mock

mock.add(
	url = "http://google.com",
	method = "get",
	mock = "text",
	to = "Hello World!"
)

mock.set(showQuery = True)
mock.set(stdout = open('out.txt', 'w'))

import requests
print(requests.get("http://google.com").text)
