-- Catalog table stores product definitions
CREATE TABLE catalog (
    id UUID PRIMARY KEY,
    sku VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Inventory table tracks stock by location
CREATE TABLE inventory (
    id UUID PRIMARY KEY,
    catalog_id UUID NOT NULL REFERENCES catalog(id),
    location VARCHAR(128) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (catalog_id, location)
);

-- Customers table
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(32),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Employees table
CREATE TABLE employees (
    id UUID PRIMARY KEY,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NOT NULL,
    role VARCHAR(64) NOT NULL,
    email VARCHAR(255) UNIQUE,
    hired_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions table (orders)
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),
    employee_id UUID REFERENCES employees(id),
    status VARCHAR(32) NOT NULL,
    total NUMERIC(12,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transaction line items
CREATE TABLE transaction_items (
    id UUID PRIMARY KEY,
    transaction_id UUID NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    catalog_id UUID NOT NULL REFERENCES catalog(id),
    quantity INTEGER NOT NULL,
    price NUMERIC(12,2) NOT NULL
);
