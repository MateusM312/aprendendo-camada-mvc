# CAMADA MVC - Separa o código em camadas, cada um com uma responsabilidade diferente
# ● Uma camada cuida só de receber/responder requisições
# ● Outra cuida só da regra de negócio
# ● Outra cuida só do acesso aos dados
# ● Isso deixa o código mais organizado, testável e fácil de manter

from fastapi import FastAPI
from controller import router as aluno_router

app = FastAPI(title="API de alunos em uma escola - Exemplo para prova")

app.include_router(aluno_router)

@app.get("/")
def raiz():
    return {"mensagem": "API rodando! Veja /docs para testar as rotas."}