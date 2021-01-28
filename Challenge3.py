import re
from Bio import ExPASy, SwissProt
import requests
import time

start_time = time.time()

def dna2tris(dna, start=0):
    mat = {'A': {'C': 0, 'G': 1, 'T': 2},
           'C': {'G': 0, 'T': 1, 'A': 2},
           'G': {'T': 0, 'A': 1, 'C': 2},
           'T': {'A': 0, 'C': 1, 'G': 2}}

    tris = []

    if start == 1:
        tris.append(mat['A'][dna[1]])

    for i in range(1, len(dna)):
        tris.append(mat[dna[i-1]][dna[i]])

    return tris


def tris_ascii(tris, mat):
    word = ''
    k = 0
    while k <= len(seq)-5:
        letter = ''.join([str(tr) for tr in tris[k:k+5]])
        if letter in mat:
            word += mat[letter]
            k += 5
        elif ''.join([str(tr) for tr in tris[k:k+6]]) in mat:
            letter = ''.join([str(tr) for tr in tris[k:k+6]])
            word += mat[letter]
            k += 6
        else:
            word += ' '
            k += 5

    return word


huff3 = open('test.txt', 'r')  # test.txt is een aangepaste versie van de huff3.cd
huff = {}
for line in huff3:
    temp = re.split(r'\t|\n', line)
    huff[temp[3]] = temp[1]

sequence = open('bpc3.dna', 'r')
seq = ''
for line in sequence:
    seq += line

print(tris_ascii(dna2tris(seq, start=1), huff))

fullurl = 'https://www.uniprot.org/uniprot/?query=homo+sapiens+2018+length%3A%5B4+TO+4%5D&sort=score&format=list'
accession = requests.get(fullurl)
handle = ExPASy.get_sprot_raw(re.sub('\n', '', accession.text))
record = SwissProt.read(handle)

aa_long = record.sequence

#get protein out of swissprot:

uniprot = open('uniprot-proteome_UP000005640+reviewed_yes.fasta', 'r')  # dit is een file met alle swissprot files in fasta format.
prots = []
s = 1
for line in uniprot:
    if re.search('^>', line):
        if s == 0:
            prots.append(prot)
        s = 0
        prot = ''
    else:
        prot += line

contains_twice100 = []
count = 0

for prot in prots:
    count += 1
    regex = '(?=' + aa_long + ')'
    begins = [m.start() for m in re.finditer(regex, prot)]

    for i in range(0, len(begins) - 1):
        if len(aa_long) <= begins[i + 1] - begins[i] <= 100 - len(aa_long):
            contains_twice100.append(count)

print(len(contains_twice100))

end_time = time.time()
print(end_time - start_time)