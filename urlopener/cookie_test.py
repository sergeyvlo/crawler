import urllib.request
from http.cookiejar import CookieJar, DefaultCookiePolicy
from urllib.request import  Request


policy = DefaultCookiePolicy(
    rfc2965=True, strict_ns_domain=DefaultCookiePolicy.DomainStrict)
cj = CookieJar(policy)
print(cj)
request = Request("http://fish.customweb.ru/admin/")
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
response = opener.open(request)

cook = cj.make_cookies(response, request)
print(cook)