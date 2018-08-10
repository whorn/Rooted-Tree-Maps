# A class for representing trees
class Tree:

    # Initializes a tree object
    def __init__(self,leaves= [] ):
        self.leaves = leaves

    # Return the tree represented as a string of 0's, 1's and 2's
    def toString(self):
        if len(self.leaves) == 0:
            return "0"
        elif len(self.leaves) == 1:
            return self.leaves[0].toString() + "0"
        else:
            string = self.leaves[0].toString()
            for i in range(1,len(self.leaves)):
                string += "1" + self.leaves[i].toString() + "2"
            return string + "0"

    # Calculates the coproduct of the tree, returns a coproduct object
    def coproduct(self):
        # If the tree has no leaves, it's the tree consisting of a single node.
        # The coproduct for this tree is hard coded to save time.
        if len(self.leaves) == 0:
            return Coproduct([1,1],[forest_from_string("0"),Forest()],[Forest(),forest_from_string("0")])
        string = self.toString()

        # an array of coefficients
        new_q = [1]

        # left side of the coproduct
        new_l = [forest_from_string(string)]

        # right side of the coproduct
        new_r = [Forest()]

        # the coproduct of the forest remaining when you remove the root node
        C = forest_from_string(string[:-1]).coproduct()
        for i in range(len(C.q)):
            C.r[i].graft()
        return Coproduct(new_q,new_l,new_r) + C

    # Uses the tree to evaluate a word. Returns a word object.
    def __call__(self, input_word):
        result = Word([],[])
        for i in range(len(input_word.q)):
            # hard coded values for the evaluation of the tree consisting of a single node
            if len(self.leaves) == 0:
                if input_word.word[i] == "x":
                    result.word.append("xy")
                    result.q.append(1)

                elif input_word.word[i] == "y":
                    result.word.append("xy")
                    result.q.append(-1)

                else:
                    temp_result = self.coproduct()(Word([input_word.q[i]],[input_word.word[i]]))
                    result = result + temp_result
            else:
                if len(input_word.word[i]) == 1:
                    temp_forest = Forest(self.leaves)

                    temp_result = temp_forest(Word([input_word.q[i]],[input_word.word[i]]))
                    temp_result.R_star()
                else:
                    temp_result = self.coproduct()(Word([input_word.q[i]],[input_word.word[i]]))
                result = result + temp_result
        return result

    def __str__(self):
        return self.toString()

# This class is a collection of trees, a forest with no trees is the empty forest.
class Forest:

    # Initializes a forest. The default is the empty forest.
    def __init__(self,trees = []):
        self.trees = trees

    # Creates a new root and makes it the root of all trees in the forest.
    def graft(self):
        new_root = Tree(self.trees)
        self.trees = [new_root]

    # Return the forest represented as a string of 0's, 1's and 2's
    def toString(self):
        if len(self.trees) == 0:
            return ""
        elif len(self.trees) == 1:
            return self.trees[0].toString()
        else:
            string = self.trees[0].toString()
            for i in range(1,len(self.trees)):
                string += "1" + self.trees[i].toString() + "2"
            return string
    # Adds the trees of another forest to its own trees.
    def merge(self,other):
        self.trees += other.trees

    # Calculates the coproduct of the forest, returns a coproduct object
    def coproduct(self):
        # Hardcoded coproduct of the empty forest.
        if len(self.trees) == 0:
            return Coproduct([1],[Forest()],[Forest()])
        total_coproduct = self.trees[0].coproduct()
        for i in range(1,len(self.trees)):
            temp = total_coproduct*self.trees[i].coproduct()
            total_coproduct = temp
        return total_coproduct

    # Merges the two forests, but returns a new forest.
    def __mul__(self, other):
        new_forest = Forest(self.trees+other.trees)
        return new_forest

    # Uses the forest to evaluate a word. Returns a word object.
    def __call__(self, word):
        if len(self.trees) == 0:
            return word
        result = Word([], [])
        for i in range(len(word.q)):
            if len(word.word[i]) == 1:
                    temp_result = self.trees[0](word)
                    for i in range(1,len(self.trees)):
                        temp_result = self.trees[i](temp_result)
                    result = result + temp_result
            else:
                temp_result = self.trees[0].coproduct()(Word([word.q[i]],[word.word[i]]))
                for j in range(1, len(self.trees)):
                    temp_result = self.trees[j].coproduct()(temp_result)
                result = result + temp_result
        return result

    def __str__(self):
        return self.toString()

    def calculate_w(self):
        w = self(Word([1],["y"]))
        return w.chi_x_inv()

