from pemfc.src import global_functions as gf

from gui.entry_value import EntryValue


def gen_dict_extract(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield var
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result
    elif isinstance(var, (list, tuple)):
        for d in var:
            for result in gen_dict_extract(key, d):
                yield result


def set_dict_entry(value, name_list, target_dict):
    if isinstance(target_dict, dict):
        sub_dict = target_dict
    else:
        raise TypeError
    for i in range(len(name_list) - 1):
        sub_dict = sub_dict[name_list[i]]
    sub_dict[name_list[-1]] = EntryValue.get_value(value)
    return target_dict


def get_dict_entry(name_list, source_dict):
    if isinstance(source_dict, dict):
        sub_dict = source_dict
    else:
        raise TypeError
    for i in range(len(name_list) - 1):
        sub_dict = sub_dict[name_list[i]]
    return sub_dict[name_list[-1]]


def gui_to_sim_transfer(source_dict, target_dict):

    # get only widgets with sim_names
    name_lists = []
    extracted_gui_entries = list(gen_dict_extract('sim_name', source_dict))
    if extracted_gui_entries:
        for gui_entry in extracted_gui_entries:
            sim_names = gui_entry['sim_name']
            sim_names = gf.ensure_list(sim_names)
            sub_dict = target_dict

            if isinstance(sim_names[0], list):
                gui_values = gf.ensure_list(gui_entry['value'])

                # if len(sim_names) != len(gui_values):
                #     gui_values = [gui_values[0] for i in range(len(sim_names))]
                if len(sim_names) == len(gui_values):
                    multi_variable = True
                else:
                    multi_variable = False

                for i, sim_name_list in enumerate(sim_names):
                    if isinstance(sim_name_list[-1], list):
                        pure_name_list = sim_name_list[:-1]
                        name_lists.append(pure_name_list)
                        value_list = []
                        for j in sim_name_list[-1]:
                            try:
                                value = gui_values[j]
                            except IndexError:
                                value = gui_values[-1]
                            value_list.append(EntryValue.get_value(value))
                        sub_dict = \
                            set_dict_entry(value_list, pure_name_list,
                                           sub_dict)
                    else:
                        name_lists.append(sim_name_list)
                        gui_value = gui_values[i] if multi_variable \
                            else gui_values[0]
                        sub_dict = set_dict_entry(gui_value, sim_name_list,
                                                  sub_dict)

            else:
                name_lists.append(sim_names)
                if 'value' in gui_entry:
                    sub_dict = \
                        set_dict_entry(gui_entry['value'], sim_names, sub_dict)
    return target_dict, name_lists


def sim_to_gui_transfer(source_dict, target_dict):

    # get list of widgets only with sim_names
    extracted_gui_entries = list(gen_dict_extract('sim_name', target_dict))
    if extracted_gui_entries:
        for gui_entry in extracted_gui_entries:
            # get reference to widget
            widget = gui_entry['object']

            sim_names = gui_entry['sim_name']
            sim_names = gf.ensure_list(sim_names)
            sub_dict = target_dict

            if isinstance(sim_names[0], list):
                gui_values = gf.ensure_list(gui_entry['value'])

                # if len(sim_names) == len(gui_values):
                #     multi_variable = True
                # else:
                #     multi_variable = False
                value_list = []
                for i, sim_name_list in enumerate(sim_names):
                    if isinstance(sim_name_list[-1], list):
                        pure_name_list = sim_name_list[:-1]
                        for j in range(len(sim_name_list[-1])):
                            value = \
                                get_dict_entry(pure_name_list, source_dict)[j]
                            value_list.append(EntryValue.get_value(value))
                    else:
                        value = get_dict_entry(sim_name_list, source_dict)
                        value_list.append(value)

                widget.set_values(value_list)
            else:
                value = get_dict_entry(sim_names, source_dict)
                widget.set_values(value)
