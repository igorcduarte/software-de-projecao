import tkinter as tk
from tkinter import filedialog, messagebox
from projecao import projetar_estrofes

# Janela principal
def criar_janela_principal():
    letras_salvas = {}  # Dicionário para armazenar as letras com seus nomes
    tema_atual = {"bg": "#ffffff", "fg": "#000000"}  # Tema padrão (claro)
    
    # Funções para gerenciar letras
    def importar_letras():
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo de letras",
            filetypes=[("Arquivos de Texto", "*.txt")]
        )
        if arquivo:
            nome = arquivo.split("/")[-1].split(".txt")[0]
            with open(arquivo, 'r', encoding='utf-8') as f:
                letras_salvas[nome] = f.read()
                atualizar_lista_letras()

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

    def exibir_letra(event):
        try:
            selecionado = lista_letras.get(lista_letras.curselection())
            letras_texto.delete(1.0, tk.END)
            letras_texto.insert(tk.END, letras_salvas[selecionado])
        except tk.TclError:
            messagebox.showwarning("Aviso", "Nenhuma letra foi selecionada!")

    def excluir_letra():
        try:
            selecionado = lista_letras.get(lista_letras.curselection())
            if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir a letra '{selecionado}'?"):
                del letras_salvas[selecionado]
                atualizar_lista_letras()
                letras_texto.delete(1.0, tk.END)
                nome_entrada.delete(0, tk.END)
        except tk.TclError:
            messagebox.showwarning("Aviso", "Nenhuma letra foi selecionada para exclusão!")

    def projetar_selecionada():
        try:
            selecionado = lista_letras.get(lista_letras.curselection())
            projetar_estrofes(letras_salvas[selecionado])
        except tk.TclError:
            messagebox.showwarning("Aviso", "Nenhuma letra foi selecionada para projeção!")

    # Função para alternar entre claro e escuro
    def alternar_tema():
        if tema_atual["bg"] == "#ffffff":
            tema_atual.update({"bg": "#333333", "fg": "#ffffff"})
        else:
            tema_atual.update({"bg": "#ffffff", "fg": "#000000"})
        aplicar_tema()
    
    def aplicar_tema():
        janela.configure(bg=tema_atual["bg"])
        frame_letras.configure(bg=tema_atual["bg"])
        lista_letras.configure(bg=tema_atual["bg"], fg=tema_atual["fg"])
        frame_editor.configure(bg=tema_atual["bg"])
        letras_texto.configure(bg=tema_atual["bg"], fg=tema_atual["fg"], insertbackground=tema_atual["fg"])
        barra_ferramentas.configure(bg=tema_atual["bg"])
        nome_entrada.configure(bg=tema_atual["bg"], fg=tema_atual["fg"], insertbackground=tema_atual["fg"])
        btn_importar.configure(bg=tema_atual["bg"], fg=tema_atual["fg"])
        btn_salvar.configure(bg=tema_atual["bg"], fg=tema_atual["fg"])
        btn_projetar.configure(bg=tema_atual["bg"], fg=tema_atual["fg"])
        btn_excluir.configure(bg=tema_atual["bg"], fg=tema_atual["fg"])
        btn_tema.configure(bg=tema_atual["bg"], fg=tema_atual["fg"])
    
    # Configuração da janela principal
    janela = tk.Tk()
    janela.title("Projeção de Letras")
    janela.geometry("1000x800")
    janela.resizable(True, True)
    janela.minsize(800, 600)

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

    btn_excluir = tk.Button(frame_letras, text="Excluir Letra", command=excluir_letra)
    btn_excluir.pack(side=tk.BOTTOM, padx=5, pady=5)
    
    # Botão para alternar tema
    btn_tema = tk.Button(frame_letras, text="Alternar Tema", command=alternar_tema)
    btn_tema.pack(side=tk.BOTTOM, padx=5, pady=5)

    # Área de edição de letras
    frame_editor = tk.Frame(frame_principal)
    frame_principal.add(frame_editor)

    nome_entrada = tk.Entry(frame_editor, font=("Arial", 14))
    nome_entrada.pack(fill=tk.X, padx=5, pady=5)
    nome_entrada.insert(0, "Nome da Letra")

    letras_texto = tk.Text(frame_editor, wrap=tk.WORD, font=("Arial", 14))
    letras_texto.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    barra_ferramentas = tk.Frame(frame_editor, bg="#f0f0f0")
    barra_ferramentas.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

    btn_importar = tk.Button(barra_ferramentas, text="Importar Letras", command=importar_letras)
    btn_importar.pack(side=tk.LEFT, padx=5, pady=5)

    btn_salvar = tk.Button(barra_ferramentas, text="Salvar Letra", command=salvar_letras)
    btn_salvar.pack(side=tk.LEFT, padx=5, pady=5)

    # Aplica o tema inicial
    aplicar_tema()
    
    janela.mainloop()