const LARGURA = 116;
const ALTURA = 68;
const ESPACO_X = 12;
const ESPACO_Y = 48;

let arvore = null;
let selecionado = null;
let destaque = null;

async function api(caminho, corpo) {
  try {
    const opcoes = corpo
      ? {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(corpo),
        }
      : undefined;
    const resposta = await fetch(caminho, opcoes);
    return await resposta.json();
  } catch (erro) {
    return { ok: false, mensagem: "Não foi possível falar com o servidor." };
  }
}

function aviso(texto, erro) {
  const el = document.getElementById("aviso");
  el.textContent = texto || "";
  el.classList.toggle("erro", Boolean(erro));
}

function buscarNome(no, nome) {
  if (!no || !nome) return null;
  if (no.jogador === nome) return no;
  return buscarNome(no.left, nome) || buscarNome(no.right, nome);
}

function emOrdem(no, lista) {
  if (!no) return;
  emOrdem(no.left, lista);
  lista.push(no);
  emOrdem(no.right, lista);
}

function posicionar(no, profundidade, estado) {
  if (!no) return;
  posicionar(no.left, profundidade + 1, estado);
  no.x = estado.i;
  no.y = profundidade;
  estado.i += 1;
  posicionar(no.right, profundidade + 1, estado);
}

function encurtar(nome) {
  if (nome.length <= 14) return nome;
  return nome.slice(0, 13) + "…";
}

function textoGols(gols) {
  return gols === 1 ? "1 gol" : `${gols} gols`;
}

function atualizarSelecao(no) {
  const el = document.getElementById("selecionado");
  const esquerda = document.getElementById("rot-esq");
  const direita = document.getElementById("rot-dir");
  const remover = document.getElementById("remover");

  if (!no) {
    selecionado = null;
    el.textContent = "Clique em um jogador na árvore.";
    el.classList.add("vazio");
    esquerda.disabled = true;
    direita.disabled = true;
    remover.disabled = true;
    esquerda.title = "";
    direita.title = "";
    return;
  }

  const filhoEsq = no.left ? `${no.left.jogador} (${no.left.gols})` : "—";
  const filhoDir = no.right ? `${no.right.jogador} (${no.right.gols})` : "—";
  el.classList.remove("vazio");
  el.textContent = `${no.jogador} · ${textoGols(no.gols)}\nEsquerda: ${filhoEsq}\nDireita: ${filhoDir}`;
  esquerda.disabled = !no.right;
  direita.disabled = !no.left;
  remover.disabled = false;
  esquerda.title = no.right ? "Sobe o filho direito" : "Precisa de filho direito";
  direita.title = no.left ? "Sobe o filho esquerdo" : "Precisa de filho esquerdo";
}

