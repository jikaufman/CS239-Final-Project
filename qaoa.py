# Jacob Kaufman 204 929 264
# Nikhil Arora 204 965 841
# QAOA (MaxSat):

import cirq
import requests
import math
import networkx as nx


'''
QAOA Implementation for the MaxCut problem

'''

#########################################################################################
#                                  Main Code                                            #
#########################################################################################

# QAOA implementation, n=3
def qaoa():
	
	# initialize qubits with architecture in mind
	qubits = [cirq.GridQubit(1, 4), cirq.GridQubit(2, 4),\
	          cirq.GridQubit(3, 4)]

	# initialize variables
	beta = math.pi/2
	gamma = math.pi/2

	graph = nx.Graph()
	graph.add_edge(0, 1)
	graph.add_edge(1, 2)
	graph.add_edge(2, 0)

	# construct circuit
	circuit = cirq.Circuit()

	circuit.append([cirq.H(q) for q in qubits])
	
	circuit.append([cirq.ZZPowGate(exponent=2 * gamma / math.pi, global_shift=-0.5).on(qubits[0], qubits[1])])
	circuit.append([cirq.ZZPowGate(exponent=2 * gamma / math.pi, global_shift=-0.5).on(qubits[1], qubits[2])])
	circuit.append([cirq.SWAP(qubits[1], qubits[2])])
	circuit.append([cirq.ZZPowGate(exponent=2 * gamma / math.pi, global_shift=-0.5).on(qubits[0], qubits[1])])
	circuit.append([cirq.SWAP(qubits[1], qubits[2])])

	circuit.append([cirq.rx(2*beta).on_each(*qubits)])
	circuit.append([cirq.measure(*qubits)])

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

	response = qaoa()
	print(response.text)

