import streamlit as st


def show_admin_panel():
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ 管理员面板")

    if st.sidebar.button("修改会议记录"):
        st.session_state.admin_mode = "edit_meetings"
    if st.sidebar.button("管理用户"):
        st.session_state.admin_mode = "manage_users"
    if st.sidebar.button("返回主界面"):
        st.session_state.admin_mode = None


def show_edit_meetings(meeting_room_manager):
    st.subheader("✏️ 修改会议记录")

    room_name = st.selectbox("选择会议室", list(meeting_room_manager.meeting_rooms.keys()))

    if room_name:
        room = meeting_room_manager.meeting_rooms[room_name]
        new_status = st.selectbox("状态", ["空闲", "占用"], index=0 if room['status'] == "空闲" else 1)
        new_capacity = st.number_input("容量", min_value=1, max_value=100, value=room['capacity'])
        new_equipment = st.text_input("设备", value=room['equipment'])

        st.subheader("预约记录")
        bookings_list = room['bookings'].copy()
        new_bookings = []
        for i, booking in enumerate(bookings_list):
            new_bookings.append(st.text_input(f"预约 {i+1}", value=booking))
        room['bookings'] = new_bookings

        new_booking = st.text_input("添加新预约")

        if st.button("保存修改"):
            meeting_room_manager.modify_room(room_name, new_status, new_capacity, new_equipment, new_booking if new_booking else None)
            st.success("会议记录已更新")


def show_manage_users(user_manager):
    st.subheader("👥 管理用户")

    action = st.selectbox("选择操作", ["查看用户", "添加用户", "修改用户", "删除用户"])

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
