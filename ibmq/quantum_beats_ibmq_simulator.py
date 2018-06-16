import math
from qiskit import QuantumProgram
from qiskit import available_backends, execute


def create_quantum_program_to_simulate_quantum_beats(lambda_angle):
    # Creating Programs# Creat
    # create your first QuantumProgram object instance.
    qp = QuantumProgram()

    # Creating Registers
    # create your first Quantum Register called "qr" with 2 qubits
    qr = qp.create_quantum_register('qr', 2)
    # create your first Classical Register  called "cr" with 2 bits
    classical_r = qp.create_classical_register('cr', 2)

    # Creating Circuits
    # create your first Quantum Circuit called "qc" involving your Quantum Register "qr"
    # and your Classical Register "cr"
    circuit = qp.create_circuit('qc', [qr], [classical_r])

    # Put system into singlet state
    circuit.x(qr[0])
    circuit.h(qr[1])
    circuit.cx(qr[1], qr[0])
    circuit.z(qr[1])

    # Timestep
    circuit.u1(lambda_angle, qr[1])

    # Measure the system state - implement the operation below
    # [
    # [1,     0,          0,     0]
    # [0, 1/sqrt(2),  1/sqrt(2), 0]
    # [0, 1/sqrt(2), -1/sqrt(2), 0]
    # [0,     0,          0,     1]
    # ]
    # Using quantum circuit from  https://arxiv.org/pdf/1206.0758.pdf

    # cx q[3],q[4];
    circuit.cx(qr[0], qr[1])
    # s q[3];
    circuit.s(qr[0])
    # s q[4];
    circuit.s(qr[1])
    # h q[3];
    circuit.h(qr[0])
    # cx q[3],q[4];
    circuit.cx(qr[0], qr[1])
    # t q[3];
    circuit.t(qr[0])

    # tdg q[4];
    circuit.tdg(qr[1])

    # cx q[3],q[4];
    circuit.cx(qr[0], qr[1])

    # h q[3];
    circuit.h(qr[0])

    # cx q[3],q[4];
    circuit.cx(qr[0], qr[1])

    # sdg q[4];
    circuit.sdg(qr[1])

    circuit.measure(qr[0], classical_r[0])
    circuit.measure(qr[1], classical_r[1])
    return circuit


if __name__ == "__main__":
    # circuit = create_quantum_program_to_simulate_quantum_beats(math.pi / 2)
    circuit = create_quantum_program_to_simulate_quantum_beats(math.pi/3)
    job_sim = execute(circuit, "local_qasm_simulator")
    sim_result = job_sim.result()
    # Execute on a quantum device
    # result_real = qp.execute(["qc"], shots=1024, max_credits=3, wait=10, timeout=240)

    # print("simulation: ", sim_result)
    # print(sim_result.get_counts(circuit)['01'])
    # print(sim_result.get_counts(circuit)['10'])

    for t in range(0, 30):
        w_larmor = 0.46  # 4.6e8 1/s as determined in the experiment

        circuit = create_quantum_program_to_simulate_quantum_beats(w_larmor * t)
        job_sim = execute(circuit, "local_qasm_simulator")
        sim_result = job_sim.result()
        singlet = sim_result.get_counts(circuit).get('01', 0)
        triplet = sim_result.get_counts(circuit).get('10', 0)
        print("%s, %s, %s" % (t, singlet, triplet))

