import re

def extract_task_method_names(pddl_data):
    # Regular expression to match method names starting with "TASK-" or "task-"
    method_pattern = re.compile(r"\( :method\s+(TASK-\S+|task-\S+)")
    # Find all matches
    methods = re.findall(method_pattern, pddl_data)
    # Get unique method names
    unique_methods = set(methods)
    return unique_methods

def write_annotated_task(method):
    """
    For example, for method TASK-COMMUNICATED_IMAGE_DATA-OBJECTIVE-MODE, 
    the task name is TASK-COMMUNICATED_IMAGE_DATA-OBJECTIVE-MODE
    the parameters are ?objective and ?mode, the type of ?objective is objective, the type of ?mode is mode
    the precondition is empty
    the effect is ( communicated_image_data ?objective ?mode ), where communicated_image_data is a predicate (which has _s) and ?objective and ?mode are parameters
    the resulting annotated task is:
    ( :task TASK-COMMUNICATED_IMAGE_DATA-OBJECTIVE-MODE
        :parameters
        (
            ?objective - objective
            ?mode - mode
        )
        :precondition
        (
        )
        :effect
        ( and
            ( communicated_image_data ?objective ?mode )
        )
    )
    """
        # Split the method name into components by '-'
    components = method.split('-')

    # The first component is always 'TASK', so we ignore it in parameters
    parameters = components[2:]

    # Create parameters string. Each parameter is in the format ?param - param
    parameters_str = "\n".join([f"            ?{param.lower()} - {param.lower()}" for param in parameters])

    # Create the predicate name by replacing '-' with '_'
    predicate_name = components[1].lower()

    # Create effect string
    effect_str = " ".join([f"?{param.lower()}" for param in parameters])

    # Construct the annotated task
    annotated_task = f"""
    ( :task {method}
        :parameters
        (
{parameters_str}
        )
        :precondition
        (
        )
        :effect
        ( and
            ( {predicate_name} {effect_str} )
        )
    )
    """

    return annotated_task

if __name__ == "__main__":
    for domain in [
            # "blocks", 
            # "logistics", 
            "rover", 
            # "satellite", 
            # "zenotravel"
            ]:
        print("Domain: {}".format(domain))
        path = "./CurricuLAMA/experiments/{}/results/result_domain_htn_949.pddl".format(domain)
        # Read PDDL data from file
        with open(path, "r") as f:
            pddl_data = f.read()
            # Extract task method names
            task_method_names = extract_task_method_names(pddl_data)
            # Print task method names
            print("\t",task_method_names)
            # Write annotated tasks
            for method in task_method_names:
                annotated_task = write_annotated_task(method)
                print(annotated_task)

            # with open("./experiment_HTN-Maker/{}/tasks.pddl".format(domain), "w") as f:
            #     f.write("( define ( tasks {}-tasks )".format(domain))
            #     for method in task_method_names:
            #         annotated_task = write_annotated_task(method)
            #         print(annotated_task)
            #         f.write(annotated_task)
            #     f.write(")")