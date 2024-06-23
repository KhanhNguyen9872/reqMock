# reqMock
Mock requests library like HTTPToolkit in python3

# Example:
## Original code
```python3
import requests
print(requests.get("https://google.com").text)
```

## Mock `https://google.com` to another website
```python3
from reqMock import mockControl as mock
mock.add(
	url = "https://google.com",	# mock 'from'
	method = "GET",			# method 'from'
	mock = "url",			# method mock ('host', 'url', 'match', 'text')
	to = "https://youtube.com",	# mock 'to'
)

# <Original code here>
```

## Mock `https://google.com` to custom result
```python3
from reqMock import mockControl as mock
mock.add(
	url = "https://youtube.com",	# mock 'from'
	method = "GET",			# method 'from'
	mock = "text",			# method mock ('host', 'url', 'match', 'text')
	to = "Hello World!",		# mock 'to'
)

# <Original code here>
# Result should is 'Hello World!'
```

## Enable `showQuery` to print info from requests
```python3
from reqMock import mockControl as mock
mock.set(showQuery = True)		# Default is False

# <Original code here>
# You will see output requests like this ">> requests: GET: https://google.com (params=None)"
```

## Enable `showQuery` to print result output from requests
```python3
from reqMock import mockControl as mock
mock.set(showResult = True)		# Default is False

# <Original code here>
# You will see output requests like this ">> result: GET: https://google.com" and below is result output
```

