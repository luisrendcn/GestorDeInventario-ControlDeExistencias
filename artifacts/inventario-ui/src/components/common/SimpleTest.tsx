import React from "react";

export function SimpleTest() {
  React.useEffect(() => {
    console.log("✅ SimpleTest component mounted!");
  }, []);

  return (
    <div style={{
      padding: "20px",
      backgroundColor: "#f0f0f0",
      color: "#000",
      fontFamily: "Arial, sans-serif",
      textAlign: "center",
    }}>
      <h1>✅ React está funcionando</h1>
      <p>Si ves este mensaje, React se ha cargado correctamente.</p>
      <details>
        <summary>Revisar la consola del navegador</summary>
        <p>Abre F12 → Consola para ver los logs de debugging</p>
      </details>
    </div>
  );
}