# The Coproduct class is the tensor product of the space of rooted forests with itself.
# It consists of a list of coefficients for the tensors and left and right hand sides for the tensors.
class Coproduct:
    # Initialises the Coproduct object. Default is completely empty arrays, without the empty forest even.
    def __init__(self,q = [ ] ,l = [ ], r = [ ]):
        self.q = q
        self.r = r
        self.l = l

    # Adds two Coproduct objects together, returns another Coproduct object.
    def __add__(self, other):
        new_q = self.q + other.q
        new_r = []
        new_l = []
        for i in range(len(self.q)):
            new_r.append(forest_from_string(self.r[i].toString()))
            new_l.append(forest_from_string(self.l[i].toString()))
        for j in range(len(other.q)):
            new_r.append(forest_from_string(other.r[j].toString()))
            new_l.append(forest_from_string(other.l[j].toString()))
        return Coproduct(new_q,new_l,new_r)

    # Multiplies two Coproduct objects together, returns another Coproduct object.
    def __mul__(self, other):
        new_q = []
        new_r = []
        new_l = []
        for i in range(len(self.q)):
            for j in range(len(other.q)):
                new_q.append(self.q[i]*other.q[j])
                new_r.append(self.r[i]*other.r[j])
                new_l.append(self.l[i] * other.l[j])
        return Coproduct(new_q,new_l,new_r)

    # Returns the Coproduct object as a string.
    def toString(self):
        output = ""
        for i in range(len(self.q)):
            output +=  str(self.q[i]) +"( "+ self.l[i].toString() + ") X ( " + self.r[i].toString() + ") + "
        if len(output)>0:
            output = output[:-2]
        return output

    # Uses the Coproduct to evaluate a word. Returns a word object.
    def __call__(self, word):
        result = Word([],[])
        for j in range(len(word.q)):
            str_word = Word([1],[word.word[j][:-1]])
            str_letter = Word([1],[word.word[j][-1]])
            for i in range(len(self.q)):
                l = word.q[j]*self.l[i](str_word)
                r = self.r[i](str_letter)
                new_word = l*r
                result = result + new_word
            result.simplify()
        return result

    def __str__(self):
        return self.toString()

    # Simplifies the Coproduct object i.e x + x = 2x
    def simplify(self):
        for i in range(len(self.q)):
            for j in range(len(self.q)-1,i,-1):
                if self.l[i].toString() == self.l[j].toString() and self.r[i].toString() == self.r[j].toString():
                    self.q[i] += self.q[j]
                    self.q.pop(j)
                    self.l.pop(j)
                    self.r.pop(j)

