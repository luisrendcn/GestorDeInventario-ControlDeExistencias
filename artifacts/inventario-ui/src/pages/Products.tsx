import { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { ExcelImportDialog } from "@/components/ExcelImportDialog";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter
} from "@/components/ui/dialog";
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
  AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle
} from "@/components/ui/alert-dialog";
import { Label } from "@/components/ui/label";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from "@/components/ui/select";
import { Plus, Search, Pencil, Trash2, AlertTriangle, Package, Upload } from "lucide-react";

type ProductType = "simple" | "perecedero" | "digital";

interface ProductFormData {
  nombre: string;
  tipo: ProductType;
  precio: string;
  stock: string;
  stockMinimo: string;
  categoria: string;
  fechaVencimiento: string;
  urlDescarga: string;
}

const defaultForm: ProductFormData = {
  nombre: "", tipo: "simple", precio: "", stock: "", stockMinimo: "5",
  categoria: "General", fechaVencimiento: "", urlDescarga: ""
};

const tipoBadge: Record<string, string> = {
  simple: "bg-blue-500/10 text-blue-700 border-blue-500/30",
  perecedero: "bg-amber-500/10 text-amber-700 border-amber-500/30",
  digital: "bg-purple-500/10 text-purple-700 border-purple-500/30",
};

