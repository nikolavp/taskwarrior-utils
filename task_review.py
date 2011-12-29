#!/usr/bin/env python2
# vim: set sw=4 sts=4 et foldmethod=indent :

import subprocess
import sys
import os

interactive_text="""Would you like to (e)dit the task, 
mark it (d)one or (D)eleted ? Hit (n)o to skip to the next task and (q)
to quit reviewing>>"""


supported_commands={
        'delete': subprocess.call,
        'edit': subprocess.call,
        'done': subprocess.check_output,
        'list': subprocess.check_output,
        '_id': subprocess.check_output,
        'info': subprocess.check_output}


class Invoker(object):
    """A delegating object that will call the task program
    to do it's job. All arguments to the methods are passed
    as filters to task. Example:
    invoker.list('project:foo', '+tag')"""
    def __getattr__(self, attr):
        if attr in supported_commands:
            def call_task(*args):
                #Convert them to strings
                arguments = list(map(str, args))
                #First the filters then the command
                all_args = ['task'] + arguments + [attr]
                function = supported_commands[attr]
                return function(all_args)
            return call_task
        raise AttributeError("'%s' object has no attribute '%s'" %
                             (self.__class__.__name__, attr))

task_invoker = Invoker()


class ReviewContext(object):
    def __init__(self, current_task_id):
        self.__current_task_id = current_task_id

    def go_to_next_task(self):
        self.__current_task_id = self.__current_task_id + 1

    def current_task_id(self):
        return str(self.__current_task_id)


def process_result(result, id):
    if result == 'e':
        task_invoker.edit(id)
        return True
    elif result == 'n':
        return True
    elif result == 'd':
        task_invoker.done(id)
        return True
    elif result == 'D':
        delete_result = task_invoker.delete(id)
        if delete_result == 0:
            return True
    return False

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main(argv):
    tasks = task_invoker._id(*argv).split(os.linesep)
    tasks = filter(None, tasks)
    context = ReviewContext(1)
    for task_id in tasks:
        current_id = str(task_id)
        output = task_invoker.info(current_id)
        processed = False
        while not processed:
            clear_console()
            print(output)
            result = raw_input(interactive_text)
            if result == 'q':
                return
            processed = process_result(result, current_id)



if __name__ == '__main__':
    main(sys.argv[1:])