# The Word class is used to represent collections of words (in the mathematical sense) and their coefficients
# It consists of a list of coefficients and a list of strings.
class Word:
    # Initializes a Word object with the empty word and the coefficient 1.
    def __init__(self,q=[1],words = [""]):
        self.q = q
        self.word = words

    # Simplifies expressions, removes duplicates in the lists and updates coefficients.
    def simplify(self):
        for i in range(len(self.q)):
            for j in range(len(self.q)-1,i,-1):
                if self.word[i]==self.word[j]:
                    self.q[i]+=self.q[j]
                    self.word.pop(j)
                    self.q.pop(j)
        for i in range(len(self.q)-1,0,-1):
            if self.q[i] == 0:
                self.word.pop(i)
                self.q.pop(i)
        if (self.q[0] == 0):
            if len(self.q) > 1:
                self.word.pop(0)
                self.q.pop(0)
            else:
                self.word[0] = ""


    # Right concatenation with a string, the letter variable.
    #  The coefficient for this letter is by default 1, but can be changed.
    def R(self, letter, q=1):
        for i in range(len(self.q)):
            self.word[i]+=letter
            self.q[i]*=q

    # Inverse Right concatenation with a letter, removes the last input letter from each word in Word object.
    def R_inv(self,letter):
        for i in range(len(self.q)):
            if self.word[i][-1] == letter:
                self.word[i] = self.word[i][:-1]

    # A combination of R, and R_inv with various input letters.
    def R_star(self):
        self.R_inv("y")
        self_copy = Word([],[]) + self
        self_copy.R("y",2)
        self.R("x",1)
        self.word += self_copy.word
        self.q += self_copy.q
        self.R("y",1)

    # Returns a Word object as a string.
    # The string is an expression with combinations of coefficients, x's and y's.
    def toString(self):
        if len(self.q) == 0:
            return ""
        self.simplify()
        string = ""
        for i in range(len(self.q)):
            string += str(self.q[i])+self.word[i] +" + "
        if len(string)>0:
            string = string[:-2]
        return string

    # Returns the Word object as a string.
    # The string is an expression with zeta value notation
    def toZeta(self):
        self.simplify()
        positive = ""
        negative = ""
        for i in range(len(self.q)):
            if self.q[i]>0 :
                if self.q[i]!=1:
                    positive += str(self.q[i])+string_to_z(self.word[i])+" + "
                else:
                    positive += string_to_z(self.word[i]) + " + "
            else:
                if self.q[i] != -1:
                    negative += str(-self.q[i]) + string_to_z(self.word[i])+" + "
                else:
                    negative += string_to_z(self.word[i]) + " + "
        return positive[:-3] + " = " + negative[:-3]

    # Returns the word as a string.
    # The string is an expression with z_k's
    def toBracketNotation(self):
        self.simplify()
        string = ""
        for i in range(len(self.q)):
            if self.q[i]>0:
                if self.q[i]!=1:
                    string += " + " + str(self.q[i])+string_to_z(self.word[i])
                else:
                    string += " + " + string_to_z(self.word[i])
            else:
                if self.q[i] != -1:
                    string += " - " + str(-self.q[i]) + string_to_z(self.word[i])
                else:
                    string += " - " +string_to_z(self.word[i])
        if string[1] == "+":
            return string[2:]
        else:
            return string

    # Adds two Word objects together, returns a new Word object.
    def __add__(self, other):
        result = Word()
        result.word = self.word + other.word
        result.q = self.q + other.q
        result.simplify()
        return result

    # Subtracts two Word objects from each other, returns a new Word object.
    def __sub__(self, other):
        result = Word()
        result.word = self.word + other.word
        result.q = self.q + [-q for q in other.q]
        result.simplify()
        return result

    # Multiplies a word by a coefficient (float) from the left.
    def __rmul__(self, other):
        result = Word([], [])
        if other is int or float:
            result.q = [other*q for q in self.q]
            result.word = [string for string in self.word]
        result.simplify()
        return result

    # Adds another Word object to the current Word object.
    def __iadd__(self, other):
        self.word = self.word + other.word
        self.q = self.q + other.q
        self.simplify()

    # Multiplies two Word objects, returns a new Word object.
    def __mul__(self, other):
        result = Word([],[])
        for i in range(len(self.q)):
            for j in range(len(other.q)):
                result.q.append(self.q[i]*other.q[j])
                result.word.append(self.word[i]+other.word[j])
        self.simplify()
        return result

    # Exponentiation of a word
    def __pow__(self, power, modulo=None):
        result = self
        if power == 0:
            return Word()
        elif power == 1:
            return result
        elif power%2 == 0:
            return (result*result)**(power/2)
        else:
            return result*(result**(power-1))

    # Turns a word into a string with the toString function. Might remove toString() entirely later.
    def __str__(self):
        return self.toString()

    # Reverses order of the word and changes x to y and y to x.
    def tau(self):
        result = Word([], [])
        for term in range(len(self.word)):
            result.q.append(self.q[term])
            result.word.append("")
            for letter in self.word[term]:
                if letter == "x":
                    result.word[term] = "y" + result.word[term]
                else:
                    result.word[term] = "x" + result.word[term]
        return result

    # Sends x to x+y and y to -y
    def phi(self):
        result = Word([],[])
        for term in range(len(self.word)):
            temp_result = Word([self.q[term]],[""])
            for letter in self.word[term]:
                if letter == "x":
                    temp_result = temp_result*Word([1,1],["x","y"])
                else:
                    temp_result = temp_result*Word([-1],["y"])

            result = result + temp_result
        return result
    # Sends x to x and y to -(x+y), ignores the last y in the word
    def eta(self):
        result = Word([], [])
        for term in range(len(self.word)):
            temp_result = Word([self.q[term]], [""])
            for i in range(len(self.word[term])-1):
                letter = self.word[term][i]
                if letter == "y":
                    temp_result = temp_result * Word([-1, -1], ["x", "y"])
                else:
                    temp_result = temp_result * Word([1], ["x"])

            result = result + temp_result

        result.R("y",-1) # -1 to make the sign correct. Since the iteration through the word ignores the last y.
        return result

    def chi_x(self):
        return self.phi().tau()*Word([1],"y")

    def chi_x_inv(self):
        result = 1*self
        result.R_inv("y")
        return result.tau().phi()

    def bootleg_dual_product(self,rhs):
        return self.chi_x_inv().harmonic_shuffle(rhs).chi_x() + self.harmonic_shuffle(rhs)

    #### Shuffle and Harmonic Shuffle
    def shuffle(self,other):
        result = Word([], [])
        for i in range(len(self.q)):
            for j in range(len(other.q)):
                if self.word[i] == "" or other.word[j] == "":
                    result = result + Word([self.q[i]*other.q[j]],[self.word[i] + other.word[j]])
                else:
                    self_temp = Word([self.q[i]], [self.word[i]])
                    other_temp = Word([other.q[j]], [other.word[j]])
                    a = Word([self.q[i]],[self.word[i][0]])*Word([1],[self.word[i][1:]]).shuffle(other_temp)
                    b = Word([other.q[j]],[other.word[j][0]])*self_temp.shuffle(Word([1],[other.word[j][1:]]))

                    result = result + a + b
        return result

    def harmonic_shuffle(self,other):
        result = Word([], [])
        for i in range(len(self.q)):
            for j in range(len(other.q)):
                if self.word[i] == "" or other.word[j] == "":
                    result = result + Word([self.q[i]*other.q[j]],[self.word[i] + other.word[j]])
                else:
                    if self.word[i][-1] == "x" or other.word[j][-1] == "x":
                        k = len(self.word[i])
                        l = len(other.word[j])
                        while self.word[i][k-1]=="x" and k>0:
                            k -= 1
                        while other.word[j][l-1]=="x" and l>0:
                            l -= 1
                        self_temp = Word([self.q[i]], [self.word[i][:k]])
                        other_temp = Word([other.q[j]], [other.word[j][:l]])
                        result = result + self_temp.harmonic_shuffle(other_temp)*Word([1],["x"*(len(self.word[i])-k+len(other.word[j])-l)])
                    else:
                        self_temp = Word([self.q[i]], [self.word[i]])
                        other_temp = Word([other.q[j]], [other.word[j]])
                        #extract z_k
                        self_zk = Word([1],[self_temp.word[0][:(self_temp.word[0].index("y")+1)]])
                        other_zk = Word([1],[other_temp.word[0][:other_temp.word[0].index("y")+1]])
                        total_zk = Word([1],["x"*(len(self_zk.word[0])+len(other_zk.word[0])-1)+"y"])
                        self_reduced = Word(self_temp.q,[self_temp.word[0][(self_temp.word[0].index("y")+1):]])
                        other_reduced = Word(other_temp.q,[other_temp.word[0][(other_temp.word[0].index("y")+1):]])
                        a = self_zk*(self_reduced.harmonic_shuffle(other_temp))
                        b = other_zk*(self_temp.harmonic_shuffle(other_reduced))
                        c = total_zk*(self_reduced.harmonic_shuffle(other_reduced))
                        result = result + a + b + c

        return result

    ### Other shuffle products
    ### Shuffle and harmonic shuffle mixed with other operators.
    def o_star(self,degree):
        if degree == 1:
            return Word([1],["x"])*self
        else:
            result = Word([],[])
            for i in range(len(self.q)):
                self_temp = Word([self.q[i]], [self.word[i]])
                # extract z_k
                self_zk = Word([1], [self_temp.word[0][:(self_temp.word[0].index("y") + 1)]])
                #total_zk = Word([1], ["x" * (len(self_zk.word[0]) + len(other_zk.word[0]) - 1) + "y"])
                self_reduced = Word(self_temp.q, [self_temp.word[0][(self_temp.word[0].index("y") + 1):]])
                result = result + self_zk * (self_reduced.harmonic_shuffle(Word([1], ["y" * (degree - 1)])))
        return Word([1],["x"])*result

    # Tau Harmonic Shuffle Tau
    def square_shuffle(self,other):
        result = self.tau().harmonic_shuffle(other.tau()).tau()
        return result
    # Phi Harminic Shuffle Phi
    def phi_stuffle(self,other):
        result = self.phi().harmonic_shuffle(other.phi()).phi()
        return result

    # Phi Shuffle Phi      NOTE: Equals normal shuffle
    def phi_shuffle(self,other):
        result = self.phi().shuffle(other.phi()).phi()
        return result

    def fancy_shuffle(self,other):
        result = self.harmonic_shuffle(other.tau()).tau()-self.tau().harmonic_shuffle(other)
        return result

    #### DERIVATIONS: Various derivations on words.

    def delta(self,n):
        dx = Word([1],["x"])*(Word([1,1],["x","y"])**(n-1))*Word([1],["y"])
        map = {"x":dx,"y":-1*dx}
        return derivate(self, map)

    def DELTA(self,n):
        dx = Word([0], [""])
        dy = Word([1], [("x" * n) + "y"])
        map = {"x": dx, "y": dy}
        return derivate(self, map)

    def DELTA_BAR(self,n):
        dx = Word([1],["x"+("y"*n)])
        dy = Word([0],[""])
        map = {"x": dx,"y": dy}
        return derivate(self,map)


