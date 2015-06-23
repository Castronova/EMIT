__author__ = 'mario'



import time
import pickle
import coordinator.emitLogging as l

# TODO: threading is not working!!!
def follow(logging, target):
    path = None
    handlers = logging.get_logger().handlers
    for handler in handlers:
        if type(handler) == l.PickleHandler:
            path = handler.stream.name
            break

    if path:

        thefile = open(path, 'r')
        last_processed = []
        last_lines = None
        while True:
            lines = tail(thefile, lines=5)
            # if lines == last_lines:
            #     time.sleep(0.8)
            # else:
            last_lines = lines
            line_list = lines.split('\n')
            line_list = filter(lambda a: a != '', line_list) # remove blank entries

            for line in line_list:
                if line not in last_processed:

                    # self.out.SetInsertionPoint(0)
                    # target is the rich text box
                    target.SetInsertionPoint(0)
                    record = pickle.loads(line.replace('~~','\n').replace('!~!~','\r'))
                    if record.levelname == 'WARNING':
                        target.BeginTextColour((255, 140, 0))
                    elif record.levelname =='ERROR':
                        target.BeginTextColour((255, 0, 0))
                    elif record.levelname == 'DEBUG':
                        target.BeginTextColour((0, 0, 0))
                    elif record.levelname == 'INFO':
                        target.BeginTextColour((42, 78, 110))
                    elif record.levelname == 'CRITICAL':
                        target.BeginTextColour((170, 57, 57))

                    # self.out.Text =  self.out.Text.Insert(string+ "\n");

                    target.WriteText(record.message+'\n')
                    target.EndTextColour()
                    target.Refresh()
            last_processed = line_list


def tail(f, lines=20 ):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from beginning
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])