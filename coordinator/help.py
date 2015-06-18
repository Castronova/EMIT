__author__ = 'tonycastronova'


"""
commandline help documentation
"""


def help_function(function):
    """
    returns the help doc for a specific function
    """

    if function == 'save':
        pass
    elif function == 'OnOpen':
        pass
    elif function =='add':
        return  "> Usage:\t Adds models to a configuration.\n" \
                ">       \t add [model filepath]\n" \
                ">       \t [model filepath] is the path to the model configuration file"

    elif function =='remove':
        return  "> Usage:\t Removes models from a configuration.\n" \
                ">       \t remove [model name]\n" \
                ">       \t [model name] is the name of the model that will be removed"
    elif function == 'link':
        return  "> Usage:\t Adds a link between models in a configuration.\n" \
                ">       \t link [from model name] [from exchange item] [to model name] [to exchange item]\n" \
                ">       \t [from model name] is the name of the model that will transfer output\n"\
                ">       \t [from exchange item] is the output item that will transfer data \n"\
                ">       \t [to model name] is the name of the model that will accept input\n"\
                ">       \t [to exchange item] is the name of the input item that will receive data"
    elif function == 'display':
        pass
    elif function == 'run':
        pass
    elif function =='showme':
        return  "> Usage:\t Displays configuration info.\n" \
                ">       \t showme [models] [links] [inputs] [outputs] [summary]\n" \
                ">       \t [models] keyword returns a summary of models in the configuration.\n"\
                ">       \t [links] keyword returns a summary of all the links in the configuration.\n" \
                ">       \t [inputs] keyword returns a summary of all inputs in the configuration.\n"\
                ">       \t [outputs] keyword returns a summary of all outputs in the configuration.\n" \
                ">       \t [summary] keyword returns a general summary of the entire configuration."

    else:
        return '> [error] function "%s" not recognized. ' % function

def info():
    """
    returns software info
    """
    return  '  Environmental Model InTegration (EMIT) Project \n' +\
            '  Released: 7/1/2014 \n' +\
            '  Version: 0.1 \n' +\
            '  Author: Anthony Castronova \n'

def help():
    """
    returns commandline help string
    """
    return  '> Basic Commands \n'+\
            '  help - displays EMIT commands \n' + \
            '  exit - closes the application \n' + \
            '  info - displays EMIT software information \n' +\
            '\n> Advanced Functions \n' +\
            '> (for more function information use the command "help {function name} )" \n'+\
            '  save    - saves model configuration \n'+\
            '  OnOpen    - opens existing configuration \n'+\
            '  add     - adds a model to the configuration \n' + \
            '  remove  - removes a model from the configuration \n'+\
            '  link    - creates link between two models \n' +\
            '  showme  - show info about the model configuration \n' +\
            '  run     - executes the simulation \n'