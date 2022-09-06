import urllib.parse

import re
from flet import Page

class UrlComponents:
    
    def _encode_url_component(self, url: str) -> str:
        """
        Function encodes querystring part of URL\n
        Ex. q=dom & dogs -> q=dom+%26+dogs
        """
        return urllib.parse.quote(url)
    
    def _decode_url_component(self, url: str) -> str:
        """
        Function decodes querystring part of URL\n
        Ex. q=dom+%26+dogs -> q=dom & dogs 
        """
        return urllib.parse.unquote(url)
    
    def _is_encoded(self) -> bool:
        """
        Function returns True if URL is already encoded
        """
        q_result = self._querystring_part()
        return True if self._decode_url_component(self.url[q_result.start() + 1: q_result.end()]) != self.url[q_result.start() + 1: q_result.end()] else False
        
    def _querystring_part(self, url_string: bool = False):
        """
        Function sliced url part and returns querystring part.\n
        Use case: checking querystring part for encode, assiging decoded value
        """
        pattern = re.compile(r'\?[\w\D]+')
        data = pattern.search(self.url)
        return data if url_string is False else self.url[data.start() + 1: data.end()]

class QueryString(UrlComponents):
    """
    Note:
            `QueryString must be inside of url on change function`\n

    Constructor:
            If `page` argument is passed, `QueryString` takes url out automatically of `page` object\n
            If `url` (customly specified url) is specified, then `QueryString` will work on `url` argument\n

    Methods:
            `get()` method takes `key` an an argument and returns value according to key. (Ex: .../?name=Joe) -> `get('name')` -> `Joe`\n
            `to_dict()` returns all the key-value pairs of querystring as a `dict`\n

    """

    def __init__(self, page: Page = None, url: str = None):
        
        # Concerning post method        
        if page is not None or url is not None:
            self.url = page.url + page.route if url is None else url

            if self._is_encoded() and page is not None:
                # Assinging decoded querystring part to url for internal use
                self.url = page.url + self._decode_url_component(self._querystring_part(url_string=True))
            
            else:
                raise NotImplementedError('Page must be specified in order to assign decoded querystring accordingly.')
        
    def get(self, key: str) -> str:
        assert hasattr(self, 'url'), '"page" or "url" is not provided in order to extract querystring'
        
        self._pattern = re.compile(f"{key}=[\w\+?]+")
        self._res = self._pattern.search(self.url)
        self._res = self.url[self._res.start() + len(key) + 1 : self._res.end()]
        return self._res if "+" not in self._res else self._res.replace("+", " ")

    def to_dict(self) -> dict:
        assert hasattr(self, 'url'), '"page" or "url" is not provided in order to extract querystring'        
        
        self._key_pattern = re.compile(r"[\w]+=")
        self._keys = [i[:-1] for i in self._key_pattern.findall(self.url)]

        self._value_pattern = re.compile(r"=[\w\+?]+")
        self._values = [
            i[1:].replace("+", " ") for i in self._value_pattern.findall(self.url)
        ]

        return {i: j for i, j in zip(self._keys, self._values)}
    
    def post(self, kwargs: dict):
        key_value = []
        for i in kwargs:
            value = kwargs[i]

            if type(value) not in [int, float]:
                if ' ' in value:
                    value = value.replace(' ', '+')
            
            key_value.append(f'{i}={value}')

        data = '?' + '&'.join(key_value)
        # return data
        return '?' + urllib.parse.urlencode(kwargs)
                
one = {
    'a': 5,
    'b': 'gurami levani',
    'c': ['Giorgi', 'Levani']
}
uri = 'http://127.0.0.1:63657/#/something/?name=5&b=some+random%2Bshit'


if __name__ == '__main__':
    a = QueryString()
    print(a.post(one))

