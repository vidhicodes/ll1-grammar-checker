from first_follow import compute_first_follow

def construct_ll1_table():
    first, follow = compute_first_follow()
    table = {}
    
    for nt, rules in first.items():
        for rule in rules:
            first_set = set()
            rule_symbols = rule.split()
            for s in rule_symbols:
                first_set |= first[s]
                if "ε" not in first[s]:
                    break
            else:
                first_set |= follow[nt]

            for terminal in first_set - {"ε"}:
                table[(nt, terminal)] = rule
            if "ε" in first_set:
                for terminal in follow[nt]:
                    table[(nt, terminal)] = rule

    return table
