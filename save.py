def save_machine(states, symbols, default, table, desc):
	assert type(states) == int and type(symbols) == int
	assert type(default) == int and default >= 0 and default < symbols
	assert type(table) == dict
	assert type(desc) == str
	print(states, symbols, default)
	assert "\n" not in desc
	print(desc)
	for key, value in table.items():
		state, symbol = key
		ostate, osymbol, omove = value
		assert type(state) == int and state >= 0 and state < states
		assert type(ostate) == int and ostate >= 0 and ostate <= states # last state is termination state
		assert type(symbol) == int and state >= 0 and state < symbols
		assert type(osymbol) == int and ostate >= 0 and ostate < symbols
		assert omove in (-1, 0, 1)
		print(state, symbol, ostate, osymbol, omove)
