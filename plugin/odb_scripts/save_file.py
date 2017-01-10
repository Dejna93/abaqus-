import os
from plugin.settings import config


def save_file(rang, storage):
    """
    :param range: It is for range (framecounter) for every running proces (parallelism)
    :return: Nothing, it is only save file
    """
    print("SaveFile Function")
    values = storage.odb.steps.values()
    values_dict = {}
    if storage.selected_vars_kind == "2D":
        for frame in range(rang):  # parallelism
            output_file = os.path.join(config.output_path, "Increment%s.txt" % frame)
            print "Tworzenie pliku\nPath: %s" % output_file
            with open(output_file, mode='w') as file:
                for var in storage.selected_vars2D:
                    values_dict[var] = values[0].frames[frame].fieldOutputs[var]
                for j in range(0, storage.values_counter):
                    output_string = '%d' % j
                    for key, value in values_dict.items():
                        if key == "S":
                            output_string += ":%s" % value.values[j].elementLabel - 1
                            output_string += ":%s" % value.values[j].mises
                        output_string += ":%s" % value.values[j].data
                    file.write(output_string + '\n')

    if storage.selected_vars_kind == "3D":
        for frame in range(rang):  # parallelism
            output_file = os.path.join(config.output_path, "Increment%s.txt" % frame)
            with open(output_file, mode='w') as file:
                for var in storage.selected_vars3D:
                    values_dict[var] = values[0].frames[frame].fieldOutputs[var]
                for j in range(0, storage.values_counter):
                    output_string = '%d' % j
                    for key, value in values_dict.items():
                        if key == "S":
                            output_string += ":%s" % value.values[j].elementLabel - 1
                            output_string += ":%s" % value.values[j].mises
                        output_string += ":%s" % value.values[j].data
                    file.write(output_string + '\n')

if __name__ == '__main__':
    save_file()