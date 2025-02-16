import re
import copy
class PDDLParser:
  def __init__(self, pddl_content, enforce_remove_methods = False, enforce_extra_precondition = False):
    self.pddl_content = pddl_content
    self.enforce_action_first = False
    self.enforce_extra_precondition = enforce_extra_precondition
    self.enforce_remove_methods = enforce_remove_methods
    self.parsed_methods, self.original_methods = self.parse_methods()
    self.pre_process()
    self.generalized_methods = []

  def pre_process(self):
    # rename the parameters in the parsed_methods
    for i in range(len(self.parsed_methods)):
      self.parsed_methods[i] = self.sufix_parameters(self.parsed_methods[i], f"a{i}")

  @staticmethod
  def process_subtasks(subtasks_str):
    # e.g., ( TASK-CLEAR-BLOCK ?auto_13 )\n      ( TASK-CLEAR-BLOCK ?auto_11
    # e.g., ( !PUTDOWN ?auto_9 )\n      ( TASK-CLEAR-BLOCK ?auto_7
    # e.g., ( !UNSTACK ?auto_2 ?auto_1 
    # add ")" to the end of subtasks_str
    subtasks_str += ")"
    # extract content in each ()
    subtasks_list = []
    # Define the pattern to match a parameter
    subtask_pattern = re.compile(r"""\(([^)]*(?:\([^)]*\)[^)]*)*)\)""")
    # Find all matches in the parameters
    subtasks = subtask_pattern.findall(subtasks_str)
    # Process each match to structure the captured data
    for subtask in subtasks:
      # e.g., subtask = 'TASK-CLEAR-BLOCK ?auto_13'
      # get ["TASK-CLEAR-BLOCK ", "?auto_13"]
      subtask = subtask.strip()
      subtask = subtask.split(" ")
      subtasks_list.append(subtask)
    return subtasks_list

  def deep_copy(self, method):
    # deep copy a method
    new_method = {
      "head": method["head"],
      "parameters": copy.deepcopy(method["parameters"]),
      "vars": copy.deepcopy(method["vars"]),
      "precondition": copy.deepcopy(method["precondition"]),
      "subtasks": copy.deepcopy(method["subtasks"])
    }
    return new_method

  def parse_parameters(self, parameters):
    # Define the pattern to match a parameter
    parameter_pattern = re.compile(r"""(\?[\S]+)\s*-\s*([\S]+)""")
    # Find all matches in the parameters
    parameters = parameter_pattern.findall(parameters)
    # Process each match to structure the captured data
    parsed_parameters = []
    for parameter in parameters:
        parsed_parameter = {
            "name": parameter[0].strip(),
            "type": parameter[1].strip()
        }
        parsed_parameters.append(parsed_parameter)

    return parsed_parameters

  def parse_precondition(self, precondition):
    """
    :param precondition: precondition string, e.g., ( and ( ON ?auto_8 ?auto_7 ) ( CLEAR ?auto_8 ) ( not ( = ?auto_7 ?auto_8 ) ) ( HOLDING ?auto_9 ) ( not ( = ?auto_7 ?auto_9 ) ) ( not ( = ?auto_8 ?auto_9 ) ) )
    :return: a list of precondition
    """
    # First, we need to remove ( and ... ) if "and" exists using regex
    # Define the pattern to match a parameter
    and_pattern = re.compile(r"""\(\s*and(.*)\)""")
    # Find all matches in the parameters
    and_match = and_pattern.findall(precondition)
    if len(and_match) > 0:
      precondition = and_match[0]
    # Define the pattern to match a parameter
    parameter_pattern = re.compile(r"""\(([^)]*(?:\([^)]*\)[^)]*)*)\)""")
    # Find all matches in the parameters
    parameters = parameter_pattern.findall(precondition)
    # Process each match to structure the captured data
    parsed_parameters = []
    for parameter in parameters:
      parsed_parameter = parameter.strip()
      # only add parsed_parameter if it does not start with "not"
      if not parsed_parameter.startswith("not"):
        parsed_parameters.append(parsed_parameter)
    return parsed_parameters

  def parse_methods(self):
    # Define the pattern to match a method section
    # method_pattern = re.compile(r""":method\s*([\S]+)\s*:parameters\s*\(([^\)]*)\)\s*:vars\s*\(([^\)]*)\)\s*:precondition\s*([^\n]*)\s*:subtasks\s+\(([^)]*(?:\([^)]*\)[^)]*)*)\)\s*\)""")
    method_pattern = re.compile(
      r""":method\s*([\S]+)\s*"""
      r""":parameters\s*\(([^\)]*)\)"""
      r"""(?:\s*:vars\s*\(([^\)]*)\))?\s*"""   # Make :vars section optional
      r""":precondition\s*([^\n]*)\s*"""
      r""":subtasks\s+\(([^)]*(?:\([^)]*\)[^)]*)*)\)\s*\)"""
    )
    # Find all matches in the PDDL content
    methods = method_pattern.findall(self.pddl_content)
    print("methods: ")
    print(len(methods))

    # Process each match to structure the captured data
    parsed_methods = []
    original_methods = []
    for method in methods:
      subtasks_str = method[4].strip()
      subtasks_list = self.process_subtasks(subtasks_str)
      parsed_method = {
        "head": method[0].strip(),
        "parameters": self.parse_parameters(method[1].strip()),
        "vars": self.parse_parameters(method[2].strip()),
        "precondition": self.parse_precondition(method[3].strip()),
        "subtasks": subtasks_list
      }
      parsed_methods.append(parsed_method)
      original_method = {
        "head": method[0].strip(),
        "parameters": method[1].strip(),
        "vars": method[2].strip(),
        "precondition": method[3].strip(),
        "subtasks": subtasks_str
      }
      original_methods.append(original_method)
    return parsed_methods, original_methods

  def have_same_subtasks(self, method1, method2):
    # this method is to check if two methods have the same subtasks
    # check if their subtasks are the same length
    if len(method1["subtasks"]) != len(method2["subtasks"]):
      return False
    else:
      # check if their subtasks are the same names
      for i in range(len(method1["subtasks"])):
        if method1["subtasks"][i][0] != method2["subtasks"][i][0]:
          return False
      # check if the parameters have the same naming relationships
      parameter1 = []
      parameter2 = []
      for i in range(len(method1["subtasks"])):
        for j in range(1, len(method1["subtasks"][i])):
          parameter1.append(method1["subtasks"][i][j])
          parameter2.append(method2["subtasks"][i][j])
      if __name__ == "__main__":
        print(parameter1, method1["subtasks"])
        print(parameter2, method2["subtasks"])
      # if some parameters in 1 have the same names, then the corresponding parameters in 2 should have the same names
      for i in range(len(parameter1)):
        for j in range(i+1, len(parameter1)):
          if parameter1[i] == parameter1[j]:
            if parameter2[i] != parameter2[j]:
              return False
      # # loop on each unique pair of parameters in parameter1
      # for i in range(len(parameter1)):
      #   for j in range(i+1, len(parameter1)):
      #     # check if the two parameters have the same relationships among parameter1 and parameter2
      #     if not self.compare_structures(method1["precondition"], method2["precondition"], parameter1[i], parameter2[i], parameter1[j], parameter2[j]):
      #       return False
      # check if the parameters have the same relationships and directly related
      mismatch = False
      at_least_one_match = False
      for prec in method1["precondition"]:
        flag_irrelevant = False
        prec_parameters = prec.split(" ")[1:]
        if not prec_parameters:
          # we don't need to care about this precondition if it has empty parameters
          continue
        for prec_parameter in prec_parameters:
          if prec_parameter not in parameter1:
            # there is an irrelevant parameter in the precondition, meaning the parameter are not in the subtasks.
            flag_irrelevant = True
            break
          else:
            # replace the parameter in prec with the corresponding parameter in parameter2
            prec = prec.replace(prec_parameter, parameter2[parameter1.index(prec_parameter)])
        if flag_irrelevant:
          # we don't need to care about this precondition because it has irrelevant parameters
          continue
        # check if the precondition is in method2
        if prec not in method2["precondition"]:
          # the two methods does not match
          mismatch = True
          break
        else:
          # if len(prec_parameters) > 1:
          # at least 
          at_least_one_match = True
          if __name__ == "__main__":
            print("Found a match: ")
            print(prec)
      return not mismatch #and at_least_one_match
      
      # # replace names
      # if __name__ == "__main__":
      #   print("Before replacing names in checking subtasks: ")
      #   print(method1["precondition"])
      # preconditions_for_method1 = method1["precondition"]
      # for i in range(len(preconditions_for_method1)):
      #   for j in range(len(parameter1)):
      #     preconditions_for_method1[i] = preconditions_for_method1[i].replace(parameter1[j], parameter2[j])
      # if __name__ == "__main__":
      #   print("After replacing names in checking subtasks: ")
      #   print(preconditions_for_method1)
      # # all full conditions/predicates in method1 should be in method2
      # for precondition in preconditions_for_method1:
      #   viriables = precondition.split(" ")[1:]
      #   flag = True
      #   for i in range(len(viriables)):
      #     if viriables[i] not in parameter2:
      #       flag = False
            
      #       break
      #   if flag:
      #     if precondition not in method2["precondition"]:
      #       return False
      # return True

  def generalize_methods(self):
    # find pairs of methods that have the same subtasks (variable names could be diffrent)
    # for i in range(len(self.parsed_methods)):
    #   for j in range(i+1, len(self.parsed_methods)):
    #     # first check if the two methods have the same head
    #     print("Checking if two methods have the same subtasks: ")
    #     if self.parsed_methods[i]["head"] == self.parsed_methods[j]["head"]:
    #       if self.have_same_subtasks(self.parsed_methods[i], self.parsed_methods[j]):
    #         print("Found two methods with the same subtasks: ")
    #         self.merge_methods(self.parsed_methods[i], self.parsed_methods[j])
    # find pairs of methods that have the same subtasks (variable names could be diffrent), merge those two methods, and delete the original methods
    for i in range(len(self.parsed_methods)):
      for j in range(i+1, len(self.parsed_methods)):
        # check if methods are not None
        if self.parsed_methods[i] is None or self.parsed_methods[j] is None:
          continue
        # first check if the two methods have the same head
        if __name__ == "__main__":
          print("Checking if two methods have the same subtasks: ")
        if self.parsed_methods[i]["head"] == self.parsed_methods[j]["head"]:
          # enforcing first subtask to be an action
          if ( not self.enforce_action_first ) or ( self.parsed_methods[i]["subtasks"] and self.parsed_methods[i]["subtasks"][0][0].startswith("!") and self.parsed_methods[j]["subtasks"] and self.parsed_methods[j]["subtasks"][0][0].startswith("!") ):
            if self.have_same_subtasks(self.deep_copy(self.parsed_methods[i]), self.deep_copy(self.parsed_methods[j])):
              if __name__ == "__main__":
                print("Found two methods with the same subtasks: ")
                self.write_method(self.parsed_methods[i])
                self.write_method(self.parsed_methods[j])
              success = self.merge_methods(self.deep_copy(self.parsed_methods[i]), self.deep_copy(self.parsed_methods[j]))
              # success = True
              if __name__ == "__main__":
                if success:
                  print("Merging success")
              if self.enforce_remove_methods and success:
                # delete the original methods
                if __name__ == "__main__":
                  print("Removing the original methods")
                self.parsed_methods[i] = None
                self.parsed_methods[j] = None
    # remove None from self.parsed_methods
    self.parsed_methods = [method for method in self.parsed_methods if method is not None]

  def remove_residual_parameters(self, method):
    # keep vars in method that are used in method's precondition
    vars = method["vars"]
    if __name__ == "__main__":
      print("\tBefore removing residual parameters: ")
      print("\t", vars)
    new_vars = []
    for var in vars:
      flag = False
      # check if var is used in method's precondition
      for prec in method["precondition"]:
        if var["name"] in prec:
          flag = True
          break
      if flag:
        new_vars.append(var)
        continue
    if __name__ == "__main__":
      print("\tAfter removing residual parameters: ")
      print("\t", new_vars)
    return new_vars
  
  def sufix_parameters(self, method1, mark):
    if __name__ == "__main__":
      print("Before renaming: ")
      self.write_method(method1)
    # Append a letter "a" to all parameter names and vars in method1
    for i in range(len(method1["parameters"])):
      original_name = method1["parameters"][i]["name"]
      method1["parameters"][i]["name"] = original_name + mark
      for j in range(len(method1["subtasks"])):
        for k in range(1, len(method1["subtasks"][j])):
          if method1["subtasks"][j][k] == original_name:
            method1["subtasks"][j][k] = original_name + mark
      for i in range(len(method1["precondition"])):
        if original_name in method1["precondition"][i]:
          method1["precondition"][i] = method1["precondition"][i].replace(original_name, original_name + mark)
    for i in range(len(method1["vars"])):
      original_name = method1["vars"][i]["name"]
      method1["vars"][i]["name"] = original_name + mark
      for j in range(len(method1["subtasks"])):
        for k in range(1, len(method1["subtasks"][j])):
          if method1["subtasks"][j][k] == original_name:
            method1["subtasks"][j][k] = original_name + mark
      for i in range(len(method1["precondition"])):
        if original_name in method1["precondition"][i]:
          method1["precondition"][i] = method1["precondition"][i].replace(original_name, original_name + mark)
    if __name__ == "__main__":
      print("After renaming: ")
      self.write_method(method1)
      print("\n")
    return method1

  def merge_methods(self, method1, method2):
    # method1 = copy.deepcopy(method1)
    # method1 = self.sufix_parameters(method1)
    # merge two methods into one
    if __name__ == "__main__":
      print("Merging two methods: ")
      print(method1)
      print(method2)
    # first we align the parameter names
    for i in range(len(method1["subtasks"])):
      for j in range(1, len(method1["subtasks"][i])):
        # if the parameter name in method1 is not the same as in method2
        if method1["subtasks"][i][j] != method2["subtasks"][i][j]:
          # rename the parameter in method2
          method2 = self.rename_parameter(method2.copy(), method2["subtasks"][i][j], method1["subtasks"][i][j])
    if __name__ == "__main__":
      print("After aligning: ")
      self.write_method(method2)
    # relavant parameters of a method are parameters that are in the subtasks's parameters

    # get method2's relavant parameters
    relevant_parameters = []
    # if first subtask is not action, get the parameters in the first subtask
    if self.enforce_extra_precondition and not method2["subtasks"][0][0].startswith("!"):
      for i in range(1, len(method2["subtasks"][0])):
        relevant_parameters.append(method2["subtasks"][0][i])

    method2["precondition"] = self.get_common_precondition(method1, method2, relevant_parameters)

    # # for each subtask in method2, add one precondition to method2, this precondition states that the subtask's goal is not true
    # for subtask in method2["subtasks"]:
    #   # pass if subtask is an action (task name starts with !)
    #   if subtask[0].startswith("!"):
    #     continue
    #   # add a precondition to method2
    #   # a task has name TAKS-PREDICATE-PARAM1TYPE-PARAM2TYPE-...
    #   subtask_breakdown = subtask[0].split("-")
    #   # print("subtask_breakdown: ", subtask_breakdown)
    #   # print(1, len(subtask_breakdown)-len(subtask))
    #   predicate = "-".join(subtask_breakdown[1:len(subtask_breakdown)-len(subtask)+1])
    #   # print("predicate: ", predicate)
    #   precondition = ["not", predicate] + subtask[1:]
    #   # print("precondition: ", precondition)
    #   method2["precondition"].append(" ".join(precondition))

    method2["vars"] = self.remove_residual_parameters(method2)
    # if __name__ == "__main__":
      # print("After merging: ")
      # self.write_method(method2)
    # check if the preconditions are over-trimmed
    # if a parameter in method2's subtasks has not related declaration in method2's precondition and vars, then the merge fails
    for subtask in method2["subtasks"]:
      for i in range(1, len(subtask)):
        if subtask[i] not in [parameter["name"] for parameter in method2["parameters"]] and subtask[i] not in [parameter["name"] for parameter in method2["vars"]]:
          return False
          # pass
    # check if method2 is already in self.generalized_methods
    flag = False
    for new_method in self.generalized_methods:
      # if new_method and method2 are equivalent
      if self.equivalent_methods(self.deep_copy(new_method), self.deep_copy(method2)):
        flag = True
        break
    if not flag:
      self.generalized_methods.append(method2)
      if __name__ == "__main__":
        print("Adding the new method to self.generalized_methods")
        self.write_method(method2)
    return True

  def equivalent_methods(self, method1, method2):
    # return False
    # check if method1 and method2 are equivalent dispite the parameter names
    # if __name__ == "__main__":
      # print("*******\nChecking if two methods are equivalent: ")
      # self.write_method(method1)
      # self.write_method(method2)

    # check if the subtasks are the same
    if not self.have_same_subtasks(method1, method2):
      return False
    # check if the parameters have the same relationships and directly related
    parameter1 = []
    parameter2 = []
    for i in range(len(method1["subtasks"])):
      for j in range(1, len(method1["subtasks"][i])):
        parameter1.append(method1["subtasks"][i][j])
        parameter2.append(method2["subtasks"][i][j])
    # if some parameters in 1 have the same names, then the corresponding parameters in 2 should have the same names
    for i in range(len(parameter1)):
      for j in range(i+1, len(parameter1)):
        if parameter1[i] == parameter1[j]:
          if parameter2[i] != parameter2[j]:
            return False
    # check if the parameters have the same relationships and directly related, every preconditions should match after replacing names
    # first check the length of the preconditions
    if len(method1["precondition"]) != len(method2["precondition"]):
      return False
    # replace names
    preconditions_for_method1 = method1["precondition"]
    # print("Before replacing names in checking subtasks: ", preconditions_for_method1)
    for i in range(len(preconditions_for_method1)):
      for j in range(len(parameter1)):
        preconditions_for_method1[i] = preconditions_for_method1[i].replace(parameter1[j], parameter2[j])
    # all full conditions/predicates in method1 should be in method2
    for precondition in preconditions_for_method1:
      if precondition not in method2["precondition"]:
        return False
    return True

  # def get_common_precondition(self, method1, method2, relevant_parameters = None):
  #   # get the common precondition of two methods
  #   common_precondition = []
  #   # print("method1's prec: ", method1["precondition"])
  #   # print("method2's prec: ", method2["precondition"])
  #   for prec in method1["precondition"]:
  #     if prec in method2["precondition"]:
  #       common_precondition.append(prec)
  #   return common_precondition

  # def get_common_precondition(self, method1, method2):
  #   # get the common precondition of two methods
  #   common_precondition = []
  #   for prec1 in method1["precondition"]:
  #     for prec2 in method2["precondition"]:
  #       # print("before: ", prec1, prec2)
  #       prec1_split = prec1.split(" ")
  #       # print("middle: ", prec1, prec2)
  #       prec2_split = prec2.split(" ")
  #       # print("after: ", prec1, prec2)
  #       if prec1_split[0] == prec2_split[0]:
  #         if prec1_split == prec2_split:
  #           common_precondition.append(prec2)
  #           continue
  #         for i in range(1, len(prec1_split)):
  #           if prec1_split[i] == prec2_split[i]:
  #             common_precondition.append(prec2)
  #             break
  #   return common_precondition

  def get_common_precondition(self, method1, method2, relevant_parameters):
    # get the common precondition of two methods
    common_precondition = []
    if __name__ == "__main__":
      print("method1's prec: ", method1["precondition"])
      print("method2's prec: ", method2["precondition"])
      print("relevant_parameters: ", relevant_parameters)
    for prec2 in method2["precondition"]:
      if prec2 in method1["precondition"]:
        common_precondition.append(prec2)
        if __name__ == "__main__":
          print(prec2, " has same prec in method1")
        continue
      # if a prec in method1 has the same first element and any 
      # of the rest elements as prec2, then prec2 is in common_precondition
      # method1_precs = copy.deepcopy(method1["precondition"])
      for prec1 in method1["precondition"]:
        if prec1.split(" ")[0] == prec2.split(" ")[0]:
          for i in range(1, len(prec1.split(" "))):
            if prec1.split(" ")[i] == prec2.split(" ")[i] and prec1.split(" ")[i] in relevant_parameters:
              common_precondition.append(prec2)
              if __name__ == "__main__":
                print(prec2, " has matching prec in method1, ", prec1)
    if __name__ == "__main__":
      print("common_precondition: ", common_precondition)
    return common_precondition

  def rename_parameter(self, method, old_name, new_name):
    # rename the parameter in the method's parameters, vars, precondition, and subtasks
    # rename the parameter in method's parameters
    for parameter in method["parameters"]:
      if parameter["name"] == old_name:
        parameter["name"] = new_name
    # rename the parameter in method's vars
    for parameter in method["vars"]:
      if parameter["name"] == old_name:
        parameter["name"] = new_name
    # rename the parameter in method's precondition
    # e.g., ['ON ?auto_8 ?auto_7', 'CLEAR ?auto_8', 'HOLDING ?auto_9']
    for i in range(len(method["precondition"])):
      if old_name in method["precondition"][i]:
        method["precondition"][i] = method["precondition"][i].replace(old_name, new_name)
    # rename the parameter in method's subtasks
    # e.g., ['TASK-CLEAR-BLOCK ', '?auto_13']
    for i in range(len(method["subtasks"])):
      for j in range(1, len(method["subtasks"][i])):
        if method["subtasks"][i][j] == old_name:
          method["subtasks"][i][j] = new_name
    return method

  def write_parameters(self, parameters):
    # print the parameters in PDDL format
    parameter_str = ""
    for parameter in parameters:
      parameter_str += parameter["name"] + " - " + parameter["type"] + " "
    return parameter_str

  def write_precondition(self, precondition):
    # print the precondition in PDDL format
    precondition_str = ""
    # print("writing precondition: ", precondition)
    for prec in precondition:
      prec = prec.split(" ")
      if prec[0] == "not":
        precondition_str += "( not ( " + " ".join(prec[1:]) + ") ) "
      else:
        precondition_str += "( " +  " ".join(prec) + ") "
    return precondition_str

  def write_subtasks(self, subtasks):
    # print the subtasks in PDDL format
    subtasks_str = ""
    for subtask in subtasks:
      subtasks_str += "(" + subtask[0] + " "
      for i in range(1, len(subtask)):
        subtasks_str += subtask[i] + " "
      subtasks_str += ")"
    return subtasks_str

  def write_method(self, method, file = None, original = False):
    # print the method in PDDL format
    if not file:
      print("(:method " + method["head"])
      print(":parameters (" + self.write_parameters(method["parameters"]) + ")")
      print(":vars (" + self.write_parameters(method["vars"]) + ")")
      print(":precondition (and " + self.write_precondition(method["precondition"]) + ")")
      print(":subtasks (" + self.write_subtasks(method["subtasks"]) + "))")
    else:
      if original:
        file.write("(:method " + method["head"] + "\n")
        file.write(":parameters (" + method["parameters"] + ")\n")
        file.write(":vars (" + method["vars"] + ")\n")
        file.write(":precondition " + method["precondition"] + "\n")
        file.write(":subtasks (" + method["subtasks"] + ")))\n\n")
      else:
        file.write("(:method " + method["head"] + "\n")
        file.write(":parameters (" + self.write_parameters(method["parameters"]) + ")\n")
        file.write(":vars (" + self.write_parameters(method["vars"]) + ")\n")
        file.write(":precondition (and " + self.write_precondition(method["precondition"]) + ")\n")
        file.write(":subtasks (" + self.write_subtasks(method["subtasks"]) + "))\n")

  def write_PDDL(self, original_filename, new_filename):
    # read the original PDDL file
    with open(original_filename, "r") as original_file:
      original_content = original_file.read()
      # delete everything from the line where "method" appears
      original_content = original_content.split("\n")
      for i in range(len(original_content)):
        if ":method" in original_content[i]:
          original_content = original_content[:i]
          break
      original_content = "\n".join(original_content)
      # write the new PDDL file
      with open(new_filename, "w") as new_file:
        new_file.write(original_content)
        new_file.write("\n")
        for method in self.parsed_methods:
          self.write_method(method, new_file)
        # for method in self.original_methods:
        #   self.write_method(method, new_file, original = True)
        new_file.write("\n")
        for method in self.generalized_methods:
          self.write_method(method, new_file)
        new_file.write(")")

