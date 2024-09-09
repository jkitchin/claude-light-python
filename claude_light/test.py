from claude_light import GreenMachine1

gm = GreenMachine1()

print([gm() for i in range(5)])
print([gm(i / 10) for i in range(11)])
