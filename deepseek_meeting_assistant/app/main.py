import streamlit as st
import time
from datetime import datetime
from backend import MeetingRoom, UserManager, ChatHistory, recognize_intent, generate_meeting_summary
from frontend import (
    show_login_page,
    show_admin_panel,
    show_edit_meetings,
    show_manage_users,
    show_right_sidebar,
    show_chat_interface
)


def init_session_state():
    if 'meeting_room_manager' not in st.session_state:
        st.session_state.meeting_room_manager = MeetingRoom()

    if 'user_manager' not in st.session_state:
        st.session_state.user_manager = UserManager()

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ChatHistory()

    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

    if 'admin_mode' not in st.session_state:
        st.session_state.admin_mode = None

    if 'current_summary' not in st.session_state:
        st.session_state.current_summary = ""


def main():
    init_session_state()

    if not st.session_state.current_user:
        username, password, role = show_login_page()

        if username and password and role:
            user = st.session_state.user_manager.login(username, password, role)
            if user:
                st.session_state.current_user = user
                st.success(f"登录成功！欢迎, {user['name']}")
                time.sleep(1)
                st.rerun()
            else:
                st.error("用户名、密码或角色不正确")
        return

    st.set_page_config(page_title="DeepSeek智能会议助手", page_icon="🤖", layout="wide")

    st.title("🚀 DeepSeek 完整智能会议助手")
    st.markdown(f"欢迎, **{st.session_state.current_user['name']}** ({'管理员' if st.session_state.current_user['role'] == 'admin' else '普通用户'})")

    if st.button("🔓 登出"):
        st.session_state.current_user = None
        st.session_state.admin_mode = None
        st.rerun()

    if st.session_state.current_user['role'] == 'admin':
        show_admin_panel()

    if st.session_state.admin_mode == "edit_meetings":
        show_edit_meetings(st.session_state.meeting_room_manager)
        return
    elif st.session_state.admin_mode == "manage_users":
        show_manage_users(st.session_state.user_manager)
        return

    col_main, col_right = st.columns([2, 1])

    with col_main:
        clear_chat, process_input, user_input = show_chat_interface(
            st.session_state.chat_history.get_history(),
            st.session_state.meeting_room_manager,
            recognize_intent
        )

        if clear_chat:
            st.session_state.chat_history.clear()
            st.rerun()

        if process_input and user_input:
            with st.spinner("AI正在思考中..."):
                time.sleep(1)

                intent_result = recognize_intent(user_input, st.session_state.chat_history.get_history())

                if intent_result.get("intent") == "query":
                    response = f"📊 当前会议室状态：\n\n{get_room_status_display(st.session_state.meeting_room_manager.meeting_rooms)}"

                elif intent_result.get("intent") == "book":
                    time_info = intent_result.get("time", "未指定时间")
                    participants = intent_result.get("participants", "未指定人数")
                    room = intent_result.get("room", "A会议室")
                    topic = intent_result.get("topic", "会议")

                    booking_info = f"{time_info} {participants}人 {topic}"
                    st.session_state.meeting_room_manager.update_room_status(room, "占用", booking_info)

                    response = f"✅ 预约成功！\n- 🏢 会议室：{room}\n- ⏰ 时间：{time_info}\n- 👥 参与人数：{participants}\n- 📝 主题：{topic}\n\n📅 状态已更新！"

                elif intent_result.get("intent") == "cancel":
                    canceled_rooms = []
                    for room_name in st.session_state.meeting_room_manager.meeting_rooms:
                        if st.session_state.meeting_room_manager.meeting_rooms[room_name]["status"] == "占用":
                            st.session_state.meeting_room_manager.update_room_status(room_name, "空闲")
                            canceled_rooms.append(room_name)

                    if canceled_rooms:
                        response = f"✅ 已取消以下会议室的预约：{', '.join(canceled_rooms)}"
                    else:
                        response = "ℹ️ 当前没有需要取消的预约。"

                elif intent_result.get("intent") == "summarize":
                    response = "📝 请使用右侧面板上传会议记录文件，我来为您生成专业总结。"

                elif intent_result.get("intent") == "error":
                    response = f"❌ 处理失败：{intent_result.get('error', '未知错误')}"
                else:
                    response = "🤔 我不太明白您的意思。请尝试：\n- 查询会议室状态\n- 预约会议（如：'预约明天上午A会议室'）\n- 取消预约\n- 总结会议内容"

                st.session_state.chat_history.add_message(user_input, response)
                st.rerun()

    with col_right:
        show_right_sidebar(st.session_state.meeting_room_manager, generate_meeting_summary)

    st.markdown("---")
    st.markdown("*Powered by DeepSeek AI | ")


def get_room_status_display(meeting_rooms):
    status_text = ""
    for room, info in meeting_rooms.items():
        status_emoji = "🟢" if info['status'] == "空闲" else "🔴"
        status_text += f"{status_emoji} **{room}**\n"
        status_text += f"   状态: {info['status']}\n"
        status_text += f"   容量: {info['capacity']}人\n"
        status_text += f"   设备: {info['equipment']}\n"
        if info['bookings']:
            status_text += "   📅 预约:\n"
            for booking in info['bookings']:
                status_text += f"      • {booking}\n"
        status_text += "\n"
    return status_text


if __name__ == "__main__":
    main()
