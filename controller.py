
# nossas rotas do FastAPI

# O Controller é o intermediário: recebe a ação do usuário, decide o que fazer
# com o Model, e escolhe qual View devolver.
# ● Recebe a requisição (clique, formulário enviado, chamada HTTP)
# ● Consulta ou atualiza o Model
# ● Devolve a resposta (renderiza uma View ou retorna um JSON)

# """
# Explicação do professor:

# CONTROLLER
# ----------
# Recebe a ação do usuário (requisição HTTP), consulta/atualiza o Model
# e devolve a View (o JSON de resposta).

# É aqui que Model e View se encontram — mas o Controller não sabe
# COMO a regra funciona por dentro, só aciona o Model.
# """

# essa parte é meio complicada

from fastapi import APIRouter, HTTPException
from model import aluno_modal, Aluno
from view import AlunoCreate, AlunoResponse, AlunoUpdate

router = APIRouter(prefix="/alunos", tags=["Alunos"])

def _buscar_ou_404(aluno_id:int) -> Aluno:
    aluno = aluno_modal.buscar_por_id(aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.post("/", response_model=AlunoResponse, status_code=201)
def criar_aluno(dados: AlunoCreate):
    aluno = aluno_modal.criar(dados.nome, dados.idade)
    return aluno

@router.get("/", response_model=list[AlunoResponse])
def listar_alunos():
    return aluno_modal.listar_todos()

@router.get("/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id):
    return _buscar_ou_404(aluno_id)

@router.put("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id:int, dados:AlunoUpdate):
    aluno = _buscar_ou_404(aluno_id)
    try:
        aluno.editar_nome(dados.nome)
        aluno.editar_idade(dados.idade)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    return aluno

@router.delete("{aluno_id}", response_model=AlunoResponse)
def deletar_aluno(aluno_id:int):
    aluno = _buscar_ou_404(aluno_id)
    aluno_modal.remover(aluno_id)