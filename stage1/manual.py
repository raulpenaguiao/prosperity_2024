
TOT = 0
for a in range(900, 1001):
    TOT += a-900



def f(x):
    if x < 900 or x > 1000:
        return 0
    return (x-900)/TOT
F = [0 for i in range(1001)]

for i in range(1, 1001):
    F[i] = F[i-1] + f(i)

def E(a, b):
    return F[a]*(b - a) + F[b]* (1000 - b)

currMax = 0
invMax = [900, 900]
for a in range(900, 1001):
    for b in range(a, 1001):
        e = E(a, b)
        if e > currMax:
            currMax = e
            invMax = [a, b]

print(invMax)
print(currMax)