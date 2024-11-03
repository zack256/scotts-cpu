import random

from circuit_component import CircuitComponent
from gates import NANDGate
from utils import rand_01

class SRLatch(CircuitComponent):
    # Might be referred to not just a "SR" latch, but with an overline above the "SR".

    required_input_ports = {
        "OVER_S": None,
        "OVER_R": None
    }
    required_output_ports = {
        "Q": None,
        "OVER_Q": None      # prob unused
    }

    NAND_1 = NANDGate()
    NAND_2 = NANDGate()

    Q_val = rand_01()
    over_Q_val = rand_01()

    def inner_evaluate(self, input_voltages):
        
        over_S = input_voltages["OVER_S"]
        over_R = input_voltages["OVER_R"]

        if over_S == 0 and over_R == 0:
            raise Exception("For SR Latch, both inputs cannot be 0")
    
        # Basically we have the 2 NAND gates alternate randomly. I'll go over it later but I think this accurately represents the behavior we want from the SR latch.

        r = rand_01()

        while True:
            old_Q_val = self.Q_val
            old_over_Q_val = self.over_Q_val
            unchanged = True
            if r:
                # NAND_1 evals before NAND_2.
                self.Q_val = self.NAND_1.evaluate({
                    "INPUT_1": over_S,
                    "INPUT_2": self.over_Q_val
                })["OUT"]
                if self.Q_val != old_Q_val:
                    unchanged = False
                self.over_Q_val = self.NAND_2.evaluate({
                    "INPUT_1": self.Q_val,
                    "INPUT_2": over_R
                })["OUT"]
                if self.over_Q_val != old_over_Q_val:
                    unchanged = False
            else:
                # NAND_2 evals before NAND_1.
                self.over_Q_val = self.NAND_2.evaluate({
                    "INPUT_1": self.Q_val,
                    "INPUT_2": over_R
                })["OUT"]
                if self.over_Q_val != old_over_Q_val:
                    unchanged = False
                self.Q_val = self.NAND_1.evaluate({
                    "INPUT_1": over_S,
                    "INPUT_2": self.over_Q_val
                })["OUT"]
                if self.Q_val != old_Q_val:
                    unchanged = False
            if unchanged:
                break
        
        return {
            "Q": self.Q_val,
            "OVER_Q": self.over_Q_val
        }