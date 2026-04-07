import { pgTable, text, integer, numeric, timestamp } from "drizzle-orm/pg-core";

export const productsTable = pgTable("products", {
  id: text("id").primaryKey(),
  nombre: text("nombre").notNull(),
  tipo: text("tipo").notNull(),
  precio: numeric("precio", { precision: 12, scale: 2 }).notNull(),
  stock: integer("stock").notNull().default(0),
  stockMinimo: integer("stock_minimo").notNull().default(5),
  categoria: text("categoria"),
  fechaVencimiento: text("fecha_vencimiento"),
  urlDescarga: text("url_descarga"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export const transactionsTable = pgTable("transactions", {
  id: text("id").primaryKey(),
  tipo: text("tipo").notNull(),
  productId: text("product_id").notNull(),
  productNombre: text("product_nombre").notNull(),
  cantidad: integer("cantidad").notNull(),
  precioUnitario: numeric("precio_unitario", { precision: 12, scale: 2 }).notNull(),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});
