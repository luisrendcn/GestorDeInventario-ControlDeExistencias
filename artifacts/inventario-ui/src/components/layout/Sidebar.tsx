import { Link, useLocation } from "wouter";
import { LayoutDashboard, Package, ArrowLeftRight, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";
import { useGetSummary } from "@workspace/api-client-react";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/products", label: "Productos", icon: Package },
  { href: "/transactions", label: "Transacciones", icon: ArrowLeftRight },
];

export function Sidebar() {
  const [location] = useLocation();
  const { data: summary, error: summaryError } = useGetSummary();

  // Don't show alerts if there's an error fetching summary
  const alertCount = !summaryError ? (summary?.productosStockBajo ?? 0) : 0;

  return (
    <aside className="fixed inset-y-0 left-0 z-30 w-60 flex flex-col bg-sidebar text-sidebar-foreground border-r border-sidebar-border">
      <div className="px-6 py-5 border-b border-sidebar-border/30">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-sidebar-primary flex items-center justify-center flex-shrink-0">
            <Package className="w-4.5 h-4.5 text-white" size={18} />
          </div>
          <div>
            <p className="text-sm font-semibold text-sidebar-foreground leading-tight">Inventario</p>
            <p className="text-[10px] text-sidebar-foreground/50 uppercase tracking-widest">Sistema de Gestión</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 py-4 px-3 space-y-0.5">
        {navItems.map(({ href, label, icon: Icon }) => {
          const isActive = location === href;
          return (
            <Link key={href} href={href}>
              <a
                data-testid={`nav-${label.toLowerCase()}`}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium cursor-pointer transition-colors",
                  isActive
                    ? "bg-sidebar-accent text-sidebar-foreground"
                    : "text-sidebar-foreground/60 hover:text-sidebar-foreground hover:bg-sidebar-accent/50"
                )}
              >
                <Icon size={16} className="flex-shrink-0" />
                {label}
              </a>
            </Link>
          );
        })}
      </nav>

      {(summary?.productosStockBajo ?? 0) > 0 && (
        <div className="mx-3 mb-4 p-3 rounded-lg bg-amber-500/10 border border-amber-500/30">
          <div className="flex items-start gap-2">
            <AlertTriangle size={14} className="text-amber-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-xs font-semibold text-amber-400">{alertCount} alertas de stock</p>
              <p className="text-[11px] text-amber-400/70 mt-0.5">Revisar inventario</p>
            </div>
          </div>
        </div>
      )}

      <div className="px-4 pb-4 text-[10px] text-sidebar-foreground/30 uppercase tracking-widest">
        Sistema v1.0
      </div>
    </aside>
  );
}
