import classes as cl
import numpy as np
import sympy as sp

z1 = cl.Word([1],["y"])
z2 = cl.Word([1],["xy"])
z3 = cl.Word([1],["xxy"])
z4 = cl.Word([1],["xxxy"])
z2z2 = cl.Word([1],["xyxy"])
z2z1 = cl.Word([1],["xyy"])

def check_if_new_relatiion(relation):
    relation.simplify()
    degree = len(relation.word[0])
    admissible_words = cl.generate_Words(degree)
    #Fill the b vector
    b = np.zeros([len(admissible_words), 1])
    for i in range(len(relation.word)):
        a = admissible_words.index(relation.word[i])
        b[a] = relation.q[i]

    A = np.zeros([len(admissible_words),(degree-2)*(2**(degree-3))])
    current_column = 0
    for n in range(1,degree-1):
        deg_n_words = cl.generate_Words(degree-n)
        deg_n_forests = cl.generate_Fn(n)
        for j in range(len(deg_n_forests)):
            for i in range(len(deg_n_words)):
                result = deg_n_forests[j](cl.Word([1],[deg_n_words[i]]))
                result.simplify()
                for k in range(len(result.word)):
                    a = admissible_words.index(result.word[k])
                    A[a, current_column] = result.q[k]

                current_column += 1
    if len(sp.Matrix(A.astype(int)).rref()[1]) < len(sp.Matrix(np.concatenate((A, b), axis=1).astype(int)).rref()[1]):
        return True
    else:
        return False

#print(check_if_new_relatiion(z3.tau().harmonic_shuffle(z2z1).tau() - z3.harmonic_shuffle(z2z1.tau())))

def dim_fancy_relation(degree):
    admissible_words = cl.generate_Words(degree)
    size = 0
    for i in range(2,degree-1):
        size += (2**(i-2))*(2**(degree-i-2))
    A = np.zeros([len(admissible_words),size])
    current_column = 0
    for i in range(2,degree-1):
        deg_i_words = cl.generate_Words(i)
        for v in deg_i_words:
            v_word =  cl.Word([1],[v])
            deg_n_minus_i_words = cl.generate_Words(degree-i)
            for w in deg_n_minus_i_words:
                result = v_word.fancy_shuffle(cl.Word([1],[w]))
                for k in range(len(result.word)):
                    a = admissible_words.index(result.word[k])
                    A[a, current_column] = result.q[k]
                current_column+=1
    S = np.linalg.svd(A.astype(int))[1]
    rank = 0
    for i in S:
        if abs(i) > 0.01:
            rank+=1

    return rank#len(A.rref()[1])

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

def kawashima_1(w,v):
    prod = w.harmonic_shuffle(v).phi()

    return cl.Word([1],["x"])*prod

def kawashima_2(w,v):
    prod = w.harmonic_shuffle(v).phi().o_star(2)-(cl.Word([1],["x"])*v.phi()).shuffle(cl.Word([1],["x"])*w.phi())
    return prod

