import time
import requests

TOO_MANY_REQUESTS_ERROR_CODE = 6
USER_WAS_DELETED_OR_BANNED_ERROR_CODE = 18


class VkApiClient:

    def __init__(self, vk_token, vk_version):
        self.vk_token = vk_token
        self.vk_version = vk_version

    def users(self):
        return Users(self.vk_token, self.vk_version)

    def friends(self):
        return Friends(self.vk_token, self.vk_version)

    def groups(self):
        return Groups(self.vk_token, self.vk_version)


class VkMethod:

    def __init__(self, token, version):
        self.token = token
        self.version = version

    def call_api_method(self, method, params):
        """
        Api method realisation
        """

        params['access_token'] = self.token
        params['v'] = self.version

        request_vk = requests.Session()

        while True:
            try:
                response = request_vk.get('/'.join(['https://api.vk.com/method', method]), params=params, timeout=1)
            except requests.exceptions.ReadTimeout:
                print('\rReadTimeout')
                continue
            except Exception as e:
                print('\rUnspecified error {}'.format(e))
                return None

            if not response.ok:
                print("\nError:\n" + response.text)
                return None
            elif "error" in response.json():
                error = response.json()["error"]

                if error["error_code"] == TOO_MANY_REQUESTS_ERROR_CODE:
                    time.sleep(0.3)
                    continue

                if error["error_code"] == USER_WAS_DELETED_OR_BANNED_ERROR_CODE:
                    print("\rUser with id={0} was deleted or banned - skipped".format(params['user_id']))
                    return None

                print("\nError:\n" + error["error_msg"])
                return None
            else:
                break

        return response.json()['response']


class Users(VkMethod):

    def get_users(self, user_id):
        """
        Return a dict with method parameters of User
        """
        return self.call_api_method("users.get", dict(user_ids=user_id))


class Friends(VkMethod):

    def get_friends(self, user_id):
        """
        Return a dict with method parameters of Friends
        """
        return self.call_api_method("friends.get", dict(user_id=user_id))


class Groups(VkMethod):
    """
    Groups method realisation
    """

    def get_groups(self, user_id):
        """
        Return the dict with method parameters
        """
        return self.call_api_method("groups.get", dict(user_id=user_id,
                                                       extended=0,
                                                       count=1000))

    def get_extend_group_info(self, user_id):
        """
        Return the dict with extended method parameters
        """
        return self.call_api_method("groups.get", dict(user_id=user_id,
                                                       extended=1,
                                                       fields='members_count',
                                                       count=1000))
