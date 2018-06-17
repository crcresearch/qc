import math
import numpy as np

from pyquil.quil import Program
from pyquil.gates import Z, X, H, CNOT, PHASE
from pyquil.api import QVMConnection, get_devices


def distribution(data):
    """ Distribution of measurement of quantum system """
    combinations = {}
    for result in data:
        result_as_tuple = tuple(result)
        if result_as_tuple not in combinations:
            combinations[result_as_tuple] = 0
        combinations[result_as_tuple] += 1
    return combinations


def create_singlet_state():
    """ Returns quantum program that constructs a Singlet state of two spins """

    p = Program()

    # Start by constructing a Triplet state of two spins (Bell state)
    # 10|> + 01|>
    # https://en.wikipedia.org/wiki/Triplet_state
    #
    p.inst(X(0))
    p.inst(H(1))
    p.inst(CNOT(1, 0))

    # Convert to Singlet
    # 01|> - 10|>
    # https://en.wikipedia.org/wiki/Singlet_state
    #
    p.inst(Z(1))

    return p


def add_switch_to_singlet_triplet_basis_gate_to_program(program):
    """ Adds SWITCH_TO_SINGLET_TRIPLET_BASIS gate to a quantum program"""

    # The "SWITCH_TO_SINGLET_TRIPLET_BASIS" gate
    # will represent the system in singlet/triplet basis
    # 11|> will mean Singlet state, and 00|> will mean Triplet state
    my_array = np.array([
        [1, 0, 0, 0],
        [0, 1 / math.sqrt(2), 1 / math.sqrt(2), 0],
        [0, 1 / math.sqrt(2), -1 / math.sqrt(2), 0],
        [0, 0, 0, 1],
    ])
    program.defgate("SWITCH_TO_SINGLET_TRIPLET_BASIS", my_array)


def main():
    qvm = QVMConnection()
    agave = get_devices(as_dict=True)['8Q-Agave']
    qvm_noisy = QVMConnection(agave)
    print("Timestamp, Singlet (Wavefunction), Triplet (Wavefunction), Singlet (QVM), Triplet (QVM),"
          "Singlet (Noise), Triplet (Noise), 00 (Noise), 11 (Noise)")
    # Rotation
    for t in range(0, 50):  # ns
        p = create_singlet_state()
        add_switch_to_singlet_triplet_basis_gate_to_program(p)
        w_larmor = 0.46  # 4.6e8 1/s as determined in the experiment
        p.inst(PHASE(w_larmor * t, 0))
        p.inst(("SWITCH_TO_SINGLET_TRIPLET_BASIS", 0, 1))
        wavefunction = qvm.wavefunction(p)
        probs = wavefunction.get_outcome_probs()

        p.measure(0, 0)
        p.measure(1, 1)
        data = qvm.run(p, trials=1000)

        # simulate physical noise on QVM
        data_noisy = qvm_noisy.run(p, trials=1000)
        noisy_data_distr = distribution(data_noisy)

        print("%s, %s, %s, %s, %s, %s, %s, %s ,%s" %
              (t, probs['01'], probs['10'],
               distribution(data).get((0, 1), 0), distribution(data).get((1, 0), 0),
               noisy_data_distr.get((0, 1), 0), noisy_data_distr.get((1, 0), 0),
               noisy_data_distr.get((0, 0), 0), noisy_data_distr.get((1, 1), 0),
               )
              )


if __name__ == '__main__':
    main()