def compare_kaw_fancy(degree):
    admissible_words = cl.generate_Words(degree)
    size = 0
    for i in range(2, degree - 1):
        size += (2 ** (i - 2)) * (2 ** (degree - i - 2))
    if degree>=4:
        size += (2**(degree-3))*((degree-1)//2) + (2**(degree-4))*((degree-2)//2)
    else:
        size += (2 ** (degree - 3)) * ((degree - 1) // 2)

    A = np.zeros([len(admissible_words), size])

    current_column = 0
    for i in range(2, degree - 1):
        deg_i_words = cl.generate_Words(i)
        for v in deg_i_words:
            v_word = cl.Word([1], [v])
            deg_n_minus_i_words = cl.generate_Words(degree - i)
            for w in deg_n_minus_i_words:
                result = v_word.fancy_shuffle(cl.Word([1], [w]))
                for k in range(len(result.word)):
                    a = admissible_words.index(result.word[k])
                    A[a, current_column] = result.q[k]
                current_column += 1

    for i in range(1,(degree+1)//2):
        deg_i_words = cl.generate_Words_Hy(i)
        deg_n_minus_i_words = cl.generate_Words_Hy(degree -i -1)
        for v in deg_i_words:
            v_word = cl.Word([1], [v])
            for w in deg_n_minus_i_words:
                result = kawashima_1(v_word,cl.Word([1],[w]))
                result.simplify()
                for k in range(len(result.word)):
                    a = admissible_words.index(result.word[k])
                    A[a, current_column] = result.q[k]
                current_column += 1

    if degree>=4:
        for i in range(1, (degree) // 2):
            deg_i_words = cl.generate_Words_Hy(i)
            deg_n_minus_i_words = cl.generate_Words_Hy(degree - i - 2)
            for v in deg_i_words:
                v_word = cl.Word([1], [v])
                for w in deg_n_minus_i_words:

                    result = kawashima_2(v_word, cl.Word([1], [w]))
                    result.simplify()
                    for k in range(len(result.word)):
                        a = admissible_words.index(result.word[k])
                        A[a, current_column] = result.q[k]
                    current_column += 1

    S = np.linalg.svd(A.astype(int))[1]
    rank = 0
    for i in S:
        if abs(i) > 0.1:
            rank += 1

    return rank  # len(A.rref()[1])

def dim_kaw(degree):
    admissible_words = cl.generate_Words(degree)
    if degree>=4:
        size = (2**(degree-3))*((degree-1)//2) + (2**(degree-4))*((degree-2)//2)
    else:
        size = (2 ** (degree - 3)) * ((degree - 1) // 2)
    A = np.zeros([len(admissible_words),size])
    current_column = 0
    for i in range(1,(degree+1)//2):
        deg_i_words = cl.generate_Words_Hy(i)
        deg_n_minus_i_words = cl.generate_Words_Hy(degree -i -1)
        for v in deg_i_words:
            v_word = cl.Word([1], [v])
            for w in deg_n_minus_i_words:
                result = kawashima_1(v_word,cl.Word([1],[w]))
                result.simplify()
                for k in range(len(result.word)):
                    a = admissible_words.index(result.word[k])
                    A[a, current_column] = result.q[k]
                current_column += 1

    if degree>=4:
        for i in range(1, (degree) // 2):
            deg_i_words = cl.generate_Words_Hy(i)
            deg_n_minus_i_words = cl.generate_Words_Hy(degree - i - 2)
            for v in deg_i_words:
                v_word = cl.Word([1], [v])
                for w in deg_n_minus_i_words:

                    result = kawashima_2(v_word, cl.Word([1], [w]))
                    result.simplify()
                    for k in range(len(result.word)):
                        a = admissible_words.index(result.word[k])
                        A[a, current_column] = result.q[k]
                    current_column += 1

    S = np.linalg.svd(A.astype(int))[1]
    #print(len(sp.Matrix(A.astype(int)).rref()[1]))
    rank = 0
    for i in S:
        if abs(i) > 0.1:
            rank += 1

    return rank

def compare_tree_fancy(degree):
    admissible_words = cl.generate_Words(degree)
    size = 0
    for i in range(2, degree - 1):
        size += (2 ** (i - 2)) * (2 ** (degree - i - 2))
    cutoff = size
    size += (2 ** (degree - 3)) * ((degree - 1) // 2)
    A = np.zeros([len(admissible_words), size])

    current_column = 0
    for i in range(2, degree - 1):
        deg_i_words = cl.generate_Words(i)
        for v in deg_i_words:
            v_word = cl.Word([1], [v])
            deg_n_minus_i_words = cl.generate_Words(degree - i)
            for w in deg_n_minus_i_words:
                result = v_word.fancy_shuffle(cl.Word([1], [w]))
                for k in range(len(result.word)):
                    a = admissible_words.index(result.word[k])
                    A[a, current_column] = result.q[k]
                current_column += 1

    for i in range(1, (degree + 1) // 2):
        deg_i_words = cl.generate_Words_Hy(i)
        deg_n_minus_i_words = cl.generate_Words_Hy(degree - i - 1)
        for v in deg_i_words:
            v_word = cl.Word([1], [v])
            for w in deg_n_minus_i_words:
                result = kawashima_1(v_word, cl.Word([1], [w]))
                result.simplify()
                for k in range(len(result.word)):
                    a = admissible_words.index(result.word[k])
                    A[a, current_column] = result.q[k]
                current_column += 1

    fancy_matrix = A[:,:cutoff]
    kaw_matrix = A[:,cutoff:]
    S = np.linalg.svd(A.astype(int))[1]
    K = np.linalg.svd(kaw_matrix.astype(int))[1]
    F = np.linalg.svd(fancy_matrix.astype(int))[1]
    rank = 0
    rank_K = 0
    rank_F = 0
    for i in S:
        if abs(i) > 0.01:
            rank += 1
    for i in K:
        if abs(i) > 0.01:
            rank_K += 1
    for i in F:
        if abs(i) > 0.01:
            rank_F += 1
    return ("Total dim:",rank,"Kawashima dim:",rank_K,"Fancy dim:",rank_F,"intersect",rank_K+rank_F-rank)  # len(A.rref()[1])
#print(z3.fancy_shuffle(z2z1).toZeta())
print(13,compare_tree_fancy(13))


#print(dim_fancy_relation(11))
#print(check_if_new_relatiion(z3.fancy_shuffle(z2z1)))