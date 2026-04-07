import { Router, type IRouter, type Request, type Response } from "express";
import { eq, ilike, and } from "drizzle-orm";
import { db, productsTable } from "@workspace/db";
import multer, { type Multer } from "multer";
import XLSX from "xlsx";
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

// Configure multer for file uploads
const upload = multer({ storage: multer.memoryStorage() });

// Import from Excel
router.post("/products/import", upload.single("file"), async (req: Request & { file?: Express.Multer.File }, res: Response): Promise<void> => {
  try {
    if (!req.file) {
      res.status(400).json({ error: "No se proporcionó archivo" });
      return;
    }

    let data: any[] = [];
    const fileName = req.file.originalname.toLowerCase();

    try {
      if (fileName.endsWith(".csv")) {
        // Parse CSV manually
        const content = req.file.buffer.toString("utf8");
        const lines = content.trim().split("\n");
        if (lines.length < 2) {
          throw new Error("CSV vacío o inválido");
        }

        const headers = lines[0].split(",").map((h: string) => h.trim());
        for (let i = 1; i < lines.length; i++) {
          const values = lines[i].split(",").map((v: string) => v.trim());
          const row: any = {};
          headers.forEach((header: string, idx: number) => {
            row[header] = values[idx] || "";
          });
          data.push(row);
        }
      } else {
        // Parse XLSX
        const workbook = XLSX.read(req.file.buffer, { type: "buffer" });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        data = XLSX.utils.sheet_to_json(worksheet);
      }
    } catch (parseErr) {
      res.status(400).json({
        error: "Error al parsear el archivo",
        details: parseErr instanceof Error ? parseErr.message : "desconocido",
      });
      return;
    }

    let exitosos = 0;
    let fallidos = 0;
    const advertencias_list: Array<{ fila: number; advertencia: string }> = [];
    const errores: Array<{ fila: number; error: string }> = [];
    const productosCreados: Array<any> = [];

    // Process each row
    for (let i = 0; i < data.length; i++) {
      const row = data[i] as any;
      const fila = i + 2;

      try {
        if (!row.nombre || !row.nombre.toString().trim()) {
          errores.push({ fila, error: "nombre está vacío" });
          fallidos++;
          continue;
        }

        const nombre = row.nombre.toString().trim();
        const precio = parseFloat(row.precio_venta || row.precio || row.precio_compra || 0);
        const stock = parseInt(row.stock || 0);
        const stockMinimo = parseInt(row.stock_minimo || row.stockMinimo || 5);

        if (isNaN(precio) || precio < 0) {
          errores.push({ fila, error: `precio inválido` });
          fallidos++;
          continue;
        }

        if (isNaN(stock) || stock < 0) {
          errores.push({ fila, error: `stock inválido` });
          fallidos++;
          continue;
        }

        let tipo: "simple" | "perecedero" | "digital" = "simple";
        const categoria = (row.categoria || "General").toString().trim().toLowerCase();

        const categoriasPerecedero = ["alimentos", "comida", "bebidas", "medicamentos", "cosméticos", "aseo", "higiene", "perecedero"];
        const categoriasDigital = ["software", "digital", "ebook", "suscripción", "app", "virtual"];

        if (categoriasPerecedero.some((cat) => categoria.includes(cat)) || row.fecha_vencimiento) {
          tipo = "perecedero";
        } else if (categoriasDigital.some((cat) => categoria.includes(cat)) || row.url_descarga) {
          tipo = "digital";
        }

        const id = `${nombre.substring(0, 4).toUpperCase().replace(/\s/g, "")}_${Math.random().toString(36).substring(2, 6).toUpperCase()}`;

        const productData: typeof productsTable.$inferInsert = {
          id,
          nombre,
          tipo,
          precio: String(precio),
          stock,
          stockMinimo,
          categoria: tipo === "simple" ? categoria || "General" : null,
          fechaVencimiento: tipo === "perecedero" && row.fecha_vencimiento ? row.fecha_vencimiento.toString() : null,
          urlDescarga: tipo === "digital" ? row.url_descarga?.toString() || "" : null,
        };

        const [createdProduct] = await db.insert(productsTable).values(productData).returning();
        exitosos++;
        productosCreados.push(computeProductFields(createdProduct));
      } catch (error) {
        fallidos++;
        errores.push({
          fila,
          error: error instanceof Error ? error.message : "Error desconocido",
        });
      }
    }

    res.json({
      exitosos,
      fallidos,
      advertencias: 0,
      errores,
      advertencias_list,
      productos_creados: productosCreados,
    });
  } catch (error) {
    res.status(500).json({
      error: "Error al procesar el archivo",
      details: error instanceof Error ? error.message : "desconocido",
    });
  }
});

// Delete all products
router.delete("/products", async (req, res): Promise<void> => {
  try {
    const result = await db.delete(productsTable).returning();
    
    res.json({
      message: "Todos los productos han sido eliminados",
      eliminados: result.length,
      productos: result.map(computeProductFields),
    });
  } catch (error) {
    res.status(500).json({
      error: "Error al eliminar productos",
      details: error instanceof Error ? error.message : "desconocido",
    });
  }
});

export default router;
