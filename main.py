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


cl.Hn_commutator(z2,1)










