#!/usr/bin/python3
# coding=utf-8

from collections import deque
from typing import List, Optional, Tuple


def max_flow_highscore(
    source: int, sink: int, n: int, capacities: List[List[int]]
) -> float:
    flows = [[0.0] * n for _ in range(n)]

    while (
        path := find_augmenting_path(source, sink, n, flows, capacities)
    ) is not None:
        bottleneck_capacity = max_path_flow(path, flows, capacities)
        send_flow(path, bottleneck_capacity, flows)

    return sum(flows[source])


# Hjelpefunksjoner du kan bruke
def find_augmenting_path(
    source: int,
    sink: int,
    nodes: int,
    flows: List[List[float]],
    capacities: List[List[int]],
) -> Optional[List[int]]:
    """
    Finn en forøkende sti i et flytnett

    :param source: indeksen til kilden i listen med noder.
    :param sink: indeksen til sluknoden i listen med noder.
    :param nodes: antaller noder i nettverket
    :param flows: flyt-matrise, verdien på indeks (i,j) er flyten mellom node i og j
    :param capacities: kapasitets-matrise, verdien på indeks (i,j) er kapasiteten til kanten (i,j).
                        ingen kant tilsvarer kapasitet 0.
    :returns: en foreldre-liste med den flytforøkende stien hvis funnet, ellers None.
    """

    def create_path(source: int, sink: int, parent: List[int]) -> List[int]:
        """Lager stien ved hjelp av foreldrelisten"""
        node = sink
        path = [sink]
        while node != source:
            node = parent[node]
            path.append(node)
        path.reverse()
        return path

    discovered = [False] * nodes
    parent = [0] * nodes
    queue = deque()
    queue.append(source)

    while queue:
        node = queue.popleft()
        if node == sink:
            return create_path(source, sink, parent)

        for neighbour in range(nodes):
            if (
                not discovered[neighbour]
                and flows[node][neighbour] < capacities[node][neighbour]
            ):
                queue.append(neighbour)
                discovered[neighbour] = True
                parent[neighbour] = node
    return None


def max_path_flow(
    path: List[int], flows: List[List[float]], capacities: List[List[int]]
) -> float:
    """
    Finn maksimal flyt som kan sendes gjennom den oppgitte stien
    """
    flow = float("inf")
    for i in range(1, len(path)):
        u, v = path[i - 1], path[i]
        flow = min(flow, capacities[u][v] - flows[u][v])
    return flow


def send_flow(path: List[int], flow: float, flows: List[List[float]]):
    """
    Oppdaterer "flows" ved å sende "flow" flyt gjennom stien "path"
    """
    for i in range(1, len(path)):
        u, v = path[i - 1], path[i]
        flows[u][v] += flow
        flows[v][u] -= flow


tests = [
    (
        0,
        5,
        6,
        [
            [0, 16, 13, 0, 0, 0],
            [0, 0, 0, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0],
        ],
        23,
    ),
    (
        0,
        5,
        6,
        [
            [0, 16, 13, 0, 0, 0],
            [16, 0, 4, 12, 0, 0],
            [13, 4, 0, 9, 14, 0],
            [0, 12, 9, 0, 7, 20],
            [0, 0, 14, 7, 0, 4],
            [0, 0, 0, 20, 4, 0],
        ],
        24,
    ),
    (
        0,
        5,
        6,
        [
            [0, 16, 13, 0, 0, 0],
            [16, 0, 4, 12, 0, 0],
            [13, 4, 0, 7, 14, 0],
            [0, 12, 7, 0, 1, 20],
            [0, 0, 14, 1, 0, 4],
            [0, 0, 0, 20, 4, 0],
        ],
        24,
    ),
    (
        0,
        4,
        5,
        [
            [0, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 0],
        ],
        4,
    ),
]

failed = False

for test_case in tests:
    (
        source,
        sink,
        nodes,
        capacities,
        answer_flow,
    ) = test_case
    student_flow = max_flow_highscore(source, sink, nodes, capacities)
    if student_flow != answer_flow:
        failed = True
        response = "Koden feilet for følgende input: (tasks={:}). ".format(
            test_case[:4]
        ) + "Din flyt: {:}. Riktig maksflyt: {:}".format(student_flow, answer_flow)
        print(response)
        break

if not failed:
    print("Koden fungerte for alle eksempeltestene.")
