import pulp


def find_k_paths(nodes, edges, k, s, t):
    # Definer problemet
    model = pulp.LpProblem("KPaths", pulp.LpMinimize)

    # Skriv din kode her
    k_paths = pulp.LpVariable("k_paths", lowBound=0, cat="Integer")
    total_weight = pulp.LpVariable("total_weight", lowBound=0, cat="Continuous")

    model += k_paths == k
    model += total_weight >= k_paths

    for edge in edges:
        model += total_weight >= edge[2]

    # Løs lineærprogrammet
    status = model.solve()

    # Sjekk om vi har funnet en løsning
    # Status er enten 'Optimal', 'Infeasible', 'Unbounded' eller 'Undefined'
    status = pulp.LpStatus[model.status]
    if status != "Optimal":
        return None
    else:
        # Hent ut målverdien
        objective_value = pulp.value(model.objective)
        return objective_value
