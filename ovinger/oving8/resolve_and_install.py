#!/usr/bin/python3
# coding=utf-8
import random
import string
from typing import Callable, List, Set, Tuple

"""
Har du noen gang trengt å installere pakker ved hjelp av et pakkesystem? En «pakke» er her programvare som installeres på datamaskinen. Python har for eksempel pakkesystemet pip som sin standard. Populære språkuavhengige pakkesystemer er APT, Homebrew, Pacman og Chocolatey.

En ting som gjør prosessen komplisert, er at en pakke kan avhenge av at andre pakker er installert for at den selv kan installeres. Disse andre pakkene kan igjen avhenge av at andre pakker er installert. På den måten kan man risikere å måtte installere veldig mange pakker. Heldigvis har vi ikke sykliske avhengigheter, siden det da ville ha vært umulig å installere pakken.

Her skal du implementere et forenklet pakkesystem. Du må implementere funksjonen resolve_and_install(package), som er en funksjon som kalles når en bruker ønsker å installere en pakke. Her er package et Package-objekt som representerer en pakke klienten ønsker å installere. Et Package-objekt har attributtene dependencies, som er et tuppel med Package-objekter pakken avhenger av, og is_installed, som er en boolsk variabel som sier om pakken allerede er installert. Flere av pakkene kan allerede være installert før resolve_and_install kalles. Du kan anta at om en pakke er installert, så er alle pakkene den avhenger av også installert.

Funksjonen resolve_and_install(package) skal sørge for å installere pakken brukeren ønsker å installere. For å gjøre det, skal du bruke funksjonen install, som er implementert av oss. Når du kaller install(package) vil metoden prøve å installere pakken package på maskinen. Du må sørge for at følgende krav er overholdt når koden din kaller install(package):

package kan ikke allerede være installert.
Alle pakkene som package er avhengig av må være installerte.
Ønsker du å teste programmet ditt lokalt, finnes det eksempeltester her.

"""
# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et sett med hardkodete instanser og
# muligheten for å generere tilfeldige instanser. Genereringen av de tilfeldige
# instansene kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests: bool = False
# Antall tilfeldige tester som genereres.
random_tests: int = 10
# Laveste mulige antall pakker i generert instans.
n_lower: int = 3
# Høyest mulig antall pakker i generert instans.
n_upper: int = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed: int = 0


class Package:
    def __init__(
        self,
        dependencies: Tuple["Package", ...],
        is_installed_func: Callable[["Package"], bool],
    ):
        self.__is_installed_func: Callable[["Package"], bool] = is_installed_func
        self.__dependencies: Tuple["Package", ...] = dependencies

    @property
    def dependencies(self) -> Tuple["Package", ...]:
        return self.__dependencies

    @property
    def is_installed(self) -> bool:
        return self.__is_installed_func(self)

    def __str__(self) -> str:
        if not self.dependencies:
            return f"● is_installed: {self.is_installed}\n"
        representation = f"┓ is_installed: {self.is_installed}\n"
        r = 0
        for dependency in self.dependencies:
            r += 1
            if r != 1:
                representation += "\n"
            if r != len(self.dependencies):
                representation += f"┣━━━" + str(dependency).replace("\n", "\n┃   ")
            else:
                representation += f"┗━━━" + str(dependency).replace("\n", "\n    ")
        return representation

    def __repr__(self) -> str:
        return str(self)

    def deepcopy(self) -> "Package":
        def gen_function(val: bool) -> Callable[["Package"], bool]:
            return lambda x: val

        return Package(
            tuple(dep.deepcopy() for dep in self.dependencies),
            gen_function(self.is_installed),
        )


def get_install_func(installed_packages: Set[Package]) -> Callable[[Package], None]:
    def install(package: Package) -> None:
        if package.is_installed:
            raise ValueError(
                'Du kjører "install" på en pakke som allerede er installert.'
            )
        if not all([p.is_installed for p in package.dependencies]):
            raise ValueError(
                'Du kjører "install" på en pakke uten å ha installert alle pakkene den er avhengig av.'
            )
        installed_packages.add(package)

    return install


"""
The solution to this problem is the following:
Perform a DFS. Color is not necessary, as we assume no cycles.
Install at the bottom of the DFS: Thus, only packages with no uninstalled dependencies will be installed
"""


def resolve_and_install(package: Package) -> None:
    for dep in package.dependencies:
        if not dep.is_installed:
            resolve_and_install(dep)
    if not package.is_installed:
        install(package)


def generate_random_test(
    num_nodes: int, p: float
) -> Tuple[Package, Callable[[Package], None]]:
    installed_packages = set()
    is_installed_func = lambda x: x in installed_packages
    packages: List[Package] = [None for i in range(num_nodes)]  # type: ignore
    incoming_edges = [[] for i in range(num_nodes)]
    installed_limit = random.randint(0, num_nodes)
    for i in range(1, num_nodes):
        predecessors = random.sample(
            range(0, i), k=random.randint(1, min(i, max(1, int(2 * p * i))))
        )
        for pre in predecessors:
            incoming_edges[pre].append(i)
    for i in range(num_nodes - 1, -1, -1):
        dependencies = tuple([packages[j] for j in incoming_edges[i]])
        packages[i] = Package(dependencies, is_installed_func)
        if i >= installed_limit:
            installed_packages.add(packages[i])
    return (packages[0], get_install_func(installed_packages))


def gen_examples(nl: int, nu: int, k: int):
    for _ in range(k):
        yield generate_random_test(random.randint(nl, nu), random.randint(1, 9) / 10)


random.seed(1)
tests = [
    generate_random_test(random.randint(1, 10), random.randint(4, 6) / 10)
    for _ in range(10)
]

if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(n_lower, n_upper, random_tests))


failed = False
for package, install_func in tests:
    global install
    install = install_func
    initial_state = package.deepcopy()
    try:
        resolve_and_install(package)
    except ValueError as e:
        if failed:
            print("-" * 50)
        print(
            f"""
Koden feilet med følgende feilmelding:
{str(e)}

Input:
{str(initial_state)}

Status ved avslutning:
{str(package)}
        """
        )
        failed = True
    else:
        if not package.is_installed:
            if failed:
                print("-" * 50)
            print(
                f"""
Koden installerte ikke pakken.

Input:
{str(initial_state)}

Status ved avslutning:
{str(package)}
            """
            )
            failed = True

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
