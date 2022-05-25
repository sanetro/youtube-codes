def nwd_for_3_args(a, b, c):
	if a == b and a == c: return a
	if a > b: return nwd_for_3_args(a - b, b, c)
	if a > c: return nwd_for_3_args(a - c, b, c)
	if b > a: return nwd_for_3_args(a, b - a, c)
	if b > c: return nwd_for_3_args(a, b - c, c)
	if c > a: return nwd_for_3_args(a, b, c - a)
	if c > b: return nwd_for_3_args(a, b, c - b)
	return print("Error") # Opcjonalne

def nwd(a, b):
	while a != b:
		if a > b:
			a -= b
		else: 
			b -= a 
	return a

def nww(a, b):
	return (a * b) / nwd(a, b)

def nww_for_3_args(a, b, c):
	return nww(a, nww(b, c))

no = [6, 3, 9]
print( "\n", no[0], no[1], no[2],
	   "nwd (3):", nwd_for_3_args(no[0], no[1], no[2]),
	   "\nnww (3):", nww_for_3_args(no[0], no[1], no[2]))

no = [12, 330, 100]
print( "\n", no[0], no[1], no[2],
	   "nwd (3):", nwd_for_3_args(no[0], no[1], no[2]),
	   "\nnww (3):", nww_for_3_args(no[0], no[1], no[2]))

no = [20, 30, 25]
print( "\n", no[0], no[1], no[2],
	   "nwd (3):", nwd_for_3_args(no[0], no[1], no[2]),
	   "\nnww (3):", nww_for_3_args(no[0], no[1], no[2]))
