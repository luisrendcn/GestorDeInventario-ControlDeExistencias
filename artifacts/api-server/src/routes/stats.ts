import { Router, type IRouter } from "express";
import { db, productsTable, transactionsTable } from "@workspace/db";
import { eq } from "drizzle-orm";

const router: IRouter = Router();

router.get("/stats/summary", async (_req, res): Promise<void> => {
  const [products, transactions] = await Promise.all([
    db.select().from(productsTable),
    db.select().from(transactionsTable),
  ]);

  const totalProductos = products.length;
  const valorInventario = products.reduce((acc, p) => acc + Number(p.precio) * p.stock, 0);
  const productosStockBajo = products.filter((p) => p.stock <= p.stockMinimo).length;

  const ventas = transactions.filter((t) => t.tipo === "venta");
  const compras = transactions.filter((t) => t.tipo === "compra");

  const ingresosVentas = ventas.reduce((acc, t) => acc + Number(t.precioUnitario) * t.cantidad, 0);
  const costoCompras = compras.reduce((acc, t) => acc + Number(t.precioUnitario) * t.cantidad, 0);

  res.json({
    totalProductos,
    valorInventario,
    productosStockBajo,
    totalTransacciones: transactions.length,
    totalVentas: ventas.length,
    totalCompras: compras.length,
    ingresosVentas,
    costoCompras,
    balance: ingresosVentas - costoCompras,
  });
});

router.get("/stats/low-stock", async (_req, res): Promise<void> => {
  const products = await db.select().from(productsTable);
  const lowStock = products
    .filter((p) => p.stock <= p.stockMinimo)
    .map((p) => ({
      ...p,
      precio: Number(p.precio),
      stockBajo: true,
      infoAdicional: "",
    }));
  res.json(lowStock);
});

export default router;
