import json


def process_percentage(whole, part_of_whole):
    """
    Function return counter in percentage format

    """
    res = (part_of_whole * 100) / whole
    if res != 100:
        return f"\rProcessing: {int(res)}%"
    elif res == 100:
        return "\rProcessing: Done"


def dump_list_of_dict_to_json_file(file_name, list_record):
    """
    Writing data on json
    """
    with open('.'.join([file_name, 'json']), 'w', encoding='utf-8') as file:
        json.dump(list_record, file, indent=2, ensure_ascii=False)


def choose_wanted_groups_with_friends_quantity(groups_users, quantity_of_friends):
    """
    Return the id numbers of groups
    """
    groups_id = []
    for key, value in groups_users.items():
        if value <= quantity_of_friends:
            groups_id.append(key)
    return groups_id


def create_list_of_dict_with_extended_data(extended_groups_info, groups_list):
    """
    Return the list of dict with extended info of groups
    """
    groups = []
    for group in extended_groups_info:
        result = {}
        if group["id"] in groups_list:
            result["id"] = group["id"]
            result["name"] = group["name"]
            result["members_count"] = group["members_count"]
        else:
            continue
        groups.append(result)
    return groups


def get_config():
    with open('config.json') as f:
        return json.load(f)


def get_friends_groups(vk_client, list_of_my_groups_ids, list_friends_id):
    """
    Return the dict with friends quantity in every group

    """

    dict_of_my_groups_ids = dict.fromkeys(list_of_my_groups_ids, 0)

    for index, friend_id in enumerate(list_friends_id, 1):
        try:
            data = vk_client.groups().get_groups(friend_id)
            if data is not None:
                list_of_friend_groups_ids = data["items"]
            else:
                continue

        except KeyError:
            continue

        for group_id in list_of_friend_groups_ids:
            if group_id in dict_of_my_groups_ids:
                dict_of_my_groups_ids[group_id] += 1

        print(process_percentage(len(list_friends_id), index), end="")

    return dict_of_my_groups_ids
