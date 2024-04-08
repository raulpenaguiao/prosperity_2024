def dEa(a, b):
    return -3*a*a+2*(b+1800)*a-(1800*b+900*900)

def dEb(a, b):
    return -3*b*b+5600*b+a*a-1800*a+900*900-1_800_000-900*900

print(dEa(951, 978))
print(dEa(952, 978))
print(dEa(953, 978))
print(dEb(952, 977))
print(dEb(952, 978))
print(dEb(952, 979))