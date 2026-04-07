import { Router, type IRouter, type Request, type Response } from "express";
import { eq, and, desc } from "drizzle-orm";
import { db, transactionsTable, productsTable } from "@workspace/db";
import {
  ListTransactionsQueryParams,
  CreateTransactionBody,
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

router.get("/transactions", async (req: Request, res: Response): Promise<void> => {
  try {
    const query = ListTransactionsQueryParams.safeParse(req.query);
    if (!query.success) {
      res.status(400).json({ error: query.error.message });
      return;
    }

    const { type, productId } = query.data;
    const conditions: any[] = [];
    if (type) conditions.push(eq(transactionsTable.tipo, type));
    if (productId) conditions.push(eq(transactionsTable.productId, productId));

    const whereClause = conditions.length > 0 ? and(...conditions) : undefined;

    const rows = await db
      .select()
      .from(transactionsTable)
      .where(whereClause)
      .orderBy(desc(transactionsTable.createdAt));

    res.json(rows.map(serializeTransaction));
  } catch (error) {
    res.status(500).json({
      error: "Error al obtener transacciones",
      details: error instanceof Error ? error.message : "desconocido",
    });
  }
});

router.post("/transactions", async (req: Request, res: Response): Promise<void> => {
  try {
    const parsed = CreateTransactionBody.safeParse(req.body);
    if (!parsed.success) {
      res.status(400).json({ error: parsed.error.message });
      return;
    }

    const { tipo, productId, cantidad, precioUnitario } = parsed.data;

    // Get product
    const results = await db
      .select()
      .from(productsTable)
      .where(eq(productsTable.id, productId));

    if (results.length === 0) {
      res.status(404).json({ error: "Producto no encontrado" });
      return;
    }

    const product = results[0];

    // Validate and update stock
    if (tipo === "venta") {
      if (product.stock < cantidad) {
        res.status(400).json({
          error: `Stock insuficiente. Disponible: ${product.stock}, solicitado: ${cantidad}`,
        });
        return;
      }
      await db
        .update(productsTable)
        .set({ stock: product.stock - cantidad })
        .where(eq(productsTable.id, productId));
    } else {
      await db
        .update(productsTable)
        .set({ stock: product.stock + cantidad })
        .where(eq(productsTable.id, productId));
    }

    const unitPrice = precioUnitario ?? Number(product.precio);
    const id = randomUUID().substring(0, 8).toUpperCase();

    const createdResults = await db
      .insert(transactionsTable)
      .values({
        id,
        tipo,
        productId,
        productNombre: product.nombre,
        cantidad,
        precioUnitario: String(unitPrice),
      })
      .returning();

    if (createdResults.length === 0) {
      res.status(500).json({ error: "Error al crear transacción" });
      return;
    }

    res.status(201).json(serializeTransaction(createdResults[0]));
  } catch (error) {
    res.status(500).json({
      error: "Error al procesar transacción",
      details: error instanceof Error ? error.message : "desconocido",
    });
  }
});

export default router;
