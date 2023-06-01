from . import cooling_settings
from . import simulation
from . import cell_settings
from . import manifold_settings
from . import physical_properties
from . import operating_conditions


main_frame_dicts = [cell_settings.tab_dict,
                    manifold_settings.tab_dict,
                    cooling_settings.tab_dict,
                    physical_properties.tab_dict,
                    operating_conditions.tab_dict,
                    simulation.tab_dict]

# remove_keys = ['grid', 'grid_location', 'columnspan', 'command',
#                'command_order']
# save_as_json = copy.deepcopy(main_frame_dicts)
# for item in remove_keys:
#     data_transfer.remove_key(item, save_as_json)
#
# with open('layout_settings.json', 'w') as file:
#     json.dump(save_as_json, file, indent=2)