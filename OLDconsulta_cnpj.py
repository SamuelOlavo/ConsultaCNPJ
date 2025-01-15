import requests
import json
import mysql.connector

def consulta_cnpj(cnpj):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{10548256000191}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para status HTTP de erro (4xx ou 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def insere_dados_mysql(dados):
    try:
        mydb = mysql.connector.connect(
            host="localhost", # ou o host do seu MySQL
            user="samuel", # seu usuário do MySQL
            password="leumas", # sua senha do MySQL
            database="ConsultaCNPJ" # nome do seu banco de dados
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO empresas (cnpj, nome_fantasia, razao_social, logradouro, numero, complemento, bairro, municipio, uf, cep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (dados['cnpj'], dados.get('nome_fantasia'), dados['razao_social'], dados['logradouro'], dados['numero'], dados.get('complemento'), dados['bairro'], dados['municipio'], dados['uf'], dados['cep']) #Usando .get para evitar erros de KeyError caso a chave não exista
        mycursor.execute(sql, val)
        mydb.commit()
        print(f"{mycursor.rowcount} registro inserido.")
        mydb.close()
    except mysql.connector.Error as err:
        print(f"Erro ao inserir no MySQL: {err}")


if __name__ == "__main__":
    cnpj_para_consultar = "00000000000191" # CNPJ de teste
    dados_cnpj = consulta_cnpj(cnpj_para_consultar)

    if dados_cnpj:
        print(json.dumps(dados_cnpj, indent=4, ensure_ascii=False)) # Imprime o JSON formatado (opcional)
        insere_dados_mysql(dados_cnpj)
    else:
        print("Não foi possível obter os dados do CNPJ.")
