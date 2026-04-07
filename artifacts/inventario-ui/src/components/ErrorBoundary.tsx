import React, { ErrorInfo, ReactNode } from "react";
import { AlertCircle } from "lucide-react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<Props, State> {
  public constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen w-full flex items-center justify-center bg-background">
          <div className="w-full max-w-md mx-4 p-6 bg-card border border-border rounded-lg">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-6 w-6 text-destructive flex-shrink-0 mt-0.5" />
              <div>
                <h1 className="text-lg font-semibold text-foreground">Error en la aplicación</h1>
                <p className="mt-2 text-sm text-muted-foreground">
                  Algo salió mal. Intenta recargar la página o contacta al soporte.
                </p>
                {process.env.NODE_ENV === "development" && this.state.error && (
                  <details className="mt-4">
                    <summary className="cursor-pointer text-xs text-muted-foreground font-mono">
                      Detalles del error
                    </summary>
                    <pre className="mt-2 text-xs bg-background p-2 rounded-md overflow-auto max-h-40 whitespace-pre-wrap break-words">
                      {this.state.error.toString()}
                    </pre>
                  </details>
                )}
                <button
                  onClick={() => window.location.reload()}
                  className="mt-4 px-4 py-2 bg-primary text-white rounded-md text-sm font-medium hover:bg-primary/90"
                >
                  Recargar página
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
