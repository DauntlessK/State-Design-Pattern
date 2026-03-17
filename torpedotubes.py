from abc import ABC, abstractmethod

class TubeBank:
    def __init__(self, name, tube_count):
        self.name = name
        self.tube_count = tube_count
        self.tubes = [None] * tube_count
        self.state = OperationalState()

    def load_tube(self, index, weapon):
        self.state.load_tube(self, index, weapon)

    def fire_tube(self, index):
        self.state.fire_tube(self, index)

    def repair(self):
        self.state.repair(self)

    def take_damage(self, severity="medium"):
        self.state.take_damage(self, severity)

class TubeBankState(ABC):
    @abstractmethod
    def load_tube(self, bank, index, weapon):
        pass

    @abstractmethod
    def fire_tube(self, bank, index):
        pass

    @abstractmethod
    def repair(self, bank):
        pass

    @abstractmethod
    def take_damage(self, bank, severity):
        pass

class OperationalState(TubeBankState):
    def load_tube(self, bank, index, weapon):
        if bank.tubes[index] is None:
            bank.tubes[index] = weapon
            print(f"{bank.name}: Loaded tube {index} with {weapon}")
        else:
            print(f"{bank.name}: Tube {index} already loaded")

    def fire_tube(self, bank, index):
        if bank.tubes[index] is None:
            print(f"{bank.name}: Tube {index} is empty")
        else:
            print(f"{bank.name}: Fired tube {index} ({bank.tubes[index]})")
            bank.tubes[index] = None

    def repair(self, bank):
        print(f"{bank.name}: Already operational")

    def take_damage(self, bank, severity):
        if severity == "light":
            print(f"{bank.name}: Damage taken, now inoperable")
            bank.state = InoperableState()
        elif severity in ("medium", "heavy"):
            print(f"{bank.name}: Severe damage, now broken")
            bank.state = BrokenState()

class InoperableState(TubeBankState):
    def load_tube(self, bank, index, weapon):
        print(f"{bank.name}: Cannot load, bank is inoperable")

    def fire_tube(self, bank, index):
        print(f"{bank.name}: Cannot fire, bank is inoperable")

    def repair(self, bank):
        print(f"{bank.name}: Repairs successful, bank operational again")
        bank.state = OperationalState()

    def take_damage(self, bank, severity):
        print(f"{bank.name}: Additional damage, bank now broken")
        bank.state = BrokenState()

class BrokenState(TubeBankState):
    def load_tube(self, bank, index, weapon):
        print(f"{bank.name}: Cannot load, bank is broken")

    def fire_tube(self, bank, index):
        print(f"{bank.name}: Cannot fire, bank is broken")

    def repair(self, bank):
        print(f"{bank.name}: Cannot repair at sea, return to port required")

    def take_damage(self, bank, severity):
        print(f"{bank.name}: Already broken")


# Create and test
fore_port = TubeBank("Fore Port", 2)
fore_starboard = TubeBank("Fore Starboard", 2)
aft = TubeBank("Aft", 1)

fore_port.load_tube(0, "G7a")
fore_port.fire_tube(0)

fore_port.take_damage("light")
fore_port.fire_tube(1)
fore_port.repair()
fore_port.load_tube(1, "G7e")

aft.take_damage("heavy")
aft.repair()