from abc import abstractmethod

from circuit_component import CircuitComponent

# Apparently everything has access to these rails?
GND = 0
VCC = 1

class TransistorOutput:
    # Transistor output is different than regular gate outputs, because they can be connected or unconnected.
    # If they are connected, then they have voltage, otherwise they don't have voltage.
    def __init__(self, connected, voltage):
        if not connected and voltage is not None:
            raise Exception("Voltage must be None if transistor is not connected.")
        self.connected = bool(connected)
        self.voltage = voltage
    def __repr__(self):
        return f"TransistorOutput(connected={self.connected}, voltage={self.voltage})"
    def copy(self):
        return TransistorOutput(self.connected, self.voltage)

class UnconnectedTransistorOutput(TransistorOutput):
    def __init__(self):
        super().__init__(False, None)

class ConnectedTransistorOutput(TransistorOutput):
    def __init__(self, voltage):
        super().__init__(True, voltage)

def generate_VCC_voltage():
    return ConnectedTransistorOutput(VCC)

def generate_GND_voltage():
    return ConnectedTransistorOutput(GND)

class MultipleTransistorOutputs:

    connected = False
    voltage = None
    
    def __init__(self, transistor_outputs=None):
        if transistor_outputs is not None:
            self.add_outputs(transistor_outputs)

    def add_output(self, transistor_output):
        if transistor_output.connected:
            if self.connected:
                if self.voltage != transistor_output.voltage:
                    raise Exception("MultipleTransistorOutputs: getting mixed voltages!")
            else:
                self.connected = True
                self.voltage = transistor_output.voltage
    
    def add_outputs(self, transistor_outputs):
        for transistor_output in transistor_outputs:
            self.add_output(transistor_output)
    
    def measure_voltage(self):
        if self.connected:
            return self.voltage
        raise Exception("MultipleTransistorOutputs: measuring voltage but no connected voltage was added!")


class Transistor(CircuitComponent):

    required_input_ports = {
        "RAIL": TransistorOutput,
        "GATE": None
    }
    required_output_ports = {
        "OUT": TransistorOutput
    }

    @abstractmethod
    def transistor_evaluate(self, input_voltages):
        pass

    def inner_evaluate(self, input_voltages):
        return self.transistor_evaluate(input_voltages)

class NTypeTransistor(Transistor):
    
    def transistor_evaluate(self, input_voltages):
        rail_voltage = input_voltages["RAIL"]
        gate_voltage = input_voltages["GATE"]
        
        res = None
        if gate_voltage:
            res = rail_voltage.copy()
        else:
            res = UnconnectedTransistorOutput()
        return {"OUT": res}

class PTypeTransistor(Transistor):
    
    def transistor_evaluate(self, input_voltages):
        rail_voltage = input_voltages["RAIL"]
        gate_voltage = input_voltages["GATE"]
        
        res = None
        if not gate_voltage:
            res = rail_voltage.copy()
        else:
            res = UnconnectedTransistorOutput()
        return {"OUT": res}
