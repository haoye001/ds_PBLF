import streamlit as st


def show_admin_panel():
    st.markdown("""
        <style>
        .admin-sidebar {
            background: #ffffff;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }
        
        .admin-title {
            font-size: 16px;
            font-weight: 700;
            color: #1a2744;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .admin-btn {
            display: block;
            width: 100%;
            padding: 12px 16px;
            background: #f1f5f9;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            color: #475569;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 8px;
        }
        
        .admin-btn:hover {
            background: #e2e8f0;
            color: #1e3a5f;
        }
        
        .admin-btn.active {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="admin-sidebar">', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="admin-title">⚙️ 管理员面板</div>', unsafe_allow_html=True)

    st.sidebar.button("修改会议记录", use_container_width=True)
    st.sidebar.button("管理用户", use_container_width=True)
    st.sidebar.button("返回主界面", use_container_width=True)

    st.sidebar.markdown('</div>', unsafe_allow_html=True)


def show_edit_meetings(meeting_room_manager):
    st.markdown("""
        <style>
        .edit-container {
            background: #ffffff;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        }
        
        .edit-title {
            font-size: 20px;
            font-weight: 700;
            color: #1a2744;
            margin-bottom: 24px;
        }
        
        .form-label {
            font-size: 13px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
            display: block;
        }
        
        .form-input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s ease;
            background: #fafbfc;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #2d5a87;
            background: #fff;
        }
        
        .btn-save {
            padding: 12px 24px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-save:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(30, 58, 95, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="edit-container">', unsafe_allow_html=True)
    st.markdown('<div class="edit-title">✏️ 修改会议记录</div>', unsafe_allow_html=True)

    room_name = st.selectbox("选择会议室", list(meeting_room_manager.meeting_rooms.keys()), label_visibility="collapsed")

    if room_name:
        room = meeting_room_manager.meeting_rooms[room_name]
        new_status = st.selectbox("", ["空闲", "占用"], index=0 if room['status'] == "空闲" else 1, label_visibility="collapsed")
        new_capacity = st.number_input("容量", min_value=1, max_value=100, value=room['capacity'])
        new_equipment = st.text_input("设备", value=room['equipment'])

        st.markdown("---")
        st.markdown("### 📅 预约记录")
        
        bookings_list = room['bookings'].copy()
        new_bookings = []
        for i, booking in enumerate(bookings_list):
            new_bookings.append(st.text_input(f"预约 {i+1}", value=booking))
        room['bookings'] = new_bookings

        new_booking = st.text_input("添加新预约")

        if st.button("保存修改", use_container_width=True):
            meeting_room_manager.modify_room(room_name, new_status, new_capacity, new_equipment, new_booking if new_booking else None)
            st.success("会议记录已更新")

    st.markdown('</div>', unsafe_allow_html=True)


def show_manage_users(user_manager):
    st.markdown("""
        <style>
        .manage-container {
            background: #ffffff;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        }
        
        .manage-title {
            font-size: 20px;
            font-weight: 700;
            color: #1a2744;
            margin-bottom: 24px;
        }
        
        .action-select {
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 14px;
            background: #fafbfc;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-label {
            font-size: 13px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
            display: block;
        }
        
        .form-input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s ease;
            background: #fafbfc;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #2d5a87;
            background: #fff;
        }
        
        .btn-action {
            padding: 12px 24px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-action:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(30, 58, 95, 0.3);
        }
        
        .user-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        
        .user-table th,
        .user-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .user-table th {
            background: #f8fafc;
            font-weight: 600;
            color: #475569;
        }
        
        .user-table tr:hover {
            background: #f8fafc;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="manage-container">', unsafe_allow_html=True)
    st.markdown('<div class="manage-title">👥 管理用户</div>', unsafe_allow_html=True)

    action = st.selectbox("选择操作", ["查看用户", "添加用户", "修改用户", "删除用户"], label_visibility="collapsed")

    if action == "查看用户":
        users_list = []
        for k, v in user_manager.users.items():
            users_list.append({
                "用户名": k,
                "姓名": v["name"],
                "角色": "管理员" if v["role"] == "admin" else "普通用户"
            })
        st.dataframe(users_list)

    elif action == "添加用户":
        new_username = st.text_input("新用户名")
        new_password = st.text_input("密码", type="password")
        new_name = st.text_input("姓名")
        new_role = st.selectbox("角色", ["admin", "user"], format_func=lambda x: "管理员" if x == "admin" else "普通用户")

        if st.button("添加用户"):
            if new_username and new_password and new_name:
                if user_manager.add_user(new_username, new_password, new_name, new_role):
                    st.success("用户添加成功")
                else:
                    st.error("用户名已存在")
            else:
                st.error("请填写完整信息")

    elif action == "修改用户":
        username = st.selectbox("选择用户", list(user_manager.users.keys()))
        if username:
            user = user_manager.get_user(username)
            if user:
                new_name = st.text_input("姓名", value=user["name"])
                new_password = st.text_input("新密码（留空不修改）", type="password")
                new_role = st.selectbox("角色", ["admin", "user"],
                                        format_func=lambda x: "管理员" if x == "admin" else "普通用户",
                                        index=0 if user["role"] == "admin" else 1)

                if st.button("保存修改"):
                    user_manager.update_user(username, new_name, new_password if new_password else None, new_role)
                    st.success("用户信息已更新")

    elif action == "删除用户":
        username = st.selectbox("选择要删除的用户", [k for k in user_manager.users.keys() if k != "admin"])
        if username and st.button("删除用户"):
            if user_manager.delete_user(username):
                st.success("用户已删除")
            else:
                st.error("删除失败")

    st.markdown('</div>', unsafe_allow_html=True)
