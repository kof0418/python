import re

# text = "my phone number is 08-75555555, and 07-4147744"
# print(re.findall(r"0\d-\d{7}", text))

# text2 = "Are you a dog person or a cat person?"
# print(re.findall(r"dog|cat", text2))

regex = r"\b[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
# regex2 = r"[^@]+@[^@]+\.[^@]+"


def check_email(email):
    if re.fullmatch(regex, email):
        print(f"{email} is a valid email!!")
    else:
        print(f"{email} is not valid.")


email1 = "anktierail326@gmail.com"
email2 = "myown.site@our-earth.org"
email3 = "hahah.com"

check_email(email1)
check_email(email2)
check_email(email3)
