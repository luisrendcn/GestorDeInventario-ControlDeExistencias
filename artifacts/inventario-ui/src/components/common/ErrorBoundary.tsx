import React, { ReactNode, ReactElement } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    console.error("🔴 Error Boundary caught:", error);
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Error details:", errorInfo);
  }

  render(): ReactElement {
    if (this.state.hasError) {
      return (
        <div
          style={{
            padding: "40px",
            backgroundColor: "#fee",
            color: "#c00",
            fontFamily: "monospace",
            whiteSpace: "pre-wrap",
          }}
        >
          <h1>⚠️ La aplicación encontró un error</h1>
          <p>{this.state.error?.message}</p>
          <details>
            <summary>Más detalles</summary>
            <p>{this.state.error?.stack}</p>
          </details>
          <button
            onClick={() => {
              this.setState({ hasError: false, error: null });
              window.location.reload();
            }}
            style={{
              padding: "10px 20px",
              backgroundColor: "#c00",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              marginTop: "20px",
            }}
          >
            Recargar página
          </button>
        </div>
      );
    }

    return this.props.children as ReactElement;
  }
}
