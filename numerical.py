import classes as cl
import numpy as np
import sympy as sp

z2 = cl.Word([1],["xy"])
z3 = cl.Word([1],["xxy"])
z4 = cl.Word([1],["xxxy"])
z2z2 = cl.Word([1],["xyxy"])
z2z1 = cl.Word([1],["xyy"])

#Forests of order 4
f1 = cl.forest_from_string("0000")
f2 = cl.forest_from_string("000102")
f3 = cl.forest_from_string("001002")
f4 = cl.forest_from_string("01020102")
f5 = cl.forest_from_string("01021020")
f6 = cl.forest_from_string("00102102")
f7 = cl.forest_from_string("0102102102")
f8 = cl.forest_from_string("010200")
f9 = cl.forest_from_string("001020")

#Forests of order 3
g1 = cl.forest_from_string("000")
g2 = cl.forest_from_string("00102")
g3 = cl.forest_from_string("0102102")
g4 = cl.forest_from_string("01020")

deg3 = [g1,g2,g3,g4]
deg4 = [f1,f2,f4,f5,f6,f7,f8,f9]
deg5 = cl.generate_Fn(5)

def check_if_new_relatiion(relation):
    degree = len(relation.word[0])
    admissible_words = cl.generate_Words(degree)
    #Fill the b vector
    b = np.zeros([len(admissible_words), 1])
    for i in range(len(relation.word)):
        a = admissible_words.index(relation.word[i])
        b[a] = relation.q[i]

    A = np.zeros([len(admissible_words),(degree-2)*(2**(degree-3))])
    current_collumn = 0
    for n in range(1,degree-1):
        deg_n_words = cl.generate_Words(degree-n)
        deg_n_forests = cl.generate_Fn(n)
        for j in range(len(deg_n_forests)):
            for i in range(len(deg_n_words)):
                result = deg_n_forests[j](cl.Word([1],[deg_n_words[i]]))
                result.simplify()
                for k in range(len(result.word)):
                    a = admissible_words.index(result.word[k])
                    A[a, current_collumn] = result.q[k]

                current_collumn += 1
    print(len(sp.Matrix(A.astype(int)).rref()[1]))
    print(len(sp.Matrix(np.concatenate((A, b), axis=1).astype(int)).rref()[1]))
    #print(A.col_insert(-1,b).rref())
    #beta = (A.transpose() * A).inv() * A.transpose() * b
    #print(beta)
    #print((b - A * beta).norm())

check_if_new_relatiion(z3.tau().harmonic_shuffle(z3).tau() - z3.harmonic_shuffle(z3.tau()))
def other_function(n,k):
    admissible_words = cl.generate_Words_Hy(n)
    current_deg = cl.generate_Fn(k)

    input_words = cl.generate_Words_Hy(n-k)
    b_word = z3.tau().harmonic_shuffle(z4).tau() - z3.harmonic_shuffle(z4.tau())
    b_word.simplify()
    for word in input_words:
        arr = np.zeros([len(admissible_words),len(current_deg)])
        b = np.zeros([len(admissible_words),1])

        for i in range(len(b_word.word)):
            a = admissible_words.index(b_word.word[i])
            b[a] = b_word.q[i]


        for j in range(len(current_deg)):
            result = current_deg[j](cl.Word([1],[word]))
            result.simplify()
            for i in range(len(result.word)):
                a = admissible_words.index(result.word[i])
                arr[a,j] = result.q[i]


        a_matrix = sp.Matrix(arr.astype(int))
        b_vec = sp.Matrix(b.astype(int))
        beta = (a_matrix.transpose()*a_matrix).inv()*a_matrix.transpose()*b_vec
        if (b_vec-a_matrix*beta).norm() == 0:
            print(word,":\t",beta)

#other_function(7,1)
#print(a_matrix.pinv_solve(b_vec))
#print(a_matrix.LDLsolve(b_vec))

#print(solve(a_matrix,b_vec))
#print(a_matrix.solve_least_squares(b_vec))
"""
print ("########################################")
arr = np.concatenate((arr,b),axis=1).astype(int)

print(arr)
arr = sp.Matrix(arr)

print(arr)
print(arr.rref())

"""
"""
#Forests of order 2
t1 = cl.forest_from_string("00")
t2 = cl.forest_from_string("0102")

deg2 = [t1,t2]
words5 = cl.generate_Words(5)

arr = np.zeros([len(words5),len(words5)])
b = np.zeros([len(words5),1])

b_word = z3.delta(2)
b_word.simplify()
for i in range(len(b_word.word)):
    a = words5.index(b_word.word[i])
    b[a] = b_word.q[i]


for j in range(len(deg2)):
    result = deg2[j](z3)
    result.simplify()
    for i in range(len(result.word)):
        a = words5.index(result.word[i])
        arr[a,j] = result.q[i]
print(np.linalg.lstsq(arr,b))
arr = np.concatenate((arr,b),axis=1).astype(int)

arr = sp.Matrix(arr)

print(arr)
print(arr.rref())
"""