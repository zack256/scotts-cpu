import itertools as it
import sys

from transistors import NTypeTransistor, PTypeTransistor, TransistorOutput
from gates import NORGateViaTransistors, ORGate, XORGate, AND3, Decoder3X8
from latches import SRLatch

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

def test_SR_latch(over_S, over_R):
    for Q in [0, 1]:
        for Q_dash in [0, 1]:
            sr_latch = SRLatch()
            sr_latch.Q_val = Q
            sr_latch.over_Q_val = Q_dash
            try:
                res = sr_latch.evaluate({
                    "OVER_S": over_S,
                    "OVER_R": over_R
                })
                print(res)
            except Exception as e:
                print(e)

def test_byte_memory(byte_memory_cell, s, bit_string):
    res = byte_memory_cell.evaluate({
        "S": s,
    } | {
        f"IN_{i}": int(bit_string[i]) for i in range(8)
    })
    return "".join([str(res[f"O_{i}"]) for i in range(8)])

if __name__ == "__main__":
    test_gate(XORGate(), "XOR", 2)
    test_gate(AND3(), "AND3", 3)
    test_gate(Decoder3X8(), "Decoder3x8", 3, "ABC", output_no_dict=True, output_port_order=[f"D{i}" for i in range(8)])
    test_SR_latch(int(sys.argv[1]), int(sys.argv[2]))