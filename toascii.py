import load, save
states, symbols, default, table, desc = load.machine
assert symbols <= 256, "too many symbols for asciification"

sym_to_ascii = [None] * symbols
ascii_to_sym = [None] * max(ord(' ') + symbols, max(map(ord,desc)) + 1)

free_sym = None
for i in range(ord(' '), 126):
	if chr(i) not in desc:
		free_sym = chr(i)
if free_sym == None:
	assert '\t' not in desc
	free_sym = '\t'

for i, d in enumerate(desc):
	od = ord(d)
	sym_to_ascii[i] = od
	assert ascii_to_sym[od] == None
	ascii_to_sym[od] = i

for i in range(symbols):
	if sym_to_ascii[i] == None:
		idx = ascii_to_sym.index(None, ord(' '))
		sym_to_ascii[i] = idx
		ascii_to_sym[idx] = i

ntable = {}

for line in table.items():
	key, value = line
	state, symbol = key
	ostate, osymbol, omove = value
	symbol = sym_to_ascii[symbol]
	osymbol = sym_to_ascii[osymbol]
	ntable[(state, symbol)] = (ostate, osymbol, omove)

save.save_machine(states, len(ascii_to_sym), sym_to_ascii[default], ntable, "".join((free_sym if x < 32 else chr(x)) for x in range(len(ascii_to_sym))))
