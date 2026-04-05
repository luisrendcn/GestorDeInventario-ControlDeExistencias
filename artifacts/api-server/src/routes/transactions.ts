import { Router, type IRouter } from "express";
import { eq, and, desc } from "drizzle-orm";
import { db, transactionsTable, productsTable } from "@workspace/db";
import {
  ListTransactionsQueryParams,
  CreateTransactionBody,
  GetRecentActivityQueryParams,
} from "@workspace/api-zod";
import { randomUUID } from "crypto";

const router: IRouter = Router();

function serializeTransaction(row: typeof transactionsTable.$inferSelect) {
  return {
    ...row,
    precioUnitario: Number(row.precioUnitario),
    total: Number(row.precioUnitario) * row.cantidad,
  };
}

router.get("/transactions", async (req, res): Promise<void> => {
  const query = ListTransactionsQueryParams.safeParse(req.query);
  if (!query.success) {
    res.status(400).json({ error: query.error.message });
    return;
  }

  const { type, productId } = query.data;
  const conditions = [];
  if (type) conditions.push(eq(transactionsTable.tipo, type));
  if (productId) conditions.push(eq(transactionsTable.productId, productId));

  const rows = await db
    .select()
    .from(transactionsTable)
    .where(conditions.length > 0 ? and(...conditions) : undefined)
    .orderBy(desc(transactionsTable.createdAt));

  res.json(rows.map(serializeTransaction));
});

router.post("/transactions", async (req, res): Promise<void> => {
  const parsed = CreateTransactionBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: parsed.error.message });
    return;
  }

  const { tipo, productId, cantidad, precioUnitario } = parsed.data;

  // Get product
  const [product] = await db.select().from(productsTable).where(eq(productsTable.id, productId));
  if (!product) {
    res.status(400).json({ error: "Producto no encontrado" });
    return;
  }

  // Validate and update stock
  if (tipo === "venta") {
    if (product.stock < cantidad) {
      res.status(400).json({ error: `Stock insuficiente. Disponible: ${product.stock}, solicitado: ${cantidad}` });
      return;
    }
    await db.update(productsTable).set({ stock: product.stock - cantidad }).where(eq(productsTable.id, productId));
  } else {
    await db.update(productsTable).set({ stock: product.stock + cantidad }).where(eq(productsTable.id, productId));
  }

  const unitPrice = precioUnitario ?? Number(product.precio);
  const id = randomUUID().substring(0, 8).toUpperCase();

  const [row] = await db.insert(transactionsTable).values({
    id,
    tipo,
    productId,
    productNombre: product.nombre,
    cantidad,
    precioUnitario: String(unitPrice),
  }).returning();

  res.status(201).json(serializeTransaction(row));
});

router.get("/stats/activity", async (req, res): Promise<void> => {
  const query = GetRecentActivityQueryParams.safeParse(req.query);
  const limit = query.success ? (query.data.limit ?? 10) : 10;

  const rows = await db
    .select()
    .from(transactionsTable)
    .orderBy(desc(transactionsTable.createdAt))
    .limit(limit);

  res.json(rows.map(serializeTransaction));
});

export default router;
