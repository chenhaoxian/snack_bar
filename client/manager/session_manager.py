from threading import Timer
from collections import Counter

class SessionManager(object):
    def __init__(self):
        self.timer = None
        self.user_session = {}
        self.reset_user_session()
        self.test = 1
        self.snack_keep_time = 0
        self.detected_faces_history = []

    def update_detected_faces_history(self, location_user_infos):
        if len(self.detected_faces_history) is 15:
            self.detected_faces_history.pop(0)
        if(any(location_user_infos)):
            if len(location_user_infos) > 1:
                self.detected_faces_history = []
            elif not any(location_user_infos[0]['user_info']) :
                self.detected_faces_history.append('Unknown')
            elif any(location_user_infos[0]['user_info']) :
                self.detected_faces_history.append(location_user_infos[0]['user_info'])
        else:
            if(any(self.detected_faces_history)):
                self.detected_faces_history.pop(0)


    def get_high_probability_user(self):
        recog_ids = []
        union_id_face_map = {}
        for user in self.detected_faces_history:
            if user is 'Unknown':
                recog_ids.append(user)
                union_id_face_map['Unknown'] = 'Unknown'
            else :
                recog_ids.append(user['profile']['unionId'])
                union_id_face_map[user['profile']['unionId']] = user

        most_common_list = Counter(recog_ids).most_common()

        high_probability_union_id = None
        for index in range(len(most_common_list)):
            if index is 0:
                high_probability_union_id = most_common_list[0][0]
            else:
                if most_common_list[index][1] is most_common_list[index-1][1]:
                    high_probability_union_id = most_common_list[index][0]
                else:
                    break

        high_probability_user = union_id_face_map.get(high_probability_union_id) or {}
        return high_probability_user


    def user_control(self, location_user_infos):
        try:
            self.update_detected_faces_history(location_user_infos)
            high_probility_user = self.get_high_probability_user()
            if(high_probility_user == 'Unknown' ) :
                self.reset_user_session()
                self.session_time_control()
            elif(high_probility_user != {} ):
                location_user_infos = location_user_infos or [{}]
                location_user_infos[0]['user_info'] = high_probility_user

            if len(location_user_infos) is 1:
                if any(location_user_infos[0]['user_info']):
                    if location_user_infos[0]['user_info'] != self.user_session['user_info']\
                            and any(self.user_session['user_info']) :
                        self.reset_user_session()
                        self.session_time_control()
                        is_start_session_time = False
                    else:
                        is_start_session_time = True
                    self.user_session['user_info'] = location_user_infos[0]['user_info']
                    if is_start_session_time and self.timer is None:
                        self.session_time_control()
                        is_start_session_time = False
            elif  len(location_user_infos) is 0:
                pass
            else :
                self.reset_user_session()
                self.session_time_control()


            if not any(self.user_session['user_info']) and any(self.user_session['snack_info']):
                if self.user_session['snack_keep_time'] is 30:
                    self.reset_user_session()
                else:
                    self.user_session['snack_keep_time'] += 1
            else:
                self.user_session['snack_keep_time'] = 0



        except Exception as e:
            print(e)
            self.reset_user_session()


    def snack_control(self, snack_info):
        if(any(snack_info)):
            snack_infos = self.user_session['snack_info']
            snack_infos.append(snack_info)
            self.user_session['snack_info'] = snack_infos
            self.session_time_control()


    def _set_session_time(self, time):
        print('time out run')
        self.user_session['session_time'] = time

    def session_time_control(self):
        if (self.timer is not None):
            self.timer.cancel()
            self.timer = None

        if (self.is_completed_info()):
            self.timer = Timer(8, self._set_session_time, args=(1,))
            self.timer.start()


    def is_completed_info(self):
        return self.check_snack() and self.check_user_info()

    def check_snack(self):
        return bool(self.user_session.get('snack_info'))

    def check_user_info(self):
        return bool(self.user_session.get('user_info'))

    def reset_user_session(self):
        self.user_session['user_info'] = {}
        self.user_session['session_time'] = 0
        self.user_session['snack_info'] = []

    def get_user_session(self):
        return self.user_session

    def set_user_session(self, user_session):
        self.user_session = user_session

    def set_test(self, num):
        self.test = num

    def get_test(self):
        return self.test