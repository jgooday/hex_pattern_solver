import hex_pattern_solver

tmp = open('input_IDs.txt', 'r').readlines()
IDs = [float(x.strip()) for x in tmp]

r = 18.5/2
precision = 0.01

for ID in IDs:
    R = (ID-5)/2

    # solve
    X, Y, d, inclusion_mask, ps = hex_pattern_solver.solve(R, r, precision)
    n = sum(inclusion_mask)
    print(n)