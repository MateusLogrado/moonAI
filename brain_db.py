import chromadb

class MemoriaMoon:
    def __init__(self, persistencia="./biblioteca_moon"):
        self.cliente = chromadb.PersistentClient(path=persistencia)

        self.colecao = self.cliente.get_or_create_collection(name="historico_interacoes")

    def guardar(self, texto, user_id, metadados=None):
        import time

        id_unico = f"msg_{int(time.time() * 1000)}"

        meta = {"user_id": str(user_id)}
        if metadados:
            meta.update(metadados)

        self.colecao.add(
            documents=[texto],
            metadatas=[meta],
            ids=[id_unico]
        )

    def recuperar(self, busca_texto, user_id, quantidade=3):
        resultados = self.colecao.query(
            query_texts=[busca_texto],
            where={"user_id": str(user_id)}, 
            n_results=quantidade
        )
        return resultados['documents'][0] if resultados['documents'] else []