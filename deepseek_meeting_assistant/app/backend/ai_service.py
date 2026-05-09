from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", "your_api_key_here"),
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
你是一个专业的会议室智能助理。你的任务是分析用户的自然语言输入，识别用户的意图，并提取关键信息。

**意图类型：**
- "query"：查询会议室状态、空闲时间等信息
- "book"：预约会议室，需要提取时间、人数等信息
- "cancel"：取消已有的预约
- "summarize"：总结会议内容
- "unknown"：不相关的其他话题

**输出格式：**
你必须严格返回JSON格式，不要包含任何其他文本：
{
  "intent": "query|book|cancel|summarize|unknown",
  "time": "提取的时间信息，如'14:00'或'明天上午'",
  "participants": 参与人数（整数）,
  "room": "会议室名称，如'A会议室'",
  "topic": "会议主题（如果是总结请求）"
}

**Few-shot示例：**
输入："会议室现在空着吗？" → {"intent": "query", "time": null, "participants": null, "room": null, "topic": null}
输入："帮我预约明天上午10点的A会议室，5个人开产品会议" → {"intent": "book", "time": "明天上午10点", "participants": 5, "room": "A会议室", "topic": "产品会议"}
输入："取消我刚才预约的会议" → {"intent": "cancel", "time": null, "participants": null, "room": null, "topic": null}
输入："总结一下这次会议的内容" → {"intent": "summarize", "time": null, "participants": null, "room": null, "topic": null}
"""


def recognize_intent(user_input, context=None):
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if context and len(context) > 0:
            context_text = "\n".join([f"用户: {msg['user']}\n助手: {msg['assistant']}" for msg in context[-3:]])
            messages.append({"role": "system", "content": f"对话上下文：\n{context_text}"})

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.1
        )

        result = response.choices[0].message.content.strip()
        return json.loads(result)
    except Exception as e:
        return {"intent": "error", "error": str(e)}


def generate_meeting_summary(meeting_notes, topic=None):
    try:
        summary_prompt = f"""
        请根据以下会议记录生成一份专业的会议纪要：

        会议主题：{topic or "未指定"}
        会议记录：
        {meeting_notes}

        请生成包含以下内容的结构化纪要：
        1. 📋 会议基本信息（时间、地点、参会人员）
        2. 🎯 会议目标与议题
        3. 💡 讨论要点与关键决策
        4. ✅ 行动项与负责人
        5. 📅 后续跟进计划

        要求：
        - 语言专业简洁
        - 使用markdown格式
        - 重点突出关键信息
        """

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.3,
            max_tokens=1500
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 生成总结失败: {str(e)}"
