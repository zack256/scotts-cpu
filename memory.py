from circuit_component import CircuitComponent
from latches import DLatch

class BitMemoryCell(CircuitComponent):

    required_input_ports = {
        "IN": None,
        "S": None
    }
    required_output_ports = {
        "O": None
    }

    def __init__(self):
        self.DLatch = DLatch()
    
    def inner_evaluate(self, input_voltages):
        output = self.DLatch.evaluate({
            "IN": input_voltages["IN"],
            "SET": input_voltages["S"]
        })["Q"]
        return { "O": output }

class ByteMemoryCell(CircuitComponent):

    required_input_ports = {
        "S": None,
    } | {
        f"IN_{i}": None for i in range(8)
    }
    required_output_ports = {
        f"O_{i}": None for i in range(8)
    }

    def __init__(self):
        self.memory_bit_cells = [
            BitMemoryCell() for i in range(8)
        ]
    
    def inner_evaluate(self, input_voltages):
        s_input = input_voltages["S"]
        return {
            f"O_{i}": self.memory_bit_cells[i].evaluate({
                "IN": input_voltages[f"IN_{i}"],
                "S": s_input 
            })["O"] for i in range(8)
        }