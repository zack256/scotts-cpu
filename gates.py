from circuit_component import CircuitComponent
from transistors import NTypeTransistor, PTypeTransistor, generate_VCC_voltage, generate_GND_voltage, MultipleTransistorOutputs, TransistorOutput

class NANDGate(CircuitComponent):

    required_input_ports = {
        "INPUT_1": None,
        "INPUT_2": None
    }
    required_output_ports = {
        "OUT": None
    }

    transistor_A = PTypeTransistor()
    transistor_B = NTypeTransistor()
    transistor_C = PTypeTransistor()
    transistor_D = NTypeTransistor()

    def inner_evaluate(self, input_voltages):
        input_1 = input_voltages["INPUT_1"]
        input_2 = input_voltages["INPUT_2"]
        
        transistor_A_out = self.transistor_A.evaluate({
            "RAIL": generate_VCC_voltage(),
            "GATE": input_1
        })["OUT"]
        transistor_C_out = self.transistor_C.evaluate({
            "RAIL": generate_VCC_voltage(),
            "GATE": input_2
        })["OUT"]
        transistor_D_out = self.transistor_D.evaluate({
            "RAIL": generate_GND_voltage(),
            "GATE": input_2
        })["OUT"]
        transistor_B_out = self.transistor_B.evaluate({
            "RAIL": transistor_D_out,
            "GATE": input_1
        })["OUT"]
        output = MultipleTransistorOutputs()
        output.add_output(transistor_A_out)
        output.add_output(transistor_C_out)
        output.add_output(transistor_B_out)
        return {
            "OUT": output.measure_voltage()
        }

class NOTGateViaNAND(CircuitComponent):

    required_input_ports = {
        "INPUT": None
    }
    required_output_ports = {
        "OUT": None
    }

    nand_gate = NANDGate()

    def inner_evaluate(self, input_voltages):
        nand_output = self.nand_gate.evaluate({
            "INPUT_1": input_voltages["INPUT"],
            "INPUT_2": input_voltages["INPUT"]
        })["OUT"]
        return {"OUT": nand_output}

class NOTGateViaTransistors(CircuitComponent):

    required_input_ports = {
        "INPUT": None
    }
    required_output_ports = {
        "OUT": None
    }

    transistor_P = PTypeTransistor()
    transistor_N = NTypeTransistor()
    
    def inner_evaluate(self, input_voltages):
        transistor_P_res = self.transistor_P.evaluate({
            "RAIL": generate_VCC_voltage(),
            "GATE": input_voltages["INPUT"]
        })
        transistor_N_res = self.transistor_N.evaluate({
            "RAIL": generate_GND_voltage(),
            "GATE": input_voltages["INPUT"]
        })
        output = MultipleTransistorOutputs()
        output.add_output(transistor_P_res["OUT"])
        output.add_output(transistor_N_res["OUT"])
        return {"OUT": output.measure_voltage()}

class ANDGateViaGates1(CircuitComponent):
    required_input_ports = {
        "INPUT_1": None,
        "INPUT_2": None
    }
    required_output_ports = {
        "OUT": None
    }

    nand_gate = NANDGate()
    not_gate = NOTGateViaNAND()
    
    def inner_evaluate(self, input_voltages):
        nand_output = self.nand_gate.evaluate({
            "INPUT_1": input_voltages["INPUT_1"],
            "INPUT_2": input_voltages["INPUT_2"]
        })["OUT"]
        not_output = self.not_gate.evaluate({
            "INPUT": nand_output
        })["OUT"]
        return {"OUT": not_output}

