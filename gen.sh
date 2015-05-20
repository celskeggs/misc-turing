import random, sys
with open("test4.txt", "w") as f:
	for i in range(int(sys.argv[1] if sys.argv[1:] else input("count: "))):
		f.write(random.choice("01"))
	f.write("#\n")
