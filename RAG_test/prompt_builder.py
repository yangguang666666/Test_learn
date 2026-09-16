def build_test_prompt(target_name,retrieved_docs,extra_contexts):
    retrieved_text="\n\n".join(retrieved_docs)

    extra_text = "\n\n".join(
        f"[{c['type']}] {c['path']}\n{c['content'][:3000]}"
        for c in extra_contexts
    )

    return f"""
你是一个python pytest测试生成助手。

目标：为函数{target_name}生成pytest测试。

要求：
1.只输出python测试代码
2.使用python
3.覆盖正常输入，边界输出
4.不要修改源代码
5.如果需要导入函数，请根据文件路径推断 import

检索到相关代码：
{retrieved_text}

额外上下文:
{extra_text}
"""


