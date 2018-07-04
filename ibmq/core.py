from qiskit import QuantumProgram


def create_quantum_program_to_simulate_quantum_beats(lambda_angle):
    # create QuantumProgram object instance.
    qp = QuantumProgram()

    # Creating Registers
    # create Quantum Register called "qr" with 2 qubits
    qr = qp.create_quantum_register('qr', 2)
    # create Classical Register  called "cr" with 2 bits
    classical_r = qp.create_classical_register('cr', 2)

    # Creating Circuits
    # create Quantum Circuit called "qc" involving Quantum Register "qr"
    # and lassical Register "cr"
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