from pyquil.quil import Program
from pyquil.gates import Z, X, H, CNOT, PHASE
from pyquil.api import QVMConnection, get_devices, QPUConnection, CompilerConnection


def distribution(data):
    """ Distribution of measurement of quantum system """
    combinations = {}
    for result in data:
        result_as_tuple = tuple(result)
        if result_as_tuple not in combinations:
            combinations[result_as_tuple] = 0
        combinations[result_as_tuple] += 1
    return combinations


if __name__ == '__main__':
    agave = get_devices(as_dict=True)['8Q-Agave']
    qpu = QPUConnection(agave)  # Physical QPU
    compiler = CompilerConnection(agave)

    p = Program()

    p.inst(X(0))
    p.inst(X(0))
    p.inst(X(1))
    p.inst(X(2))
    p.inst(X(3))
    p.inst(X(4))
    p.inst(X(5))
    p.measure(0, 0)
    p.measure(1, 1)
    p.measure(2, 2)
    p.measure(3, 3)
    p.measure(4, 4)
    p.measure(5, 5)
    data_qpu = qpu.run(p, trials=100)
    print(distribution(data_qpu))
    # print(data_qpu.ge)

    # Should measure number of errors (bit flips). Can be different for different qubits, too
    p = Program("""#   prepare a Bell state
H 0
CNOT 0 1
#   wait a while
PRAGMA PRESERVE_BLOCK
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
X 0
X 1
PRAGMA END_PRESERVE_BLOCK
#   and read out the results
MEASURE 0 [0]
MEASURE 1 [1]""")
    job_id = compiler.compile_async(p)
    job = compiler.wait_for_job(job_id)
    print(job.compiled_quil())
    data_qpu = qpu.run(p, trials=1024)
    print(distribution(data_qpu))
