import streamlit as st
import random


def generate_captcha():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
    return ''.join(random.choice(chars) for _ in range(4))


def show_login_page():
    st.set_page_config(page_title="智能会议登录", page_icon="🔐", layout="centered")

    if 'captcha' not in st.session_state:
        st.session_state.captcha = generate_captcha()

    st.title("🔐 智能会议登录")
    st.markdown("请选择角色并输入登录信息")

    role = st.selectbox("选择角色", ["admin", "user"], format_func=lambda x: "管理员" if x == "admin" else "普通用户")

    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("用户名")
    with col2:
        password = st.text_input("密码", type="password")

    col_captcha, col_refresh = st.columns([2, 1])
    with col_captcha:
        captcha_input = st.text_input("验证码", placeholder="请输入验证码")
    with col_refresh:
        if st.button("🔄 刷新验证码"):
            st.session_state.captcha = generate_captcha()
            st.rerun()

    st.markdown(f"**验证码：** `{st.session_state.captcha}`")

    if st.button("登录"):
        if not captcha_input or captcha_input.upper() != st.session_state.captcha.upper():
            st.error("验证码错误，请重试")
            st.session_state.captcha = generate_captcha()
        else:
            return username, password, role
    return None, None, None