export default function Products() {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState<string>("all");
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showImportDialog, setShowImportDialog] = useState(false);
  const [showClearAllDialog, setShowClearAllDialog] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [form, setForm] = useState<ProductFormData>(defaultForm);
  const { toast } = useToast();

  // Load products
  const loadProducts = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://localhost:3000/api/products");
      if (!res.ok) throw new Error("Error cargando productos");
      const data = await res.json();
      setProducts(data);
    } catch (err) {
      toast({ title: "Error", description: String(err), variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const openCreate = () => { setForm(defaultForm); setEditingId(null); setShowCreateDialog(true); };
  const openEdit = (p: any) => {
    setForm({
      nombre: p.nombre, tipo: p.tipo as ProductType,
      precio: String(p.precio), stock: String(p.stock), stockMinimo: String(p.stockMinimo),
      categoria: p.categoria ?? "General",
      fechaVencimiento: p.fechaVencimiento ?? "",
      urlDescarga: p.urlDescarga ?? "",
    });
    setEditingId(p.id);
    setShowCreateDialog(true);
  };

  // Filter products
  const filteredProducts = products.filter(p => {
    const matchesSearch = p.nombre.toLowerCase().includes(search.toLowerCase());
    const matchesType = filterType === "all" || p.tipo === filterType;
    return matchesSearch && matchesType;
  });

  const handleSubmit = async () => {
    if (!form.nombre || !form.precio || !form.stock) {
      toast({ title: "Campos incompletos", description: "Completa nombre, precio y stock.", variant: "destructive" });
      return;
    }
    const payload = {
      nombre: form.nombre, tipo: form.tipo as ProductType,
      precio: parseFloat(form.precio), stock: parseInt(form.stock),
      stockMinimo: parseInt(form.stockMinimo) || 5,
      categoria: form.tipo === "simple" ? form.categoria : undefined,
      fechaVencimiento: form.tipo === "perecedero" && form.fechaVencimiento ? form.fechaVencimiento : undefined,
      urlDescarga: form.tipo === "digital" && form.urlDescarga ? form.urlDescarga : undefined,
    };

    try {
      setSubmitting(true);
      const method = editingId ? "PATCH" : "POST";
      const url = editingId ? `http://localhost:3000/api/products/${editingId}` : "http://localhost:3000/api/products";
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Error guardando producto");
      
      toast({ title: editingId ? "Producto actualizado" : "Producto creado" });
      setShowCreateDialog(false);
      loadProducts();
    } catch (err) {
      toast({ title: "Error", description: String(err), variant: "destructive" });
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!deletingId) return;
    try {
      setSubmitting(true);
      const res = await fetch(`http://localhost:3000/api/products/${deletingId}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Error eliminando producto");
      toast({ title: "Producto eliminado" });
      setDeletingId(null);
      loadProducts();
    } catch (err) {
      toast({ title: "Error", description: String(err), variant: "destructive" });
    } finally {
      setSubmitting(false);
    }
  };

  const handleClearAll = async () => {
    try {
      const response = await fetch("http://localhost:3000/api/products", { method: "DELETE" });
      if (!response.ok) throw new Error("Error al limpiar la base de datos");
      
      const data = await response.json();
      toast({ 
        title: "Base de datos limpiada",
        description: `${data.eliminados} productos eliminados`
      });
      setShowClearAllDialog(false);
      loadProducts();
    } catch (e) {
      toast({
        title: "Error",
        description: e instanceof Error ? e.message : "Error desconocido",
        variant: "destructive"
      });
    }
  };

  return (
    <AppLayout
      title="Productos"
      subtitle="Gestión del catálogo de inventario"
      actions={
        <div className="flex gap-2">
          <Button onClick={() => setShowImportDialog(true)} size="sm" variant="outline" className="gap-1.5">
            <Upload size={14} /> Importar Excel
          </Button>
          <Button onClick={() => setShowClearAllDialog(true)} size="sm" variant="destructive" className="gap-1.5">
            <Trash2 size={14} /> Limpiar todo
          </Button>
          <Button onClick={openCreate} size="sm" className="gap-1.5">
            <Plus size={14} /> Nuevo producto
          </Button>
        </div>
      }
    >
      {/* Filters */}
      <div className="flex gap-3 mb-5">
        <div className="relative flex-1 max-w-xs">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Buscar productos..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select value={filterType} onValueChange={setFilterType}>
          <SelectTrigger className="w-44">
            <SelectValue placeholder="Tipo" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos los tipos</SelectItem>
            <SelectItem value="simple">Simple</SelectItem>
            <SelectItem value="perecedero">Perecedero</SelectItem>
            <SelectItem value="digital">Digital</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Table */}
      <div className="bg-card border border-card-border rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border bg-muted/40">
              <th className="text-left px-5 py-3 font-medium text-muted-foreground">Producto</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Tipo</th>
              <th className="text-right px-4 py-3 font-medium text-muted-foreground">Precio</th>
              <th className="text-right px-4 py-3 font-medium text-muted-foreground">Stock</th>
              <th className="text-left px-4 py-3 font-medium text-muted-foreground">Info</th>
              <th className="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {loading ? (
              Array.from({ length: 6 }).map((_, i) => (
                <tr key={i}>
                  <td colSpan={6} className="px-5 py-3"><Skeleton className="h-6 w-full" /></td>
                </tr>
              ))
            ) : filteredProducts.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-5 py-12 text-center text-muted-foreground">
                  <Package size={32} className="mx-auto mb-2 opacity-30" />
                  No se encontraron productos
                </td>
              </tr>
            ) : (
              filteredProducts.map((p) => (
                <tr key={p.id} className="hover:bg-muted/30 transition-colors">
                  <td className="px-5 py-3">
                    <div className="flex items-center gap-2">
                      {p.stockBajo && <AlertTriangle size={13} className="text-amber-500 flex-shrink-0" />}
                      <div>
                        <p className="font-medium text-foreground">{p.nombre}</p>
                        <p className="text-[11px] text-muted-foreground font-mono">{p.id}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <Badge variant="outline" className={`text-[10px] capitalize ${tipoBadge[p.tipo] ?? ""}`}>
                      {p.tipo}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-right font-medium">${Number(p.precio).toFixed(2)}</td>
                  <td className="px-4 py-3 text-right">
                    <span className={`font-bold ${p.stockBajo ? "text-amber-500" : "text-foreground"} ${p.stock === 0 ? "text-destructive" : ""}`}>
                      {p.stock}
                    </span>
                    <span className="text-muted-foreground text-xs"> / {p.stockMinimo}</span>
                  </td>
                  <td className="px-4 py-3 text-xs text-muted-foreground max-w-[180px] truncate">{p.infoAdicional}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1 justify-end">
                      <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => openEdit(p)}>
                        <Pencil size={13} />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive hover:text-destructive" onClick={() => setDeletingId(p.id)}>
                        <Trash2 size={13} />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Create/Edit dialog */}
      <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>{editingId ? "Editar producto" : "Nuevo producto"}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <Label htmlFor="nombre">Nombre</Label>
                <Input id="nombre" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} placeholder="Nombre del producto" />
              </div>
              {!editingId && (
                <div className="col-span-2">
                  <Label>Tipo</Label>
                  <Select value={form.tipo} onValueChange={(v) => setForm({ ...form, tipo: v as ProductType })}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="simple">Simple</SelectItem>
                      <SelectItem value="perecedero">Perecedero</SelectItem>
                      <SelectItem value="digital">Digital</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              )}
              <div>
                <Label htmlFor="precio">Precio ($)</Label>
                <Input id="precio" type="number" min="0" step="0.01" value={form.precio} onChange={(e) => setForm({ ...form, precio: e.target.value })} />
              </div>
              <div>
                <Label htmlFor="stock">Stock</Label>
                <Input id="stock" type="number" min="0" value={form.stock} onChange={(e) => setForm({ ...form, stock: e.target.value })} />
              </div>
              <div className="col-span-2">
                <Label htmlFor="stockMinimo">Stock mínimo de alerta</Label>
                <Input id="stockMinimo" type="number" min="0" value={form.stockMinimo} onChange={(e) => setForm({ ...form, stockMinimo: e.target.value })} />
              </div>
              {form.tipo === "simple" && (
                <div className="col-span-2">
                  <Label htmlFor="categoria">Categoría</Label>
                  <Input id="categoria" value={form.categoria} onChange={(e) => setForm({ ...form, categoria: e.target.value })} placeholder="Ej: Electrónica, Ropa..." />
                </div>
              )}
              {form.tipo === "perecedero" && (
                <div className="col-span-2">
                  <Label htmlFor="fechaVencimiento">Fecha de vencimiento</Label>
                  <Input id="fechaVencimiento" type="date" value={form.fechaVencimiento} onChange={(e) => setForm({ ...form, fechaVencimiento: e.target.value })} />
                </div>
              )}
              {form.tipo === "digital" && (
                <div className="col-span-2">
                  <Label htmlFor="urlDescarga">URL de descarga</Label>
                  <Input id="urlDescarga" value={form.urlDescarga} onChange={(e) => setForm({ ...form, urlDescarga: e.target.value })} placeholder="https://..." />
                </div>
              )}
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreateDialog(false)}>Cancelar</Button>
            <Button onClick={handleSubmit} disabled={submitting}>
              {editingId ? "Guardar cambios" : "Crear producto"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete confirm */}
      <AlertDialog open={!!deletingId} onOpenChange={(open) => !open && setDeletingId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Eliminar producto</AlertDialogTitle>
            <AlertDialogDescription>
              Esta acción es irreversible. El producto será eliminado permanentemente del inventario.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={submitting}>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} disabled={submitting} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              Eliminar
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Clear all confirm */}
      <AlertDialog open={showClearAllDialog} onOpenChange={setShowClearAllDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Limpiar base de datos</AlertDialogTitle>
            <AlertDialogDescription>
              Esto eliminará TODOS los productos. Esta acción es irreversible.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={submitting}>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={handleClearAll} disabled={submitting} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
              Eliminar todos
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Import Excel Dialog */}
      <ExcelImportDialog open={showImportDialog} onOpenChange={setShowImportDialog} />
    </AppLayout>
  );
}