# Translates a string of 0's, 1's and 2's to a forest object. Returns the forest.
def forest_from_string(string):
    if len(string) == 0:
        return Forest()
    else:
        f = Forest()
        level = [f]
        current_level = 0
        for char in string:
            if char == "0":
                level[current_level].graft()
            elif char == "1":
                current_level += 1
                if current_level >= len(level):
                    level.append(Forest())
                else:
                    level[current_level] = Forest()
            elif char == "2":
                current_level -= 1
                level[current_level].merge(level[current_level + 1])
        return f

# Translates a string of x's and y's into a zeta value.
def string_to_z(string):
    if string == "":
        return ""
    counter = 0
    result = "("

    for letter in string:
        if letter == "y":
            result += str((counter+1)) +","
            counter = 0
        else:
            counter += 1
    result = result[:-1] +")"
    return result

# Derivates a word with x's and y's with respect to Leibniz' rule. letter_map is the map for x and y.
def derivate(input_word,letter_map):
    result = Word([],[])
    input_word.simplify()
    for term in range(len(input_word.word)):
        if len(input_word.word[term]) == 1:
            result = result + (letter_map[input_word.word[term]])

        else:
            for letter in range(0, len(input_word.word[term])):
                left_hand_side = Word([1], [input_word.word[term][:letter]])
                right_hand_side = Word([1], [input_word.word[term][letter + 1:]])
                du = letter_map[input_word.word[term][letter]]
                if letter == 0:
                    result = result + (du * right_hand_side)
                elif letter == len(input_word.word[term]) - 1:
                    result = result + (left_hand_side * du)
                else:
                    result = result + (left_hand_side * du * right_hand_side)

    return result



