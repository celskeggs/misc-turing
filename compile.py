import load, sys
states, symbols, default, table, desc = load.machine

def get_for_state(state):
	out = []
	for line in table:
		if line[0] == state:
			out.append((line[1],) + table[line])
	return out

lastsym = -1
def gensym():
	global lastsym
	lastsym += 1
	return "g%d" % lastsym

print("BITS 32")
print("section .text")
print("global turing_main")
print("extern load")
print("extern release")

print("turing_main:")
print("\tpush ebx")
print("\tpush esi")
print("\tpush edi")
print("\tpush ebp")
count_default = 4096
# esi: head, edi: base, ebx: end
print("\tpush dword", count_default)
print("\tpush dword", count_default)
print("\tpush dword", default)
print("\tpush dword 0") # NULL
print("\tcall load")
print("\tadd esp, 16")
print("\tmov edi, eax")
print("\tmov esi, eax")
print("\tmov ebx, eax")
print("\tadd ebx,", count_default)
print("\tjmp s0")
extend_use, extend_total = 0, 0
for state in range(0, states):
	uses_extended = False
	#uses_extended = True
	for state2 in range(0, states):
		for symbol, ostate, osymbol, omove in get_for_state(state2):
			if omove == 1 and ostate == state:
				uses_extended = True
				break
	extend_use += uses_extended
	extend_total += 1
	if uses_extended:
		print("s%dx:" % state)
		print("\tinc esi")
		print("\tcmp esi, ebx")
		print("\tjl s%d" % state)
		print("\tcall extend")
	print("s%d:" % state)
	print("\tmov al, [esi]")
	later = []
	for symbol, ostate, osymbol, omove in get_for_state(state):
		print("\tcmp al, byte", symbol)
		elab = gensym()
		print("\tje", elab)
		later.append("%s:" % elab)
		if osymbol != symbol:
			later.append("\tmov [esi], byte %s" % osymbol)
		assert omove in (-1,0,1)
		if omove == 1:
			later.append("\tjmp s%dx" % ostate)
		else:
			if omove == -1:
				later.append("\tdec esi")
				# assuming well-formed programs...
				# later.append("\tcmp esi, edi")
				# later.append("\tjl error")
			later.append("\tjmp s%d" % ostate)
	print("\tmovzx esi, al")
	print("\tor esi, %d" % (state << 8)) # error
	print("\tjmp done")
	for k in later:
		print(k)
print("s%d:" % states)
print("\tmov esi, -1")
print("done:")
print("\tpush ebx")
print("\tpush edi")
print("\tcall release")
print("\tadd esp, 8")
print("\tmov eax, esi")
print("\tpop ebp")
print("\tpop edi")
print("\tpop esi")
print("\tpop ebx")
print("\tret")
print()
print("extend:")
print("\tsub esi, edi")
print("\tsub ebx, edi")
print("\tadd ebx,", count_default)
print("\tpush dword", count_default)
print("\tpush ebx")
print("\tpush dword", default)
print("\tpush edi")
print("\tcall load")
print("\tadd esp, 16")
print("\tmov edi, eax")
print("\tadd esi, eax")
print("\tadd ebx, eax")
print("\tret")
print("; out: %d %d" % (extend_use, extend_total))
