import { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Package, TrendingUp, AlertTriangle, ArrowLeftRight, ShoppingCart, DollarSign } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

function StatCard({ label, value, sub, icon: Icon, color }: {
  label: string; value: string | number; sub?: string; icon: React.ElementType; color: string;
}) {
  return (
    <div className="bg-card border border-card-border rounded-xl p-5 flex gap-4 items-start">
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${color}`}>
        <Icon size={18} className="text-white" />
      </div>
      <div>
        <p className="text-2xl font-bold text-foreground">{value}</p>
        <p className="text-sm font-medium text-foreground/80 mt-0.5">{label}</p>
        {sub && <p className="text-xs text-muted-foreground mt-0.5">{sub}</p>}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);
  const [lowStock, setLowStock] = useState<any>(null);
  const [activity, setActivity] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const summaryRes = await fetch("http://localhost:3000/api/stats/summary");
        if (!summaryRes.ok) {
          throw new Error(`Stats summary failed: ${summaryRes.status}`);
        }
        const summaryData = await summaryRes.json();
        setSummary(summaryData);

        const lowStockRes = await fetch("http://localhost:3000/api/stats/low-stock");
        if (!lowStockRes.ok) {
          throw new Error(`Low stock failed: ${lowStockRes.status}`);
        }
        const lowStockData = await lowStockRes.json();
        setLowStock(lowStockData);

        const activityRes = await fetch("http://localhost:3000/api/stats/activity?limit=8");
        if (!activityRes.ok) {
          throw new Error(`Activity failed: ${activityRes.status}`);
        }
        const activityData = await activityRes.json();
        setActivity(activityData);
      } catch (err) {
        console.error("Error fetching dashboard data:", err);
        setError(String(err));
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <AppLayout title="Dashboard" subtitle="Resumen del sistema de inventario">
      {error && (
        <div className="p-4 mb-4 bg-red-50 border border-red-200 rounded text-red-700">
          Error al cargar datos: {error}
        </div>
      )}
      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {summary && !loading ? (
          <>
            <StatCard label="Productos" value={summary.totalProductos} icon={Package} color="bg-primary" sub="en inventario" />
            <StatCard label="Valor del inventario" value={`$${Number(summary.valorInventario).toLocaleString("es", { minimumFractionDigits: 2 })}`} icon={DollarSign} color="bg-teal-600" />
            <StatCard label="Alertas de stock bajo" value={summary.productosStockBajo} icon={AlertTriangle} color={summary.productosStockBajo > 0 ? "bg-amber-500" : "bg-green-600"} sub={summary.productosStockBajo > 0 ? "Requieren atención" : "Todo en orden"} />
            <StatCard label="Total transacciones" value={summary.totalTransacciones} icon={ArrowLeftRight} color="bg-slate-600" />
            <StatCard label="Ingresos por ventas" value={`$${Number(summary.ingresosVentas).toLocaleString("es", { minimumFractionDigits: 2 })}`} icon={TrendingUp} color="bg-green-600" sub={`${summary.totalVentas} ventas`} />
            <StatCard label="Costo de compras" value={`$${Number(summary.costoCompras).toLocaleString("es", { minimumFractionDigits: 2 })}`} icon={ShoppingCart} color="bg-blue-700" sub={`${summary.totalCompras} compras`} />
          </>
        ) : (
          Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-24 rounded-xl" />
          ))
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Low stock alerts */}
        <div className="bg-card border border-card-border rounded-xl overflow-hidden">
          <div className="px-5 py-4 border-b border-border flex items-center gap-2">
            <AlertTriangle size={15} className="text-amber-500" />
            <h2 className="text-sm font-semibold">Alertas de stock bajo</h2>
          </div>
          <div className="divide-y divide-border">
            {loading ? (
              <div className="p-5 space-y-3">
                {Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-8" />)}
              </div>
            ) : lowStock && lowStock.length === 0 ? (
              <div className="p-8 text-center text-muted-foreground text-sm">
                Todos los productos tienen stock suficiente
              </div>
            ) : (
              (lowStock || []).map((p: any) => (
                <div key={p.id} className="px-5 py-3 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-foreground">{p.nombre}</p>
                    <p className="text-xs text-muted-foreground capitalize">{p.tipo}</p>
                  </div>
                  <div className="text-right">
                    <span className={`text-sm font-bold ${p.stock === 0 ? "text-destructive" : "text-amber-500"}`}>
                      {p.stock} uds
                    </span>
                    <p className="text-xs text-muted-foreground">mín: {p.stockMinimo}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent activity */}
        <div className="bg-card border border-card-border rounded-xl overflow-hidden">
          <div className="px-5 py-4 border-b border-border flex items-center gap-2">
            <ArrowLeftRight size={15} className="text-primary" />
            <h2 className="text-sm font-semibold">Actividad reciente</h2>
          </div>
          <div className="divide-y divide-border">
            {loading ? (
              <div className="p-5 space-y-3">
                {Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-8" />)}
              </div>
            ) : activity && activity.length === 0 ? (
              <div className="p-8 text-center text-muted-foreground text-sm">
                No hay transacciones registradas
              </div>
            ) : (
              (activity || []).map((t: any) => (
                <div key={t.id} className="px-5 py-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Badge
                      variant="outline"
                      className={`text-[10px] uppercase tracking-wide ${t.tipo === "venta" ? "bg-green-600/15 text-green-700 border-green-600/30" : "bg-blue-600/15 text-blue-700 border-blue-600/30"}`}
                    >
                      {t.tipo}
                    </Badge>
                    <span className="text-sm text-foreground truncate max-w-[130px]">{t.productNombre}</span>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <p className="text-sm font-semibold text-foreground">${Number(t.total).toFixed(2)}</p>
                    <p className="text-[11px] text-muted-foreground">x{t.cantidad} uds</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
