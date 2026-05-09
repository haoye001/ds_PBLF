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
    st.markdown("""
        <style>
        .sidebar-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }
        
        .sidebar-title {
            font-size: 16px;
            font-weight: 700;
            color: #1a2744;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .room-status-card {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            border-left: 4px solid #2d5a87;
        }
        
        .room-name {
            font-size: 15px;
            font-weight: 600;
            color: #1a2744;
            margin-bottom: 8px;
        }
        
        .room-meta {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 4px;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .status-available {
            background: #dcfce7;
            color: #16a34a;
        }
        
        .status-occupied {
            background: #fee2e2;
            color: #dc2626;
        }
        
        .btn-action {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 12px;
        }
        
        .btn-action:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(30, 58, 95, 0.3);
        }
        
        .btn-secondary-action {
            width: 100%;
            padding: 12px;
            background: #f1f5f9;
            color: #475569;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-secondary-action:hover {
            background: #e2e8f0;
        }
        
        .upload-area {
            border: 2px dashed #cbd5e1;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            transition: all 0.3s ease;
            margin-bottom: 16px;
        }
        
        .upload-area:hover {
            border-color: #2d5a87;
            background: #f8fafc;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📅 会议室状态</div>', unsafe_allow_html=True)
    
    for room_name, room_info in meeting_room_manager.meeting_rooms.items():
        status_class = "status-available" if room_info['status'] == "空闲" else "status-occupied"
        status_text = "空闲" if room_info['status'] == "空闲" else "占用"
        status_icon = "🟢" if room_info['status'] == "空闲" else "🔴"
        
        st.markdown(f'''
        <div class="room-status-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <div class="room-name">🏢 {room_name}</div>
                <span class="status-badge {status_class}">{status_icon} {status_text}</span>
            </div>
            <div class="room-meta">👥 容量: {room_info['capacity']}人</div>
            <div class="room-meta">⚙️ 设备: {room_info['equipment'].split('、')[0]}</div>
            {f'<div style="margin-top: 8px; padding: 8px; background: rgba(251, 191, 36, 0.1); border-radius: 8px; font-size: 12px; color: #b45309;">📅 {room_info["bookings"][0]}</div>' if room_info['bookings'] else ''}
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🎯 AI助手设置</div>', unsafe_allow_html=True)
    
    personality = st.selectbox(
        "",
        ["专业助理", "幽默风趣", "严谨正式", "友好亲切"],
        key="personality",
        label_visibility="hidden"
    )
    
    st.button("应用设置", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📝 会议总结</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=['txt', 'md', 'docx'],
        label_visibility="hidden",
        help="支持 txt, md, docx 格式"
    )
    summary_topic = st.text_input("会议主题（可选）", key="summary_topic", placeholder="请输入会议主题")

    if st.button("生成专业总结", use_container_width=True) and uploaded_file:
        with st.spinner("正在分析会议内容..."):
            try:
                if uploaded_file.type == "text/plain":
                    meeting_notes = uploaded_file.read().decode("utf-8")
                else:
                    meeting_notes = "文件内容读取演示"

                summary = generate_summary_func(meeting_notes, summary_topic)
                st.session_state.current_summary = summary

                st.markdown("### 📋 AI生成的会议纪要")
                st.markdown(summary)
            except Exception as e:
                st.error(f"处理文件失败: {str(e)}")

    if st.session_state.get('current_summary'):
        st.markdown("---")
        st.markdown("### 📄 当前纪要")

        col1, col2 = st.columns(2)
        with col1:
            st.text_area(
                "",
                st.session_state.current_summary,
                height=120,
                key="summary_display",
                label_visibility="collapsed"
            )
        with col2:
            st.markdown("<div style='height: 120px; display: flex; align-items: center;'>", unsafe_allow_html=True)
            pdf_content = export_summary_to_pdf(st.session_state.current_summary)
            st.download_button(
                label="📥 下载纪要",
                data=pdf_content,
                file_name=f"会议纪要_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_chat_interface(chat_history, meeting_room_manager, recognize_intent_func):
    st.markdown("""
        <style>
        .chat-container {
            background: #ffffff;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
            min-height: 400px;
        }
        
        .chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .chat-title {
            font-size: 18px;
            font-weight: 700;
            color: #1a2744;
        }
        
        .quick-actions {
            display: flex;
            gap: 8px;
        }
        
        .quick-btn {
            padding: 8px 14px;
            background: #f1f5f9;
            border: none;
            border-radius: 8px;
            font-size: 13px;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .quick-btn:hover {
            background: #e2e8f0;
            color: #1e3a5f;
        }
        
        .message-wrapper {
            margin-bottom: 20px;
        }
        
        .message-user {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .message-assistant {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .avatar-user {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 16px;
            flex-shrink: 0;
        }
        
        .avatar-assistant {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #2d5a87 0%, #3b82f6 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 16px;
            flex-shrink: 0;
        }
        
        .message-content {
            flex: 1;
            padding: 14px 18px;
            background: #f8fafc;
            border-radius: 14px;
            font-size: 14px;
            line-height: 1.6;
            color: #334155;
        }
        
        .message-content-assistant {
            flex: 1;
            padding: 14px 18px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            border-radius: 14px;
            font-size: 14px;
            line-height: 1.6;
            color: white;
        }
        
        .message-time {
            font-size: 12px;
            color: #94a3b8;
            margin-top: 4px;
        }
        
        .empty-state {
            text-align: center;
            padding: 48px 24px;
            color: #64748b;
        }
        
        .input-area {
            background: #ffffff;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
            margin-top: 20px;
        }
        
        .input-wrapper {
            display: flex;
            gap: 12px;
        }
        
        .chat-input {
            flex: 1;
            padding: 14px 18px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 14px;
            transition: all 0.3s ease;
            background: #fafbfc;
        }
        
        .chat-input:focus {
            outline: none;
            border-color: #2d5a87;
            background: #fff;
        }
        
        .send-btn {
            padding: 14px 28px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(30, 58, 95, 0.3);
        }
        
        .action-buttons {
            display: flex;
            gap: 12px;
            margin-top: 16px;
        }
        
        .action-btn {
            flex: 1;
            padding: 12px;
            background: #f1f5f9;
            border: none;
            border-radius: 10px;
            font-size: 13px;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .action-btn:hover {
            background: #e2e8f0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('''
        <div class="chat-header">
            <div class="chat-title">💬 智能对话助手</div>
            <div class="quick-actions">
                <button class="quick-btn" onclick="insertText('查询会议室状态')">查询状态</button>
                <button class="quick-btn" onclick="insertText('预约会议室')">预约会议</button>
                <button class="quick-btn" onclick="insertText('取消预约')">取消预约</button>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if chat_history:
        for msg in chat_history[-10:]:
            st.markdown(f'''
            <div class="message-wrapper">
                <div class="message-user">
                    <div class="avatar-user">👤</div>
                    <div>
                        <div class="message-content">{msg['user']}</div>
                        <div class="message-time">{msg['timestamp']}</div>
                    </div>
                </div>
                
                <div class="message-assistant">
                    <div class="avatar-assistant">🤝</div>
                    <div>
                        <div class="message-content-assistant">{msg['assistant']}</div>
                        <div class="message-time">DeepSeek · {msg['timestamp']}</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="empty-state">
            <div style="font-size: 56px; margin-bottom: 16px;">💼</div>
            <h3 style="margin-bottom: 8px; color: #475569;">开始对话</h3>
            <p style="font-size: 14px;">输入您的需求，我将为您提供专业的会议管理服务</p>
            <div style="margin-top: 20px;">
                <button class="quick-btn" style="margin-right: 8px;" onclick="insertText('查询会议室状态')">查询会议室状态</button>
                <button class="quick-btn" onclick="insertText('预约明天上午10点A会议室')">预约会议</button>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    
    col_input, col_send = st.columns([4, 1])
    with col_input:
        user_input = st.text_input(
            "",
            key="user_input",
            placeholder="输入您的指令或问题...",
            label_visibility="collapsed"
        )
    with col_send:
        send_button = st.button("发送", use_container_width=True)

    col_clear, col_help = st.columns(2)
    with col_clear:
        if st.button("🗑️ 清空历史", use_container_width=True):
            return True, False, None
    with col_help:
        if st.button("❓ 帮助", use_container_width=True):
            st.info("""
            **💡 使用指南：**

            1. **查询状态**：输入"查询会议室状态"
            2. **预约会议**：输入"预约明天上午10点A会议室"
            3. **取消预约**：输入"取消预约"
            4. **生成总结**：上传会议记录并点击生成总结
            """)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <script>
        function insertText(text) {
            var input = window.parent.document.querySelector('input[aria-label=""]');
            if (input) {
                input.value = text;
                input.dispatchEvent(new Event('input'));
            }
        }
        </script>
    """, unsafe_allow_html=True)

    if send_button and user_input.strip():
        return False, True, user_input

    return False, False, None
