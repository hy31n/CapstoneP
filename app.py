from flask import Flask, jsonify, make_response, request
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS
import os
import uuid

# Flask 설정
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
CORS(app)

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 메시지 저장소
messages = []

# 메시지 추가 함수
def addMessage(role, content):
    messages.append({
        "role": role,
        "content": content,
        "uid": uuid.uuid4().hex 
    })

# OpenAI API 호출 함수
def requestAI(includePast):
    if includePast and len(messages) > 2:
        tempMessages = messages[-4:]
    else:
        tempMessages = messages[-1:]
    cleanMessages = [{"role": m["role"], "content": m["content"]} for m in tempMessages]

    try:
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            messages=cleanMessages
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        # 쿼터 초과 에러 잡기
        if 'insufficient_quota' in str(e):
            # 더미 답변 반환
            return "현재 API 사용량이 초과되어 답변을 제공할 수 없습니다. 잠시 후 다시 시도해주세요."
        # 그 외 에러는 다시 raise하거나 로그 출력 가능
        raise e

# JSON 응답 생성 함수
def makeResponse(status, result, resultCode, data):
    return make_response(jsonify({
        "result": result,
        "resultCode": resultCode,
        "data": data
    }), status)

# Chat API 엔드포인트
@app.route('/api/chat', methods=['POST'])
def chat():
    print('Request:: Chat')
    try:
        question = request.form['question']
        addMessage("user", question)
        answer = requestAI(includePast=False)
        addMessage("assistant", answer)
        return makeResponse(200, True, 200, {"answer": answer})

    except Exception as e:
        print('---------------') 
        print('Error:: Chat')
        print(e)
        print('---------------')

        # 쿼터 초과 에러 처리
        if 'insufficient_quota' in str(e):
            return makeResponse(200, True, 200, {
                "answer": "현재 API 사용량이 초과되어 답변을 제공할 수 없습니다. 잠시 후 다시 시도해주세요."
            })

        return makeResponse(500, False, 500, {"resultMessage": "문제가 발생했습니다."})

if __name__ == '__main__':
    app.run(debug=True)