###
### OTHER COMMANDS
###

# Calculates the lie-bracket  [DELTA_BAR,DELTA](word)
def d1_commutator(input_word):
    print(input_word.DELTA(1).DELTA_BAR(1)-input_word.DELTA_BAR(1).DELTA(1))

def Hn_commutator(input_word,n):
    zn = Word([1],["x"*(n-1)+"y"])
    print(input_word.harmonic_shuffle(zn).tau().harmonic_shuffle(zn).tau()-input_word.tau().harmonic_shuffle(zn).tau().harmonic_shuffle(zn))

# Creates words that read the same backwards as forwards of a given length. These words are Tau-invariant.
def generate_symmetric_words(length):
    symmetric_words = []
    for n in range(2**(length-1)):
        current_word = ""
        for b in ('{0:0'+str(2**(length-1))+'b}').format(n):
            if b == "0":
                current_word = "x"+current_word+"y"
            else:
                current_word = "y" + current_word + "x"
        current_word = "x" + current_word + "y"
        symmetric_words.append(current_word)
    return symmetric_words

# Returns a list of strings with all admissible words of the given length
def generate_Words(length):
    word_list = []
    if length == 2:
        return ["xy"]
    for n in range(int(2**(length-2))):
        binary = bin(n)[2:]
        binary = "0"*(length-len(binary)-2) + binary
        current_word = ""
        for b in binary:
            if b == "0":
                current_word += "x"
            else:
                current_word += "y"
        current_word = "x" + current_word + "y"
        word_list.append(current_word)
    return word_list

