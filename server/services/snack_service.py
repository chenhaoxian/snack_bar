from dao.snack_dao import SnackDao


class SnackService:
    def __init__(self):
        self.snack_dao = SnackDao()

    def get_snack_by_code(self, snack_code):
        get_snack_by_code_criteria = {"snack_code": snack_code}
        snack_list = self.snack_dao.get_snack_list(get_snack_by_code_criteria)
        return snack_list

    def update_snack(self, snack):
        snack_update_result = self.snack_dao.update_snack(snack)
        return snack_update_result

    def get_snack_list(self):
        get_all_list_criteria = {}
        snack_list = self.snack_dao.get_snack_list(get_all_list_criteria)
        return snack_list

    def remove_snack(self, snack_id):
        snack_remove_result = self.snack_dao.remove_snack(snack_id)
        return snack_remove_result
