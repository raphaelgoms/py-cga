from cGA import *

n = 40   # population size
l = 100  # chromossome lenght

p = sGA(n, l)
print("sGA: ", fitness(p))

p = cGA(n, l)
print("cGA: ", fitness(p))

p = fb_cGA(n, l)
print("fb_cGA: ", fitness(p))

p = ls_cGA(n, l)
print("ls_cGA: ", fitness(p))

p = pe_cGA(n, l)
print("pe_cGA: ", fitness(p))

p = pe_cGA(n, l)
print("ne_cGA: ", fitness(p))

p = cp_cGA(n, l)
print("cp_cGA: ", fitness(p))

p = cpe_cGA(n, l)
print("cpe_cGA: ", fitness(p))