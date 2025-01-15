**Documentação do Código de Consulta de CNPJ com Interface Gráfica (usando `tkinter`)**

**Nome do arquivo:** `consulta_cnpj_gui.py` (ou o nome que você escolher)

**Descrição:** Este script Python fornece uma interface gráfica simples para consultar informações de CNPJ usando a API da BrasilAPI e armazenar os dados em um banco de dados MySQL local.

**Bibliotecas utilizadas:**

*   `tkinter`: Para a criação da interface gráfica.
*   `requests`: Para fazer as requisições HTTP para a API da BrasilAPI.
*   `json`: Para manipular dados em formato JSON.
*   `mysql.connector`: Para interagir com o banco de dados MySQL.

**Estrutura do código:**

1.  **Importações:**

    ```python
    import tkinter as tk
    from tkinter import messagebox
    import requests
    import json
    import mysql.connector
    ```

    Importa as bibliotecas necessárias.

2.  **Função `consulta_cnpj(cnpj)`:**

    ```python
    def consulta_cnpj(cnpj):
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        try:
            response = requests.get(url)
            response.raise_for_status() # Verifica se a requisição foi bem-sucedida (status 2xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para o CNPJ {cnpj}: {e}")
            return None
    ```

    *   Recebe o CNPJ como string.
    *   Constrói a URL da API.
    *   Faz a requisição GET usando `requests.get()`.
    *   `response.raise_for_status()`: Lança uma exceção se a resposta HTTP tiver um código de erro (4xx ou 5xx). Isso é importante para o tratamento de erros.
    *   Retorna os dados em formato JSON se a requisição for bem-sucedida ou `None` em caso de erro.
    *   Inclui tratamento de exceções para lidar com erros de requisição.

3.  **Função `insere_dados_mysql(dados)`:**

    ```python
    def insere_dados_mysql(dados):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="seu_usuario",
                password="sua_senha",
                database="nome_do_seu_banco"
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
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao inserir no MySQL para o CNPJ {dados.get('cnpj', 'Desconhecido')}: {err}")
            return False
    ```

    *   Recebe os dados do CNPJ em formato de dicionário Python.
    *   Estabelece a conexão com o banco de dados MySQL.
    *   Cria a query SQL com placeholders (`%s`) para evitar injeção de SQL.
    *   Converte os valores para string antes de inserir no banco de dados, tratando valores `None`.
    *   Executa a query e commita as mudanças.
    *   Retorna `True` em caso de sucesso e `False` em caso de erro.
    *   Inclui tratamento de exceções para lidar com erros de banco de dados.

4.  **Função `buscar_cnpj()`:**

    ```python
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
    ```

    *   Obtém o CNPJ digitado na interface.
    *   Valida se o campo não está vazio.
    *   Chama `consulta_cnpj()` para obter os dados da API.
    *   Se os dados forem obtidos, chama `insere_dados_mysql()` para inserir no banco.
    *   Exibe mensagens de sucesso ou erro usando `messagebox`.

5.  **Criação da interface gráfica:**

    ```python
    janela = tk.Tk()
    janela.title("Consulta CNPJ")

    label_cnpj = tk.Label(janela, text="CNPJ:")
    label_cnpj.grid(row=0, column=0, padx=5, pady=5)

    entry_cnpj = tk.Entry(janela)
    entry_cnpj.grid(row=0, column=1, padx=5, pady=5)

    botao_buscar = tk.Button(janela, text="Buscar", command=buscar_cnpj)
    botao_buscar.grid(row=1, column=0, columnspan=2, pady=10)

    janela.mainloop()
    ```

    *   Cria a janela principal (`tk.Tk()`).
    *   Cria os widgets: um rótulo (`tk.Label`), um campo de entrada (`tk.Entry`) e um botão (`tk.Button`).
    *   Usa o gerenciador de layout `grid` para posicionar os widgets.
    *   `janela.mainloop()`: Inicia o loop principal da interface gráfica, que fica aguardando eventos do usuário.

**Passos para Execução do Script:**

Após configurar o ambiente virtual e instalar as dependências, siga estes passos para executar o script:

