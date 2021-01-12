import urllib.request
from http.cookiejar import CookieJar, DefaultCookiePolicy
from urllib.request import  Request
from urlopener.request_handlers import CookiejarHandler, MozillaCookiejarHandler


#policy = DefaultCookiePolicy(
#    rfc2965=True, strict_ns_domain=DefaultCookiePolicy.DomainStrict)
#cj = CookieJar(policy)
#print(cj)

request = Request("http://fish.customweb.ru/admin/")

cookie_handler = MozillaCookiejarHandler()
policy = {'rfc2965': True, 'strict_ns_domain': DefaultCookiePolicy.DomainStrict}
opener = urllib.request.build_opener(cookie_handler.cookiejar(policy))
response = opener.open(request)

cookie_handler.mozillaCookieJar.save()
cook = cookie_handler.make_cookies(response, request)

print(cook)