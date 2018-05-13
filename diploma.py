from api import VkApiClient

import utils

if __name__ == '__main__':
    config = utils.get_config()
    vkClient = VkApiClient(config['vk_api_token'], config['vk_api_version'])

    username = input('Enter id or nickname of user: ')
    quantity_of_friends = int(input('Enter max quantity of friends consisting in groups: '))

    # Getting user id by username
    my_user_id = vkClient.users().get_users(username)[0]["id"]

    # Getting id list friends id
    list_of_friends_id = vkClient.friends().get_friends(my_user_id)["items"]

    # Getting list groups, where user consist
    list_of_my_groups_id = vkClient.groups().get_groups(my_user_id)["items"]

    # Getting dict with groups and quantity friends in this groups
    groups = utils.get_friends_groups(vkClient, list_of_my_groups_id, list_of_friends_id)

    # Getting wanted groups list
    result_list = utils.choose_wanted_groups_with_friends_quantity(groups, quantity_of_friends)

    # Getting list of extended groups, where user consist
    list_groups_full = vkClient.groups().get_extend_group_info(my_user_id)["items"]

    # Getting wanted list with extended data dict
    json_file = utils.create_list_of_dict_with_extended_data(list_groups_full, result_list)

    # Record file json format
    utils.dump_list_of_dict_to_json_file("groups", json_file)
