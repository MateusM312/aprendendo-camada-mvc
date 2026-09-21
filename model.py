from typing import Optional

# O Model representa os dados da aplicação e as regras que existem sobre eles.
# ● Guarda a estrutura dos dados (ex: um Produto tem nome, preço, estoque)
# ● Pode conter regras próprias dos dados (ex: "estoque não pode ser negativo")
# ● Não sabe nada sobre como os dados são exibidos, nem sobre a requisição HTTP

# nossos Schemas/Pydantic e os dados em si

class Aluno():
    def __init__(self, id:int, nome:str, idade:str, matriculado:bool = True):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.matriculado = matriculado

    def matricular(self):
        # Regra de negócio, não se pode matricular alguem já matriculado
        if self.matriculado:
            raise ValueError("Esse aluno já está matriculado!")
        self.matriculado = True
    
    def editar_nome(self, novo_nome: str):
        if not novo_nome.strip():
            raise ValueError("O nome não pode estar vazio.")
        self.nome = novo_nome

    def editar_idade(self, nova_idade: int):
        if nova_idade < 0:
            raise ValueError("A idade não pode ser negativa.")
        self.idade = nova_idade

    def editar_matriculado(self, novo_matriculado: bool):
        self.matriculado = novo_matriculado

class AlunoModel:
    # Guarda e organiza as tarefas (nossa 'base de dados' em memória).
    def __init__(self):
        self._alunos: dict[int, Aluno] = {}
        self._proximo_id = 1

    def criar(self, nome:str, idade:str) -> Aluno:
        aluno = Aluno(self._proximo_id, nome, idade)
        self._alunos[aluno.id] = aluno
        self._proximo_id += 1
        return aluno

    def buscar_por_id(self, aluno_id:int) -> Optional[Aluno]:
        return self._alunos.get[aluno_id]

    def listar_todos(self) -> list[Aluno]:
        return list(self._alunos.values())

    def remover(self, aluno_id:int) -> bool:
        if aluno_id in self._alunos:
            del self._alunos[aluno_id]
            return True
        return False

aluno_modal = AlunoModel()