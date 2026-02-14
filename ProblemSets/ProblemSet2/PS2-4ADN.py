# Imports
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Function Definition
def CreateDeutschJonesCircuit(n, case="balanced"):
    
    # Size of N + 1 Ancilla Qubit
    DJCircuit = QuantumCircuit(n+1, n)
    
    # Initialize an Ancilla Qubit with |1> state, and apply Hadamard to all other Qubits
    DJCircuit.x(n)
    for q in range(n+1):
        DJCircuit.h(q)
        
    DJCircuit.barrier()
    
    # Add an Oracle to the Circuit
    if case == "balanced":
        for q in range(n):
            DJCircuit.cx(q, n)
            
    elif case == "constant":
        if np.random.randint(2) == 1:
            DJCircuit.x(n)
            
    DJCircuit.barrier()
    
    
    # Apply the Hadamard to the Input register and measure it 
    for q in range(n):
        DJCircuit.h(q)
        
    for q in range(n):
        DJCircuit.measure(q, q)
        
    return DJCircuit    

# Using the Deutsch Jones
n=5
Case = "balanced"

circuit = CreateDeutschJonesCircuit(n, Case)
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(circuit, simulator)
result = simulator.run(compiled_circuit, shots=1024).result()
counts = result.get_counts()

print(f"Results for {n}-qubit {Case} function:")
print(counts)

if '00000' in counts and counts['00000'] == 1024:
    print("Result: The function is CONSTANT.")
else:
    print("Result: The function is BALANCED.")
    
    
n=5
Case = "constant"

circuit = CreateDeutschJonesCircuit(n, Case)
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(circuit, simulator)
result = simulator.run(compiled_circuit, shots=1024).result()
counts = result.get_counts()

print(f"Results for {n}-qubit {Case} function:")
print(counts)

if '00000' in counts and counts['00000'] == 1024:
    print("Result: The function is CONSTANT.")
else:
    print("Result: The function is BALANCED.")
