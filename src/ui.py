import tkinter as tk
from tkinter import filedialog, messagebox
from projecao import projetar_estrofes

# Janela principal
def criar_janela_principal():
    letras_salvas = {}  # Dicionário para armazenar as letras com seus nomes
    tema_claro = True

    def alternar_tema():
        nonlocal tema_claro
        tema_claro = not tema_claro
        cores = {
            True: {"bg": "#ffffff", "fg": "#000000"},
            False: {"bg": "#333333", "fg": "#ffffff"},
        }

        tema = cores[tema_claro]
        janela.config(bg=tema["bg"])
        frame_letras.config(bg=tema["bg"])
        frame_editor.config(bg=tema["bg"])
        barra_ferramentas.config(bg=tema["bg"])

        lista_letras.config(bg=tema["bg"], fg=tema["fg"])
        letras_texto.config(bg=tema["bg"], fg=tema["fg"])
        nome_entrada.config(bg=tema["bg"], fg=tema["fg"])

    def abrir_janela_criacao():
        janela_criacao = tk.Toplevel()
        janela_criacao.title("Criar Letra")
        janela_criacao.geometry("1000x800")  # Tamanho igual à janela principal
        janela_criacao.minsize(800, 600)
        janela_criacao.resizable(True, True)

        def importar_letras():
            arquivo = filedialog.askopenfilename(
                title="Selecione o arquivo de letras",
                filetypes=[("Arquivos de Texto", "*.txt")]
            )
            if arquivo:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    letras_texto.insert(tk.END, f.read())

        def salvar_letras():
            nome = nome_entrada.get()
            if not nome:
                messagebox.showwarning("Aviso", "Insira um nome para salvar a letra!")
                return

            letras_salvas[nome] = letras_texto.get(1.0, tk.END).strip()
            atualizar_lista_letras()
            messagebox.showinfo("Sucesso", f"Letra '{nome}' salva com sucesso!")

        def atualizar_lista_letras():
            lista_letras.delete(0, tk.END)
            for nome in letras_salvas:
                lista_letras.insert(tk.END, nome)

        frame_criacao = tk.Frame(janela_criacao)
        frame_criacao.pack(fill=tk.BOTH, expand=True)

        nome_entrada = tk.Entry(frame_criacao, font=("Arial", 14))
        nome_entrada.pack(fill=tk.X, padx=5, pady=5)
        nome_entrada.insert(0, "Nome da Letra")

        letras_texto = tk.Text(frame_criacao, wrap=tk.WORD, font=("Arial", 14))
        letras_texto.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        barra_ferramentas = tk.Frame(frame_criacao)
        barra_ferramentas.pack(side=tk.BOTTOM, fill=tk.X)

        btn_importar = tk.Button(barra_ferramentas, text="Importar Letra", command=importar_letras)
        btn_importar.pack(side=tk.LEFT, padx=5, pady=5)

        btn_salvar = tk.Button(barra_ferramentas, text="Salvar Letra", command=salvar_letras)
        btn_salvar.pack(side=tk.LEFT, padx=5, pady=5)

    def atualizar_lista_letras():
        lista_letras.delete(0, tk.END)
        for nome in letras_salvas:
            lista_letras.insert(tk.END, nome)

    def exibir_letra(event):
        try:
            selecionado = lista_letras.get(lista_letras.curselection())
            letras_texto.delete(1.0, tk.END)
            letras_texto.insert(tk.END, letras_salvas[selecionado])
        except tk.TclError:
            messagebox.showwarning("Aviso", "Nenhuma letra foi selecionada!")

    def projetar_selecionada():
        try:
            selecionado = lista_letras.get(lista_letras.curselection())
            projetar_estrofes(letras_salvas[selecionado])
        except tk.TclError:
            messagebox.showwarning("Aviso", "Nenhuma letra foi selecionada para projeção!")

    janela = tk.Tk()
    janela.title("Projeção de Letras")
    janela.geometry("1000x800")
    janela.minsize(800, 600)
    janela.resizable(True, True)

    # Divisão principal
    frame_principal = tk.PanedWindow(janela, orient=tk.HORIZONTAL)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Aba lateral para letras salvas
    frame_letras = tk.Frame(frame_principal, bg="#f0f0f0")
    frame_principal.add(frame_letras, width=200)

    lista_letras = tk.Listbox(frame_letras)
    lista_letras.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
    lista_letras.bind("<<ListboxSelect>>", exibir_letra)

    btn_projetar = tk.Button(frame_letras, text="Projetar", command=projetar_selecionada)
    btn_projetar.pack(side=tk.BOTTOM, padx=5, pady=5)

    # Área de edição de letras
    frame_editor = tk.Frame(frame_principal)
    frame_principal.add(frame_editor)

    nome_entrada = tk.Entry(frame_editor, font=("Arial", 14))
    nome_entrada.pack(fill=tk.X, padx=5, pady=5)
    nome_entrada.insert(0, "Nome da Letra")

    letras_texto = tk.Text(frame_editor, wrap=tk.WORD, font=("Arial", 14))
    letras_texto.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    barra_ferramentas = tk.Frame(frame_editor)
    barra_ferramentas.pack(side=tk.BOTTOM, fill=tk.X)

    btn_criar_letra = tk.Button(barra_ferramentas, text="Criar Letra", command=abrir_janela_criacao)
    btn_criar_letra.pack(side=tk.LEFT, padx=5, pady=5)

    btn_alternar_tema = tk.Button(barra_ferramentas, text="Alternar Tema", command=alternar_tema)
    btn_alternar_tema.pack(side=tk.LEFT, padx=5, pady=5)

    janela.mainloop()