if __name__ == "__main__":
  # read an argument as the problem number using argparse
  import argparse
  parser = argparse.ArgumentParser()
  # add domain in arguments
  parser.add_argument("domain", help="domain name")
  parser.add_argument("problem_number", help="problem number", type=int)
  # enforce_extra_precondition, default is False
  parser.add_argument("--enforce_extra_precondition", help="enforce extra precondition", action="store_true")
  args = parser.parse_args()
  problem_number = args.problem_number
  enforce_remove_methods = True
  enforce_extra_precondition = args.enforce_extra_precondition
  # Read the PDDL file
  # file = "../CurricuLAMA/experiments/blocks_recursion/results/result_domain_htn_20.pddl"
  # domain = "blocks_recursion"
  # domain = "minigrid"
  domain = args.domain
  # domain = "depots"
  # domain = "blocks_recursion"
  root_dir = f"/home/rli12314/scratch/CurricuLAMA/experiments/{domain}/results"
  if problem_number == -1:
    file = "./domain.pddl"
    file2 = "./new_domain.pddl"
  else:
    file = f"{root_dir}/result_domain_htn_{problem_number}.pddl"
    file2 = f"{root_dir}/result_domain_htn_{problem_number}_generalized.pddl"
  with open(file, "r") as pddl_file:
    pddl_content = pddl_file.read()
    # Parse the PDDL file
    parser = PDDLParser(pddl_content, enforce_remove_methods = enforce_remove_methods)
    original_num = len(parser.parsed_methods)
    parser.generalize_methods()
    if __name__ == "__main__":
      print(original_num, len(parser.generalized_methods), len(parser.generalized_methods) + len(parser.parsed_methods))
    parser.write_PDDL(file, file2)
  import difflib

  def read_file(file_path):
    # Read a file and remove all whitespace (spaces, tabs, newlines)
    with open(file_path, 'r') as file:
      return ''.join(file.read().split())

  file_content = read_file(file)
  file2_content = read_file(file2)

  if __name__ == "__main__":
    print("\n")
    print(len(parser.generalized_methods),  "generalized methods learned.")
    # count how many string "method" in each file
    print(file_content.count("method"), "methods original.")
    print(file2_content.count("method"), "methods now.")
    # how many deleted
    if enforce_remove_methods:
      print(file_content.count("method") - file2_content.count("method"), "methods deleted.")
    else:
      print("Original methods are kept.")
