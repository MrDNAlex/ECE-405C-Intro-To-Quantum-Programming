# Imports
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector

# Defining the Function
def CreateModulo2Circuit(nQubits) -> QuantumCircuit:
    """Created a Circuit to compute  f(x) = x mod 2 for a N-Qubit System"""
    qc = QuantumCircuit(nQubits)
    qc.cx(0, nQubits - 1)    
    return qc

# Generating the circuits
for i in range(2, 10, 2):
    n = i
    my_circuit = CreateModulo2Circuit(n)
    print(f"Circuit for {n} qubits generated.")
    print(my_circuit.draw())