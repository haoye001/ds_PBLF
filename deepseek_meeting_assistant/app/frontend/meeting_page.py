import streamlit as st
from datetime import datetime


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


def export_summary_to_pdf(summary_text):
    return f"PDF导出功能演示：\n{summary_text}"


def show_right_sidebar(meeting_room_manager, generate_summary_func):
    st.subheader("📅 会议室状态")
    st.markdown(get_room_status_display(meeting_room_manager.meeting_rooms))

    st.markdown("---")
    st.subheader("🎭 AI性格切换")
    personality = st.selectbox(
        "选择AI助手性格：",
        ["专业助理", "幽默风趣", "严谨正式", "友好亲切"],
        key="personality"
    )
    if st.button("应用性格"):
        st.success(f"AI性格已切换为：{personality}")

    st.markdown("---")
    st.subheader("📝 会议总结")
    uploaded_file = st.file_uploader("上传会议记录", type=['txt', 'md', 'docx'])
    summary_topic = st.text_input("会议主题（可选）", key="summary_topic")

    if st.button("🎯 生成总结") and uploaded_file:
        with st.spinner("正在生成专业会议纪要..."):
            try:
                if uploaded_file.type == "text/plain":
                    meeting_notes = uploaded_file.read().decode("utf-8")
                else:
                    meeting_notes = "文件内容读取演示"

                summary = generate_summary_func(meeting_notes, summary_topic)
                st.session_state.current_summary = summary
                st.markdown("### 📋 会议纪要")
                st.markdown(summary)
            except Exception as e:
                st.error(f"处理文件失败: {str(e)}")

    if st.session_state.get('current_summary'):
        st.markdown("---")
        st.markdown("**当前纪要：**")
        st.text_area("内容", st.session_state.current_summary, height=150, key="summary_display")
        if st.button("📄 导出"):
            pdf_content = export_summary_to_pdf(st.session_state.current_summary)
            st.download_button(
                label="📥 下载",
                data=pdf_content,
                file_name="meeting_summary.txt",
                mime="text/plain"
            )


def show_chat_interface(chat_history, meeting_room_manager, recognize_intent_func):
    st.subheader("💬 多轮对话")

    chat_container = st.container(height=600)
    with chat_container:
        if chat_history:
            for msg in chat_history[-10:]:
                with st.chat_message("user"):
                    st.write(f"**{msg['timestamp']}** {msg['user']}")
                with st.chat_message("assistant"):
                    st.write(msg['assistant'])
        else:
            st.info("开始您的第一次对话吧！")

    user_input = st.text_input("请输入您的问题或指令：", key="user_input")

    col_send, col_clear = st.columns([1, 1])
    with col_send:
        send_button = st.button("🚀 发送", use_container_width=True)
    with col_clear:
        if st.button("🗑️ 清空历史", use_container_width=True):
            return True, False, None

    if send_button and user_input.strip():
        return False, True, user_input

    return False, False, None
