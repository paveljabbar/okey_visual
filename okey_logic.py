
from collections import defaultdict

def parse_card(card):
    if len(card) != 2:
        return None
    value, color = card[0], card[1]
    if not value.isdigit() or color not in ['r', 'y', 'b']:
        return None
    val = int(value)
    if 1 <= val <= 8:
        return val, color
    return None

def find_combinations(cards):
    parsed = [parse_card(c) for c in cards if parse_card(c)]
    by_color = defaultdict(list)
    for val, col in parsed:
        by_color[col].append(val)

    valid_sets = []
    for col in by_color:
        vals = sorted(set(by_color[col]))
        for i in range(len(vals) - 2):
            if vals[i+1] == vals[i]+1 and vals[i+2] == vals[i]+2:
                valid_sets.append([(vals[i], col), (vals[i+1], col), (vals[i+2], col)])
    return valid_sets

def recommend_discard(cards):
    parsed = [parse_card(c) for c in cards if parse_card(c)]
    if len(parsed) <= 3:
        return None
    freq = defaultdict(int)
    for val, col in parsed:
        freq[(val, col)] += 1
    # Einfacher Heuristik: Karte, die zu keiner möglichen Folge beiträgt
    for card in cards:
        tmp = cards.copy()
        tmp.remove(card)
        if find_combinations(tmp):
            continue
        return card
    return None
