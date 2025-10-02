# Calculadora Flask

revisão 2.01-10-2025

Uma aplicação web de calculadora simples e responsiva construída com Flask, que permite realizar operações matemáticas com valores de até 2 casas decimais e mantém um histórico das últimas 10 operações.

[Link da aplicação](https://bksolutions.pythonanywhere.com)
## Características

- **Operações matemáticas**: Suporta adição, subtração, multiplicação, divisão e parênteses
- **Precisão decimal**: Trabalha com valores de até 2 casas decimais
- **Histórico**: Mantém as últimas 10 operações realizadas
- **Limpar memória**: Permite limpar todo o histórico de operações
- **Layout responsivo**: Funciona perfeitamente em desktop (widescreen) e mobile (portrait)
- **Interface intuitiva**: Design moderno e fácil de usar

## Requisitos

- Python 3.13, adeque se usar Python 3.11
- pip ou pip3

## Instalação

1. Descompacte o arquivo zip
2. Navegue até a pasta do projeto:
   ```bash
   cd app
   ```

   ```
   cd app
   ```

4. Instale as dependências:
   ```bash
   pip3 install -r requirements.txt
   ```

   ```
   pip install -r requirements.txt
   ```
## Layout Inicial
<img src="https://github.com/kasshinokun/Calculadora_Flask/blob/main/images/Calculadora_Flask_Landscape-1.png" width="800" height="500" alt="Aplicação em Landscape">
<img src="https://github.com/kasshinokun/Calculadora_Flask/blob/main/images/Calculadora_Flask_Portrait-1.png " width="500" height="800" alt="Aplicação em Landscape">
## Execução

Para iniciar a aplicação, execute:

```bash
python3 main.py
```

```
python main.py
```


A aplicação estará disponível em `http://localhost:5000`

## Uso

### Interface da Calculadora

- **Botões numéricos**: Clique nos botões de 0 a 9 para inserir números
- **Operadores**: Use +, -, ×, / para operações matemáticas
- **Ponto decimal**: Clique no botão "." para inserir decimais
- **Igual (=)**: Calcula o resultado da expressão
- **Limpar (Limpar Tudo)**: Limpa o display
- **Apagar (Limpar)**: Remove o último caractere

### Campo de Expressão

Você também pode digitar expressões matemáticas diretamente no campo de entrada e clicar em "Calcular Expressão" ou pressionar Enter.

Exemplos:
- `2+3*4` = 14
- `2+3x4` = 14
- `(10+5)/3` = 5
- `(10+5):3` = 5
- `15.50*2` = 31
- `15,50x2` = 31

### Histórico

- O histórico mostra as últimas 10 operações realizadas
- Clique em uma operação do histórico para carregar o resultado no display
- Use o botão "Limpar Histórico" para remover todas as operações

### Atalhos de Teclado

- **Números (0-9)**: Inserir números
- **Operadores (+, -, *, x, /, :)**: Inserir operadores
- **Enter ou =**: Calcular resultado
- **Escape ou C**: Limpar display(em adaptação)
- **Backspace**: Apagar último caractere(em adaptação)

## Estrutura do Projeto

```
app/
├── main.py                 # Arquivo principal da aplicação
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py        # Modelo de usuário e configuração do banco
│   │   └── calculator.py  # Modelo de operação
│   └── routes/
│       ├── __init__.py
│       ├── user.py        # Rotas de usuário
│       └── calculator.py  # Rotas da calculadora
├── static/
│   └── index.html         # Interface da aplicação
└── database/
    └── app.db             # Banco de dados SQLite (criado automaticamente)
```

## API Endpoints

### POST /api/calculate
Calcula uma expressão matemática e salva no histórico.

**Request Body:**
```json
{
  "expression": "2+3*4"
}
```

**Response:**
```json
{
  "expression": "2+3*4",
  "result": 14,
  "timestamp": "2025-10-02T12:00:00"
}
```

### GET /api/history
Retorna o histórico das últimas 10 operações.

**Response:**
```json
[
  {
    "id": 1,
    "expression": "2+3*4",
    "result": 14,
    "timestamp": "2025-10-02T12:00:00"
  }
]
```

### DELETE /api/clear
Limpa todo o histórico de operações.

**Response:**
```json
{
  "message": "Histórico limpo com sucesso"
}
```

## Tecnologias Utilizadas

- **Backend**: Flask 3.1.2
- **Banco de Dados**: SQLite com Flask-SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Responsivo com CSS Grid e Media Queries

## Licença

Este projeto é de código aberto e está disponível para uso livre.
