# Jacob Kaufman 204 929 264
# Nikhil Arora 204 965 841
# Bernstein-Vazirani Problem:

import cirq
import requests

'''
Input: a function f: {0,1}^n → {0,1}.

Assumption: f(x) = a*x+b

Output: a,b

Notation: {0,1}^n is the set of bit strings of length n, a is an unknown bit string
of length n, * is inner product mod 2, + is addition mod 2, and b is an unknown single bit
'''

#########################################################################################
#                                  Main Code                                            #
#########################################################################################

# constructs a bernstein-vazirani circuit
# example circuit: a = 0101101, b = 0
def bernstein(error_correct=False):

	# initialize qubits with architecture in mind
	qubits = [cirq.GridQubit(0, 5), cirq.GridQubit(1, 4),\
	          cirq.GridQubit(0, 6), cirq.GridQubit(2, 5),\
	          cirq.GridQubit(2, 3), cirq.GridQubit(1, 5),\
	          cirq.GridQubit(3, 4), cirq.GridQubit(2, 4)]

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

	# turn helper qubit to 1
	circuit.append([cirq.Z(qubits[7])])

	# oracle
	circuit.append([cirq.CNOT(qubits[1], qubits[7])])
	circuit.append([cirq.CNOT(qubits[3], qubits[7])])
	circuit.append([cirq.CNOT(qubits[4], qubits[7])])
	circuit.append([cirq.CNOT(qubits[6], qubits[7])])

	# hadamards
	circuit.append([cirq.H(q) for q in qubits[:-1]])

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

	# measure
	circuit.append([cirq.measure(q) for q in qubits[:-1]])

	print(circuit)

	# check for sycamore
	cirq.google.optimized_for_sycamore(circuit=circuit, new_device=cirq.google.Sycamore, optimizer_type='sycamore')

	url = 'http://quant-edu-scalability-tools.wl.r.appspot.com/send'
	job_payload = {"circuit":cirq.to_json(circuit),\
					"email":"jacobkaufman4@gmail.com",\
					"repetitions":1000,\
					"student_id":204929264}

	return requests.post(url, json=job_payload)


if __name__ == '__main__':
	response = bernstein()
	print(response.text)
	
