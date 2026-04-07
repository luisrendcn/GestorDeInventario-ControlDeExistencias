import { db } from "./index";
import { productsTable, transactionsTable } from "./schema.consolidated";
import crypto from "crypto";

const generateId = () => crypto.randomUUID();

async function seedDatabase() {
  console.log("🌱 Iniciando seed de base de datos...");

  try {
    // Clear existing data
    await db.delete(transactionsTable);
    await db.delete(productsTable);
    console.log("✓ Tablas limpiadas");

    // Insert test products
    const products = [
      {
        id: generateId(),
        nombre: "Laptop Dell XPS 13",
        tipo: "Electrónica",
        precio: "1299.99",
        stock: 5,
        stockMinimo: 2,
        categoria: "Computadoras",
      },
      {
        id: generateId(),
        nombre: "Mouse Logitech MX Master",
        tipo: "Accesorios",
        precio: "99.99",
        stock: 1,
        stockMinimo: 5,
        categoria: "Periféricos",
      },
      {
        id: generateId(),
        nombre: "Teclado Mecánico Corsair K95",
        tipo: "Accesorios",
        precio: "199.99",
        stock: 8,
        stockMinimo: 3,
        categoria: "Periféricos",
      },
      {
        id: generateId(),
        nombre: "Monitor LG 27\" 4K",
        tipo: "Electrónica",
        precio: "499.99",
        stock: 3,
        stockMinimo: 1,
        categoria: "Monitores",
      },
      {
        id: generateId(),
        nombre: "Memoria RAM 32GB DDR5",
        tipo: "Componentes",
        precio: "159.99",
        stock: 12,
        stockMinimo: 5,
        categoria: "Hardware",
      },
    ];

    const insertedProducts = await db
      .insert(productsTable)
      .values(products)
      .returning();

    console.log(`✓ ${insertedProducts.length} productos insertados`);

    // Insert test transactions
    const transactions = [
      {
        id: generateId(),
        tipo: "venta",
        productId: insertedProducts[0].id,
        productNombre: insertedProducts[0].nombre,
        cantidad: 2,
        precioUnitario: "1299.99",
      },
      {
        id: generateId(),
        tipo: "compra",
        productId: insertedProducts[1].id,
        productNombre: insertedProducts[1].nombre,
        cantidad: 10,
        precioUnitario: "45.00",
      },
      {
        id: generateId(),
        tipo: "venta",
        productId: insertedProducts[2].id,
        productNombre: insertedProducts[2].nombre,
        cantidad: 1,
        precioUnitario: "199.99",
      },
      {
        id: generateId(),
        tipo: "venta",
        productId: insertedProducts[3].id,
        productNombre: insertedProducts[3].nombre,
        cantidad: 3,
        precioUnitario: "499.99",
      },
      {
        id: generateId(),
        tipo: "compra",
        productId: insertedProducts[4].id,
        productNombre: insertedProducts[4].nombre,
        cantidad: 20,
        precioUnitario: "120.00",
      },
    ];

    const insertedTransactions = await db
      .insert(transactionsTable)
      .values(transactions)
      .returning();

    console.log(`✓ ${insertedTransactions.length} transacciones insertadas`);
    console.log("✅ Seed completado exitosamente!");
    process.exit(0);
  } catch (error) {
    console.error("❌ Error durante seed:", error);
    process.exit(1);
  }
}

seedDatabase();
