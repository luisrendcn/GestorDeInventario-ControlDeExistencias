import { Router, type IRouter } from "express";
import { eq, ilike, and } from "drizzle-orm";
import { db, productsTable } from "@workspace/db";
import {
  ListProductsQueryParams,
  CreateProductBody,
  GetProductParams,
  UpdateProductParams,
  UpdateProductBody,
  DeleteProductParams,
} from "@workspace/api-zod";
import { randomUUID } from "crypto";

const router: IRouter = Router();

function computeProductFields(row: typeof productsTable.$inferSelect) {
  const stockBajo = row.stock <= row.stockMinimo;
  const tipo = row.tipo;
  let infoAdicional = "";
  if (tipo === "simple") {
    infoAdicional = `Categoría: ${row.categoria ?? "General"}`;
  } else if (tipo === "perecedero") {
    if (row.fechaVencimiento) {
      const today = new Date();
      const exp = new Date(row.fechaVencimiento);
      const diff = Math.ceil((exp.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
      const expired = today > exp;
      infoAdicional = `Vencimiento: ${row.fechaVencimiento} (${expired ? "VENCIDO" : `vence en ${diff} días`})`;
    } else {
      infoAdicional = "Vencimiento: no especificado";
    }
  } else if (tipo === "digital") {
    infoAdicional = `Licencias disponibles: ${row.stock} | URL: ${row.urlDescarga ?? "no especificada"}`;
  }
  return {
    ...row,
    precio: Number(row.precio),
    stockBajo,
    infoAdicional,
  };
}

router.get("/products", async (req, res): Promise<void> => {
  const query = ListProductsQueryParams.safeParse(req.query);
  if (!query.success) {
    res.status(400).json({ error: query.error.message });
    return;
  }

  const { search, type, lowStock } = query.data;
  const conditions = [];

  if (search) {
    conditions.push(ilike(productsTable.nombre, `%${search}%`));
  }
  if (type) {
    conditions.push(eq(productsTable.tipo, type));
  }

  let rows = await db
    .select()
    .from(productsTable)
    .where(conditions.length > 0 ? and(...conditions) : undefined)
    .orderBy(productsTable.nombre);

  let products = rows.map(computeProductFields);

  if (lowStock === true || lowStock === "true" as unknown) {
    products = products.filter((p) => p.stockBajo);
  }

  res.json(products);
});

router.post("/products", async (req, res): Promise<void> => {
  const parsed = CreateProductBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: parsed.error.message });
    return;
  }

  const data = parsed.data;
  const id = (data.nombre.substring(0, 4).toUpperCase().replace(/\s/g, "") + randomUUID().substring(0, 4).toUpperCase());

  const [row] = await db.insert(productsTable).values({
    id,
    nombre: data.nombre,
    tipo: data.tipo,
    precio: String(data.precio),
    stock: data.stock,
    stockMinimo: data.stockMinimo,
    categoria: data.categoria ?? null,
    fechaVencimiento: data.fechaVencimiento ?? null,
    urlDescarga: data.urlDescarga ?? null,
  }).returning();

  res.status(201).json(computeProductFields(row));
});

router.get("/products/:id", async (req, res): Promise<void> => {
  const params = GetProductParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [row] = await db.select().from(productsTable).where(eq(productsTable.id, params.data.id));
  if (!row) {
    res.status(404).json({ error: "Producto no encontrado" });
    return;
  }

  res.json(computeProductFields(row));
});

router.put("/products/:id", async (req, res): Promise<void> => {
  const params = UpdateProductParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const body = UpdateProductBody.safeParse(req.body);
  if (!body.success) {
    res.status(400).json({ error: body.error.message });
    return;
  }

  const updates: Partial<typeof productsTable.$inferInsert> = {};
  const d = body.data;
  if (d.nombre !== undefined) updates.nombre = d.nombre;
  if (d.precio !== undefined) updates.precio = String(d.precio);
  if (d.stockMinimo !== undefined) updates.stockMinimo = d.stockMinimo;
  if (d.categoria !== undefined) updates.categoria = d.categoria;
  if (d.fechaVencimiento !== undefined) updates.fechaVencimiento = d.fechaVencimiento;
  if (d.urlDescarga !== undefined) updates.urlDescarga = d.urlDescarga;

  const [row] = await db
    .update(productsTable)
    .set(updates)
    .where(eq(productsTable.id, params.data.id))
    .returning();

  if (!row) {
    res.status(404).json({ error: "Producto no encontrado" });
    return;
  }

  res.json(computeProductFields(row));
});

router.delete("/products/:id", async (req, res): Promise<void> => {
  const params = DeleteProductParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [row] = await db
    .delete(productsTable)
    .where(eq(productsTable.id, params.data.id))
    .returning();

  if (!row) {
    res.status(404).json({ error: "Producto no encontrado" });
    return;
  }

  res.json(computeProductFields(row));
});

export default router;
