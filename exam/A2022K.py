#!/usr/bin/python3
# coding=utf-8
import random

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler: et sett med håndlagde instanser
# og muligheten til å generere tilfeldige instanser. Du kan styre
# testmengden med flaggene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 20
# Lavest mulig antall nyhetssaker i generert instans.
articles_lower = 0
# Høyest mulig antall nyhetssaker i generert instans.
articles_upper = 15
# Lavest mulig publiseringstid (timer).
time_lower = 0
# Høyest mulig publiseringstid (timer).
time_upper = 72
# Maksimalt k som genereres (timer).
k_upper = 12
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 1


def min_heapify(A, n, i):
    l = 2 * i + 1
    r = 2 * i + 2
    m = i
    if l < n and A[l] < A[m]:
        m = l
    if r < n and A[r] < A[m]:
        m = r
    if m != i:
        A[i], A[m] = A[m], A[i]
        min_heapify(A, n, m)


def build_min_heap(A, n):
    for i in range(n // 2 - 1, -1, -1):
        min_heapify(A, n, i)


def extract_min(A, n):
    if n <= 0:
        raise IndexError("extract_min called on empty heap")
    if n == 1:
        return A.pop()
    A[0], A[n - 1] = A[n - 1], A[0]
    min_heapify(A, n - 1, 0)
    return A.pop()


def solve(articles):
    """
    Returner det minimale antallet e-poster som trengs for å dekke alle
    nyhetssakene slik at hver sak er med i en e-post senest på sitt egen
    sluttidspunkt.

    Args:
        articles: Liste av (publiseringstid, deadline)-tupler (absolutt sluttid).
                  En e-post kan sendes når som helst, men alle sakene som
                  samles i e-posten må ha deadline ≥ sendetid.

    Returns:
        Et heltall som er det minimale antallet e-poster. Hvis du i tillegg
        ønsker å returnere selve utsendelsestidspunktene kan du returnere
        en tuple/list på formen (antall, [tid_1, tid_2, ...]). Testene
        vil i så fall sjekke første element.

    Viktig:
        Implementasjonen skal du fylle inn selv. Test-harnessen under
        bruker en (ineffektiv) referanseløsning for å sjekke svaret ditt.
    """
    build_min_heap(articles, len(articles))
    count = 0
    mails = []
    current_mail = []
    current_end = 1e9
    while len(articles) > 0:
        publish, deadline = extract_min(articles, len(articles))
        if publish > current_end:
            mails.append(current_mail)
            current_mail = [(publish, deadline)]
            current_end = deadline
            count += 1
        else:
            current_mail.append((publish, deadline))
            current_end = min(current_end, deadline)
    if len(current_mail) > 0:
        mails.append(current_mail)
        count += 1
    return count, mails


# =====================================================================
# Referanseløsning (brute force) for små instanser
# =====================================================================


def _reference_min_emails(articles):
    """Eksponentiell DP som gir fasit for små test-instanser (liste + dict)."""
    items = sorted(articles, key=lambda x: x[0])  # sort by publish time
    times = [t for t, _ in items]
    deadlines = [d for _, d in items]
    n = len(times)

    memo = {}

    def dp(i):
        if i in memo:
            return memo[i]
        if i >= n:
            return 0
        best = n  # øvre grense
        current_end = deadlines[i]
        j = i
        while j < n and times[j] <= current_end:
            current_end = min(current_end, deadlines[j])
            j += 1
            best = min(best, 1 + dp(j))
        memo[i] = best
        return best

    return dp(0)


# =====================================================================
# Testhjelpere
# =====================================================================


def _extract_count(student_answer):
    """Aksepterer både int og (int, liste)-returverdier."""
    if isinstance(student_answer, tuple) or isinstance(student_answer, list):
        if not student_answer:
            return None
        student_answer = student_answer[0]
    return student_answer


def get_feedback(student_answer, expected_answer, articles):
    if not isinstance(student_answer, (int, tuple, list)):
        return f"Du returnerte ikke et heltall (eller (heltall, plan)), men {type(student_answer).__name__}"

    count = _extract_count(student_answer)
    if not isinstance(count, int):
        return f"Første element må være et heltall, men var {type(count).__name__}"

    if count != expected_answer:
        return (
            f"Returnerte {count} e-poster, men optimalt er {expected_answer} "
            f"for saker {sorted(articles, key=lambda x: x[0])}"
        )

    return None


def format_instance(articles):
    items = sorted(articles, key=lambda x: x[0])
    return f"Saker (tid, deadline): {items}"


# =====================================================================
# Håndlagde tester
# =====================================================================


tests = [
    # articles (publish, deadline), expected, description
    ([], 0, "Ingen nyhetssaker"),
    ([(3, 5)], 1, "En nyhetssak trenger alltid én e-post"),
    ([(0, 2), (1, 3), (2, 4)], 1, "Alle innenfor overlappende vinduer"),
    ([(0, 1), (3, 4), (6, 7)], 3, "Hver sak tvinger egen utsendelse"),
    ([(0, 2), (1, 3), (4, 6), (5, 7), (9, 11)], 3, "Flere klynger"),
    ([(5, 8), (0, 3), (7, 10), (10, 13)], 3, "Usortert input håndteres"),
    ([(0, 2), (3, 5), (3, 6), (3, 7), (6, 8)], 3, "Duplikate tidspunkter"),
    (
        [(0, 3), (1, 4), (5, 8), (6, 9), (7, 10), (11, 14)],
        3,
        "Tette grupper med overlapp",
    ),
    (
        [(1, 4), (2, 5), (8, 12), (9, 13), (15, 19), (16, 20), (22, 26)],
        4,
        "Flere naturlige batcher",
    ),
    (
        [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11)],
        6,
        "Stramme vinduer gir mange utsendelser",
    ),
]


# =====================================================================
# Tilfeldige tester
# =====================================================================


def generate_random_test():
    """Genererer en tilfeldig instans med fasit fra referanseløsningen."""
    if seed != 0:
        random.seed(seed)

    n = random.randint(articles_lower, articles_upper)
    items = []
    for _ in range(n):
        t = random.randint(time_lower, time_upper)
        slack = random.randint(1, k_upper)
        items.append((t, t + slack))
    expected = _reference_min_emails(items)
    return items, expected, f"Tilfeldig instans (n={n})"


# =====================================================================
# Kjør testene
# =====================================================================


def _run_tests():
    failed = False
    all_tests = list(tests)

    if generate_random_tests:
        for _ in range(random_tests):
            all_tests.append(generate_random_test())

    for i, (articles, expected_answer, description) in enumerate(all_tests, 1):
        try:
            student_answer = solve(list(articles))  # kopi for sikkerhet
        except NotImplementedError:
            print("Du må implementere solve() før du kan kjøre testene.")
            return
        except Exception as e:
            print(f"Test {i} feilet med unntak: {e}")
            failed = True
            continue

        response = get_feedback(student_answer, expected_answer, articles)

        if response is not None:
            if failed:
                print("-" * 70)
            failed = True
            print(
                f"""
Test {i} feilet: {description}
{format_instance(articles)}

Ditt svar: {student_answer}
Forventet svar: {expected_answer}
Feilmelding: {response}
"""
            )

    if not failed:
        print(f"Koden fungerte for alle {len(all_tests)} testene! ✓")


if __name__ == "__main__":
    _run_tests()
