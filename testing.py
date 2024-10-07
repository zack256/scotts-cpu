import itertools as it

from transistors import NTypeTransistor, PTypeTransistor, TransistorOutput
from gates import NORGateViaTransistors, ORGate, XORGate, AND3, Decoder3X8


def test_gate(gate, gate_name, num_inputs, input_port_names=None, output_no_dict=False, output_port_order=None):
    print("Testing", gate_name)
    for prod in it.product((0, 1), repeat=num_inputs):
        try:
            input_dict = {}
            for i in range(num_inputs):
                if input_port_names is None:
                    port_name = f"INPUT_{i + 1}"
                else:
                    port_name = input_port_names[i]
                input_dict[port_name] = prod[i]
            res = gate.evaluate(input_dict)
            if output_no_dict:
                if output_port_order is None:
                    raise Exception("If \"output_no_dict\" is requested, then \"output_port_order\" must be provided")
                print(prod, "".join(str(res[port]) for port in output_port_order))
            else:
                print(prod, res)
        except Exception as e:
            print(prod, "Error occured!", e)

if __name__ == "__main__":
    test_gate(XORGate(), "XOR", 2)
    test_gate(AND3(), "AND3", 3)
    test_gate(Decoder3X8(), "Decoder3x8", 3, "ABC", output_no_dict=True, output_port_order=[f"D{i}" for i in range(8)])