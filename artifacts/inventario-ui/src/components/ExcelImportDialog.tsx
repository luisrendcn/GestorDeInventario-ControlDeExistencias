import { useState, useRef } from "react";
import { Upload, File, AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";
import { useToast } from "@/hooks/use-toast";
import { getListProductsQueryKey } from "@workspace/api-client-react";
import { useQueryClient } from "@tanstack/react-query";

interface ImportResult {
  exitosos: number;
  fallidos: number;
  advertencias: number;
  errores: Array<{ fila: number; error: string }>;
  advertencias_list: Array<{ fila: number; advertencia: string }>;
}

interface ExcelImportDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function ExcelImportDialog({ open, onOpenChange }: ExcelImportDialogProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ImportResult | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const droppedFile = files[0];
      const isValidFormat = droppedFile.name.endsWith(".xlsx") || droppedFile.name.endsWith(".csv");
      if (isValidFormat) {
        setFile(droppedFile);
      } else {
        toast({
          title: "Formato incorrecto",
          description: "Por favor carga un archivo Excel (.xlsx) o CSV (.csv)",
          variant: "destructive",
        });
      }
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      setFile(files[0]);
    }
  };

  const openFileDialog = () => {
    inputRef.current?.click();
  };

  const handleImport = async () => {
    if (!file) {
      toast({
        title: "Error",
        description: "Por favor selecciona un archivo Excel o CSV",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      console.log("📤 Iniciando importación de archivo:", file.name, "Size:", file.size);

      const response = await fetch("/api/products/import", {
        method: "POST",
        body: formData,
      });

      console.log("📥 Respuesta del servidor:", response.status, response.statusText);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error("❌ Error del servidor:", errorData);
        throw new Error(
          errorData.details || errorData.error || `Error HTTP ${response.status}`
        );
      }

      const data: ImportResult = await response.json();
      console.log("✅ Datos importados:", data);
      setResult(data);

      // Recargar la lista de productos
      await queryClient.invalidateQueries({
        queryKey: getListProductsQueryKey(),
      });

      toast({
        title: "Importación completada",
        description: `${data.exitosos} productos importados exitosamente`,
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido";
      console.error("❌ Error al importar:", errorMessage);
      toast({
        title: "Error en la importación",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFile(null);
    setResult(null);
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Upload className="w-5 h-5" />
            Importar Productos
          </DialogTitle>
          <DialogDescription>
            Carga un archivo .xlsx o .csv con tus productos. Se detectarán automáticamente el tipo de producto
            (Simple, Perecedero o Digital).
          </DialogDescription>
        </DialogHeader>

        {!result ? (
          <div className="space-y-4">
            {/* Drop Zone */}
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={openFileDialog}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                dragActive
                  ? "border-primary bg-primary/5"
                  : "border-gray-300 hover:border-gray-400"
              }`}
            >
              <File className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <p className="text-sm font-medium">Arrastra tu archivo aquí o haz clic para seleccionar</p>
              <p className="text-xs text-gray-500 mt-1">Formato: .xlsx o .csv</p>
              <input
                ref={inputRef}
                type="file"
                accept=".xlsx,.csv"
                onChange={handleFileSelect}
                className="hidden"
                aria-label="Seleccionar archivo Excel o CSV"
              />
            </div>

            {/* Selected File */}
            {file && (
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border">
                <div className="flex items-center gap-3">
                  <File className="w-5 h-5 text-primary" />
                  <div className="min-w-0">
                    <p className="text-sm font-medium truncate">{file.name}</p>
                    <p className="text-xs text-gray-500">
                      {(file.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setFile(null)}
                >
                  ✕
                </Button>
              </div>
            )}

            {/* Info Box */}
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Información</AlertTitle>
              <AlertDescription>
                <ul className="list-disc list-inside text-xs space-y-1 mt-2">
                  <li>Columnas requeridas: nombre, precio_venta, stock</li>
                  <li>Se detectan automáticamente: alimentos (perecedero), software (digital), otros (simple)</li>
                  <li>Fechas en formato YYYY-MM-DD para productos perecederos</li>
                  <li>URLs para productos digitales</li>
                </ul>
              </AlertDescription>
            </Alert>

            <Button
              onClick={handleImport}
              disabled={!file || loading}
              className="w-full"
            >
              {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              {loading ? "Importando..." : "Importar"}
            </Button>
          </div>
        ) : (
          // Results View
          <div className="space-y-4">
            {result.fallidos === 0 ? (
              <Alert className="border-green-200 bg-green-50">
                <CheckCircle2 className="h-4 w-4 text-green-600" />
                <AlertTitle className="text-green-800">¡Importación Exitosa!</AlertTitle>
                <AlertDescription className="text-green-700">
                  {result.exitosos} productos importados correctamente
                </AlertDescription>
              </Alert>
            ) : (
              <Alert className="border-amber-200 bg-amber-50">
                <AlertCircle className="h-4 w-4 text-amber-600" />
                <AlertTitle className="text-amber-800">Importación Parcial</AlertTitle>
                <AlertDescription className="text-amber-700">
                  {result.exitosos} exitosos, {result.fallidos} fallidos
                </AlertDescription>
              </Alert>
            )}

            {/* Stats */}
            <div className="grid grid-cols-3 gap-4">
              <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-2xl font-bold text-blue-600">{result.exitosos}</p>
                <p className="text-xs text-blue-700">Exitosos</p>
              </div>
              <div className="p-3 bg-red-50 rounded-lg border border-red-200">
                <p className="text-2xl font-bold text-red-600">{result.fallidos}</p>
                <p className="text-xs text-red-700">Fallidos</p>
              </div>
              <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                <p className="text-2xl font-bold text-yellow-600">{result.advertencias}</p>
                <p className="text-xs text-yellow-700">Advertencias</p>
              </div>
            </div>

            {/* Errors */}
            {result.errores.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-red-700">Errores encontrados:</h4>
                <div className="bg-red-50 rounded-lg p-3 max-h-48 overflow-y-auto space-y-1">
                  {result.errores.slice(0, 20).map((error, idx) => (
                    <div key={idx} className="text-xs text-red-700">
                      <span className="font-medium">Fila {error.fila}:</span> {error.error}
                    </div>
                  ))}
                  {result.errores.length > 20 && (
                    <div className="text-xs text-red-600 italic">
                      ... y {result.errores.length - 20} errores más
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Warnings */}
            {result.advertencias_list.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-yellow-700">Advertencias:</h4>
                <div className="bg-yellow-50 rounded-lg p-3 max-h-32 overflow-y-auto space-y-1">
                  {result.advertencias_list.map((warning, idx) => (
                    <div key={idx} className="text-xs text-yellow-700">
                      <span className="font-medium">Fila {warning.fila}:</span> {warning.advertencia}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        <DialogFooter>
          {result ? (
            <Button onClick={handleClose} className="w-full">
              Cerrar
            </Button>
          ) : (
            <>
              <Button variant="outline" onClick={() => onOpenChange(false)}>
                Cancelar
              </Button>
              <Button
                onClick={handleImport}
                disabled={!file || loading}
              >
                {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                {loading ? "Importando..." : "Importar"}
              </Button>
            </>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
