#!/usr/bin/python3
import random
import string

# De lokale testene består av to deler: et sett med håndlagde instanser
# og muligheten til å generere tilfeldige instanser. Du kan styre
# testmengden med flaggene under.
generate_random_tests = True
random_tests = 20
# Maksimal lengde på strengene som genereres i tilfeldige tester.
max_length = 16
# Alfabet som brukes i tilfeldige tester.
alphabet = string.ascii_uppercase[:6]  # A–F holder testene kompakte
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, så lenge parameterne over ikke endres.
seed = 1


def solve(a, b):
    """
    Returner lengden på den lengste felles delsekvensen mellom a og b.

    Du kan valgfritt også returnere selve delsekvensen, f.eks. som
    `(lengde, subsekvens)` eller `(lengde, [tegn ...])`. Testene under
    aksepterer både et heltall alene og et par med (lengde, subsekvens).

    Args:
        a: Første sekvens (typisk en streng).
        b: Andre sekvens (typisk en streng).

    Returns:
        Enten:
            - Et heltall som er lengden på LCS
            - En tuple/list der første element er lengden, og andre
              element (valgfritt) er en gyldig felles delsekvens
    """
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            m = max(dp[i][j - 1], dp[i - 1][j])
            if a[i - 1] == b[j - 1]:
                m = max(m, dp[i - 1][j - 1] + 1)
            dp[i][j] = m
    return dp[len(a)][len(b)]


# =====================================================================
# Referanseløsning (DP) for å generere fasit
# =====================================================================


def _reference_lcs(a, b):
    """Returner (lengde, en mulig LCS) ved bruk av klassisk DP."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

    # Rekonstruer en faktisk subsekvens (for validering)
    i = j = 0
    subseq = []
    while i < n and j < m:
        if a[i] == b[j]:
            subseq.append(a[i])
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1
        else:
            j += 1

    return dp[0][0], subseq if isinstance(a, (list, tuple)) else "".join(subseq)


# =====================================================================
# Testhjelpere
# =====================================================================


def _is_subsequence(candidate, text):
    """Sjekk om candidate er en subsekvens av text."""
    try:
        cand = list(candidate)
    except TypeError:
        return False

    try:
        haystack = list(text)
    except TypeError:
        haystack = []

    i = 0
    for ch in haystack:
        if i < len(cand) and ch == cand[i]:
            i += 1
    return i == len(cand)


def _extract_answer(student_answer):
    """
    Aksepterer flere returformater:
    - int (kun lengde)
    - str / liste / tuple (tolkes som subsekvens, lengde = len(subsekvens))
    - (lengde, subsekvens)
    """
    if isinstance(student_answer, int):
        return student_answer, None, None

    if isinstance(student_answer, str):
        return len(student_answer), student_answer, None

    if isinstance(student_answer, (list, tuple)):
        if not student_answer:
            return None, None, "Tom liste/tuple er ikke gyldig svar."
        first = student_answer[0]
        if isinstance(first, int):
            length = first
            subseq = student_answer[1] if len(student_answer) > 1 else None
            return length, subseq, None
        try:
            length = len(first)
        except Exception:
            return None, None, "Klarte ikke å tolke subsekvensen din."
        return length, first, None

    return None, None, f"Ugyldig returtype {type(student_answer).__name__}"


def get_feedback(student_answer, expected_length, a, b, reference_subsequence):
    length, subseq, parse_error = _extract_answer(student_answer)
    if parse_error:
        return parse_error

    if not isinstance(length, int):
        return f"Første element må være heltall, men var {type(length).__name__}"

    if length != expected_length:
        return f"Returnerte lengde {length}, men optimal lengde er {expected_length}"

    if subseq is not None:
        try:
            subseq_len = len(subseq)
        except Exception:
            return "Subsekvensen din kan ikke lengde-beregnes."

        if subseq_len != expected_length:
            return (
                f"Subsekvensen har lengde {subseq_len}, men forventet {expected_length}"
            )
        if not _is_subsequence(subseq, a) or not _is_subsequence(subseq, b):
            return (
                "Subsekvensen du returnerte finnes ikke i begge strengene. "
                f"Eksempel på gyldig LCS: {reference_subsequence}"
            )

    return None


def format_instance(a, b):
    return f"a: {a!r}\nb: {b!r}"


# =====================================================================
# Håndlagde tester
# =====================================================================


tests = [
    ("", "", 0, "To tomme strenger"),
    ("ABC", "", 0, "Én tom streng"),
    ("ABCDEF", "ABC", 3, "Prefiks matcher"),
    ("ABC", "DEF", 0, "Ingen felles bokstaver"),
    ("AGGTAB", "GXTXAYB", 4, "Klassisk LCS-eksempel (AGTB)"),
    ("AAAA", "AA", 2, "Duplikate tegn"),
    ("XMJYAUZ", "MZJAWXU", 4, "Kryssende matchmønstre"),
    ("ABCBDAB", "BDCAB", 4, "Overlapper på flere måter"),
    ("BANANA", "ATANA", 4, "Flere like beste valg"),
]


# =====================================================================
# Tilfeldige tester
# =====================================================================


def generate_random_test():
    """Generer en tilfeldig testinstans med fasit fra referanseløsningen."""
    if seed != 0:
        random.seed(seed)

    n = random.randint(0, max_length)
    m = random.randint(0, max_length)
    a = "".join(random.choice(alphabet) for _ in range(n))
    b = "".join(random.choice(alphabet) for _ in range(m))
    expected_length, reference_subsequence = _reference_lcs(a, b)
    return (
        a,
        b,
        expected_length,
        reference_subsequence,
        f"Tilfeldig test (n={n}, m={m})",
    )


# =====================================================================
# Kjør testene
# =====================================================================


def _run_tests():
    failed = False
    all_tests = []

    # Legg til håndlagde tester
    for a, b, expected, description in tests:
        ref_len, ref_subseq = _reference_lcs(a, b)
        assert ref_len == expected, f"Test '{description}' har feil fasit."
        all_tests.append((a, b, expected, ref_subseq, description))

    # Legg til tilfeldige tester
    if generate_random_tests:
        for _ in range(random_tests):
            all_tests.append(generate_random_test())

    for i, (a, b, expected, ref_subseq, description) in enumerate(all_tests, 1):
        try:
            student_answer = solve(a, b)
        except NotImplementedError:
            print("Du må implementere solve() før du kan kjøre testene.")
            return
        except Exception as e:
            print(f"Test {i} feilet med unntak: {e}")
            failed = True
            continue

        response = get_feedback(student_answer, expected, a, b, ref_subseq)
        if response is not None:
            if failed:
                print("-" * 70)
            failed = True
            print(
                f"""
Test {i} feilet: {description}
{format_instance(a, b)}

Ditt svar: {student_answer}
Forventet lengde: {expected}
Fasit-eksempel: {ref_subseq!r}
Feilmelding: {response}
"""
            )

    if not failed:
        print(f"Koden fungerte for alle {len(all_tests)} testene! ✓")


if __name__ == "__main__":
    _run_tests()
