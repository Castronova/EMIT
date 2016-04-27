import sys
import help as h
from emitLogging import elog
from engine import Coordinator


def get_configuration_details(coordinator, arg):

    if len(coordinator.__models.keys()) == 0:
        elog.warning('No models found in configuration.')

    if arg.strip() == 'summary':
        elog.info('Here is everything I know about the current simulation...\n')

    # print model info
    if arg.strip() == 'models' or arg.strip() == 'summary':

        # loop through all known models
        for name,model in coordinator.__models.iteritems():
            model_output = []
            model_output.append('Model: '+name)
            model_output.append('desc: ' + model.description())
            model_output.append('id: ' + model.id())

            for item in model.get_input_exchange_items() + model.get_output_exchange_items():
                model_output.append(str(item.id()))
                model_output.append( 'name: '+item.name())
                model_output.append( 'description: '+item.description())
                model_output.append( 'unit: '+item.unit().UnitName())
                model_output.append( 'variable: '+item.variable().VariableNameCV())
                model_output.append( ' ')

            # get formatted width
            w = get_format_width(model_output)

            # print model info
            elog.info('  |'+(w)*'-'+'|')
            elog.info('  *'+format_text(model_output[0], w,'center')+'*')
            elog.info('  |'+(w)*'='+'|')
            elog.info('  |'+format_text(model_output[1], w,'left')+'|')
            elog.info('  |'+format_text(model_output[2], w,'left')+'|')
            elog.info('  |'+(w)*'-'+'|')
            for l in model_output[3:]:
                elog.info('  |'+format_text(l,w,'left')+'|')
            elog.info('  |'+(w)*'-'+'|')
            elog.info(' ')

    # print link info
    if arg.strip() == 'links' or arg.strip() == 'summary':
        # string to store link output
        link_output = []
        # longest line in link_output
        maxlen = 0

        for linkid,link in coordinator.__links.iteritems():
            # get the link info
            From, To = link.get_link()

            link_output.append('LINK ID : ' + linkid)
            link_output.append('from: ' + From[0].name() + ' -- output --> ' + From[1].name())
            link_output.append('to: ' + To[0].name() + ' -- input --> ' + To[1].name())

            # get the formatted width
            w = get_format_width(link_output)

            # print the output
            elog.info('  |'+(w)*'-'+'|')
            elog.info('  *'+format_text(link_output[0], w,'center')+'*')
            elog.info('  |'+(w)*'='+'|')
            for l in link_output[1:]:
                elog.info('  |'+format_text(l,w,'left')+'|')
            elog.info('  |' + w * '-' + '|')

    # print database info
    if arg.strip() == 'db' or arg.strip() == 'summary':

        for id, db_dict in coordinator._db.iteritems():

            # string to store db output
            db_output = []
            # longest line in db_output
            maxlen = 0

            # get the session args
            name = db_dict['name']
            desc = db_dict['description']
            engine = db_dict['args']['engine']
            address = db_dict['args']['address']
            user = db_dict['args']['user']
            pwd = db_dict['args']['pwd']
            db = db_dict['args']['db']


            db_output.append('DATABASE : ' + id)
            db_output.append('name: '+name)
            db_output.append('description: '+desc)
            db_output.append('engine: '+engine)
            db_output.append('address: '+address)
            db_output.append('database: '+db)
            db_output.append('user: '+user)
            db_output.append('connection string: '+db_dict['args']['connection_string'])

            # get the formatted width
            w = get_format_width(db_output)

            # print the output
            elog.info('  |'+(w)*'-'+'|')
            elog.info('  *'+format_text(db_output[0], w,'center')+'*')
            elog.info('  |'+(w)*'='+'|')
            for l in db_output[1:]:
                elog.info('  |'+format_text(l,w,'left')+'|')
            elog.info('  |'+(w)*'-'+'|')


def get_format_width(output_array):
        width = 0
        for line in output_array:
            if len(line) > width: width = len(line)
        return width + 4

def format_text(text, width, option='right'):

    if option == 'center':
        # determine the useable padding
        padding = width - len(text)
        lpadding = padding/2
        rpadding = padding - lpadding

        # center the text
        return lpadding*' '+text+rpadding*' '

    elif option == 'left':
        # determine the useable padding
        padding = width - len(text)

        # center the text
        return text+padding*' '

    elif option == 'right':
        # determine the useable padding
        padding = width - len(text)

        # center the text
        return padding*' ' + text


def parse_args(coordinator, arg):

    if ''.join(arg).strip() != '':
        if arg[0] == 'help':
            if len(arg) == 1:
                elog.info(h.help())
            else:
                elog.info(h.help_function(arg[1]))

        elif arg[0] == 'add' :
            if len(arg) == 1:
                elog.info(h.help_function('add'))
            else:
                coordinator.add_model(arg[1])

        elif arg[0] == 'remove':
            if len(arg) == 1:
                elog.info(h.help_function('remove'))
            else:
                coordinator.remove_model_by_id(arg[1])

        elif arg[0] == 'link':
            if len(arg) != 5:
                elog.info(h.help_function('link'))
            else:
                coordinator.add_link(arg[1],arg[2],arg[3],arg[4])

        elif arg[0] == 'showme':
            if len(arg) == 1:
                elog.info(h.help_function('showme'))
            else:
                coordinator.get_configuration_details(coordinator, arg[1])

        elif arg[0] == 'connect_db':
            if len(arg) == 1:
                elog.info(h.help_function('connect_db'))
            else:
                coordinator.connect_to_db(arg[1:])

        elif arg[0] == 'default_db':
            if len(arg) == 1:
                elog.info(h.help_function('default_db'))
            else:
                coordinator.set_default_db(arg[1:])

        elif arg[0] == 'run':
            elog.info('Running Simulation in Feed Forward Mode')
            coordinator.run_simulation()

        elif arg[0] == 'load':
            if len(arg) == 1:
                elog.info(h.help_function('load'))
            else:
                coordinator.load_simulation(arg[1:])

        elif arg[0] == 'db':
            if len(arg) == 1:
                elog.info(h.help_function('db'))
            else:
                coordinator.show_db_results(arg[1:])



        #todo: show database time series that are available

        elif arg[0] == 'info': print h.info()

        else:
            print 'Command not recognized.  Type "help" for a complete list of commands.'

def main(argv):
    print '|-------------------------------------------------|'
    print '|      Welcome to the Utah State University       |'
    print '| Environmental Model InTegration (EMIT) Project! |'
    print '|-------------------------------------------------|'
    print '\nPlease enter a command or type "help" for a list of commands'

    arg = None

    # create instance of coordinator
    coordinator = Coordinator()

    # TODO: This should be handled by gui
    # connect to databases
    coordinator.connect_to_db(['../data/connections'])
    coordinator.set_default_database()

    while arg != 'exit':
        # get the users command
        arg = raw_input("> ").split(' ')
        parse_args(coordinator, arg)

if __name__ == '__main__':
    main(sys.argv[1:])