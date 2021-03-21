# Jacob Kaufman 204 929 264
# Nikhil Arora 204 965 841
# Deutsch-Jozsa Problem:

import cirq
from qiskit import IBMQ, assemble, transpile
from qiskit.circuit import QuantumCircuit as qiskitqc
import requests


'''
Input: a function f: {0,1}^n → {0,1}.

Output: a1 if there exists x in {0,1}^n such that f(x) = 1, and 0 otherwise

Notation: {0,1}^n is the set of bit strings of length n.

'''

#########################################################################################
#                                  Main Code                                            #
#########################################################################################

# Grover's algorithm implementation and simulation
# oracle string = 111, 3 qubits
def grover(error_correct=False):

	API_TOKEN = '7cf33cd2f0d7044af8518c33321fa74d7380d3ba58d08b271404e8226aa1f5490818ba86e1635f89e6c3cfbf10aa091ff04c1f5ff61f0f391ed780b4484e0b18'

	# initialize qiskit
	IBMQ.save_account(API_TOKEN)
	provider = IBMQ.load_account()
	print(provider.backends())
	backend = provider.backends.ibmq_16_melbourne
	
	# initialize qubits with architecture in mind
	qubits = [cirq.GridQubit(1, 4), cirq.GridQubit(2, 4),\
	          cirq.GridQubit(3, 4)]

	if error_correct:
		error_qubits = [cirq.GridQubit(3, 4), cirq.GridQubit(3, 3),\
	                    cirq.GridQubit(3, 2), cirq.GridQubit(4, 3)]

	# construct circuit
	circuit = cirq.Circuit()

	# error correction setup. error correct qubit (2,3)
	if error_correct:
		circuit.append([cirq.CNOT(qubits[2], error_qubits[1])])
		circuit.append([cirq.SWAP(error_qubits[0], error_qubits[1])])
		circuit.append([cirq.CNOT(qubits[2], error_qubits[1])])
		circuit.append([cirq.SWAP(error_qubits[0], error_qubits[1])])

	# hadamards
	circuit.append([cirq.H(q) for q in qubits])

	# Grover's algorithm repetitions; O(sqrt(2^n)) = 2
	for _ in range(2):

		circuit.append([cirq.CCZ(*qubits)])

		circuit.append([cirq.H(q) for q in qubits])
		circuit.append([cirq.X(q) for q in qubits])
		circuit.append([cirq.CCZ(*qubits)])
		circuit.append([cirq.X(q) for q in qubits])
		circuit.append([cirq.H(q) for q in qubits])

	# error detection and correction
	if error_correct:
		circuit.append([cirq.SWAP(error_qubits[2], error_qubits[1])])
		circuit.append([cirq.CNOT(qubits[2], error_qubits[1])])
		circuit.append([cirq.SWAP(error_qubits[2], error_qubits[1])])
		circuit.append([cirq.CNOT(error_qubits[1], error_qubits[2])])
		circuit.append([cirq.SWAP(error_qubits[3], error_qubits[1])])
		circuit.append([cirq.CNOT(qubits[2], error_qubits[1])])
		circuit.append([cirq.CNOT(error_qubits[0], error_qubits[1])])
		circuit.append([cirq.SWAP(error_qubits[1], error_qubits[3])])
		circuit.append([cirq.measure(error_qubits[2]), cirq.measure(error_qubits[3])])
		circuit.append([cirq.CCNOT(qubits[2], error_qubits[1], error_qubits[0])])

	circuit.append([cirq.measure(q) for q in qubits])

	# export to qasm
	qasm_str = circuit.to_qasm()

	# import qiskit from qasm
	qiskit_circuit = qiskitqc.from_qasm_str(qasm_str)

	# run qiskit
	transpiled = transpile(qiskit_circuit, backend)
	qobj = assemble(transpiled, backend, shots=100)
	job = backend.run(qobj)
	print(job.job_id())
	result = job.result()
	counts = result.get_counts()
	delayed_result = backend.retrieve_job(job.job_id()).result()
	delayed_counts = delayed_result.get_counts()
	print(counts)
	print(delayed_counts)


# Main loop
if __name__ == "__main__":
	response = grover()

	