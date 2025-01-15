import tkinter as tk
from tkinter import messagebox
import requests
import json
import mysql.connector

def consulta_cnpj(cnpj):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para o CNPJ {cnpj}: {e}")
        return None

def insere_dados_mysql(dados):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="samuel",
            password="leumas",
            database="ConsultaCNPJ"
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO empresas (cnpj, nome_fantasia, razao_social, logradouro, numero, complemento, bairro, municipio, uf, cep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        val = (
            str(dados['cnpj']),
            str(dados.get('nome_fantasia') or ''),
            str(dados['razao_social']),
            str(dados['logradouro']),
            str(dados['numero']),
            str(dados.get('complemento') or ''),
            str(dados['bairro']),
            str(dados['municipio']),
            str(dados['uf']),
            str(dados['cep'])
        )

        mycursor.execute(sql, val)
        mydb.commit()
        print(f"{mycursor.rowcount} registro inserido para o CNPJ {dados['cnpj']}.")
        mydb.close()
        return True # Retorna True em caso de sucesso
    except mysql.connector.Error as err:
        print(f"Erro ao inserir no MySQL para o CNPJ {dados.get('cnpj', 'Desconhecido')}: {err}")
        return False # Retorna False em caso de falha

def buscar_cnpj():
    cnpj = entry_cnpj.get()
    if not cnpj:
        messagebox.showerror("Erro", "Por favor, digite um CNPJ.")
        return

    dados_cnpj = consulta_cnpj(cnpj)
    if dados_cnpj:
        print(json.dumps(dados_cnpj, indent=4, ensure_ascii=False))
        if insere_dados_mysql(dados_cnpj):
            messagebox.showinfo("Sucesso", f"Dados do CNPJ {cnpj} inseridos com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao inserir dados do CNPJ {cnpj} no banco de dados.")
    else:
        messagebox.showerror("Erro", f"Não foi possível obter os dados do CNPJ {cnpj}.")


# Cria a janela principal
janela = tk.Tk()
janela.title("Consulta CNPJ")

# Cria um rótulo (label)
label_cnpj = tk.Label(janela, text="CNPJ:")
label_cnpj.grid(row=0, column=0, padx=5, pady=5)

# Cria uma caixa de entrada (entry)
entry_cnpj = tk.Entry(janela)
entry_cnpj.grid(row=0, column=1, padx=5, pady=5)

# Cria um botão
botao_buscar = tk.Button(janela, text="Buscar", command=buscar_cnpj)
botao_buscar.grid(row=1, column=0, columnspan=2, pady=10) # columnspan para centralizar

# Inicia o loop principal da janela
janela.mainloop()
