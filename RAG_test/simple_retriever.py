import bm25s
from repo_indexer import index_repo


def tokenize(text: str):
    return (
        text.replace("(", " ")
        .replace(")", " ")
        .replace("_", " ")
        .replace(".", " ")
        .replace("/", " ")
        .lower()
        .split()
    )


class CodeRetriever:
    def __init__(self, repo_path: str):
        self.functions = index_repo(repo_path)
        tokenized_docs = [
            tokenize(f["code"] + " " + f["name"] + " " + " ".join(f["args"]))
            for f in self.functions
        ]
        self.retriever = bm25s.BM25()
        self.retriever.index(tokenized_docs)

    def search(self, query: str, top_k: int = 3):
        tokenized_query = tokenize(query)
        # bm25s 输入必须是二维列表 [ [token1,token2...] ]
        docs, scores = self.retriever.retrieve(
            [tokenized_query],
            corpus=self.functions,
            k=top_k
        )
        # 去掉batch外层维度
        return list(zip(docs[0], scores[0]))


if __name__ == "__main__":
    retriever = CodeRetriever(r"E:\Indoor\PythonProject_learntest\Test_ex")
    results = retriever.search("classify number zero negative positive", top_k=3)

    for i, (func_meta, score) in enumerate(results, 1):
        print("=" * 50)
        print(f"RESULT {i} | score: {score:.3f}")
        print(f"func name: {func_meta['name']}")
        print(f"file: {func_meta['file']} lines:{func_meta['start_line']}-{func_meta['end_line']}")
        print("-" * 20)
        print(func_meta["code"])