def generate_Words_Hy(length):
    admissible = generate_Words(length)
    word_list = []
    if length == 1:
        return ["y"]
    for word in admissible:
        word_list.append(word)
        word_list.append("y"+word[1:])
    return word_list

# Input is a LIST of STRINGS
# Generates tables for easy comparison of results
def generate_table(strings):
    z2 = Word([1], ["xy"])
    table = []
    for word in strings:
        w = Word([1],[word])
        delta = w.delta(2).toBracketNotation()
        harmonic_product = w.harmonic_shuffle(z2).toBracketNotation()
        square_product = w.square_shuffle(z2).toBracketNotation()
        D2_bar = w.DELTA_BAR(2).toBracketNotation()
        D2 = w.DELTA(2).toBracketNotation()
        D1BARD1 = w.DELTA(1).DELTA_BAR(1).toBracketNotation()
        D1D1BAR = w.DELTA_BAR(1).DELTA(1).toBracketNotation()
        commutator = (w.DELTA(1).DELTA_BAR(1) - w.DELTA_BAR(1).DELTA(1)).toBracketNotation()
        output = word + "\t" + delta +"\t" + harmonic_product + "\t" + square_product + "\t" + D2_bar + "\t" + D2 + "\t" + D1BARD1 + "\t" + D1D1BAR + "\t" + commutator
        table.append(output)
    for i in table:
        print(i)

# Input is a LIST of STRINGS
# Generates tables for easy comparison of results
def generate_table3(strings):
    z3 = Word([1], ["xxy"])
    table = []
    for word in strings:
        w = Word([1],[word])
        delta = w.delta(3).toBracketNotation()
        harmonic_product = w.harmonic_shuffle(z3).toBracketNotation()
        square_product = w.square_shuffle(z3).toBracketNotation()
        D3_bar = w.DELTA_BAR(3).toBracketNotation()
        D3 = w.DELTA(3).toBracketNotation()
        output = word + "\t" + delta +"\t" + harmonic_product + "\t" + square_product + "\t" + D3_bar + "\t" + D3# + "\t" + D1BARD1 + "\t" + D1D1BAR + "\t" + commutator
        table.append(output)
    for i in table:
        print(i)

def generate_Fn(n):
    F = [forest_from_string("0")]
    for i in range(n-1):
        new_F = []
        for forest in F:
            new_F.append(forest*forest_from_string("0"))
            grafted = forest_from_string(forest.toString())
            grafted.graft()
            new_F.append(grafted)
        F = new_F
    return F