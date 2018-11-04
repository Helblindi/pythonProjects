class Shift:
    # Shift represents an operator with a start time and an end time
    # Shift also contains a variable indicating the level of the shift

    # Non-Default Constructor
    def __init__(self, _role, _level, _initials, _start_time, _end_time):
        self.role = _role
        self.level = _level
        self.initials = _initials
        self.start_time = _start_time
        self.end_time = _end_time

    def __str__(self):
        return self.initials + ": " + self.start_time + "-" + self.end_time

    def get_role(self):
        return self.role

    def set_role(self, _role):
        self.role = _role

    def get_level(self):
        return self.level

    def set_level(self, _level):
        self.level = _level

    def get_shift_initials(self):
        return self.initials

    def set_shift_initials(self, _initials):
        self.initials = _initials

    def get_shift_start_time(self):
        return self.start_time

    def set_shift_start_time(self, _start_time):
        self.start_time = _start_time

    def get_shift_end_time(self):
        return self.end_time

    def set_shift_end_time(self, _end_time):
        self.end_time = _end_time

def build_middle():
    return

def build_everything_else():
    return

def main():
    print('\t---Main called---')
    return


# While not required, it is considered good practice to have
# a main function and use this syntax to call it.
if __name__ == "__main__":
    main()