1.  **Navegue até o diretório do projeto:** Abra o terminal ou prompt de comando e use o comando `cd` para navegar até o diretório onde você salvou o arquivo `consulta_cnpj_gui.py`. Por exemplo:

    ```bash
    cd /home/seu_usuario/projetos/ConsultaCNPJ  # Linux/macOS
    cd C:\Users\seu_usuario\projetos\ConsultaCNPJ   # Windows
    ```

2.  **Ative o ambiente virtual:** Este é um passo **essencial**. Você precisa ativar o ambiente virtual para que o Python correto e as bibliotecas instaladas estejam disponíveis.

    *   **Linux/macOS:**

        ```bash
        source .venv/bin/activate
        ```

        (Lembre-se de substituir `.venv` pelo nome do seu ambiente virtual se você usou um nome diferente).

    *   **Windows:**

        ```bash
        .venv\Scripts\activate
        ```

        (Novamente, substitua `.venv` se necessário).

    Após a ativação, você deverá ver o nome do ambiente virtual entre parênteses no prompt do seu terminal ou prompt de comando, como `(.venv)`.

3.  **Execute o script Python:** Agora, com o ambiente virtual ativado, execute o script usando o comando:

    ```bash
    python consulta_cnpj_gui.py
    ```

    (Ou `python3 consulta_cnpj_gui.py` se você tiver várias versões do Python instaladas e quiser usar explicitamente o Python 3).

4.  **Interaja com a interface:** Uma janela com o título "Consulta CNPJ" será aberta.

    *   Digite o CNPJ que você deseja consultar no campo de texto.
    *   Clique no botão "Buscar".

5.  **Observe os resultados:**

    *   As informações do CNPJ (em formato JSON) serão impressas no seu terminal ou prompt de comando.
    *   Uma mensagem de sucesso ou erro será exibida na janela usando caixas de diálogo (`messagebox`).
    *   Os dados do CNPJ serão inseridos no seu banco de dados MySQL (se a conexão e a inserção forem bem-sucedidas).

**Exemplo completo (Linux/macOS):**

```bash
cd /home/seu_usuario/projetos/ConsultaCNPJ
source .venv/bin/activate
python consulta_cnpj_gui.py
```

**Exemplo completo (Windows):**

```bash
cd C:\Users\seu_usuario\projetos\ConsultaCNPJ
.venv\Scripts\activate
python consulta_cnpj_gui.py
```

**Resumo completo da documentação (incluindo o funcionamento do ambiente virtual e os passos de execução):**

**(Repetindo as seções anteriores para melhor organização)**

**Documentação do Código de Consulta de CNPJ com Interface Gráfica (usando `tkinter`)**

**Nome do arquivo:** `consulta_cnpj_gui.py`

**Descrição:** Este script Python fornece uma interface gráfica simples para consultar informações de CNPJ usando a API da BrasilAPI e armazenar os dados em um banco de dados MySQL local.

**(Bibliotecas utilizadas, Estrutura do código: Funções `consulta_cnpj`, `insere_dados_mysql`, `buscar_cnpj`, Criação da interface gráfica - permanecem iguais à resposta anterior)**

**Funcionamento do Ambiente Virtual do Python (`venv`)**

(A explicação sobre o funcionamento do ambiente virtual permanece igual à resposta anterior)

**Passos para Execução do Script:**

(Conforme detalhado acima)

**Resolução de problemas comuns:**

*   **`ModuleNotFoundError: No module named 'tkinter'`:** Certifique-se de que o `tkinter` está instalado corretamente (veja as instruções detalhadas na resposta anterior).
*   **Erro de conexão com o MySQL:** Verifique as credenciais do banco de dados (host, usuário, senha, nome do banco) na função `insere_dados_mysql()`.
*   **Erros na requisição da API:** Verifique se o CNPJ digitado está correto e se você tem conexão com a internet. Verifique os logs no terminal para mensagens de erro mais detalhadas.
*   **Nenhuma janela aparece:** Certifique-se de que o ambiente virtual está ativado. Se estiver usando um ambiente de desenvolvimento remoto (como SSH), pode ser necessário configurar o X11 forwarding ou usar outra solução para exibir interfaces gráficas.

Com esta documentação completa, incluindo os passos de execução e a explicação do ambiente virtual, você deve conseguir executar o script sem problemas. Se ainda tiver dúvidas, por favor, forneça mais detalhes sobre o erro ou o comportamento inesperado que você está encontrando.

