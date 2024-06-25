__import__('requests')

class function:
    def __init__(self, Session):
        self.__Enable = False
        self.__name = __name__
        self.__package = __package__
        self.__modulePath = __file__
        if (self.__modulePath):
            self.__modulePath = "/".join("/".join(self.__modulePath.split("\\")).split("/")[:-1])


        self.__Session = Session()
        self.__request = Session.request
        self.__urlparse = __import__('urllib').parse
        self.__showQuery = False
        self.__showResult = False
        self.__stdout = __import__('sys').stdout
        self.__qualname__ = self.__request.__qualname__

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

    def add(self, url, method, mock, to, headers = None, data = None, status_code = 200):
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

    def remove(self, url):
        for type in self.__mockData:
            for i in range(0, len(self.__mockData[type]), 1):
                if (self.__mockData[type][i]['url'] == url):
                    del self.__mockData[type][i]
        return

    def __call__(self, method, url, **kwargs):
        if self.__Enable:
            isBreak = False
            isText = None
            status_code = None
            url = self.__urlparse.urlparse(url)
            mock = None

            for _type in self.__mockData:
                for i in range(0, len(self.__mockData[_type]), 1):
                    if (self.__mockData[_type][i]['method'] == method):
                        if _type == "text":
                            if (self.__mockData[_type][i]['url'] == self.__urlparse.urlunparse(url)):
                                isBreak = True
                                mock = _type

                                url = "http://google.com"
                                isText = self.__mockData[_type][i]['to']
                                status_code = self.__mockData[_type][i]['status_code']
                                if not status_code:
                                    status_code = 200
                                break
        
                        elif _type == "url":
                            if (self.__mockData[_type][i]['url'] == self.__urlparse.urlunparse(url)):
                                isBreak = True
                                mock = _type

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
                                mock = _type

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
                                mock = _type

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

        if (self.__showQuery) and mock != "text":
            text = ">> requests: {method}: {url}".format(method = method.upper(), url = url)
            if (kwargs) and (len(kwargs) > 0):
                count = 0
                args = "("
                for i in kwargs:
                    if kwargs[i]:
                        args = args + "{key}={value}".format(key = i, value = kwargs[i])
                        if (len(kwargs) > 1) and (count != len(kwargs) - 1):
                            args = args + ", "
                    count = count + 1
                args = args + ")"
            
            if args == "()":
                args = ""

            if args:
                text = text + " " + args

            self.__stdout.write(text + "\n")

        result = self.__request(self.__Session, method=method, url=url, **kwargs)

        if (self.__showResult) and mock != "text":
            text = ">> result: {method}: {url}\n{result}\n".format(method = method.upper(), url = url, result = result.text)
            self.__stdout.write(text + "\n")

        if self.__Enable:
            if isText:
                result._content = isText
            if status_code:
                result.status_code = status_code

        return result

    def set(self, **kwargs):
        if kwargs:
            for i in kwargs:
                if i == "showQuery":
                    self.__showQuery = bool(kwargs[i])
                elif i == "showResult":
                    self.__showResult = bool(kwargs[i])
                elif i == "stdout":
                    if kwargs[i] and (type(kwargs[i]) == __import__('_io').TextIOWrapper):
                        self.__stdout = kwargs[i]
                    else:
                        raise TypeError("invalid stdout. Found '{found}'".format(found = type(kwargs[i])))
                elif i == "enable":
                    self.__Enable = bool(kwargs[i])
                    if self.__Enable:
                        for i in [self.__name, self.__package]:
                            try:
                                del __import__('sys').modules[i]
                            except KeyError:
                                continue
                        self.__stdout.write("> mock enabled!\n")
                    else:
                        self.__stdout.write("> mock disabled!\n")
                elif i == "moduleName":
                    name = str(kwargs[i])
                    if name:
                        current_name = self.__modulePath.split("/")[-1]

                        print(">> WARNING: You choose rename module from '{old}' to '{new}'".format(old = current_name, new = name))
                        if input(">> Do you want to rename? [Y/*]: ").lower() == "y":
                            new_path = "/".join(self.__modulePath.split("/")[:-1]) + "/" + name
                            try:
                                __import__(name)
                                print(">> ERROR: Same name as another library! try another one!".format(name))
                                return
                            except (ModuleNotFoundError, ImportError):
                                try:
                                    __import__('os').rename(self.__modulePath, new_path)
                                except FileExistsError:
                                    print(">> ERROR: module name ({}) EXIST! try another one!".format(name))
                                    return
                                self.__modulePath = new_path
                                print(">> WARNING: restart script to apply change!")
                        else:
                            print(">> Cancelled!")
                    else:
                        print(">> WARNING: module name empty!")
                else:
                    raise TypeError("config '{name}' not found!".format(name = i))
        return

# exec(compile("""
# # __import__
# class __import:
#     def __init__(self, __import):
#         self.__import = __import
#         self.__qualname__ = self.__import.__qualname__
#         return

#     @property
#     def __name__(self):
#         return self.__import.__name__

#     @property
#     def __module__(self):
#         return self.__import.__module__

#     @property
#     def __dir__(self):
#         return self.__import.__dir__

#     def __repr__(self):
#         return "<built-in function __import__>"

#     def __call__(self, *args, **kwargs):
#         if (args[0] == __package__):
#             raise ModuleNotFoundError("No module named '{}'".format(__package__))
#         return self.__import(*args, **kwargs)

# __import = __import(vars(__import__('builtins')).copy()['__import__'])

# __import__('builtins').__import__ = __import
# """, "<stdin>", "exec"))


# mock
mockControl = function(__import__('requests').Session)

for reqMock in ["__name__", "__file__", "__cached__", "__spec__", "__loader__", "__doc__", "__path__"]:
    globals()[reqMock] = __import__('requests').__dict__[reqMock]

class Session:
    def request(self, method, url, **kwargs):
        return mockControl(method, url, **kwargs)

try:
    __import__('requests').Session.request = Session.request
except Exception as e:
    raise e

del function, Session
