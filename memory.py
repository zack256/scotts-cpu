from circuit_component import CircuitComponent
from latches import DLatch
from transistors import TriState, TransistorOutput

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

class ByteEnabler(CircuitComponent):
    
    required_input_ports = {
        f"IN_{i}": None for i in range(8)
    } |  {"E": None}

    required_output_ports = {
        f"O_{i}": TransistorOutput for i in range(8)
    }

    tri_states = [
        TriState() for i in range(8)
    ]

    def inner_evaluate(self, input_voltages):
        return {
            f"O_{i}": self.tri_states[i].evaluate({
                "IN": input_voltages[f"IN_{i}"],
                "E": input_voltages["E"]
            })["OUT"] for i in range(8)
        }

class ByteRegister(CircuitComponent):
    
    required_input_ports = {
        "S": None,
        "E": None
    } | {
        f"IN_{i}": None for i in range(8)
    }
    required_output_ports = {
        f"O_{i}": TransistorOutput for i in range(8)
    }

    byte_enabler = ByteEnabler()

    def __init__(self):
        self.byte_memory_cell = ByteMemoryCell()
    
    def inner_evaluate(self, input_voltages):
        
        memory_output = self.byte_memory_cell.evaluate({
            "S": input_voltages["S"]
        } | {
            f"IN_{i}": input_voltages[f"IN_{i}"] for i in range(8)
        })

        return self.byte_enabler.evaluate({
            "E": input_voltages["E"]
        } | {
            f"IN_{i}": memory_output[f"O_{i}"] for i in range(8)
        })
