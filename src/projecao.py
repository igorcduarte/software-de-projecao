import tkinter as tk

# Janela de projeção
def projetar_estrofes(letras):
    estrofes = letras.strip().split("\n\n")
    projecao = tk.Toplevel()
    projecao.title("Projeção de Estrofes")
    projecao.attributes('-fullscreen', True)

    indice = [0]  # Lista para permitir modificação dentro de funções

    def atualizar_estrofe():
        texto_projecao.config(text=estrofes[indice[0]])

    def proxima_estrofe(event=None):
        if indice[0] < len(estrofes) - 1:
            indice[0] += 1
            atualizar_estrofe()

    def estrofe_anterior(event=None):
        if indice[0] > 0:
            indice[0] -= 1
            atualizar_estrofe()

    texto_projecao = tk.Label(projecao, text="", font=("Arial", 30), wraplength=1200, justify="center")
    texto_projecao.pack(expand=True)

    projecao.bind("<Right>", proxima_estrofe)
    projecao.bind("<Left>", estrofe_anterior)
    projecao.bind("<Escape>", lambda e: projecao.destroy())

    atualizar_estrofe()