class ANDGateVia2NANDs(CircuitComponent):
    required_input_ports = {
        "INPUT_1": None,
        "INPUT_2": None
    }
    required_output_ports = {
        "OUT": None
    }

    nand_gate_1 = NANDGate()
    nand_gate_2 = NANDGate()
    
    def inner_evaluate(self, input_voltages):
        nand_1_output = self.nand_gate_1.evaluate({
            "INPUT_1": input_voltages["INPUT_1"],
            "INPUT_2": input_voltages["INPUT_2"]
        })["OUT"]
        nand_2_output = self.nand_gate_1.evaluate({
            "INPUT_1": nand_1_output,
            "INPUT_2": nand_1_output
        })["OUT"]
        return {"OUT": nand_2_output}

class ANDGateViaTransistors(CircuitComponent):
    required_input_ports = {
        "INPUT_1": None,
        "INPUT_2": None
    }
    required_output_ports = {
        "OUT": None
    }

    transistor_A = PTypeTransistor()
    transistor_B = NTypeTransistor()
    transistor_C = PTypeTransistor()
    transistor_D = NTypeTransistor()
    transistor_P = PTypeTransistor()
    transistor_N = NTypeTransistor()
    
    def inner_evaluate(self, input_voltages):

        input_1 = input_voltages["INPUT_1"]
        input_2 = input_voltages["INPUT_2"]

        transistor_A_out = self.transistor_A.evaluate({
            "RAIL": generate_VCC_voltage(),
            "GATE": input_1
        })["OUT"]
        transistor_C_out = self.transistor_C.evaluate({
            "RAIL": generate_VCC_voltage(),
            "GATE": input_2
        })["OUT"]
        transistor_D_out = self.transistor_D.evaluate({
            "RAIL": generate_GND_voltage(),
            "GATE": input_2
        })["OUT"]
        transistor_B_out = self.transistor_B.evaluate({
            "RAIL": transistor_D_out,
            "GATE": input_1
        })["OUT"]
        nand_out = MultipleTransistorOutputs([
            transistor_A_out,
            transistor_B_out,
            transistor_C_out
        ]).measure_voltage()
        transistor_P_out = self.transistor_P.evaluate({
            "RAIL": generate_VCC_voltage(),
            "GATE": nand_out
        })["OUT"]
        transistor_N_out = self.transistor_N.evaluate({
            "RAIL": generate_GND_voltage(),
            "GATE": nand_out
        })["OUT"]
        res = MultipleTransistorOutputs([
            transistor_P_out,
            transistor_N_out
        ]).measure_voltage()
        return {
            "OUT": res
        }

class NORGateViaTransistors(CircuitComponent):
    required_input_ports = {
        "INPUT_1": None,
        "INPUT_2": None
    }
    required_output_ports = {
        "OUT": None
    }

    transistor_A = NTypeTransistor()
    transistor_B = PTypeTransistor()
    transistor_C = NTypeTransistor()
    transistor_D = PTypeTransistor()
    
    def inner_evaluate(self, input_voltages):
        input_1 = input_voltages["INPUT_1"]
        input_2 = input_voltages["INPUT_2"]

        transistor_A_out = self.transistor_A.evaluate({
            "RAIL": generate_GND_voltage(),
            "GATE": input_1
        })["OUT"]
        transistor_C_out = self.transistor_C.evaluate({
            "RAIL": generate_GND_voltage(),
            "GATE": input_2
        })["OUT"]
        transistor_B_out = self.transistor_B.evaluate({
            "RAIL": generate_VCC_voltage(),
            "GATE": input_1
        })["OUT"]
        transistor_D_out = self.transistor_D.evaluate({
            "RAIL": transistor_B_out,
            "GATE": input_2
        })["OUT"]
        res = MultipleTransistorOutputs([
            transistor_A_out,
            transistor_C_out,
            transistor_D_out
        ]).measure_voltage()
        return {
            "OUT": res
        }

