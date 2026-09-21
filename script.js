const API_BASE = "http://127.0.0.1:8000";

async function carregarLista(){
  const container = document.getElementById("lista-alunos");
  try{
    const resp = await fetch(`${API_BASE}/alunos/`);
    if(!resp.ok) throw new Error("Falha ao carregar");
    const alunos = await resp.json();
    renderizarTabela(container, alunos);
  }catch(e){
    container.innerHTML = `<p class="vazio">Não foi possível conectar à API em ${API_BASE}. Verifique se o servidor FastAPI está rodando.</p>`;
  }
}

function renderizarTabela(container, alunos){
  if(!alunos.length){
    container.innerHTML = `<p class="vazio">Nenhum aluno cadastrado ainda.</p>`;
    return;
  }
  const linhas = alunos.map(a => `
    <tr data-id="${a.id}">
      <td>${a.id}</td>
      <td>${escapeHtml(a.nome)}</td>
      <td>${escapeHtml(String(a.idade))}</td>
      <td><span class="status ${a.matriculado ? 'sim' : 'nao'}">${a.matriculado ? 'Matriculado' : 'Não matriculado'}</span></td>
      <td><button class="excluir" onclick="excluirAluno(${a.id})">Excluir</button></td>
    </tr>`).join("");

  container.innerHTML = `
    <table>
      <thead><tr><th>ID</th><th>Nome</th><th>Idade</th><th>Situação</th><th></th></tr></thead>
      <tbody>${linhas}</tbody>
    </table>`;
}

function escapeHtml(str){
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

document.getElementById("form-criar").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const nome = document.getElementById("c-nome").value.trim();
  const idade = document.getElementById("c-idade").value;
  const aviso = document.getElementById("aviso-criar");
  aviso.textContent = "";
  aviso.className = "aviso";

  try{
    const resp = await fetch(`${API_BASE}/alunos/`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ nome, idade: String(idade) })
    });
    if(!resp.ok){
      const erro = await resp.json().catch(() => ({}));
      throw new Error(erro.detail || "Não foi possível matricular o aluno.");
    }
    aviso.textContent = "Aluno matriculado com sucesso.";
    aviso.classList.add("ok");
    document.getElementById("form-criar").reset();
    carregarLista();
  }catch(e){
    aviso.textContent = e.message;
    aviso.classList.add("erro");
  }
});

document.getElementById("btn-buscar").addEventListener("click", async () => {
  const id = document.getElementById("busca-id").value;
  const resultado = document.getElementById("resultado-busca");
  if(!id){
    resultado.innerHTML = `<p class="aviso erro">Informe um ID para buscar.</p>`;
    return;
  }
  try{
    const resp = await fetch(`${API_BASE}/alunos/${id}`);
    if(resp.status === 404){
      resultado.innerHTML = `<p class="aviso erro">Nenhum aluno encontrado com o ID ${id}.</p>`;
      return;
    }
    if(!resp.ok) throw new Error();
    const a = await resp.json();
    resultado.innerHTML = `
      <div class="cartao">
        <strong>${escapeHtml(a.nome)}</strong> — ID ${a.id}, ${escapeHtml(String(a.idade))} anos,
        <span class="status ${a.matriculado ? 'sim' : 'nao'}">${a.matriculado ? 'Matriculado' : 'Não matriculado'}</span>
      </div>`;
  }catch(e){
    resultado.innerHTML = `<p class="aviso erro">Erro ao buscar o aluno.</p>`;
  }
});

async function excluirAluno(id){
  if(!confirm(`Excluir o aluno de ID ${id}?`)) return;
  try{
    const resp = await fetch(`${API_BASE}/alunos/${id}`, { method: "DELETE" });
    if(!resp.ok) throw new Error();
    carregarLista();
  }catch(e){
    alert("Não foi possível excluir o aluno.");
  }
}

carregarLista();
