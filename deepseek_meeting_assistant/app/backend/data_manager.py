from datetime import datetime


SIMULATED_USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "name": "管理员"
    },
    "user1": {
        "password": "user123",
        "role": "user",
        "name": "张三"
    },
    "user2": {
        "password": "user123",
        "role": "user",
        "name": "李四"
    }
}


class MeetingRoom:
    def __init__(self):
        self.meeting_rooms = {
            "A会议室": {"status": "空闲", "capacity": 10, "bookings": [], "equipment": "投影仪、白板"},
            "B会议室": {"status": "占用", "capacity": 20, "bookings": ["2024-01-15 14:00-16:00 张三的产品评审会"], "equipment": "视频会议系统、投影仪"},
            "C会议室": {"status": "空闲", "capacity": 5, "bookings": [], "equipment": "白板、电视"}
        }

    def get_room_status(self, room_name):
        if room_name in self.meeting_rooms:
            return self.meeting_rooms[room_name]
        return None

    def update_room_status(self, room_name, status, booking_info=None):
        if room_name in self.meeting_rooms:
            self.meeting_rooms[room_name]["status"] = status
            if booking_info:
                self.meeting_rooms[room_name]["bookings"].append(booking_info)
            elif status == "空闲":
                self.meeting_rooms[room_name]["bookings"] = []
            return True
        return False

    def get_all_rooms(self):
        return self.meeting_rooms

    def modify_room(self, room_name, status=None, capacity=None, equipment=None, new_booking=None):
        if room_name in self.meeting_rooms:
            if status:
                self.meeting_rooms[room_name]["status"] = status
            if capacity:
                self.meeting_rooms[room_name]["capacity"] = capacity
            if equipment:
                self.meeting_rooms[room_name]["equipment"] = equipment
            if new_booking:
                self.meeting_rooms[room_name]["bookings"].append(new_booking)
            return True
        return False


class UserManager:
    def __init__(self):
        self.users = SIMULATED_USERS.copy()

    def login(self, username, password, role):
        if username in self.users:
            user = self.users[username]
            if user['password'] == password and user['role'] == role:
                return {
                    'username': username,
                    'name': user['name'],
                    'role': user['role']
                }
        return None

    def get_user(self, username):
        if username in self.users:
            return self.users[username]
        return None

    def get_all_users(self):
        return self.users

    def add_user(self, username, password, name, role):
        if username not in self.users:
            self.users[username] = {
                "password": password,
                "role": role,
                "name": name
            }
            return True
        return False

    def update_user(self, username, name=None, password=None, role=None):
        if username in self.users:
            if name:
                self.users[username]["name"] = name
            if password:
                self.users[username]["password"] = password
            if role:
                self.users[username]["role"] = role
            return True
        return False

    def delete_user(self, username):
        if username in self.users and username != "admin":
            del self.users[username]
            return True
        return False
