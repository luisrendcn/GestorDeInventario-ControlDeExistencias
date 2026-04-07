import { LayoutDashboard, Package, ArrowLeftRight } from "lucide-react";

export function AppLoadingShell() {
  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar skeleton */}
      <aside className="fixed inset-y-0 left-0 z-30 w-60 flex flex-col bg-sidebar text-sidebar-foreground border-r border-sidebar-border">
        <div className="px-6 py-5 border-b border-sidebar-border/30">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-sidebar-primary flex items-center justify-center flex-shrink-0">
              <Package className="w-4.5 h-4.5 text-white" size={18} />
            </div>
            <div>
              <div className="h-4 w-24 bg-sidebar-foreground/20 rounded"></div>
              <div className="h-2 w-32 bg-sidebar-foreground/10 rounded mt-2"></div>
            </div>
          </div>
        </div>

        <nav className="flex-1 py-4 px-3 space-y-0.5">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium cursor-pointer"
            >
              <div className="w-4 h-4 rounded bg-sidebar-foreground/20"></div>
              <div className="h-4 w-24 bg-sidebar-foreground/20 rounded"></div>
            </div>
          ))}
        </nav>
      </aside>

      {/* Main content skeleton */}
      <main className="flex-1 ml-60 flex flex-col min-h-screen overflow-hidden">
        <header className="sticky top-0 z-20 bg-background/80 backdrop-blur border-b border-border px-8 py-4 flex items-center justify-between">
          <div>
            <div className="h-6 w-40 bg-foreground/10 rounded mb-2"></div>
            <div className="h-4 w-56 bg-muted-foreground/20 rounded"></div>
          </div>
        </header>
        <div className="flex-1 overflow-auto px-8 py-6 space-y-4">
          <div className="h-8 w-48 bg-foreground/10 rounded"></div>
          <div className="grid grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-card border border-card-border rounded-xl p-5 h-24 animate-pulse"></div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
