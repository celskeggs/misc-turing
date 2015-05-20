#!/usr/bin/env python3
assert print, "Expects python 3"
import sys
if len(sys.argv) != 2:
	print("Usage: %s <TURING MACHINE>" % sys.argv[0])
	sys.exit(1)
with open(sys.argv[1], "r") as machine:
	machine = filter(lambda line: line[0] != "#", machine)
	states, symbols, default = next(machine).split()
	description = next(machine).strip("\n")
	states, symbols, default = int(states), int(symbols), int(default)
	assert symbols >= 0, "must be at least one symbol!"
	assert len(description) <= symbols
	table = {}
	for line in machine:
		state, symbol, ostate, osymbol, omove = map(int, line.split())
		assert state >= 0 and state < states, "bad state %d" % state
		# ostate == states means end
		assert ostate >= 0 and ostate <= states, "bad ostate %d" % ostate
		
		assert symbol >= 0 and symbol < symbols, "bad symbol %d" % symbol
		assert osymbol >= 0 and osymbol < symbols, "bad osymbol %d" % osymbol
		
		assert omove in (-1,0,1), "invalid movement: %d" % omove
		
		assert (state, symbol) not in table, "duplicate table entry: %s, %s" % (state, symbol)
		table[(state, symbol)] = (ostate, osymbol, omove)

machine = (states, symbols, default, table, description)
