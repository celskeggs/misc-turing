import load, sys
states, symbols, default, table, desc = load.machine

state = 0
tape = []
head = 0
step = 0
def process(sym):
	global state, head, step
	tape.append(sym)
	while head < len(tape):
		if state == states:
			return True
		key = (state, tape[head])
		assert key in table, "erroneous state/symbol combination: %d %d" % key
		state, nsym, move = table[key]
		tape[head] = nsym
		head += move
		assert head >= 0, "tape underflow"
		step += 1
		if step % 1000000 == 0:
			print("at", step)
	return False

for line in sys.stdin:
	for symbol in line.strip("\n"):
		assert symbol in desc, "invalid symbol: %s" % symbol
		sym = desc.index(symbol)
		done = process(sym)
		if done:
			break
	if done:
		break
while not done:
	done = process(default)
print("after", step, "steps:", "".join((desc[x] if x < len(desc) else "{%d}" % x) for x in tape))
