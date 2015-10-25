import datetime
import subprocess
# test

class ResultParser():
    def __init__(self):
        self.logs = {}  # dictionary of dictionaries {input file: {'commit id':commit_id,'result',result ...}}

    def parse_results(self, input_files):
        def get_commit_id():
            return subprocess.getoutput("git log | head -n1 | cut -d' ' -f2")

        def get_timestamp():
            return datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

        def get_result(tiny_output):
            pass
            # return result

        def get_cycles(tiny_output):
            pass
            # return cycles

        def get_instructions(tiny_output):
            pass
            # return instructions

        def get_reg_used(tiny_output):
            pass
            # return reg_used

        def parse_error_info(input_file):
            pass
            # stdout should be redirected somewhere that this method will parse for info
            # return error_info

        commit_id = get_commit()
        timestamp = get_timestamp()

        for f in input_files:
            tmp = {}
            tmp['timestamp'] = timestamp
            tmp['commit_id'] = commit_id
            tiny_output = getTinyOutput(f)

            tmp['result'] = get_result(f)
            tmp['cycles'] = get_cycles(f)
            tmp['instructions'] = get_instructions(f)
            tmp['registers_used'] = get_reg_used(f)
            tmp['error_info'] = parse_error_info(f)

            self.logs[f] = tmp
