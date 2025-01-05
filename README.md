# E-commerce API com Flask

## Descrição

Este é um sistema de e-commerce simples, desenvolvido com **Flask**. A aplicação permite o cadastro de produtos, gerenciamento de carrinho de compras e autenticação de usuários. Os usuários podem se registrar, fazer login e realizar operações de adicionar/remover itens do carrinho, além de realizar o checkout.

## Funcionalidades

- **Login e Logout**: Permite que usuários façam login e logout para acessar funcionalidades restritas.
- **Cadastro de Produtos**: Administradores podem adicionar, editar e excluir produtos.
- **Carrinho de Compras**: Usuários autenticados podem adicionar, remover itens e visualizar o carrinho de compras.
- **Checkout**: Permite que o usuário finalize a compra e esvazie o carrinho.

## Tecnologias Utilizadas

- **Python** com **Flask**: Framework web para Python.
- **SQLite**: Banco de dados para armazenar informações sobre produtos, usuários e carrinhos.
- **Flask-SQLAlchemy**: Extensão para facilitar o uso do SQLAlchemy com Flask.
- **Flask-Login**: Para gerenciamento de sessão de usuários.
- **Flask-CORS**: Para habilitar CORS e permitir requisições de diferentes origens.

## Endpoints da API

- **POST** `/login`: Realiza o login do usuário com nome de usuário e senha.
- **POST** `/logout`: Realiza o logout do usuário autenticado.
- **POST** `/api/products/add`: Adiciona um novo produto (somente para administradores).
- **DELETE** `/api/products/delete/<int:product_id>`: Deleta um produto pelo ID.
- **GET** `/api/products`: Retorna a lista de todos os produtos.
- **GET** `/api/products/<int:product_id>`: Detalha um produto específico.
- **PUT** `/api/products/update/<int:product_id>`: Atualiza um produto existente.
- **POST** `/api/cart/add/<int:product_id>`: Adiciona um produto ao carrinho do usuário.
- **DELETE** `/api/cart/remove/<int:product_id>`: Remove um produto do carrinho do usuário.
- **GET** `/api/cart`: Retorna o conteúdo do carrinho do usuário.
- **POST** `/api/cart/checkout`: Realiza o checkout e limpa o carrinho de compras.

## Como Rodar o Projeto

### Pré-requisitos

- **Python 3.x** instalado.
- **pip** para instalar dependências.

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ecommerce-flask.git

