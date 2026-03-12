# Imports
from math import gcd

# Quantum
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram

from qiskit_aer.primitives import Sampler as AerSampler

# Define Variables and Initialize U Matrix 
CountingRegisterQubits = 8
InitialStateQubits = 4

x = 7
N = 15

def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2,4,7,8,11,13]:
        raise ValueError("'a' must be 2,4,7,8,11 or 13")
    U = QuantumCircuit(4)
    for _iteration in range(power):
        if a in [2,13]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a in [7,8]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [4, 11]:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    c_U = U.control()
    return c_U

# Create the Quantum Circuit
qc = QuantumCircuit(CountingRegisterQubits + InitialStateQubits, CountingRegisterQubits)

# Apply Hadamards tot he Counting Registers to create Superposition
for q in range(CountingRegisterQubits):
    qc.h(q)
    
# Initialize the Initial state to superposition sum |1> = |0001> (This is done by applying a Not operation to the last qubit in the initial state)
qc.x(-1)

# Apply the Unitary U matrices
for q in range(CountingRegisterQubits):
    qc.append(c_amod15(x, 2**q), [q] + [i+CountingRegisterQubits for i in range(InitialStateQubits)])

# Apply Invserse QFT 
qc.append(QFT(CountingRegisterQubits).inverse(), range(CountingRegisterQubits))

# Add the measurements 
qc.measure(range(CountingRegisterQubits), range(CountingRegisterQubits))

# Draw to Visualize the Matrix
qc.draw('mpl')

# Simulate the Circuit
# Initialize Circuit Simulation Components
sampler=AerSampler()
job_sim = sampler.run(qc , shots=4096)

# Simulate the Circuit and Plot the results in a Histogram
quasi_dists = job_sim.result().quasi_dists[0].binary_probabilities()
plot_histogram(quasi_dists)

# Convert the Counting register to Integers 
intKeys = list(quasi_dists.keys())
intKeyDecimals = [int(k, 2) for k in intKeys]

print(intKeys)
print(intKeyDecimals)

# Calculate the s/r or Thetas
denom = 2**CountingRegisterQubits

thetas = [i / denom for i in intKeyDecimals]

print(thetas)

# Calculate the prime factors
r = 4
rDiv2 = 2

p = gcd(x**(rDiv2) + 1, N)
q = gcd(x**(rDiv2) - 1, N)

print("The prime factors of 15 are :")
print(f"q = {q}")
print(f"p = {p}")