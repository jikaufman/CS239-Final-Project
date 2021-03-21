# Jacob Kaufman 204 929 264
# Nikhil Arora 204 965 841
# Deutsch-Jozsa Problem:

import cirq
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
def grover():
	
	# initialize qubits with architecture in mind
	qubits = [cirq.GridQubit(1, 4), cirq.GridQubit(2, 4),\
	          cirq.GridQubit(3, 4)]

	# construct circuit
	circuit = cirq.Circuit()

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

	circuit.append([cirq.measure(q) for q in qubits])

	# check for sycamore
	cirq.google.optimized_for_sycamore(circuit=circuit, new_device=cirq.google.Sycamore, optimizer_type='sycamore')

	url = 'http://quant-edu-scalability-tools.wl.r.appspot.com/send'
	job_payload = {"circuit":cirq.to_json(circuit),\
					"email":"jacobkaufman4@gmail.com",\
					"repetitions":1000,\
					"student_id":204929264}

	return requests.post(url, json=job_payload)

# Main loop
if __name__ == "__main__":
	response = grover()
	print(response.text)

	