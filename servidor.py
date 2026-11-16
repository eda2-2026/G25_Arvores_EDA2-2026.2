import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from arvore_bin import Arvore, No

PASTA_FRONT = Path(__file__).resolve().parent / "front"
arvore = Arvore()

EXEMPLO = [
    ("Pedro", 18),
    ("Neymar", 12),
    ("Haaland", 27),
    ("Endrick", 7),
    ("Vinicius", 15),
    ("Rodrygo", 22),
    ("Mbappé", 31),
    ("Messi", 25),
]


def estado():
    return {"arvore": arvore.para_dict()}


def inteiro(valor):
    if isinstance(valor, bool):
        raise ValueError
    if isinstance(valor, int):
        return valor
    if isinstance(valor, float) and valor.is_integer():
        return int(valor)
    if isinstance(valor, str) and valor.strip().lstrip("-").isdigit():
        return int(valor.strip())
    raise ValueError


class Handler(BaseHTTPRequestHandler):
    def _json(self, codigo, dados):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _ler_json(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        if tamanho == 0:
            return {}
        bruto = self.rfile.read(tamanho)
        return json.loads(bruto.decode("utf-8"))

    def do_GET(self):
        caminho = urlparse(self.path).path
        if caminho == "/api/arvore":
            self._json(200, estado())
            return
        if caminho == "/":
            caminho = "/index.html"
        self._arquivo(caminho)

    def do_POST(self):
        caminho = urlparse(self.path).path
        try:
            dados = self._ler_json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._json(400, {"ok": False, "mensagem": "JSON inválido."})
            return

        if caminho == "/api/inserir":
            self._inserir(dados)
        elif caminho == "/api/remover":
            self._remover(dados)
        elif caminho == "/api/rotacionar":
            self._rotacionar(dados)
        elif caminho == "/api/buscar":
            self._buscar(dados)
        elif caminho == "/api/limpar":
            self._limpar()
        elif caminho == "/api/exemplo":
            self._exemplo()
        else:
            self._json(404, {"ok": False, "mensagem": "Rota não encontrada."})

    def _inserir(self, dados):
        nome = str(dados.get("jogador", "")).strip()
        if nome == "":
            self._json(400, {"ok": False, "mensagem": "Informe o nome do jogador."})
            return
        if arvore.buscar_jogador(arvore.root, nome) != None:
            self._json(400, {"ok": False, "mensagem": "Esse jogador já está na árvore."})
            return
        try:
            gols = inteiro(dados.get("gols"))
        except (TypeError, ValueError):
            self._json(400, {"ok": False, "mensagem": "Gols precisa ser um número inteiro."})
            return
        if gols < 0:
            self._json(400, {"ok": False, "mensagem": "Gols não pode ser negativo."})
            return

        arvore.insert(No(nome, gols))
        self._json(200, {"ok": True, "mensagem": f"{nome} entrou com {gols} gols.", **estado()})

    def _remover(self, dados):
        nome = str(dados.get("jogador", "")).strip()
        if nome == "":
            self._json(400, {"ok": False, "mensagem": "Informe o jogador."})
            return
        if not arvore.remover_jogador(nome):
            self._json(404, {"ok": False, "mensagem": "Jogador não encontrado."})
            return
        self._json(200, {"ok": True, "mensagem": f"{nome} foi removido.", **estado()})

    def _rotacionar(self, dados):
        nome = str(dados.get("jogador", "")).strip()
        direcao = dados.get("direcao")
        no = arvore.buscar_jogador(arvore.root, nome)
        if no == None:
            self._json(404, {"ok": False, "mensagem": "Jogador não encontrado."})
            return

        if direcao == "esquerda":
            ok = arvore.left_rotate(no)
            texto = "Rotação à esquerda"
            falta = f"{nome} não tem filho direito, então não dá para rotacionar à esquerda."
        elif direcao == "direita":
            ok = arvore.right_rotate(no)
            texto = "Rotação à direita"
            falta = f"{nome} não tem filho esquerdo, então não dá para rotacionar à direita."
        else:
            self._json(400, {"ok": False, "mensagem": "Direção inválida."})
            return

        if not ok:
            self._json(400, {"ok": False, "mensagem": falta, **estado()})
            return
        self._json(200, {"ok": True, "mensagem": f"{texto} aplicada em {nome}.", **estado()})

    def _buscar(self, dados):
        try:
            gols = inteiro(dados.get("gols"))
        except (TypeError, ValueError):
            self._json(400, {"ok": False, "mensagem": "Informe um número inteiro de gols."})
            return

        no = arvore.busca(arvore.root, gols)
        if no == False or no == None:
            self._json(200, {
                "ok": True,
                "encontrado": False,
                "mensagem": "Nenhum jogador com esses gols.",
                **estado(),
            })
            return

        self._json(200, {
            "ok": True,
            "encontrado": True,
            "jogador": no.jogador,
            "gols": no.gols,
            "mensagem": f"Encontrado: {no.jogador} ({no.gols} gols).",
            **estado(),
        })

    def _limpar(self):
        global arvore
        arvore = Arvore()
        self._json(200, {"ok": True, "mensagem": "Árvore limpa.", **estado()})

    def _exemplo(self):
        global arvore
        arvore = Arvore()
        for nome, gols in EXEMPLO:
            arvore.insert(No(nome, gols))
        self._json(200, {"ok": True, "mensagem": "Exemplo carregado.", **estado()})

    def _arquivo(self, caminho):
        relativo = caminho.lstrip("/")
        base = PASTA_FRONT.resolve()
        arquivo = (base / relativo).resolve()
        if not arquivo.is_relative_to(base) or not arquivo.is_file():
            self._json(404, {"ok": False, "mensagem": "Arquivo não encontrado."})
            return

        tipos = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
        }
        conteudo = arquivo.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", tipos.get(arquivo.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)


def main():
    porta = 8000
    if len(sys.argv) > 1:
        porta = int(sys.argv[1])

    try:
        servidor = ThreadingHTTPServer(("127.0.0.1", porta), Handler)
    except OSError:
        print(f"Não consegui abrir a porta {porta}. Tente: python3 servidor.py 8001")
        return

    print(f"Árvore disponível em http://127.0.0.1:{porta}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        servidor.server_close()


if __name__ == "__main__":
    main()
