# Imports
import numpy as np
from math import gcd

# Quantum
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Operator

from qiskit_aer.primitives import Sampler as AerSampler

# Brute force find the r value
N = 35
a = 2
r = 1

def Satisfies(r):
    remainder = a**r % N
    print(f"{a}^({r}) mod {N} = {remainder}")
    return remainder == 1

while (not Satisfies(r)):
    r+=1 

print(f"The order r={r} satisfies the equation")

rDiv2 = int(r/2)

p = gcd(a**(rDiv2) + 1, N)
q = gcd(a**(rDiv2) - 1, N)

print(f"The prime factors of {N} are :")
print(f"q = {q}")
print(f"p = {p}")


#
# Question 2 (b)
#

# Define Variables and Initialize U Matrix 
CountingRegisterQubits = 11
InitialStateQubits = 6

x = 2
N = 35

# Function for modular exponentiation (simplified for N=35)
def c_amod35(a, power):
    if gcd(a, N) != 1:
        raise ValueError("a must be coprime to N")
    
    dimensions = 2**InitialStateQubits
    
    UMatrix = np.zeros((dimensions, dimensions))
    
    for y in range(dimensions):
        
        if y < N:
            newY = (pow(a, power) * y) % N
            UMatrix[newY, y] = 1
        else:
            UMatrix[y, y] = 1
    
    UGate = Operator(UMatrix).to_instruction()
    UGate.name = f"{a}^{power} mod 35"
    
    qc = QuantumCircuit(InitialStateQubits)
    qc.append(UGate, range(InitialStateQubits))
    return qc.to_gate(label=f"{a}^{power} mod 35").control()

# Create the Quantum Circuit
qc = QuantumCircuit(CountingRegisterQubits + InitialStateQubits, CountingRegisterQubits)

# Apply Hadamards tot he Counting Registers to create Superposition
for q in range(CountingRegisterQubits):
    qc.h(q)
    
# Initialize the Initial state to superposition sum |1> = |0001> (This is done by applying a Not operation to the last qubit in the initial state)
qc.x(-1)

# Apply the Unitary U matrices
for q in range(CountingRegisterQubits):
    qc.append(c_amod35(x, 2**q), [q] + [i+CountingRegisterQubits for i in range(InitialStateQubits)])

# Apply Invserse QFT 
qc.append(QFT(CountingRegisterQubits).inverse(), range(CountingRegisterQubits))

# Add the measurements 
qc.measure(range(CountingRegisterQubits), range(CountingRegisterQubits))

# Draw to Visualize the Matrix
qc.draw('mpl')

# Simulate the Circuit
# Initialize Circuit Simulation Components
sampler=AerSampler()
job_sim = sampler.run(qc , shots=4096 * 2**8)

# Simulate the Circuit and Plot the results in a Histogram
quasi_dists = job_sim.result().quasi_dists[0].binary_probabilities()
plot_histogram(quasi_dists, figsize=(20, 10))

# Filter the results to reduce the 
threshold = 0.02
filtered_dists = {k: v for k, v in quasi_dists.items() if v > threshold}
plot_histogram(filtered_dists, figsize=(20, 10))


# Convert the Counting register to Integers 
intKeys = list(filtered_dists.keys())
intKeyDecimals = [int(k, 2) for k in intKeys]

print(intKeys)
print(intKeyDecimals)

# Calculate the s/r or Thetas
denom = 2**CountingRegisterQubits

thetas = [i / denom for i in intKeyDecimals]

print(thetas)

thetaAdjusted = [i * 12 for i in thetas]

print(thetaAdjusted)

# Calculate the prime factors
r = 12
rDiv2 = int(r/2)

p = gcd(x**(rDiv2) + 1, N)
q = gcd(x**(rDiv2) - 1, N)

print(f"The prime factors of {N} are :")
print(f"q = {q}")
print(f"p = {p}")