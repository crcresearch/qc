include "qelib1.inc";
qreg q[5];
creg c[5];

// Put system into Singlet state
x q[3];
h q[4];
cx q[4],q[3];
z q[4];

// Implement SWITCH_TO_SINGLET_TRIPLET_BASIS operation
//
// [1, 0, 0, 0]
//[0, 1/sqrt(2), 1/sqrt(2), 0]
//[0, 1/sqrt(2), -1/sqrt(2), 0]
//[0, 0, 0, 1]
// Using quantum circuit from  https://arxiv.org/pdf/1206.0758.pdf
cx q[3],q[4];
s q[3];
s q[4];
h q[3];
cx q[3],q[4];
t q[3];
tdg q[4];
cx q[3],q[4];
h q[3];
cx q[3],q[4];
sdg q[4];

// Measure results in single/triple basis
measure q[4] -> c[4];
measure q[3] -> c[3];
