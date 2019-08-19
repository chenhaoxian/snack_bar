class Order:
    def __init__(self, order_id, user, snack_list, total_price, total_amount, created_date, location):
        self.order_id = order_id
        self.user = user
        self.snack_list = snack_list
        self.total_price = total_price
        self.total_amount = total_amount
        self.created_date = created_date
        self.location = location
