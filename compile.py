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
for state in range(0, states):
	print("s%d:" % state)
	for symbol, ostate, osymbol, omove in get_for_state(state):
		print("\tcmp [esi], byte", symbol)
		elab = gensym()
		print("\tjne", elab)
		if osymbol != symbol:
			print("\tmov [esi], byte", osymbol)
		assert omove in (-1,0,1)
		if omove == 1:
			print("\tinc esi")
			print("\tcmp esi, ebx")
			print("\tjl s%d" % ostate)
			print("\tcall extend")
		elif omove == -1:
			print("\tdec esi")
			print("\tcmp esi, edi")
			print("\tjge s%d" % ostate)
			print("\tcall extend")
		print("\tjmp s%d" % ostate)
		print("%s:" % elab)
	print("xor eax, eax")
	print("mov al, byte [esi]")
	print("mov esi, eax")
	print("add esi, %d" % (state << 8)) # error
	print("jmp done")
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
