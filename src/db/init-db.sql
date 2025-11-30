-- SQL para criar o banco mercado em SQLite

-- Tabela de cliente
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de compra
CREATE TABLE IF NOT EXISTS compra (
  id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
  id cliente INTEGER NOT NULL,
  data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
  total_compra DECIMAL(10,2) DEFAULT 0.00,
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

-- Tabela de item_compra
CREATE TABLE IF NOT EXISTS item_compra (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_compra INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compra(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto) ON DELETE RESTRICT
);

-- Tabela de produto
CREATE TABLE IF NOT EXISTS produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    quantidade INTEGER NOT NULL DEFAULT 0,
    preco DECIMAL(10, 2) NOT NULL,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de fornecedor
CREATE TABLE IF NOT EXISTS fornecedor (
    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);


-- Tabela produto_fornecedor
-- N:N
CREATE TABLE IF NOT EXISTS produto_fornecedor (
    id_produto_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER NOT NULL,
    id_fornecedor INTEGER NOT NULL,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto) ON DELETE CASCADE,
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id_fornecedor) ON DELETE CASCADE,
    UNIQUE(id_produto, id_fornecedor)
);
