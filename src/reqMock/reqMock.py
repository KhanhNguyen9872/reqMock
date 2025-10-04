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
        self.__showTrace = False
        self.__stdout = __import__('sys').stdout
        self.__traceback = __import__('traceback')
        self.__inspect = __import__('inspect')
        self.__trace_stdout = None
        self.__qualname__ = self.__request.__qualname__

        self.__mockData = {
            "host": [
       
               ],
            "url": [
                
            ],
            "match": [
                
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

    def add(self, url, method, mockCheck, mockMethod, to, headers = None, data = None, status_code = 200):
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

        if not mockCheck in self.__mockData:
            raise TypeError("add(): [mockCheck] must be a {text}. Found '{found}'".format(text = ", ".join([("'" + x + "'") for x in self.__mockData]), found = mock))

        if not mockMethod in ["url", "text"]:
            raise TypeError("add(): [mockMethod] must is ('url', 'text'). Found '{found}'".format(found = mockMethod))

        if mockMethod == "url":
            try:
                tmp = self.__urlparse.urlparse(to)
                if to and all([tmp.scheme, tmp.netloc]):
                    pass
                else:
                    raise ValueError
            except ValueError:
                raise ValueError("add(): In mockMethod ('url', 'host', 'match'), [to] must is a url")

        try:
            if len(str(status_code)) == 3:
                int(status_code)
            else:
                raise ValueError
        except ValueError:
            raise ValueError("add(): [status_code] must be a integer, and from 000 to 999")

        if mockMethod == "text":
            if type(to) != type(b''):
                to = str(to).encode('utf8')
    
        data = {
            'url': url,
            'method': method.lower(),
            'mockMethod': mockMethod,
            'to': to,
            'headers': headers,
            'data': data,
            'status_code': status_code
        }
        self.__mockData[mockCheck].append(data)
        return

    def remove(self, url):
        for type in self.__mockData:
            for i in range(0, len(self.__mockData[type]), 1):
                if (self.__mockData[type][i]['url'] == url):
                    del self.__mockData[type][i]
        return

    def __call__(self, method, url, **kwargs):
        mock = None
        isBreak = False
        status_code = None
        isText = None

        if self.__Enable:
            url = self.__urlparse.urlparse(url)
            
            for _type in self.__mockData:
                for i in range(0, len(self.__mockData[_type]), 1):
                    if (self.__mockData[_type][i]['method'] == method):
                        # if _type == "text":
                        #     if (self.__mockData[_type][i]['url'] == self.__urlparse.urlunparse(url)):
                        #         isBreak = True
                        #         mock = _type

                        #         url = "http://google.com"
                        #         isText = self.__mockData[_type][i]['to']
                        #         status_code = self.__mockData[_type][i]['status_code']
                        #         if not status_code:
                        #             status_code = 200
                        #         break
        
                        if _type == "url":
                            if (self.__mockData[_type][i]['url'] == self.__urlparse.urlunparse(url)):
                                isBreak = True
                                mock = self.__mockData[_type][i]['mockMethod']

                                if mock == "text":
                                    isText = self.__mockData[_type][i]['to']
                                    url = "http://google.com"
                                else:
                                    url = self.__mockData[_type][i]['to']

                                    if self.__mockData[_type][i]['headers']:
                                        kwargs['headers'] = self.__mockData[_type][i]['headers']
                                    if self.__mockData[_type][i]['data']:
                                        kwargs['data'] = self.__mockData[_type][i]['data']

                                status_code = self.__mockData[_type][i]['status_code']
                                if mock == "text":
                                    if not status_code:
                                        status_code = 200
                                break
                        
                        elif _type == "host":
                            if (self.__mockData[_type][i]['url'] == "{scheme}://{netloc}".format(scheme = url.scheme, netloc = url.netloc)):
                                isBreak = True
                                mock = self.__mockData[_type][i]['mockMethod']

                                if mock == "text":
                                    isText = self.__mockData[_type][i]['to']
                                    url = "http://google.com"
                                else:
                                    url = "{host}{path}".format(host = self.__mockData[_type][i]['to'], path = url.query if url.query else url.path)
                                    if self.__mockData[_type][i]['headers']:
                                        kwargs['headers'] = self.__mockData[_type][i]['headers']
                                    if self.__mockData[_type][i]['data']:
                                        kwargs['data'] = self.__mockData[_type][i]['data']
                                status_code = self.__mockData[_type][i]['status_code']
                                if mock == "text":
                                    if not status_code:
                                        status_code = 200
                                break
        
                        elif _type == "match":
                            if (self.__mockData[_type][i]['url'] in self.__urlparse.urlunparse(url)):
                                isBreak = True
                                mock = self.__mockData[_type][i]['mockMethod']

                                if mock == "text":
                                    isText = self.__mockData[_type][i]['to']
                                    url = "http://google.com"
                                else:
                                    url = self.__mockData[_type][i]['to']
                                    if self.__mockData[_type][i]['headers']:
                                        kwargs['headers'] = self.__mockData[_type][i]['headers']
                                    if self.__mockData[_type][i]['data']:
                                        kwargs['data'] = self.__mockData[_type][i]['data']
                                status_code = self.__mockData[_type][i]['status_code']
                                if mock == "text":
                                    if not status_code:
                                        status_code = 200
                                break
                        else:
                            raise TypeError("unknown method '{}'".format(_type))
                    
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

        if self.__showTrace:
            if self.__trace_stdout is None:
                try:
                    self.__trace_stdout = open('stack_trace.txt', 'w', encoding='utf-8')
                except Exception:
                    self.__trace_stdout = self.__stdout
            
            stack = self.__traceback.extract_stack()
            
            filtered_frames = []
            for frame in stack[:-1]:
                filename = frame.filename
                filtered_frames.append(frame)
            
            if filtered_frames:
                self.__trace_stdout.write(">> trace:\n")
                for i, frame in enumerate(filtered_frames, 1):
                    filename = frame.filename
                    func_name = frame.name
                    line_num = frame.lineno
                    line_content = frame.line.strip() if frame.line else ""
                    
                    if filename.endswith('.py'):
                        module_name = filename.split('/')[-1].split('\\')[-1].replace('.py', '')
                    else:
                        module_name = '<unknown>'
                    
                    args_str = ""
                    try:
                        current_frame = self.__inspect.currentframe()
                        if current_frame:
                            frame_obj = current_frame
                            for _ in range(len(stack) - i):
                                if frame_obj:
                                    frame_obj = frame_obj.f_back
                            
                            if frame_obj:
                                frame_locals = frame_obj.f_locals
                                frame_globals = frame_obj.f_globals
                                
                                if frame_locals:
                                    arg_parts = []
                                    for key, value in frame_locals.items():
                                        if not key.startswith('__'):
                                            try:
                                                if isinstance(value, str):
                                                    arg_parts.append(f"{key}='{value}'")
                                                else:
                                                    arg_parts.append(f"{key}={value}")
                                            except:
                                                arg_parts.append(f"{key}=<{type(value).__name__}>")
                                    
                                    if arg_parts:
                                        args_str = "(" + ", ".join(arg_parts[:10]) + ")"  # Giới hạn 10 tham số
                                        if len(arg_parts) > 5:
                                            args_str += "..."
                    except:
                        pass
                    
                    if args_str:
                        args_clean = args_str.strip('()')
                        if args_clean:
                            args_list = [arg.strip() for arg in args_clean.split(',')]
                            
                            self.__trace_stdout.write("   {num}. {func}(\n".format(num=i, func=func_name))
                            
                            for j, arg in enumerate(args_list):
                                if j == len(args_list) - 1:  # Dòng cuối
                                    self.__trace_stdout.write("      {arg}\n".format(arg=arg))
                                else:
                                    self.__trace_stdout.write("      {arg},\n".format(arg=arg))
                            
                            if i >= 100:
                                indent_spaces = "   " + " " * (len(str(i)) - 1)  # Căn chỉnh với số thứ tự
                            elif i >= 10:
                                indent_spaces = "   " + " " * (len(str(i)) - 1)  # Căn chỉnh với số thứ tự
                            else:
                                indent_spaces = "   "  # 3 spaces cho số < 10
                            
                            if line_content:
                                max_length = 80
                                if len(line_content) > max_length:
                                    truncated_content = line_content[:max_length-3] + "..."
                                else:
                                    truncated_content = line_content
                                self.__trace_stdout.write("{indent}) of <{module}> at line {line} -> {content}\n".format(
                                    indent=indent_spaces, module=module_name, line=line_num, content=truncated_content
                                ))
                            else:
                                self.__trace_stdout.write("{indent}) of <{module}> at line {line}\n".format(
                                    indent=indent_spaces, module=module_name, line=line_num
                                ))
                        else:
                            if line_content:
                                max_length = 80
                                if len(line_content) > max_length:
                                    truncated_content = line_content[:max_length-3] + "..."
                                else:
                                    truncated_content = line_content
                                self.__trace_stdout.write("   {num}. {func}() of <{module}> at line {line} -> {content}\n".format(
                                    num=i, func=func_name, module=module_name, line=line_num, content=truncated_content
                                ))
                            else:
                                self.__trace_stdout.write("   {num}. {func}() of <{module}> at line {line}\n".format(
                                    num=i, func=func_name, module=module_name, line=line_num
                                ))
                    else:
                        if line_content:
                            max_length = 80
                            if len(line_content) > max_length:
                                truncated_content = line_content[:max_length-3] + "..."
                            else:
                                truncated_content = line_content
                            self.__trace_stdout.write("   {num}. {func}() of <{module}> at line {line} -> {content}\n".format(
                                num=i, func=func_name, module=module_name, line=line_num, content=truncated_content
                            ))
                        else:
                            self.__trace_stdout.write("   {num}. {func}() of <{module}> at line {line}\n".format(
                                num=i, func=func_name, module=module_name, line=line_num
                            ))
                
                params_str = ""
                param_parts = []
                
                if url:
                    if isinstance(url, str):
                        param_parts.append(f"url='{url}'")
                    else:
                        param_parts.append(f"url={url}")
                
                if kwargs:
                    for key, value in kwargs.items():
                        if value is not None:
                            if isinstance(value, str):
                                param_parts.append(f"{key}='{value}'")
                            else:
                                param_parts.append(f"{key}={value}")
                
                if param_parts:
                    params_str = "(" + ", ".join(param_parts) + ")"
                
                self.__trace_stdout.write("   {num}. requests.{method}{params}\n".format(
                    num=len(filtered_frames) + 1, method=method.lower(), params=params_str
                ))
                
                if self.__trace_stdout != self.__stdout:
                    self.__trace_stdout.flush()

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
                elif i == "showTrace":
                    self.__showTrace = bool(kwargs[i])
                elif i == "trace_stdout":
                    if kwargs[i] is None:
                        self.__trace_stdout = None
                    elif kwargs[i] and (type(kwargs[i]) == __import__('_io').TextIOWrapper):
                        self.__trace_stdout = kwargs[i]
                    else:
                        raise TypeError("invalid trace_stdout. Found '{found}'".format(found = type(kwargs[i])))
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
                                print(">> ERROR: Same name as another module! try another one!".format(name))
                                return
                            except (ImportError, SyntaxError):
                                print(">> ERROR: Wrong module name! try another one!")
                                return
                            except (ModuleNotFoundError):
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

# mock
mockControl = function(__import__('requests').Session)

for reqMock in ["__name__", "__file__", "__cached__", "__spec__", "__loader__", "__doc__", "__package__", "__path__"]:
    globals()[reqMock] = __import__('requests').__dict__[reqMock]

del reqMock

class Session:
    def request(self, method, url, **kwargs):
        return mockControl(method, url, **kwargs)

try:
    __import__('requests').Session.request = Session.request
except Exception as e:
    raise e

del function, Session
