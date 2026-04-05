import { pgTable, text, integer, numeric, boolean, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

export const productsTable = pgTable("products", {
  id: text("id").primaryKey(),
  nombre: text("nombre").notNull(),
  tipo: text("tipo").notNull(), // 'simple' | 'perecedero' | 'digital'
  precio: numeric("precio", { precision: 12, scale: 2 }).notNull(),
  stock: integer("stock").notNull().default(0),
  stockMinimo: integer("stock_minimo").notNull().default(5),
  categoria: text("categoria"),
  fechaVencimiento: text("fecha_vencimiento"), // ISO date string
  urlDescarga: text("url_descarga"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export const insertProductSchema = createInsertSchema(productsTable).omit({ createdAt: true });
export type InsertProduct = z.infer<typeof insertProductSchema>;
export type Product = typeof productsTable.$inferSelect;
