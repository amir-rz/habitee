import requests
import json
from datetime import datetime


def get_formated_date(date=None):
    """ Return today's date in yyyyMMdd format. Ex. 20210212 """
    now: date
    if date != None:
        now = date
    else:
        now = datetime.now()
    today = now.strftime("%Y%m%d")

    return today


class Habitee:
    """ Using pixela API to track our habits """

    def __init__(self, username, token):
        self.username = username
        self.token = token
        self.headers = {
            "X-USER-TOKEN": self.token
        }
        self.pixela_endpoint = "https://pixe.la/v1/users"

    def create_user(self, agreeTermsOfService="yes", notMinor="yes"):
        """ Sign up a new user on pixela """
        uesr_params = {
            "token": self.token,
            "username": self.username,
            "agreeTermsOfService": agreeTermsOfService,
            "notMinor": notMinor
        }
        res = requests.post(self.pixela_endpoint, json=uesr_params)
        print(res.text)
        return res

    def update_user(self, newToken=str):
        update_user_data = {
            "newToken": newToken
        }
        res = requests.put(f"{self.pixela_endpoint}/{self.username}",
                           json=update_user_data, headers=self.headers)
        print(res.text)
        return res

    def create_graph(self, id=str, name=str, unit=str, type=str, color=str):
        """ Create a new graph to track you're habits on. """
        self.pixela_graph_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs"

        graph_config = {
            "id": id,
            "name": name,
            "unit": unit,
            "type": type,
            "color": color
        }
        res = requests.post(self.pixela_graph_endpoint,
                            json=graph_config, headers=self.headers)
        print(
            f"Graph link: https://pixe.la/v1/users/{self.username}/graphs/{id}.html")
        print(res.text)
        return res

    def pixel_new(self, graphId=str, date=str, quantity=str, optionalData=''):
        """ Create a new pixel """
        self.pixela_new_pixel_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs/{graphId}"
        new_pixel_data = {
            "date": date,
            "quantity": quantity,
            "optionalData": optionalData,

        }
        res = requests.post(url=self.pixela_new_pixel_endpoint,
                            json=new_pixel_data, headers=self.headers)
        print(self.pixela_new_pixel_endpoint)
        return res.text

    def pixel_update(self, graphId, date, quantity=str):
        """ Update an existing pixel """
        new_date = get_formated_date(date)
        self.pixela_update_pixel_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs/{graphId}/{new_date}"
        data = {
            "quantity": quantity
        }
        res = requests.put(self.pixela_update_pixel_endpoint,
                           json=data, headers=self.headers)
        print(res.text)
        return res

    def pixel_delete(self, graphId, date):
        """ delete an existing pixel """
        new_date = get_formated_date(date)
        self.pixela_update_pixel_endpoint = f"{self.pixela_endpoint}/{self.username}/graphs/{graphId}/{new_date}"

        res = requests.delete(
            self.pixela_update_pixel_endpoint, headers=self.headers)
        print(res.text)
        return res


my_habitee = Habitee("username", "token")

today = get_formated_date()

# TODO:
# - create a user
# - create a graph 
# - and start using the app

# -- create user
# my_habitee.create_user()

# -- create graph
# my_habitee.create_graph("Running","Daily running graph", "Kilometers", "int", "sora")

# -- new pixel
# pixel_new = my_habitee.pixel_new(
#     "coding-1", today, "60")

# -- update pixel
# my_habitee.pixel_update("coding-1",datetime.now(),"180")

# -- delete pixel
# my_habitee.pixel_delete("coding-1",datetime.now())