#Playground for testing stuff.
import classes as cl

def table_gen():

    #input_list = ["xy","xxy","xyy","xyxy","xxyy","xxxy","xyyy","xxxxy","xyxyy","xyxxy","xyyyy"]
    five_words = cl.generate_Words(5)
    cl.generate_table(five_words)

#table_gen()
z1 = cl.Word([1],["y"])
z2 = cl.Word([1],["xy"])
z3 = cl.Word([1],["xxy"])
z4 = cl.Word([1],["xxxy"])
z2z2 = cl.Word([1],["xyxy"])
z2z1 = cl.Word([1],["xyy"])
x = cl.Word([1],["x"])
yy = cl.Word([1],["yy"])
t1 = cl.forest_from_string("00")
t2 = cl.forest_from_string("0102")
print(t1(z2).toBracketNotation())
print(t2(z2).toBracketNotation())
"""
print((z2.tau().harmonic_shuffle(z4).tau()-z2.harmonic_shuffle(z4.tau())).toZeta())
t1 = cl.forest_from_string("00000")
t2 = cl.forest_from_string("01021021020")
t3 = cl.forest_from_string("01021020102")
t4 = cl.forest_from_string("010210200")
#print(t1.calculate_w().toBracketNotation())
print(t1(z1).toBracketNotation())
print(t2(z1).toBracketNotation())
print(t3(z1).toBracketNotation())
print(t4(z1).toBracketNotation())
#cl.Hn_commutator(z2,1)

#print(yy.harmonic_shuffle(z1).tau().harmonic_shuffle(z1))

"""







