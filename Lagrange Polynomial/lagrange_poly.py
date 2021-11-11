class Lagrange_Poly:

    def __init__(self):
        self.seq_length = 0
        self.num_seq = 0
        self.x_seq = []
        self.y_seq = []
        self.pruned_seq_length = 0
        self.pruned_x_seq = []
        self.pruned_y_seq = []
        self.is_set = 0
        self.was_pruned = 0
        self.accuracy = 20

    def set_polynomial(self, seq_length, x_seq, y_seq):   
        self.set_polynomial_multi(seq_length, 1, [x_seq], y_seq)
    
    def set_polynomial_multi(self, seq_length, num_seq, x_seq, y_seq):
        self.reset_polynomial()
        self.seq_length = seq_length
        self.is_set = 1
        self.num_seq = num_seq
        for j in range(num_seq):
            for i in range(seq_length):
                self.x_seq.append(x_seq[j][i])
                if (len(str(y_seq[i])) != 0):
                    self.pruned_x_seq.append(x_seq[j][i])
        for k in range(seq_length):
            self.y_seq.append(y_seq[k])
            if (len(str(y_seq[k])) != 0):
                self.pruned_seq_length += 1
                self.pruned_y_seq.append(y_seq[k])
        if (self.pruned_seq_length != self.seq_length):
            self.was_pruned = 1

    def reset_polynomial(self):
        self.seq_length = 0
        self.pruned_seq_length = 0
        self.num_seq = 0
        self.accuracy = 20
        self.x_seq = []
        self.y_seq = []
        self.pruned_x_seq = []
        self.pruned_y_seq = []
        self.is_set = 0
        self.was_pruned = 0

    def print_x_seq(self):
        if (self.is_set == 0):
            print("ERR: print_x_seq: Values have not yet been set")
            return
        for j in range(self.num_seq):
            for i in range(self.seq_length):
                print("x" + str(j) + "_seq: index " + str(i) + " : " + str(self.x_seq[i + (j * self.num_seq)]))

    def print_y_seq(self):
        if (self.is_set == 0):
            print("ERR: print_y_seq: Values have not yet been set")
            return
        for i in range(self.seq_length):
            print("y_seq: index: " + str(i) + " : " + str(self.y_seq[i]))

    def print_pruned_x_seq(self):
        if (self.is_set == 0):
            print("ERR: print_pruned_x_seq: Values have not yet been set")
            return
        for j in range(self.num_seq):
            for i in range(self.pruned_seq_length):
                print("pruned_x" + str(j) + "_seq: index " + str(i) + " : " + str(self.pruned_x_seq[i + (j * self.pruned_seq_length)]))

    def print_pruned_y_seq(self):
        if (self.is_set == 0):
            print("ERR: print_pruned_y_seq: Values have not yet been set")
            return
        for i in range(self.pruned_seq_length):
            print("pruned_y_seq" + str(i) + " : " + str(self.pruned_y_seq[i]))
        
    def generate_polynomial_string(self):
        if (self.is_set == 0):
            print("ERR: generate_polynomial_string: Values have not yet been set")
            return
        poly_str = ""
        for i in range(self.pruned_seq_length):
            poly_str = poly_str + str(self.pruned_y_seq[i]) + " * (" 
            for a in range(self.num_seq):
                for j in range (self.pruned_seq_length):
                    if (i != j):
                        poly_str = poly_str + "(x" + str(a) + " - " + str(self.pruned_x_seq[j + (a* self.pruned_seq_length)]) + ")"
            poly_str = poly_str + "/"
            for b in range(self.num_seq):
                for k in range (self.pruned_seq_length):
                    if (i != k):
                        poly_str = poly_str + "( " + str(self.pruned_x_seq[i + (b* self.pruned_seq_length)]) + " - " + str(self.pruned_x_seq[k + (b* self.pruned_seq_length)]) + ")"
            poly_str = poly_str + ")"
            if (i < self.pruned_seq_length - 1):
                poly_str = poly_str + " + "
        return poly_str

    def print_polynomial(self):
        if (self.is_set == 0):
            print("ERR: print_polynomial: Values have not yet been set")
            return
        if (self.num_seq > 1):
            print("Lagrange Polynomial: " + self.generate_polynomial_string())
            return
        print("Lagrange Polynomial: " + self.generate_polynomial_string())

    def solve_for_x(self, x):
        if (self.is_set == 0):
            print("ERR: solve_for_x: Values have not yet been set")
            return
        value = 0
        if (isinstance(x, float)):
            return self.solve_for_x([x])
        for i in range(self.pruned_seq_length):
            term = self.pruned_y_seq[i]
            for a in range(self.num_seq):
                for j in range (self.pruned_seq_length):
                    if (i != j):
                        term *= (x[a] - self.pruned_x_seq[j + (a * self.pruned_seq_length)])
            for b in range(self.num_seq):
                for k in range (self.pruned_seq_length):
                    if (i != k):
                        term /= (self.pruned_x_seq[i + (b * self.pruned_seq_length)] - self.pruned_x_seq[k + (b *self.pruned_seq_length)])
            value += term
        return round(value, self.accuracy)
   
    def fill_in_missing_values(self):
        if (self.is_set == 0):
            print("ERR: fill_in_missing_values: Values have not yet been set")
            return
        if (self.was_pruned != 1):
            print("ERR: fill_in_missing_values: No missing values to fill in")
            return
        for i in range(self.seq_length):
            if (len(str(self.y_seq[i])) == 0):
                array = []
                for j in range(self.num_seq):
                    array.append(self.x_seq[i + (j * self.num_seq)])
                self.y_seq[i] = self.solve_for_x(array)
    
    def set_accuracy(self, accuracy):
        self.accuracy = accuracy

        
