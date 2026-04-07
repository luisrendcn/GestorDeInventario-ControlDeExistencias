interface AppLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
}

export function AppLayout({ children, title, subtitle, actions }: AppLayoutProps) {
  return (
    <div className="flex flex-col min-h-screen bg-background flex-1">
        <header className="sticky top-0 z-20 bg-background/80 backdrop-blur border-b border-border px-8 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-foreground">{title}</h1>
            {subtitle && <p className="text-sm text-muted-foreground">{subtitle}</p>}
          </div>
          {actions && <div className="flex items-center gap-2">{actions}</div>}
        </header>
      <div className="flex-1 overflow-auto px-8 py-6">
          {children}
        </div>
    </div>
  );
}
