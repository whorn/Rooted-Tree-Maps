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
                    result.q += temp_result.q
                    result.word += temp_result.word
            else:
                temp_forest = Forest(self.leaves)
                temp_result = temp_forest(Word([input_word.q[i]],[input_word.word[i]]))
                temp_result.R_star()
                result.q += temp_result.q
                result.word += temp_result.word
        return result

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
                    result.q += temp_result.q
                    result.word += temp_result.word
            else:
                temp_result = self.trees[0].coproduct()(Word([word.q[i]],[word.word[i]]))
                for j in range(1, len(self.trees)):
                    temp_result = self.trees[j].coproduct()(temp_result)
                result.q += temp_result.q
                result.word += temp_result.word
        return result

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
                result.word += new_word.word
                result.q += new_word.q
            result.simplify()
        return result

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

    # Adds two Word objects together, returns a new Word object.
    def __add__(self, other):
        result = Word()
        result.word = self.word + other.word
        result.q = self.q + other.q
        return result
    
    # Subtracts two Word objects from each other, returns a new Word object.
    def __sub__(self, other):
        result = Word()
        result.word = self.word + other.word
        result.q = self.q + [-q for q in other.q]
        return result
    
    # Multiplies a word by a coefficient (float) from the left.
    def __rmul__(self, other):
        if other is int or float:
            self.q = [other*q for q in self.q]
        return self
    
    # Adds another Word object to the current Word object.
    def __iadd__(self, other):
        self.word = self.word + other.word
        self.q = self.q + other.q
    
    # Multiplies two Word objects, returns a new Word object.
    def __mul__(self, other):
        result = Word([],[])
        for i in range(len(self.q)):
            for j in range(len(other.q)):
                result.q.append(self.q[i]*other.q[j])
                result.word.append(self.word[i]+other.word[j])
        return result

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
    counter = 0
    result = "z("

    for letter in string:
        if letter == "y":
            result += str((counter+1)) +","
            counter = 0
        else:
            counter += 1
    result = result[:-1] +")"
    return result
