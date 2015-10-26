import csv
import getpass
import os.path

BASELOGDIR = "logs/"

class TestLogger():
    def __init__(self, file_name):
        self.file_name = file_name

    def add_entry_to_log(self, entry_dict):
        log_name = getpass.getuser() + '-' + self.file_name + '-log.csv'

        already_existed = os.path.isfile(os.path.join(BASELOGDIR, log_name))

        with open(os.path.join(BASELOGDIR, log_name), 'a') as csvfile:
            fieldnames = ['timestamp', 'commit_id', 'result', 'cycles', 'instructions', 'registers_used', 'memory_used', 'error_info']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not already_existed:
                writer.writeheader()
            writer.writerow(entry_dict)

    def get_previous_entry(self):
        pass

    def calculate_difference(self, other_entry):
        # calculates how cycles, instr, registers have changed since last test
        pass
