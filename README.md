# reqMock
Mock requests library like HTTPToolkit in python3

# Installation
```bash
pip install reqMock
```

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

## Enable mock
```python3
# To enable mock
mock.set(enable = True)

# To disable mock
mock.set(enable = False)
```

## Mock `https://google.com` to another website
```python3
mock.add(
	url = "https://google.com",	# mock 'from'
	method = "GET",			# method 'from'
	mockCheck = "url",			# method mock ('host', 'url', 'match')
	mockMethod = "url",			# mock to 'url' or 'text'
	to = "https://youtube.com",	# data
)
```

## Mock `https://youtube.com` to custom result
```python3
mock.add(
	url = "https://youtube.com",
	method = "GET",	
	mockCheck = "url",	
	mockMethod = "text",
	to = "Hello World!"
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

# If you want to rename this module for hide from check
```python3
# Open a python3 shell
from reqMock import mockControl as mock

# Example change module name from 'reqMock' to 'Khanh'
mock.set(moduleName = "Khanh")
# Choose 'y' and new name will applied in new session

# For new session, import it by using new name
from Khanh import mockControl as mock
```
