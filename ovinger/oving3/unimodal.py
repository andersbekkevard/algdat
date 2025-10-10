"""
En unimodal tabell er en tabell med tall som, etter å ha blitt rotert et bestemt antall ganger,
kan deles i to intervaller, der det første er strengt stigende, og det andre strengt synkende.

Med rotasjon mener vi her å ta det første elementet ut av tabellen og sette det inn bak alle
de andre elementene i tabellen.

Et eksempel er tabellen ⟨8,6,3,1,5,9,12,10⟩:
- Hvis man roterer denne tabellen 3 ganger ender man opp med ⟨1,5,9,12,10,8,6,3⟩
- ⟨1,5,9,12,10,8,6,3⟩ har egenskapen at tabellen først er strengt stigende og deretter strengt synkende
- ⟨8,6,3,1,5,9,12,10⟩ er derfor en unimodal tabell

I en slik unimodal tabell er det en bestemt største verdi.
Du skal implementere en algoritme med kjøretid Θ(log n) som finner denne verdien.

Viktige restriksjoner:
- Testene vil ikke godkjenne løsninger som prøver å skrive til tabellen (f.eks. x[0]=1)
- Du vil få en feilmelding hvis du prøver å endre tabellen

Ønsker du å teste programmet ditt lokalt, finnes det eksempeltester her.
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall verdier i generert instans.
n_lower = 3
# Høyest mulig antall verdier i generert instans.
n_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def find_maximum(x):
    d, n = len(x), len(x)
    i = 0
    while d > 0:
        prev = x[i]
        i = (i + d) % n
        if x[i] > prev:
            continue
        d = -(d // 2)
    return max(x[i], x[(i + d) % n])


# Hardkodete tester på format: (x, svar)
tests = [
    ([1], 1),
    ([1, 3], 3),
    ([3, 1], 3),
    ([1, 2, 1], 2),
    ([1, 0, 2], 2),
    ([2, 0, 1], 2),
    ([0, 2, 1], 2),
    ([0, 1, 2], 2),
    ([2, 1, 0], 2),
    ([2, 3, 1, 0], 3),
    ([2, 3, 4, 1], 4),
    ([2, 1, 3, 4], 4),
    ([4, 2, 1, 3], 4),
]


# En liste som ikke kan skrives til
class List:
    def __init__(self, li):
        self.__internal_list = li

    def __getitem__(self, key):
        return self.__internal_list[key]

    def __len__(self):
        return len(self.__internal_list)

    def __setitem__(self):
        raise NotImplementedError("Du skal ikke trenge å skrive til listen")


# Genererer tilfeldige instanser med svar
def generate_examples(k, nl, nu):
    for _ in range(k):
        n = random.randint(nl, nu)
        x = random.sample(range(5 * n), k=n)
        answer = max(x)
        t = x.index(answer)
        x = sorted(x[:t]) + [answer] + sorted(x[t + 1 :], reverse=True)
        t = random.randint(0, n)
        x = x[t:] + x[:t]
        yield x, answer


if generate_random_tests:
    if seed:
        random.seed(seed)

    tests.extend(generate_examples(random_tests, n_lower, n_upper))


failed = False
for x, answer in tests:
    x_ro = List(x[:])
    student = find_maximum(x_ro)
    if student != answer:
        if failed:
            print("-" * 50)

        failed = True

        print(
            f"""
Koden ga feil svar for følgende instans:
x: {x}

Ditt svar: {student}
Riktig svar: {answer}
"""
        )

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
