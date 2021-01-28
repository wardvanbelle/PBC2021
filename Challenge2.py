import re


def number_to_letter(numbers):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    letters = {numbr: letter for numbr, letter in zip(range(1, len(letters)), letters)}
    letters[0] = ' '

    sentence = ''
    for number in numbers:
        sentence += letters[number]

    return sentence


file = open('IDs.txt', 'r')
IDs = []

for line in file:
    if re.search('^[A-Z]', line):
        IDs.append(re.sub('\n', '', line))

file = open('prosite.dat')
PATTERNS = {ID: '' for ID in IDs}
k = 0

for line in file:
    if re.search(r'^ID .* PATTERN\.', line):
        IDp = re.match(r"^ID (.*); PATTERN\.", line)
        IDp = IDp.group(1).strip()
        if IDp in IDs:
            k = 1

    if k == 1 and re.search(r'^PA ', line):
        PATTERNS[IDp] += re.match(r"^PA (.*)", line).group(1).strip()
        if line[-2] == '.':
            k = 0


for ID in PATTERNS:
    pattern = PATTERNS[ID]
    regex_pattern = pattern.replace(".", "")
    regex_pattern = regex_pattern.replace("-", "")
    regex_pattern = regex_pattern.replace("<", "^")
    regex_pattern = regex_pattern.replace(">]", "]$")
    regex_pattern = regex_pattern.replace("{", "[^")
    regex_pattern = regex_pattern.replace("}", "]")
    regex_pattern = regex_pattern.replace("(", "{")
    regex_pattern = regex_pattern.replace(")", "}")
    regex_pattern = regex_pattern.replace("x", "[ARNDCQEGHILKMFPSTWYV]")
    PATTERNS[ID] = regex_pattern

file = open('Login.html', 'r')
prot = ''

for line in file:
    if re.search('^<span.*"">(.*)</span>', line):
        prots = re.split('</span>', line)
        for i in range(len(prots)-1):
            prot += re.search('<span.*"">(.*)', prots[i]).group(1)

COUNTS = []
for ID in PATTERNS:
    found = re.findall(PATTERNS[ID], prot)
    COUNTS.append(len(found))

sentence = number_to_letter(COUNTS)

print(sentence)
