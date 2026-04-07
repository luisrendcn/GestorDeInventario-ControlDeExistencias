import { AlertCircle, Info, Loader } from "lucide-react";
import { ReactNode } from "react";

interface DataGuardProps {
  children: ReactNode;
  isLoading?: boolean;
  error?: Error | null;
  label: string;
}

export function DataGuard({ children, isLoading, error, label }: DataGuardProps) {
  if (error) {
    return (
      <div className="flex items-center gap-2 p-4 bg-destructive/10 border border-destructive/30 rounded-lg text-destructive">
        <AlertCircle size={16} className="flex-shrink-0" />
        <span className="text-sm font-medium">Error cargando {label}</span>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex items-center gap-2 p-4 bg-muted/50 rounded-lg text-muted-foreground">
        <Loader size={16} className="animate-spin flex-shrink-0" />
        <span className="text-sm font-medium">Cargando {label}...</span>
      </div>
    );
  }

  return <>{children}</>;
}
