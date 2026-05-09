import streamlit as st
import random


def generate_captcha():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
    return ''.join(random.choice(chars) for _ in range(4))


def show_login_page():
    if 'captcha' not in st.session_state:
        st.session_state.captcha = generate_captcha()

    st.markdown("""
        <style>
        .main-login {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .login-header {
            text-align: center;
            margin-bottom: 32px;
        }
        .login-icon {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px;
            font-size: 36px;
        }
        .login-title {
            font-size: 24px;
            font-weight: 700;
            color: #1a2744;
            margin-bottom: 6px;
        }
        .login-subtitle {
            font-size: 14px;
            color: #64748b;
        }
        .captcha-display {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            padding: 12px 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: 700;
            color: #2d5a87;
            letter-spacing: 6px;
            font-family: 'Courier New', monospace;
            margin-bottom: 8px;
        }
        .login-footer {
            text-align: center;
            margin-top: 24px;
            color: #94a3b8;
            font-size: 13px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="main-login">
                <div class="login-header">
                    <div class="login-icon">📅</div>
                    <div class="login-title">会议室预约系统</div>
                    <div class="login-subtitle">专业、高效的会议管理助手</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        role = st.selectbox(
            "选择角色",
            ["admin", "user"],
            format_func=lambda x: "管理员" if x == "admin" else "普通用户"
        )

        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")

        st.markdown(f'<div class="captcha-display">{st.session_state.captcha}</div>', unsafe_allow_html=True)
        captcha_input = st.text_input("验证码")

        c1, c2 = st.columns([3, 1])
        with c1:
            submitted = st.button("登录", type="primary", use_container_width=True)
        with c2:
            if st.button("🔄"):
                st.session_state.captcha = generate_captcha()
                st.rerun()

        st.markdown("""
            <div class="login-footer">
                © 2024 会议室预约系统 · 专业办公助手
            </div>
        """, unsafe_allow_html=True)

        if submitted:
            if not username or not password:
                st.error("请填写完整的用户名和密码")
            elif not captcha_input or captcha_input.upper() != st.session_state.captcha.upper():
                st.error("验证码错误")
                st.session_state.captcha = generate_captcha()
            else:
                return username, password, role

    return None, None, None
