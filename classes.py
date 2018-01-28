class Tree:

    def __init__(self,leaves= [] ):
        self.leaves = leaves

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


    def coproduct(self):
        if len(self.leaves) == 0:
            return Coproduct([1,1],[forest_from_string("0"),Forest()],[Forest(),forest_from_string("0")])

        string = self.toString()

        new_q = [1]
        new_l = [forest_from_string(string)]
        new_r = [Forest()]
        C = forest_from_string(string[:-1]).coproduct()
        for i in range(len(C.q)):
            C.r[i].graft()
        return Coproduct(new_q,new_l,new_r) + C

    def __call__(self, input_word):
        result = Word([],[])
        for i in range(len(input_word.q)):
            if len(self.leaves) == 0:
                if input_word.word[i] == "x":
                    result.word.append("xy")
                    result.q.append(1)
                elif input_word.word[i] == "y":
                    result.word.append("xy")
                    result.q.append(-1)
                #elif input_word.word[i] == "":
                #    result.word.append("")
                #    result.q.append(1)
                else:
                    result = self.coproduct()(Word([input_word.q[i]],[input_word.word[i]]))
            else:
                temp_forest = Forest(self.leaves)
                temp_result = temp_forest(Word([input_word.q[i]],[input_word.word[i]]))
                temp_result.R_star()
                result.q += temp_result.q
                result.word += temp_result.word
        return result

class Forest:
    def __init__(self,trees = []):
        self.trees = trees

    def graft(self):
        new_root = Tree(self.trees)
        self.trees = [new_root]

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

    def merge(self,other):
        self.trees += other.trees

    def coproduct(self):
        if len(self.trees) == 0:
            return Coproduct([1],[Forest()],[Forest()])
        total_coproduct = self.trees[0].coproduct()
        temp = total_coproduct
        for i in range(1,len(self.trees)):
            #total_coproduct *= self.trees[i].coproduct()
            temp = total_coproduct*self.trees[i].coproduct()
            total_coproduct = temp
        #total_coproduct.simplify()
        return total_coproduct

    def __mul__(self, other):
        #new_forest = forest_from_string(self.toString())
        #other_forest = forest_from_string(other.toString())
        #new_forest.trees += other_forest.trees
        new_forest = Forest(self.trees+other.trees)
        return new_forest

    def __call__(self, word): #SKAL MAN TA INN STRING ELLER WORD
        for i in range(len(word.q)):
            if len(word.word[i]) == 1:
                if len(self.trees) == 0:
                    return word
                else:
                    result = self.trees[0](word)
                    for i in range(1,len(self.trees)):
                        result = self.trees[i](result)
                    return result
            else:
                return self.coproduct()(word)

class Coproduct:

    def __init__(self,q = [ ] ,l = [ ], r = [ ]):
        self.q = q
        self.r = r
        self.l = l

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

    def __imul__(self, other):
        new_q = []
        new_r = []
        new_l = []
        for i in range(len(self.q)):
            for j in range(len(other.q)):
                new_q.append(self.q[i] * other.q[j])
                new_r.append(self.r[i] * other.r[j])
                new_l.append(self.l[i] * other.l[j])
        self.q = new_q
        self.r = new_r
        self.l = new_l

    def toString(self):
        output = ""
        for i in range(len(self.q)):
            output +=  str(self.q[i]) +"( "+ self.l[i].toString() + ") X ( " + self.r[i].toString() + ") + "
        if len(output)>0:
            output = output[:-2]
        return output

    def __call__(self, word):
        result = Word([],[])
        for j in range(len(word.q)):
            str_word = Word([word.q[j]],[word.word[j][:-1]])
            str_letter = Word([1],[word.word[j][-1]])
            for i in range(len(self.q)):
                l = self.l[i](str_word)
                r = self.r[i](str_letter)
                new_word = l*r
                new_word.simplify()
                result.word += new_word.word
                #result.simplify()
                result.q += new_word.q
            result.simplify()
        return result

    def simplify(self):
        for i in range(len(self.q)):
            for j in range(len(self.q)-1,i,-1):
                if self.l[i].toString() == self.l[j].toString() and self.r[i].toString() == self.r[j].toString():
                    self.q[i] += self.q[j]
                    self.q.pop(j)
                    self.l.pop(j)
                    self.r.pop(j)

class Word: #variables q and word

    def __init__(self,q=[1],words = [""]):
        self.q = q
        self.word = words

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
    def R(self, letter, q=1):
        for i in range(len(self.q)):
            self.word[i]+=letter
            self.q[i]*=q

    def R_inv(self,letter):
        for i in range(len(self.q)):
            if self.word[i][-1] == letter:
                self.word[i] = self.word[i][:-1]

    def R_star(self):
        self.R_inv("y")
        self_copy = Word([],[]) + self
        self_copy.R("y",2)
        self.R("x",1)
        self.word += self_copy.word
        self.q += self_copy.q
        self.R("y",1)


    def toString(self):
        self.simplify()
        string = ""
        for i in range(len(self.q)):
            string += str(self.q[i])+self.word[i] +" + "
        if len(string)>0:
            string = string[:-2]
        return string

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

    def __add__(self, other):
        result = Word()
        result.word = self.word + other.word
        result.q = self.q + other.q
        return result

    def __iadd__(self, other):
        self.word = self.word + other.word
        self.q = self.q + other.q

    def __mul__(self, other):
        result = Word([],[])
        for i in range(len(self.q)):
            for j in range(len(other.q)):
                result.q.append(self.q[i]*other.q[j])
                result.word.append(self.word[i]+other.word[j])
        return result



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


f = forest_from_string("0102")

print(f.coproduct().toString())
w = Word([1],["xyxy"])
y = Word([1],["xy"])

print(f(y).toString())
print(f(y).toZeta())

