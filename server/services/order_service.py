from dao.order_dao import OrderDao


class OrderService:
    def __init__(self):
        self.order_dao = OrderDao()

    def get_order_by_user(self, user):
        order_list = self.order_dao.get_order_by_user(user)
        return order_list

    def add_order(self, user, snack_list, location):
        result = self.order_dao.add_order(user, snack_list, location)
        return result