class ORGate(CircuitComponent):
    required_input_ports = {
        "INPUT_1": None,
        "INPUT_2": None
    }
    required_output_ports = {
        "OUT": None
    }

    nor_gate = NORGateViaTransistors()
    not_gate = NOTGateViaTransistors()

    def inner_evaluate(self, input_voltages):
        input_1 = input_voltages["INPUT_1"]
        input_2 = input_voltages["INPUT_2"]
        
        nor_gate_out = self.nor_gate.evaluate({
            "INPUT_1": input_1,
            "INPUT_2": input_2
        })["OUT"]
        not_gate_out = self.not_gate.evaluate({
            "INPUT": nor_gate_out
        })["OUT"]
        return {"OUT": not_gate_out}

class XORGate(CircuitComponent):
    required_input_ports = {
        "INPUT_1": None,
        "INPUT_2": None
    }
    required_output_ports = {
        "OUT": None
    }

    transistor_P_1 = PTypeTransistor()
    transistor_N_1 = NTypeTransistor()
    transistor_P_2 = PTypeTransistor()
    transistor_N_2 = NTypeTransistor()

    def inner_evaluate(self, input_voltages):
        input_1 = input_voltages["INPUT_1"]
        input_2 = input_voltages["INPUT_2"]

        transistor_P_1_out = self.transistor_P_1.evaluate({
            "RAIL": generate_VCC_voltage(),
            "GATE": input_1
        })["OUT"]
        transistor_N_1_out = self.transistor_N_1.evaluate({
            "RAIL": generate_GND_voltage(),
            "GATE": input_1
        })["OUT"]
        A_circuit_out = MultipleTransistorOutputs([
            transistor_P_1_out,
            transistor_N_1_out
        ]).measure_voltage()

        transistor_P_2_out = self.transistor_P_2.evaluate({
            "RAIL": TransistorOutput(True, input_1),
            "GATE": input_2
        })["OUT"]
        transistor_N_2_out = self.transistor_N_2.evaluate({
            "RAIL": TransistorOutput(True, A_circuit_out),
            "GATE": input_2
        })["OUT"]
        res = MultipleTransistorOutputs([
            transistor_P_2_out,
            transistor_N_2_out
        ]).measure_voltage()
        return {"OUT": res}

class AND3(CircuitComponent):
    required_input_ports = {
        "INPUT_1": None,
        "INPUT_2": None,
        "INPUT_3": None
    }
    required_output_ports = {
        "OUT": None
    }

    AND_gate_1 = ANDGateViaTransistors()
    AND_gate_2 = ANDGateViaTransistors()

    def inner_evaluate(self, input_voltages):
        and_1_res = self.AND_gate_1.evaluate({
            "INPUT_1": input_voltages["INPUT_1"],
            "INPUT_2": input_voltages["INPUT_2"]
        })["OUT"]
        and_2_res = self.AND_gate_2.evaluate({
            "INPUT_1": and_1_res,
            "INPUT_2": input_voltages["INPUT_3"]
        })["OUT"]
        return {"OUT": and_2_res}

class Decoder3X8(CircuitComponent):
    required_input_ports = {
        "A": None,
        "B": None,
        "C": None
    }
    required_output_ports = {f"D{i}": None for i in range(8)}

    NOT_gate_A = NOTGateViaTransistors()
    NOT_gate_B = NOTGateViaTransistors()
    NOT_gate_C = NOTGateViaTransistors()
    AND3s = [AND3() for i in range(8)]

    def inner_evaluate(self, input_voltages):

        A = input_voltages["A"]
        B = input_voltages["B"]
        C = input_voltages["C"]
        
        not_A = self.NOT_gate_A.evaluate({"INPUT": A})["OUT"]
        not_B = self.NOT_gate_B.evaluate({"INPUT": B})["OUT"]
        not_C = self.NOT_gate_C.evaluate({"INPUT": C})["OUT"]

        output = {}

        for i in range(8):
            output[f"D{i}"] = self.AND3s[i].evaluate({
                "INPUT_1": A if i % 8 >= 4 else not_A,
                "INPUT_2": B if i % 4 >= 2 else not_B,
                "INPUT_3": C if i % 2 >= 1 else not_C,
            })["OUT"]
        
        return output