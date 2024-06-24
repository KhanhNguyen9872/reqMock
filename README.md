# reqMock
Mock requests library like HTTPToolkit in python3

# Example:
## Original code
```python3
import requests
print(requests.get("https://google.com").text)
```

## Import in first line of code
```python3
from reqMock import mockControl as mock
```

## Mock `https://google.com` to another website
```python3
mock.add(
	url = "https://google.com",	# mock 'from'
	method = "GET",			# method 'from'
	mock = "url",			# method mock ('host', 'url', 'match', 'text')
	to = "https://youtube.com",	# mock 'to'
)
```

## Mock `https://google.com` to custom result
```python3
mock.add(
	url = "https://youtube.com",	# mock 'from'
	method = "GET",			# method 'from'
	mock = "text",			# method mock ('host', 'url', 'match', 'text')
	to = "Hello World!",		# mock 'to'
)
```

## Enable `showQuery` to print info from requests
```python3
mock.set(showQuery = True)		# Default is False

# You will see output requests like this 
# ">> requests: GET: https://google.com (headers={'abc': 'def'})" and below is result output
```

## Enable `showResult` to print result output from requests
```python3
mock.set(showResult = True)		# Default is False

# You will see output requests like this 
# ">> result: GET: https://google.com" and below is result output
```

## Redirect output of `show` to file
```python3
mock.set(stdout = open('out.txt', 'w'))

# Output of 'show' option will write to file instead of write to output
```