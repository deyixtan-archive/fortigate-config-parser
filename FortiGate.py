from collections import OrderedDict
import shlex
import csv

class ConfigParser:
    '''
    MADE BY: DE YI <https://github.com/deyixtan>
    '''
    
    def __init__(self, input_config_file):
        with open(input_config_file, 'r') as file:
            self.file_lines = [x.strip() for x in file.readlines()] 

        self.__parse()

    def __parse(self):
        self.configs_list = []
        current_config_dict = None
        current_config_name = ''

        for line_index,file_line in enumerate(self.file_lines):
            if len(file_line) == 0:
                continue
            elif file_line.startswith("config"):
                current_config_name = shlex.split(file_line)
                current_config_name.pop(0)
                current_config_name = '-'.join(current_config_name)
                continue
            elif file_line.startswith("edit"):
                if len(current_config_name) <= 0:
                    current_config_dict = OrderedDict([("config", '')])
                else:
                    current_config_dict = OrderedDict([("config", current_config_name)])
                edit_number = shlex.split(file_line)[1]
                current_config_dict.update([("edit", edit_number)])
                continue
            elif file_line.startswith("next"):
                self.configs_list.append(current_config_dict)
                continue
            elif file_line.startswith("end"):
                if (line_index + 1) < len(self.file_lines): 
                    if not self.file_lines[line_index + 1].startswith("config"):
                        current_config_dict = OrderedDict([("config", '')])
                        current_config_name = ''

            set_command_line = shlex.split(file_line, posix=False)
            if "set" in set_command_line[0]:
                set_command_line.pop(0)
            
            parameter_name = set_command_line[0]
            parameter_value = ''
            for value in range(1, len(set_command_line)):
                if (value + 1) >= len(set_command_line):
                    parameter_value += set_command_line[value]
                else:
                    parameter_value += (set_command_line[value] + ' ')

            current_config_dict.update([(parameter_name, parameter_value)])
    
    def save(self, output_config_file):
        csv_headers_list = []
        for config in self.configs_list:
            for config_key in config.keys():
                if config_key not in csv_headers_list:
                    csv_headers_list.append(config_key)

        with open(output_config_file, "w", newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=csv_headers_list)
            csv_writer.writeheader()
            csv_writer.writerows(self.configs_list)