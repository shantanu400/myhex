from heapq import heappop, heappush
from collections import OrderedDict
 
def positions(i, j, n):
    positionArr = []
    if i is not 0:
        positionArr.append([i - 1, j])
        if j is not n - 1:
            positionArr.append([i - 1, j + 1])
    if i is not n - 1:
        positionArr.append([i + 1, j])
        if j is not 0:
            positionArr.append([i + 1, j - 1])
    if j is not 0:
        positionArr.append([i, j - 1])
    if j is not n - 1:
        positionArr.append([i, j + 1])
    return positionArr
 
 
def score(val, player):
    if val == '0':
        return 1
    elif val == player:
        return 0
 
 
def h(a, player):
    transpose = [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
    if player == '2':
        a = transpose
    parents = [(j, 0) for j in range(len(a))]
    visited = {}
    priorityQ = []
    n = len(a)
    for pair in parents:
        val = score(a[pair[0]][pair[1]], player)
        if a[pair[0]][pair[1]] == '0':
            visited[str(pair[0]) + str(pair[1])] = 1
            heappush(priorityQ, (1, str(pair[0]) + str(pair[1])))
        elif a[pair[0]][pair[1]] == player:
            visited[str(pair[0]) + str(pair[1])] = 0
            heappush(priorityQ, (0, str(pair[0]) + str(pair[1])))
 
    while priorityQ:
        parent = heappop(priorityQ)
        parentPos = parent[1]
        parentVal = parent[0]
        if parentPos[1] == str(n - 1):
            return parentVal
        children = positions(int(parentPos[0]), int(parentPos[1]), n)
        for child in children:
            temp = score(a[child[0]][child[1]], player)
            if temp is not None:
                val = parentVal + temp
                if str(child[0]) + str(child[1]) not in visited.keys() or visited[str(child[0]) + str(child[1])] > val:
                    val = parentVal + score(a[child[0]][child[1]], player)
                    visited[str(child[0]) + str(child[1])] = val
                    heappush(priorityQ, (val, str(child[0]) + str(child[1])))
 
 
 
def vacantPlaces(a):
    nextLIst = []
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] is '0':
                pairs = (chr(65 + i), j)
                nextLIst.append(pairs)
    return nextLIst
 
 
def check(a, x, player, visited):
    if a[x[0]][x[1]] == str(player):
        pathList = positions(x[0], x[1], len(a))
        for y in pathList:
            if str(y) not in visited.keys():
                if a[y[0]][y[1]] == str(player):
                    visited[str(y)] = True
                    if y[1] == len(a) - 1:
                        return 302
                    val = check(a, y, player, visited)
                    if val == 302:
                        return 302
    return 404
 
 
def gameStatus(a, player):
    transpose = [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]
    if player == '2':
        a = transpose
    firstList = [(j, 0) for j in range(len(a))]
    for i in firstList:
        visited = {str([i[0], i[1]]): True}
        result = check(a, i, player, visited)
        if result == 302:
            return True
    return False
 
 
def minimax(a, d, player1, player2, start):
    h1 = h(a, player2)
    if h1 == 0:
        if player2 == start:
            return 1000, '99'
        else:
            return -1000, '99'
    if d <= 0:
        h2 = h(a, player1)
        return h1 - h2, '99'
 
    else:
        seats = vacantPlaces(a)
        valList = OrderedDict()
        for pair in seats:
            x = ord(pair[0]) - 65
            y = int(pair[1])
            newA = list(map(list, a))
            newA[x][y] = player1
            val, kkl = minimax(newA, d - 1, player2, player1, start)
            valList[str(x) + str(y)] = val
        if player1 is start:
            pos = sorted(valList.items(), key=lambda bla: bla[1], reverse=True)[0][0]
            maxVal = sorted(valList.items(), key=lambda bla: bla[1], reverse=True)[0][1]
            return maxVal, pos
        else:
            pos = sorted(valList.items(), key=lambda bla: bla[1])[0][0]
            minVal = sorted(valList.items(), key=lambda bla: bla[1])[0][1]
            return minVal, pos
 
def start(a, d):
    player1 = '1'
    player2 = '2'
    steps = OrderedDict()
    while True:
        if gameStatus(a, '1'):
            printing(steps)
            print('player 1 wins')
            break
        elif gameStatus(a, '2'):
            printing(steps)
            print('player 2 wins')
            break
        else:
            val, pos = minimax(a, d, player1, player2, player1)
            x = int(pos[0])
            y = int(pos[1])
            a[x][y] = str(player1)
            pos1 = chr(int(pos[0]) + 65)
            pos2 = pos[1]
            pos = pos1 + pos2
            steps[pos] = player1
        player1, player2 = player2, player1
 
 
def printing(steps):
    for i in steps:
        print(str(steps[i]) + ' ' + str(i))
 
 
def main():
    t = int(input())
    for _ in range(t):
        n, d = input().split()
        n = int(n)
        d = int(d)
        a = []
        for i in range(n):
            b = [str(j) for j in input().split()]
            a.append(b)
        start(a, d)
 
 
if __name__ == "__main__":
    main()