function desenhar(raiz) {
  const recipiente = document.getElementById("arvore");
  const faixa = document.getElementById("em-ordem");
  recipiente.replaceChildren();

  if (!raiz) {
    const vazio = document.createElement("p");
    vazio.className = "vazia";
    vazio.textContent = "A árvore está vazia. Insira um jogador ou carregue o exemplo.";
    recipiente.appendChild(vazio);
    faixa.textContent = "";
    atualizarSelecao(null);
    return;
  }

  const lista = [];
  emOrdem(raiz, lista);
  faixa.textContent = "Em ordem: " + lista.map((no) => `${no.jogador} (${no.gols})`).join(" · ");

  posicionar(raiz, 0, { i: 0 });
  let maxX = 0;
  let maxY = 0;
  lista.forEach((no) => {
    maxX = Math.max(maxX, no.x);
    maxY = Math.max(maxY, no.y);
  });

  const passoX = LARGURA + ESPACO_X;
  const passoY = ALTURA + ESPACO_Y;
  const margem = 16;
  const largura = margem * 2 + maxX * passoX + LARGURA;
  const altura = margem * 2 + maxY * passoY + ALTURA;
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.setAttribute("width", largura);
  svg.setAttribute("height", altura);

  function coordenadas(no) {
    return {
      x: margem + no.x * passoX,
      y: margem + no.y * passoY,
    };
  }

  function arestas(no) {
    if (!no) return;
    const pai = coordenadas(no);
    [no.left, no.right].forEach((filho) => {
      if (!filho) return;
      const ponto = coordenadas(filho);
      const linha = document.createElementNS(ns, "line");
      linha.setAttribute("class", "aresta");
      linha.setAttribute("x1", pai.x + LARGURA / 2);
      linha.setAttribute("y1", pai.y + ALTURA);
      linha.setAttribute("x2", ponto.x + LARGURA / 2);
      linha.setAttribute("y2", ponto.y);
      svg.appendChild(linha);
      arestas(filho);
    });
  }

  function nos(no) {
    if (!no) return;
    const ponto = coordenadas(no);
    const grupo = document.createElementNS(ns, "g");
    grupo.setAttribute("class", "no");
    grupo.setAttribute("role", "button");
    grupo.setAttribute("aria-label", `${no.jogador}, ${textoGols(no.gols)}`);
    grupo.setAttribute("transform", `translate(${ponto.x}, ${ponto.y})`);
    if (no.jogador === selecionado) grupo.classList.add("selecionado");
    if (no.jogador === destaque) grupo.classList.add("destaque");
    grupo.addEventListener("click", () => {
      selecionado = no.jogador;
      destaque = null;
      desenhar(arvore);
    });

    const retangulo = document.createElementNS(ns, "rect");
    retangulo.setAttribute("width", LARGURA);
    retangulo.setAttribute("height", ALTURA);
    retangulo.setAttribute("rx", "14");
    grupo.appendChild(retangulo);

    const nome = document.createElementNS(ns, "text");
    nome.setAttribute("class", "nome");
    nome.setAttribute("x", LARGURA / 2);
    nome.setAttribute("y", 30);
    nome.textContent = encurtar(no.jogador);
    grupo.appendChild(nome);

    const gols = document.createElementNS(ns, "text");
    gols.setAttribute("class", "gols");
    gols.setAttribute("x", LARGURA / 2);
    gols.setAttribute("y", 52);
    gols.textContent = textoGols(no.gols);
    grupo.appendChild(gols);

    const titulo = document.createElementNS(ns, "title");
    titulo.textContent = `${no.jogador} — ${textoGols(no.gols)}`;
    grupo.appendChild(titulo);

    svg.appendChild(grupo);
    nos(no.left);
    nos(no.right);
  }

  arestas(raiz);
  nos(raiz);
  recipiente.appendChild(svg);
  atualizarSelecao(buscarNome(raiz, selecionado));
}

function aplicar(dados) {
  if (dados.mensagem) aviso(dados.mensagem, dados.ok === false);
  if (dados.arvore !== undefined) {
    arvore = dados.arvore;
    if (selecionado && !buscarNome(arvore, selecionado)) selecionado = null;
    desenhar(arvore);
  }
}

document.getElementById("form-inserir").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const dadosForm = new FormData(evento.target);
  destaque = null;
  const dados = await api("/api/inserir", {
    jogador: dadosForm.get("jogador"),
    gols: Number(dadosForm.get("gols")),
  });
  if (dados.ok) evento.target.reset();
  aplicar(dados);
});

document.getElementById("form-buscar").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const dadosForm = new FormData(evento.target);
  const dados = await api("/api/buscar", { gols: Number(dadosForm.get("gols")) });
  destaque = dados.encontrado ? dados.jogador : null;
  if (dados.encontrado) selecionado = dados.jogador;
  aplicar(dados);
});

async function rotacionar(direcao) {
  if (!selecionado) return;
  destaque = null;
  const dados = await api("/api/rotacionar", { jogador: selecionado, direcao });
  aplicar(dados);
}

document.getElementById("rot-esq").addEventListener("click", () => rotacionar("esquerda"));
document.getElementById("rot-dir").addEventListener("click", () => rotacionar("direita"));

document.getElementById("remover").addEventListener("click", async () => {
  if (!selecionado) return;
  destaque = null;
  const dados = await api("/api/remover", { jogador: selecionado });
  aplicar(dados);
});

document.getElementById("exemplo").addEventListener("click", async () => {
  selecionado = null;
  destaque = null;
  aplicar(await api("/api/exemplo", {}));
});

document.getElementById("limpar").addEventListener("click", async () => {
  selecionado = null;
  destaque = null;
  aplicar(await api("/api/limpar", {}));
});

api("/api/arvore").then(aplicar);
