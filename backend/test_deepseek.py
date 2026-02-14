import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY')
print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
print(f"API Key length: {len(api_key)}")

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )
    
    print("\n测试API调用...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "你好"}
        ],
        max_tokens=10
    )
    
    print(f"✅ API调用成功！")
    print(f"响应: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ API调用失败！")
    print(f"错误信息: {e}")
    
    error_str = str(e)
    if '401' in error_str or 'authentication' in error_str.lower() or 'unauthorized' in error_str.lower():
        print("\n🔑 问题：API密钥无效或认证失败")
        print("解决方案：")
        print("1. 检查API密钥是否正确复制，没有多余空格")
        print("2. 确认API密钥来自DeepSeek官方平台：https://platform.deepseek.com")
        print("3. 检查API密钥是否已过期或被撤销")
        print("4. 重新生成API密钥")
    elif '429' in error_str or 'quota' in error_str.lower():
        print("\n📊 问题：API配额已用完")
        print("解决方案：等待配额重置或升级API计划")
    else:
        print("\n❓ 其他错误，请检查网络连接和API配置")