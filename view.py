from pydantic import BaseModel, Field
# o próprio JSON de resposta (não é uma página HTML)

# A View é a camada responsável por apresentar informação pro usuário.
# ● Não decide regra de negócio, só exibe o que recebe
# ● Pode ser uma página HTML, uma tela de app, um PDF, ou até um retorno
# em JSON
# ● A mesma informação (Model) pode ser exibida de formas bem diferentes

# nome:str, idade:str,
class AlunoCreate(BaseModel):
    nome: str = Field(..., min_length=1, examples=["Caio Santana"])
    idade: str = Field(..., min_length=1, examples=["23"])

class AlunoUpdate(BaseModel):
    nome: str = Field(..., min_length=1, examples=["Caio Santana"])
    idade: str = Field(..., min_length=1, examples=["23"])

class AlunoResponse(BaseModel):
    id:int
    nome:str
    idade:str
    matriculado:bool

class Config:
    from_attributes = True  # permite montar a partir do objeto Model (Tarefa)