def main():
    poly = Lagrange_Poly()
    print("*********************************USING SINGLE X MODE*************************************************")
    poly.set_polynomial(8, [0.148,0.693,0.427,0.967, 0.153, 0.822, 0.191, 0.156], [13.283,"",21.053,"","","",3.507,15.006])
    poly.print_x_seq()
    poly.print_y_seq()
    poly.print_pruned_x_seq()
    poly.print_pruned_y_seq()
    poly.print_polynomial()
    print(str(poly.solve_for_x(0.693)))
    print(str(poly.solve_for_x(0.148)))
    print(str(poly.solve_for_x(0.153)))
    poly.fill_in_missing_values()
    poly.print_y_seq()
    print("***********************************PASSING A SINGLE X INTO MULTMODE*********************************************")
    poly.set_polynomial_multi(8, 1, [[0.148,0.693,0.427,0.967, 0.153, 0.822, 0.191, 0.156]], [13.283,"",21.053,"","","",3.507,15.006])
    poly.set_accuracy(3)
    poly.print_x_seq()
    poly.print_y_seq()
    poly.print_pruned_x_seq()
    poly.print_pruned_y_seq()
    poly.print_polynomial()
    print(str(poly.solve_for_x([0.693])))
    print(str(poly.solve_for_x([0.148])))
    print(str(poly.solve_for_x([0.153])))
    poly.fill_in_missing_values()
    poly.print_y_seq()
    print("************************************PASSING MULTIPLE Xs INTO MULTIMODE**********************************************")
    poly.set_polynomial_multi(8, 3, [[0.148,0.693,0.427,0.967, 0.153, 0.822, 0.191, 0.156],[8.76, 5.393,4.621,8.622,7.797, 9.968,6.115,8.401],[73.201,68.224,72.191,12.303,83.466,51.702,42.621,54.954]], [13.283,"",21.053,"","","",3.507,15.006])
    poly.print_x_seq()
    poly.print_y_seq()
    poly.print_pruned_x_seq()
    poly.print_pruned_y_seq()
    poly.print_polynomial()
    print(str(poly.solve_for_x([0.693, 5.393, 68.224])))
    print(str(poly.solve_for_x([0.967, 8.622, 12.191])))
    print(str(poly.solve_for_x([0.153, 7.797, 83.466])))
    print(str(poly.solve_for_x([0.427, 4.621, 72.191])))
    print(str(poly.solve_for_x([0.148, 8.76, 73.201])))
    poly.fill_in_missing_values()
    poly.print_y_seq()

main()