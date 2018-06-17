# Simulating chemical systems on a quantum computer

This is a repository for code to simulate Quantum beats (Dynamic singlet–triplet transitions) in spin-correlated radical pairs
on a quantum computer. We are going to use Riggeti Forest and IBM Q as our platforms.
Modeling quantum beats might be one of the applications where quantum supremacy can be demonstrated.

This effect was discovered in 1976 by J. Klein and R. Voltz and B. Brocklehurst and developed into a spectroscopic tecnique by professor Yu N Molin's group in Russia.
Please refer to the 2007 review by V A Bagryansky, V I Borovkov and Yu N Molin http://iopscience.iop.org/article/10.1070/RC2007v076n06ABEH003715/pdf for additional information.

# Usage - Rigetti Forest platform - QVM

Follow instructions on http://pyquil.readthedocs.io/en/latest/start.html page. I personally prefer creating a separate virtual environment for every project, but it is a matter of taste. 

You will need to request a Forest API key. I got mine in a minute after request. 

Run the program:
```
python quantum_beats_rigetti_qvm.py
```

# Usage - Rigetti Forest platform - QPU (In progress)

To run the code on a physical Quantum Processing Unit, you will have to request timeslot on https://www.rigetti.com/qpu-request
My request was approved in a couple of hours, and I got 2 hour timeslot for day after tomorrow.

... 

# Usage - IBM Q platform - simulator

Follow instructions on https://github.com/QISKit/qiskit-core#installation-1

You don't need to provide credentials if you just run your code on simulator.


# Usage - IBM Q platform - physical device

Same as running on the simulator, but you should Create 'Qconfig.py' file in ibmq directory. Put in your API token

```python
APItoken = 'Your IBM Q API token'

config = {
    'url': 'https://quantumexperience.ng.bluemix.net/api',

    # If you have access to IBM Q features, you also need to fill the "hub",
    # "group", and "project" details. Replace "None" on the lines below
    # with your details from Quantum Experience, quoting the strings, for
    # example: 'hub': 'my_hub'
    # You will also need to update the 'url' above, pointing it to your custom
    # URL for IBM Q.
    'hub': None,
    'group': None,
    'project': None
}
```
