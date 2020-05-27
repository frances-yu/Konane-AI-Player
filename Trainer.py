from Game import Game
from Agent import Agent

SIZE = 10
SMALL_EPOCH = 2
BIG_EPOCH = 10

def adjust(i, weights, adj_factor, pos = True, count = 0):
    if count == SMALL_EPOCH: return weights

    cur = weights.copy()
    new = weights.copy()
    if pos: new[i] += adj_factor
    else:
        new[i] -= adj_factor
        if new[i] < 0: new[i] = 0

    w = Agent("WHITE", False)
    b = Agent("BLACK", True)
    w.set_weights(new)
    b.set_weights(cur)
    g = Game(w, b, SIZE)

    base = []
    if g.winner == 1:
        new_factor = 2 * adj_factor
        base = new
    else:
        new_factor = adj_factor + adj_factor/2
        base = cur

    return adjust(i, base, new_factor, pos, count + 1)

def best_weight(i, baseline, adj):
    pos = adjust(i, baseline, adj)
    neg = adjust(i, baseline, adj, False)

    w = Agent("WHITE", False)
    b = Agent("BLACK", True)
    w.set_weights(pos)
    b.set_weights(neg)
    g = Game(w,b,SIZE)

    if g.winner == 1:
        return pos
    else:
        return neg

def adjust_weights(base, adj):
    bw = base.copy()
    for i in range(0, len(bw)):
        clone = bw.copy()
        bw = best_weight(i, clone, adj)
    #bw = [int(x) for x in bw]
    return bw

def cycle(baseline, adj):
    count = 0
    weights = baseline.copy()
    while count < BIG_EPOCH:
        weights = adjust_weights(weights, adj)
        count += 1
    return weights

def steps(baseline, adj_list):
    bw_list = []
    for step in adj_list:
        bw = cycle(baseline, step)
        bw_list.append(bw)
    return bw_list

def compare(factors):
    weight_list = steps([1,1,1,1], factors)
    white = []
    black = []
    victory_points = []

    for i in range(0, len(weight_list)):
        w = Agent("WHITE", False)
        b = Agent("BLACK", True)
        v = 0
        w.set_weights(weight_list[i])
        b.set_weights(weight_list[i])

        white.append(w)
        black.append(b)
        victory_points.append(v)

    for i in range(0, len(white)):
        for j in range(0, len(black)):
            if i != j:
                g = Game(white[i], black[j], SIZE)
                if g.winner == 1:
                    victory_points[i] += 1
                else:
                    victory_points[j] += 1

    index = -1
    max = -1
    for v in range(0, len(victory_points)):
        if victory_points[v] > max:
            index = v
            max = victory_points[v]

    return weight_list[index]

factors = [0.5,1,2,4]
bw = compare(factors)
print(bw)

# With a Baseline of [1,1,1,1] with learning steps of [0.5, 1, 2, 4], the Artificial Intelligence learns a weighting of [3,1,0,0]
# It only cares about raw piece total and doesn't give preference to side or corner pieces
# It weighs the number of moves available more heavily than the number of pieces available
