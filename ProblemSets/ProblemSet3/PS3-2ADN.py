# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Quantum
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector

from qiskit_aer import AerSimulator

# Load the Datafile
df = pd.read_csv('raw_signal_data.csv', header=None, skiprows=1)
signal = df.iloc[:, 1].values
signal = signal.astype(float)

# Define some of the data properties
N = 1024
T = 1.0
dt = T / N

# Create a Time Array
t = np.linspace(0, T, N, endpoint=False)

# Compute the Fast Fourier Transform
FFTResult = np.fft.fft(signal)

# Get the Frequency bins
frequencies = np.fft.fftfreq(N, d=dt)

# Get the Positive / Nyquist Frequencies only
NyquistMask = frequencies > 0
NyquistFreq = frequencies[NyquistMask]
NyquistFFT = FFTResult[NyquistMask]

# Compute the Magnitudes of the Frequencies
Magnitudes = 2.0 / N * np.abs(NyquistFFT)

# Compute the Phase
Phase = np.angle(NyquistFFT)

# Display the frequencies that have magntiudes larger than 10% of the Max magnitude
threshold = np.max(Magnitudes) * 0.1
PeakIndices = np.where(Magnitudes > threshold)[0]

for idx in PeakIndices:
    print(f"Freq: {NyquistFreq[idx]:.2f} Hz | Mag: {Magnitudes[idx]:.2f} | Phase: {Phase[idx]:.2f} rad")

if len(PeakIndices) >= 2:
    idx1, idx2, idx3 = PeakIndices[0], PeakIndices[1], PeakIndices[2]
    idx2, idx2 = PeakIndices[0], PeakIndices[1]
    phase_diff1 = abs(Phase[idx1] - Phase[idx2])
    phase_diff2 = abs(Phase[idx2] - Phase[idx3])
    print(f"\nRelative phase difference: {phase_diff1:.2f} and {phase_diff2:.2f} radians.")

# Plot the Data
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))

# Plot the Raw Signal
ax1.plot(t, signal, color='blue')
ax1.set_title('Raw Signal')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.grid(True)

# Plot the Magnitudes vs Frequency
ax2.plot(NyquistFreq, Magnitudes, color='red')
ax2.set_title('Analyzed Frequency Components')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Magnitude (Relative Units)')
ax2.set_xlim(0, max(NyquistFreq)) # Limit to positive frequencies
ax2.grid(True)

plt.tight_layout()
plt.show()

#
# Question 2 (b)
#

# Load the Datafile
df = pd.read_csv('raw_signal_data.csv', header=None, skiprows=1)
signal = df.iloc[:, 1].values
signal = signal.astype(float)

# Normalize the Signal
NormalizedSignal = signal / np.linalg.norm(signal)
print(NormalizedSignal)

# Create the Quantum Circuit
NQubits = 10
qc = QuantumCircuit(NQubits)

# Initialize the Circuit with the Normalized Signal
qc.initialize(NormalizedSignal, qc.qubits)

# Add the Built in QFT circuit
QFTCircuit = QFT(num_qubits=NQubits, approximation_degree=0, do_swaps=True, inverse=False)
qc.append(QFTCircuit, qc.qubits)

# Measure all the Qubits at the end of the Circuit
qc.measure_all()

# Draw the Circuit
qc.draw("mpl")

# Run the AerSimulator
simulator = AerSimulator()
CompiledCircuit = transpile(qc, simulator)
job = simulator.run(CompiledCircuit, shots=4096)
result = job.result()
counts = result.get_counts()

# Plot the Magntiudes vs Frequency Components
plot_histogram(counts, title="Quantum Frequency Components (Magnitude Squared)", figsize=(16, 10))

#
# Question 3 (c)
#

# Load the Datafile
df = pd.read_csv('raw_signal_data.csv', header=None, skiprows=1)
signal = df.iloc[:, 1].values
signal = signal.astype(float)

# Define some of the data properties
N = 1024
T = 1.0
dt = T / N

# Normalize the Signal
norm = np.linalg.norm(signal)
NormalizedSignal = signal / norm

# Create the Quantum Circuit
NQubits = 10
qc = QuantumCircuit(NQubits)

# Initialize the Circuit with the Normalized Signal
qc.initialize(NormalizedSignal, qc.qubits)

# Add the Built in QFT circuit
QFTCircuit = QFT(num_qubits=NQubits, approximation_degree=0, do_swaps=True, inverse=False)
qc.append(QFTCircuit, qc.qubits)

# Simulate the Circuit State without Measuring, this allows us to preserve the Phase of the data
state = Statevector(qc)
ComplexAmplitudes = np.asarray(state)

# Extract the Magnitudes and Phase
Phase = np.angle(ComplexAmplitudes)
QuantumAmplitudes = np.abs(ComplexAmplitudes)
QuantumMagnitudes = QuantumAmplitudes * (2.0 * norm / np.sqrt(N))

# Get the Frequency bins
frequencies = np.fft.fftfreq(N, d=dt)

# Get the Positive / Nyquist Frequencies only
NyquistMask = frequencies > 0
NyquistFreq = frequencies[NyquistMask]
NyquistProbabilities = QuantumMagnitudes[NyquistMask]
NyquistPhases = Phase[NyquistMask]

# 5. Find dominant frequencies and phase difference
threshold = np.max(NyquistProbabilities) * 0.1
PeakIndices = np.where(NyquistProbabilities > threshold)[0]

print("Quantum Simulated Dominant Frequencies:")
for idx in PeakIndices:
    print(f"Freq: {NyquistFreq[idx]:.2f} Hz | Prob: {NyquistProbabilities[idx]:.4f} | Phase: {NyquistPhases[idx]:.2f} rad")

if len(PeakIndices) >= 2:
    idx1, idx2, idx3 = PeakIndices[0], PeakIndices[1], PeakIndices[2]
    idx2, idx2 = PeakIndices[0], PeakIndices[1]
    phase_diff1 = abs(NyquistPhases[idx1] - NyquistPhases[idx2])
    phase_diff2 = abs(NyquistPhases[idx2] - NyquistPhases[idx3])
    print(f"\nRelative phase difference: {phase_diff1:.2f} and {phase_diff2:.2f} radians.")

# 6. Plotting
plt.figure(figsize=(10, 5))
plt.plot(NyquistFreq, NyquistProbabilities, color='purple')
plt.title('Quantum Simulated Frequency Spectrum (Statevector)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Measurement Probability')
plt.xlim(0, max(NyquistFreq))
plt.grid(True)
plt.tight_layout()
plt.show()


