from multiprocessing import process
import requests
from config import config_option

class StoreSnack(object):
    def __init__(self):
        pass

    def store(self, barcodes, user_session):
        self.put_in_order_data(barcodes, user_session)
        # process(target=self.put_in_order_data, args=(barcodes,order_data))

    def put_in_order_data(self, barcodes, user_session):
        result = self.get_product_info(barcodes)
        print(result)
        if(result is not None and any(result)):
            user_session.get('session_manager').snack_control(result)


    def get_product_info(self, barcodes):
        # product_info_barcode_map = {'6937748304630':'note book1', '6921180962022':'note book2'}
        # return 'note book'

        # build request params
        result = {}
        if(barcodes):
            barcode_id = [x.data for x in barcodes][0].decode("utf-8")
            try:
                res = requests.get(config_option['BACKEND_URL']+config_option['QUERY_SNACK_API']+barcode_id, timeout=5)
                # res = requests.request('GET', 'http://shaza-2-w7:5901/api/snack/',
                #                      timeout=3)
                print('request snack info')
                result = res.json()
                return map_snack_by_phase(result)
            except Exception as e:
                print(e)
            print('result:{result}'.format(result=result))
        return result

def map_snack_by_phase(snacks):
    for item in snacks:
        if(item['location'] == config_option['LOCATION']):
            return item
    return {}


def process_order_for_server(snack_info):
    # snack_info = order_data['snack_info']
    processed_datas = []
    # for item in snack_info:
    #     amount = snack_info.count(item)
    #     processed_data.append(dict({'amount': amount}, **item))

    # have_count = []
    # for item1 in snack_info:
    #     if(item1['snack_code'] not in snack_info):
    #         amount = 0
    #         for item2 in snack_info:
    #             if(item1['snack_code'] == item2['snack_code']):
    #                 amount +=1
    #         processed_datas.append(dict({'amount': amount}, **item1))
    #         have_count.append(item1['snack_code'])



    for snack_info_index in range(len(snack_info)):
        item = snack_info[snack_info_index]
        if len(processed_datas) is 0:
            item['amount'] = 1
            processed_datas.append(item)
        else:
            is_exist = False
            for index in range(len(processed_datas)):
                data = processed_datas[index]
                if item['snack_code'] == data['snack_code']:
                    processed_datas[index]['amount'] += 1
                    is_exist = True
                    break
            if not is_exist:
                item['amount'] = 1
                processed_datas.append(item)



        # for index in range(len(processed_datas)) :
        #     data = processed_datas[index]
        #     if data['snack_code'] == item['snack_code']:
        #         amount = data.get('amount',0)
        #         amount += 1
        #         processed_datas[index]['amount'] = amount
        #     else:
        #         processed_datas.append(item)
        #         processed_datas[index+1]['amount'] = 1



    return {'record':processed_datas, 'total_price':calculate_total_price(processed_datas)}

def calculate_total_price(data):
    total_price = 0
    for item in data:
        total_price  += float(item['snack_price']) * int(item['amount'])
    return total_price