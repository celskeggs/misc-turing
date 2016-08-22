import load, sys
states, symbols, default, table, desc = load.machine

def get_for_state(state):
	out = []
	for line in table:
		if line[0] == state:
			out.append((line[1],) + table[line])
	return out

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
print("\tmov eax, t0")
print("loop:")
print("\tmov cl, [esi]")
print("\tmov ecx, [eax+8*cl+4]")
print("\tmov [esi], cl")
print("\tadd esi, ch")
print("\tmov eax, [eax+8*ecx]")
print("\tcmp eax, 1")
print("\tjg loop")
print("\t
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
