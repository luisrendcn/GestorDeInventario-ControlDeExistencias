import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import {
  useListTransactions, useCreateTransaction, useListProducts,
  getListTransactionsQueryKey, getListProductsQueryKey,
  getGetSummaryQueryKey, getGetLowStockProductsQueryKey, getGetRecentActivityQueryKey
} from "@workspace/api-client-react";
import { useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from "@/components/ui/select";
import { Plus, ArrowLeftRight } from "lucide-react";

export default function Transactions() {
  const [filterType, setFilterType] = useState<string>("all");
  const [showDialog, setShowDialog] = useState(false);
  const [tipo, setTipo] = useState<"venta" | "compra">("venta");
  const [productId, setProductId] = useState("");
  const [cantidad, setCantidad] = useState("");
  const [precioUnitario, setPrecioUnitario] = useState("");
  const { toast } = useToast();
  const qc = useQueryClient();

  const params = filterType !== "all" ? { type: filterType as "venta" | "compra" } : {};
  const { data: transactions } = useListTransactions(params, { query: { queryKey: getListTransactionsQueryKey(params) } });
  const { data: products } = useListProducts({}, { query: { queryKey: getListProductsQueryKey() } });
  const createTransaction = useCreateTransaction();

  const invalidateAll = () => {
    qc.invalidateQueries({ queryKey: getListTransactionsQueryKey() });
    qc.invalidateQueries({ queryKey: getListProductsQueryKey() });
    qc.invalidateQueries({ queryKey: getGetSummaryQueryKey() });
    qc.invalidateQueries({ queryKey: getGetLowStockProductsQueryKey() });
    qc.invalidateQueries({ queryKey: getGetRecentActivityQueryKey() });
  };

  const handleSubmit = () => {
    if (!productId || !cantidad) {
      toast({ title: "Campos incompletos", description: "Selecciona un producto y cantidad.", variant: "destructive" });
      return;
    }
    createTransaction.mutate({
      data: {
        tipo,
        productId,
        cantidad: parseInt(cantidad),
        precioUnitario: precioUnitario ? parseFloat(precioUnitario) : undefined,
      }
    }, {
      onSuccess: () => {
        toast({ title: tipo === "venta" ? "Venta registrada" : "Compra registrada" });
        setShowDialog(false);
        setProductId(""); setCantidad(""); setPrecioUnitario("");
        invalidateAll();
      },
      onError: (e: Error) => toast({ title: "Error", description: e.message, variant: "destructive" }),
    });
  };

  const totalVentas = transactions?.filter(t => t.tipo === "venta").reduce((acc, t) => acc + Number(t.total), 0) ?? 0;
  const totalCompras = transactions?.filter(t => t.tipo === "compra").reduce((acc, t) => acc + Number(t.total), 0) ?? 0;

  return (
    <AppLayout
      title="Transacciones"
      subtitle="Historial de ventas y compras"
      actions={
        <Button onClick={() => setShowDialog(true)} size="sm" className="gap-1.5">
          <Plus size={14} /> Nueva transacción
        </Button>
      }
    >
      {/* Summary row */}
      {transactions && (
        <div className="grid grid-cols-3 gap-4 mb-5">
          <div className="bg-card border border-card-border rounded-xl px-5 py-3 flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Total movimientos</span>
            <span className="font-bold text-foreground">{transactions.length}</span>
          </div>
          <div className="bg-green-600/10 border border-green-600/20 rounded-xl px-5 py-3 flex items-center justify-between">
            <span className="text-sm text-green-700">Ingresos (ventas)</span>
            <span className="font-bold text-green-700">${totalVentas.toFixed(2)}</span>
          </div>
          <div className="bg-blue-600/10 border border-blue-600/20 rounded-xl px-5 py-3 flex items-center justify-between">
            <span className="text-sm text-blue-700">Costos (compras)</span>
            <span className="font-bold text-blue-700">${totalCompras.toFixed(2)}</span>
          </div>
        </div>
      )}

      {/* Filter */}
      <div className="flex gap-3 mb-4">
        <Select value={filterType} onValueChange={setFilterType}>
          <SelectTrigger className="w-44">
            <SelectValue placeholder="Tipo" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos</SelectItem>
            <SelectItem value="venta">Solo ventas</SelectItem>
            <SelectItem value="compra">Solo compras</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Table */}
      <div className="bg-card border border-card-border rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border bg-muted/40">
              <th className="text-left px-5 py-3 font-medium text-muted-foreground">ID</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Tipo</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Producto</th>
              <th className="text-right px-4 py-3 font-medium text-muted-foreground">Cantidad</th>
              <th className="text-right px-4 py-3 font-medium text-muted-foreground">Precio unit.</th>
              <th className="text-right px-4 py-3 font-medium text-muted-foreground">Total</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Fecha</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {!transactions ? (
              Array.from({ length: 6 }).map((_, i) => (
                <tr key={i}><td colSpan={7} className="px-5 py-3"><Skeleton className="h-5 w-full" /></td></tr>
              ))
            ) : transactions.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-5 py-12 text-center text-muted-foreground">
                  <ArrowLeftRight size={32} className="mx-auto mb-2 opacity-30" />
                  No hay transacciones registradas
                </td>
              </tr>
            ) : (
              transactions.map((t) => (
                <tr key={t.id} className="hover:bg-muted/30 transition-colors">
                  <td className="px-5 py-3 font-mono text-xs text-muted-foreground">{t.id}</td>
                  <td className="px-4 py-3">
                    <Badge variant="outline" className={`text-[10px] uppercase ${t.tipo === "venta" ? "bg-green-600/10 text-green-700 border-green-600/30" : "bg-blue-600/10 text-blue-700 border-blue-600/30"}`}>
                      {t.tipo}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 font-medium max-w-[160px] truncate">{t.productNombre}</td>
                  <td className="px-4 py-3 text-right">{t.cantidad} uds</td>
                  <td className="px-4 py-3 text-right text-muted-foreground">${Number(t.precioUnitario).toFixed(2)}</td>
                  <td className="px-4 py-3 text-right font-semibold">${Number(t.total).toFixed(2)}</td>
                  <td className="px-4 py-3 text-xs text-muted-foreground">
                    {new Date(t.createdAt).toLocaleString("es", { dateStyle: "short", timeStyle: "short" })}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* New transaction dialog */}
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Nueva transacción</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div>
              <Label>Tipo</Label>
              <Select value={tipo} onValueChange={(v) => setTipo(v as "venta" | "compra")}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="venta">Venta (reduce stock)</SelectItem>
                  <SelectItem value="compra">Compra (aumenta stock)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Producto</Label>
              <Select value={productId} onValueChange={setProductId}>
                <SelectTrigger>
                  <SelectValue placeholder="Seleccionar producto..." />
                </SelectTrigger>
                <SelectContent>
                  {(products ?? []).map((p) => (
                    <SelectItem key={p.id} value={p.id}>
                      {p.nombre} — Stock: {p.stock}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="cantidad">Cantidad</Label>
              <Input id="cantidad" type="number" min="1" value={cantidad} onChange={(e) => setCantidad(e.target.value)} />
            </div>
            <div>
              <Label htmlFor="precioUnitario">Precio unitario (opcional)</Label>
              <Input id="precioUnitario" type="number" min="0" step="0.01" value={precioUnitario} onChange={(e) => setPrecioUnitario(e.target.value)} placeholder="Usa el precio del producto por defecto" />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDialog(false)}>Cancelar</Button>
            <Button onClick={handleSubmit} disabled={createTransaction.isPending}>
              Registrar {tipo}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </AppLayout>
  );
}
