""" Estimate standard deviation for measurement error on a quantum computer """


from qiskit import available_backends, execute

from ibmq.core import create_quantum_program_to_simulate_quantum_beats


if __name__ == "__main__":
    from qiskit import register
    import Qconfig

    register(Qconfig.APItoken, Qconfig.config["url"],
             hub=Qconfig.config["hub"],
             group=Qconfig.config["group"],
             project=Qconfig.config["project"])

    # circuit = create_quantum_program_to_simulate_quantum_beats(math.pi / 2)
    w_larmor = 0.46  # 4.6e8 1/s as determined in the experiment
    print(available_backends())
    for t in range(0, 30):
        circuit = create_quantum_program_to_simulate_quantum_beats(w_larmor*t)
        if 'ibmqx4' not in available_backends():
            raise RuntimeError("Can't execute the program on ibmqx4")

        # Execute on a quantum device
        job_real = execute(circuit, "ibmqx4")
        result_real = job_real.result()
        # Execute on simulator
        job_sim = execute(circuit, "local_qasm_simulator")
        result_sim = job_sim.result()
        singlet_sim = result_sim.get_counts(circuit).get('01', 0)
        triplet_sim = result_sim.get_counts(circuit).get('10', 0)
        singlet = result_real.get_counts(circuit).get('01', 0)
        triplet = result_real.get_counts(circuit).get('10', 0)
        state00 = result_real.get_counts(circuit).get('00', 0)
        state11 = result_real.get_counts(circuit).get('11', 0)
        # print("Result: %s, %s" % (t, result_real))
        print("%s, %s, %s, %s, %s, %s, %s" % (t, singlet_sim, triplet_sim, singlet, triplet, state00, state11))
