
def single_bit_or(a, b):
	'''
	a: bit único, 1 ou 0
    b: bit único, 1 ou 0
	'''

	if a == 1 or b == 1:
		return 1
	else:
		return 0

def single_bit_not(a):
	'''
um: bit único, 1 ou 0
	'''

	if a == 1:
		return 0
	elif a == 0:
		return 1

def single_bit_and(a, b):
	'''
	
um: bit único, 1 ou 0
b: bit único, 1 ou 0
	'''

	if a == 1 and b == 1:
		return 1
	else:
		return 0


print(single_bit_and(1, 1))
print(single_bit_or(1, 1))
print(single_bit_not(1))


def single_bit_mux(a, b, sel):

	if sel == 0:
		return a
	else:
		return b

def single_bit_xor(a, b):

	if a == b:
		return 0
	else:
		return 1

def sixteen_bit_not(a8):
	'''
	a8: número binário, formatado como lista [1, 1, 0, 0, 1, 1, 1, 1]

Flip bits de todas as entradas
	'''
	return [0 if bit == 1 else 1 for bit in a8]

def sixteen_bit_and(a8, b8):
	'''
	
a8: número binário, formatado como lista [1, 1, 0, 0, 1, 1, 1, 1]
b8: número binário, formatado como lista [1, 1, 0, 0, 1, 0, 1, 1]

Binário E bits de todas as entradas
	'''
	out = []
	for i, b in enumerate(a8):
		out.append(single_bit_and(a8[i], b8[i]))

	return out


#adição binaria
# 01
#+
# 11
# ____
# 100
#  


def sixteen_bit_mux(a8, b8, sel):
	'''

a8: número binário, formatado como lista [1, 1, 0, 0, 1, 1, 1, 1]
b8: número binário, formatado como lista [1, 1, 0, 0, 1, 1, 1, 1]

Se o bit do seletor (sel) == 0, retorne a8
Mais retorno b8
	'''

	if sel == 0:
		return a8
	else:
		return b8

def half_adder(a, b):
	'''
	
Saídas:
soma: bit certo de a + b
transportar: bit esquerdo de a + b
	'''
	sum = single_bit_xor(a, b)
	carry = single_bit_and(a, b)

	return sum, carry

def full_adder(a, b, right_carry):
	'''
	
Saídas:
soma: certo bit de a + b + right_carry
carry: bit da esquerda de a + b + right_carry
	'''
	sum = single_bit_xor(a, b)
	carry = single_bit_and(a, b)

	return sum, carry

	right_sum, carry1 = half_adder(a, b)
	sum, carry2 = half_adder(right_sum, right_carry)
	carry = single_bit_or(carry1, carry2)
	
	return sum, carry



#somador 


def sixteen_bit_adder(a8, b8):
	'''
	Saídas:
    soma: uma soma de 8 bits de dois números

    Descarte o bit de transporte mais significativo.
	'''
	sum = [ 0, 0, 0, 0, 0, 0, 0, 0]

	sum[0], carry0 = half_adder(a8[0], b8[0])
	sum[1], carry1 = full_adder(a8[1], b8[1], carry0)
	sum[2], carry2 = full_adder(a8[2], b8[2], carry1)
	sum[3], carry3 = full_adder(a8[3], b8[3], carry2)
	sum[4], carry4 = full_adder(a8[4], b8[4], carry3)
	sum[5], carry5 = full_adder(a8[5], b8[5], carry4)
	sum[6], carry6 = full_adder(a8[6], b8[6], carry5)
	sum[7], carry7 = full_adder(a8[7], b8[7], carry6)
	

	return sum

def alu(x8, y8, zx, nx, zy, ny, f, no):
	'''
	Inputs:

	a8, b8,  // 8bit entrada       
	zx, // zero a entrada
	nx, // negar a entrada
	zy, // zerar a entrada y
	ny, // negar a entrada y
	f,  // compute out = x + y (if 1) or x & y (if 0)
	no; // negar a saida 
	'''
	all_zeroes = [0,0,0,0,0,0,0,0]

	### dertemina x para usar ele 

	# zero o x se zx for definido, senão a saída x
	zerox = sixteen_bit_mux(a8=x8, b8=all_zeroes, sel=zx)

	# não o x 
	notx = sixteen_bit_not(x8)

	usex = sixteen_bit_mux(a8=zerox, b8=notx, sel=nx)

	### dertemina o x para usar 

	# zerar o y se zy estiver definido, senão a saída y
	zeroy = sixteen_bit_mux(a8=y8, b8=all_zeroes, sel=zy)

	# não o y 
	noty = sixteen_bit_not(y8)

	usey = sixteen_bit_mux(a8=zeroy, b8=noty, sel=ny)

	### cacular o fs

	addxy = sixteen_bit_adder(a8=usex, b8=usey)
	andxy = sixteen_bit_and(a8=usex, b8=usey)

	posout = sixteen_bit_mux(a8=addxy, b8=addxy, sel=f)
	negout = sixteen_bit_not(posout)

	out8 = sixteen_bit_mux(a8=posout, b8=negout, sel=no)
	ng = out8[7]

	
    ### determina se a saída é zero
    ### out16 == all_zeroes

	c1 = single_bit_or(out8[0], out8[1])
	c2 = single_bit_or(out8[2], out8[3])
	c3 = single_bit_or(out8[4], out8[5])
	c4 = single_bit_or(out8[6], out8[7])


	c5 = single_bit_or(c1, c2)
	c6 = single_bit_or(c3, c4)
	c7 = single_bit_or(c5, c6)
	check = single_bit_or(c6, c7)

	zr = single_bit_not(check)

	return out8, zr, ng

a = [ 0, 0, 0, 0, 0, 1, 0, 0]
b = [ 0, 0, 0, 0, 1, 0, 0, 0]
a.reverse()
b.reverse() 

test_add = sixteen_bit_adder(a, b)
test_add.reverse()
print(test_add)

out, zr, ng = alu(a, b, 0, 0, 0, 0, 1, 0)
out.reverse()
print(out)
print(zr, ng)
print(test_add==out)