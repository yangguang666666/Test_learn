from langchain.agents import create_agent
from dotenv import load_dotenv
from prompt_builder import build_test_prompt
load_dotenv()

agent= create_agent(
    model="deepseek-v4-flash"
)

if __name__ == "__main__":
    from simple_retriever import CodeRetriever

    # 配置参数
    repo = r"E:\Indoor\PythonProject_learntest\Test_ex"
    target_name = "Sanjiao_S"
    ret = CodeRetriever(repo)
    res = ret.search(target_name, top_k=3)

    # 提取有效代码片段
    docs = []
    for meta, s in res:
        if s > 0:
            docs.append(f"文件:{meta['file']}\n{meta['code']}")

    # 无额外上下文
    extra = []
    prompt = build_test_prompt(target_name, docs, extra)
    messages=agent.stream(
        {
            "messages":[{"role":"user","content":f"{prompt}"}]
        },
        stream_mode="messages"
    )
    print("----------------调用大模型中--------------")
    print(type(messages))
    for token,metadata in messages:
        if token.content:
            print(token.content,end="",flush=True)
    print("\n")
    print("----------------调用完成-----------------")


