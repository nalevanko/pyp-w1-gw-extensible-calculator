from datetime import datetime

from calculator.operations import *
from calculator.exceptions import *


def create_new_calculator(operations=None):
    """
    Creates a configuration dict for a new calculator. Optionally pre loads an
    initial set of operations. By default a calculator with no operations
    is created. Returns a dict containing operations(dict) and history(list).

    :param operations: Dict with initial operations.
                       ie: {'sum': sum_function, ...}
    """
    calculator = {'operations':{}, 'history':[]}
    if operations is not None:
        if not isinstance(operations, dict):
            raise InvalidParams()
        for key, value in operations.items():
            calculator['operations'][key] = value
    return calculator


def perform_operation(calc, operation, params):
    """
    Executes given operation with given params. It returns the result of the
    operation execution.

    :param calc: A calculator.
    :param operation: String with the operation name. ie: 'add'
    :param params: Tuple containing the list of nums to operate with.
                   ie: (1, 2, 3, 4.5, -2)
    """
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    for i in params:
        if not isinstance(i, int) and not isinstance(i, float):
            raise InvalidParams()
    result = calc['operations'][operation](*params)
    calc['history'].append((now_str, operation, params, result))
    
    return result


def add_new_operation(calc, operation):
    """
    Adds given operation to the list of supported operations for given calculator.

    :param calc: A calculator.
    :param operation: Dict with the single operation to be added.
                      ie: {'add': add_function}
    """
    if not isinstance(operation, dict):
        raise InvalidOperation()
        
    for key, value in operation.items():
        calc['operations'][key] = value
        
    

def get_operations(calc):
    """
    Returns the list of operation names supported by given calculator.
    """
    op_list = []
    for key, values in calc['operations'].items():
        op_list.append(key)
        
    return op_list


def get_history(calc):
    """
    Returns the history of the executed operations since the last reset or
    since the calculator creation.

    History items must have the following format:
        (:execution_time, :operation_name, :params, :result)

        ie:
        ('2016-05-20 12:00:00', 'add', (1, 2), 3),
    """
    records = []
    for item in calc['history']:
        records.append(item)
        
    return records


def reset_history(calc):
    """
    Resets the calculator history back to an empty list.
    """
    calc['history'] = []


def repeat_last_operation(calc):
    """
    Returns the result of the last operation executed in the history.
    """
    #First: retrieve info about the last informat
    if len(calc['history']) > 0:
        _, operation, params, _ = calc['history'][-1]
        return perform_operation(calc, operation, params)