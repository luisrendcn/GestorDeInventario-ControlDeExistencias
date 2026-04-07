import { Router, type IRouter } from "express";
import { db, productsTable, transactionsTable } from "@workspace/db";
import { eq } from "drizzle-orm";

const router: IRouter = Router();

// Mock data for development without database
const mockProducts = [
  { id: 1, nombre: "Laptop Dell", tipo: "electrónica", precio: 1200, stock: 5, stockMinimo: 3 },
  { id: 2, nombre: "Mouse Logitech", tipo: "accesorios", precio: 25, stock: 1, stockMinimo: 5 },
  { id: 3, nombre: "Teclado Mecánico", tipo: "accesorios", precio: 120, stock: 8, stockMinimo: 3 },
];

const mockTransactions = [
  { id: 1, tipo: "venta", productID: 1, productNombre: "Laptop Dell", cantidad: 2, precioUnitario: 1200 },
  { id: 2, tipo: "compra", productID: 2, productNombre: "Mouse Logitech", cantidad: 10, precioUnitario: 15 },
  { id: 3, tipo: "venta", productID: 3, productNombre: "Teclado Mecánico", cantidad: 1, precioUnitario: 120 },
];

router.get("/stats/summary", async (_req, res): Promise<void> => {
  try {
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
  } catch (error) {
    // Return mock data if database is not available
    const totalProductos = mockProducts.length;
    const valorInventario = mockProducts.reduce((acc, p) => acc + p.precio * p.stock, 0);
    const productosStockBajo = mockProducts.filter((p) => p.stock <= p.stockMinimo).length;

    const ventas = mockTransactions.filter((t) => t.tipo === "venta");
    const compras = mockTransactions.filter((t) => t.tipo === "compra");

    const ingresosVentas = ventas.reduce((acc, t) => acc + t.precioUnitario * t.cantidad, 0);
    const costoCompras = compras.reduce((acc, t) => acc + t.precioUnitario * t.cantidad, 0);

    res.json({
      totalProductos,
      valorInventario,
      productosStockBajo,
      totalTransacciones: mockTransactions.length,
      totalVentas: ventas.length,
      totalCompras: compras.length,
      ingresosVentas,
      costoCompras,
      balance: ingresosVentas - costoCompras,
    });
  }
});

router.get("/stats/low-stock", async (_req, res): Promise<void> => {
  try {
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
  } catch (error) {
    // Return mock low stock data if database is not available
    const lowStock = mockProducts
      .filter((p) => p.stock <= p.stockMinimo)
      .map((p) => ({
        id: p.id,
        nombre: p.nombre,
        tipo: p.tipo,
        precio: p.precio,
        stock: p.stock,
        stockMinimo: p.stockMinimo,
        stockBajo: true,
        infoAdicional: "Datos de demostración",
      }));
    res.json(lowStock);
  }
});

router.get("/stats/activity", async (req, res): Promise<void> => {
  try {
    const limit = parseInt(req.query.limit as string) || 10;
    const transactions = await db.select().from(transactionsTable).limit(limit);
    res.json(transactions.map((t) => ({
      ...t,
      precioUnitario: Number(t.precioUnitario),
      total: Number(t.precioUnitario) * t.cantidad,
    })));
  } catch (error) {
    // Return mock transactions if database is not available
    const limit = parseInt(req.query.limit as string) || 10;
    const transactions = mockTransactions.slice(0, limit).map((t) => ({
      id: t.id,
      tipo: t.tipo,
      productID: t.productID,
      productNombre: t.productNombre,
      cantidad: t.cantidad,
      precioUnitario: t.precioUnitario,
      total: t.precioUnitario * t.cantidad,
    }));
    res.json(transactions);
  }
});

export default router;
