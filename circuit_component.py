from abc import ABC, abstractmethod

from utils import ValidationException

class CircuitComponent(ABC):

    def check_io_is_valid_helper(self, voltages, required_ports):
        if len(voltages) != len(required_ports):
            raise ValidationException("Number of voltages doesn't equal number of required ports")
        for port_name in required_ports:
            if port_name not in voltages:
                raise ValidationException(f"Required port \"{port_name}\" doesn't appear in given voltages")
            port_type = required_ports[port_name]
            voltage_value = voltages[port_name]
            if port_type is None:
                if type(voltage_value) != int:
                    raise ValidationException(f"Given port \"{port_name}\" isn't an int, the required type")
                if voltage_value != 0 and voltage_value != 1:
                    raise ValidationException(f"Given port \"{port_name}\" doesn't have a voltage value of the required 0 or 1")
            else:
                if not isinstance(voltage_value, port_type):
                    raise ValidationException(f"Given port \"{port_name}\" isn't of the correct type")
                
    def check_io_is_valid(self, io_voltages, which):
        if which:   # Checking input
            try:
                return self.check_io_is_valid_helper(io_voltages, self.required_input_ports)
            except ValidationException as e:
                raise ValidationException("Error when constructing inputs!") from e
        else:       # Checking output
            try:
                return self.check_io_is_valid_helper(io_voltages, self.required_output_ports)
            except ValidationException as e:
                raise ValidationException("Error when constructing outputs!") from e
    
    @abstractmethod
    def inner_evaluate(self, input_voltages):
        pass

    def evaluate(self, input_voltages):
        # These checks are prob entirely optional and will prob slow down the program eventually.
        self.check_io_is_valid(input_voltages, True)
        output_voltages = self.inner_evaluate(input_voltages)
        self.check_io_is_valid(output_voltages, False)
        return output_voltages
