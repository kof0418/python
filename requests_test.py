import requests

result = requests.get("http://www.example.com")

# print(result.headers)
# print(result.encoding)
# print(result.cookies)
# print(result.status_code)

# print(type(result.text))
# print("-------------------")
# print(result.text)

parameters = {'key1': 1, 'key2': 2}
result = requests.get("http://www.example.com", params=parameters)
print(result.url)
