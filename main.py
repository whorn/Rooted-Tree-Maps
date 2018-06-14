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
z2z2 = cl.Word([1],["xyxy"])
x = cl.Word([1],["x"])
yy = cl.Word([1],["yy"])

tree1 = cl.forest_from_string("0")
tree2 = cl.forest_from_string("00")
tree3 = cl.forest_from_string("000")
tree4 = cl.forest_from_string("0000")

w = z2
v = z2

print(w.phi_shuffle(v)-v.phi_shuffle(w))

print((w.shuffle(v)-x*w.phi_stuffle(z1)).toZeta())

print(z2.delta(3))
print(z2.square_shuffle(z3).toZeta())

print(z2z2.phi_hat())

