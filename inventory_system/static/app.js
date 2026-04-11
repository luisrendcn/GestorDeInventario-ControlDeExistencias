// ============================================================
// CONTROL DE EXISTENCIAS - Frontend JavaScript
// ============================================================

// ============================================================
// 1. GESTIÓN DE PESTAÑAS
// ============================================================

document.querySelectorAll('.pestaña').forEach(boton => {
    boton.addEventListener('click', () => {
        // Remover clase activo de todas las pestañas y contenido
        document.querySelectorAll('.pestaña').forEach(b => b.classList.remove('activo'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('activo'));
        
        // Añadir clase activo al botón y contenido seleccionado
        boton.classList.add('activo');
        const tabId = boton.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('activo');
        
        // Cargar datos según la pestaña
        if (tabId === 'dashboard') cargarDashboard();
        if (tabId === 'productos') cargarProductos();
    });
});

// ============================================================
// 1.5 ADMINISTRACIÓN - INICIALIZAR Y LIMPIAR
// ============================================================

document.getElementById('btn-inicializar').addEventListener('click', async () => {
    if (!confirm('¿Cargar el inventario de demostración?\n\nEsto reemplazará los datos actuales.')) return;
    
    try {
        const respuesta = await llamarAPI('POST', '/inicializar');
        mostrarMensajeAdmin(`✅ ${respuesta.mensaje}`, 'exito');
        setTimeout(() => cargarDashboard(), 1000);
        setTimeout(() => cargarProductos(), 1000);
    } catch (error) {
        mostrarMensajeAdmin(`❌ Error: ${error.message}`, 'error');
    }
});

document.getElementById('btn-limpiar').addEventListener('click', async () => {
    if (!confirm('⚠️ ADVERTENCIA: ¿Limpiar toda la base de datos?\n\nEsta acción NO se puede deshacer.')) return;
    
    try {
        const respuesta = await llamarAPI('POST', '/limpiar');
        mostrarMensajeAdmin(`✅ ${respuesta.mensaje}`, 'exito');
        setTimeout(() => cargarDashboard(), 1000);
        setTimeout(() => cargarProductos(), 1000);
    } catch (error) {
        mostrarMensajeAdmin(`❌ Error: ${error.message}`, 'error');
    }
});

function mostrarMensajeAdmin(texto, tipo) {
    const msgDiv = document.getElementById('admin-mensaje');
    msgDiv.textContent = texto;
    msgDiv.className = `mensaje ${tipo}`;
    msgDiv.style.display = 'block';
    
    setTimeout(() => {
        msgDiv.style.display = 'none';
    }, 5000);
}

// ============================================================
// 2. FUNCIONES DE API
// ============================================================

const API_BASE = 'http://localhost:5000/api';

// Función genérica para llamadas a API
async function llamarAPI(metodo, endpoint, datos = null) {
    try {
        const opciones = {
            method: metodo,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (datos) {
            opciones.body = JSON.stringify(datos);
        }
        
        const respuesta = await fetch(`${API_BASE}${endpoint}`, opciones);
        
        if (!respuesta.ok) {
            const error = await respuesta.json();
            throw new Error(error.error || 'Error en la solicitud');
        }
        
        return await respuesta.json();
    } catch (error) {
        console.error('Error API:', error);
        mostrarMensaje(`Error: ${error.message}`, 'error');
        throw error;
    }
}

// ============================================================
// 3. DASHBOARD
// ============================================================

async function cargarDashboard() {
    try {
        // Cargar alertas
        const alertas = await llamarAPI('GET', '/alertas');
        document.getElementById('total-productos').textContent = alertas.total_productos || 0;
        document.getElementById('stock-bajo').textContent = alertas.stock_bajo || 0;
        document.getElementById('agotados').textContent = alertas.agotados || 0;
        
        // Cargar reporte
        const reporte = await llamarAPI('GET', '/reporte');
        document.getElementById('valor-total').textContent = '$' + reporte.valor_total.toFixed(2);
        document.getElementById('stock-promedio').textContent = reporte.stock_promedio.toFixed(1);
        document.getElementById('total-unidades').textContent = reporte.total_unidades;
        document.getElementById('precio-promedio').textContent = '$' + reporte.precio_promedio.toFixed(2);
        document.getElementById('disponibles').textContent = alertas.total_productos - alertas.agotados;
    } catch (error) {
        console.error('Error cargando dashboard:', error);
    }
}

// ============================================================
// 4. GESTIÓN DE PRODUCTOS
// ============================================================

async function cargarProductos() {
    try {
        const productos = await llamarAPI('GET', '/productos');
        const tbody = document.querySelector('#tabla-productos tbody');
        tbody.innerHTML = '';
        
        productos.forEach(prod => {
            const estado = prod.agotado ? '❌ Agotado' : (prod.stock_bajo ? '⚠️ Bajo' : '✅ Normal');
            const fila = `
                <tr>
                    <td>${prod.id}</td>
                    <td>${prod.nombre}</td>
                    <td>$${prod.precio.toFixed(2)}</td>
                    <td>${prod.stock}</td>
                    <td>${prod.stock_minimo}</td>
                    <td>$${prod.valor_total.toFixed(2)}</td>
                    <td>${estado}</td>
                    <td>
                        <button class="btn btn-small btn-warning" onclick="verDetalles('${prod.id}')">Ver</button>
                        <button class="btn btn-small btn-danger" onclick="eliminarProducto('${prod.id}')">Eliminar</button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += fila;
        });
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}

// Crear producto
document.getElementById('form-producto').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const datos = {
        id: document.getElementById('pro-id').value,
        nombre: document.getElementById('pro-nombre').value,
        precio: parseFloat(document.getElementById('pro-precio').value),
        stock: parseInt(document.getElementById('pro-stock').value),
        stock_minimo: parseInt(document.getElementById('pro-stock-min').value),
        descripcion: document.getElementById('pro-descripcion').value || null
    };
    
    try {
        await llamarAPI('POST', '/productos', datos);
        mostrarMensaje('Producto creado exitosamente', 'exito');
        document.getElementById('form-producto').reset();
        cargarProductos();
    } catch (error) {
        console.error('Error creando producto:', error);
    }
});

// Eliminar producto
async function eliminarProducto(id) {
    if (!confirm(`¿Eliminar producto ${id}?`)) return;
    
    try {
        await llamarAPI('DELETE', `/productos/${id}`);
        mostrarMensaje('Producto eliminado', 'exito');
        cargarProductos();
    } catch (error) {
        console.error('Error eliminando producto:', error);
    }
}

// Ver detalles (futuro: modal con historial del producto)
function verDetalles(id) {
    alert(`Detalles del producto: ${id}`);
}

// ============================================================
// 5. OPERACIONES DE STOCK
// ============================================================

// Entrada de stock
document.getElementById('form-entrada').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const datos = {
        producto_id: document.getElementById('entrada-id').value,
        cantidad: parseInt(document.getElementById('entrada-cantidad').value),
        motivo: document.getElementById('entrada-motivo').value || 'Entrada manual'
    };
    
    try {
        await llamarAPI('POST', '/entrada', datos);
        mostrarMensaje(`Entrada registrada: +${datos.cantidad} unidades`, 'exito');
        document.getElementById('form-entrada').reset();
        cargarProductos();
    } catch (error) {
        console.error('Error registrando entrada:', error);
    }
});

// Salida de stock
document.getElementById('form-salida').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const datos = {
        producto_id: document.getElementById('salida-id').value,
        cantidad: parseInt(document.getElementById('salida-cantidad').value),
        motivo: document.getElementById('salida-motivo').value || 'Salida manual'
    };
    
    try {
        await llamarAPI('POST', '/salida', datos);
        mostrarMensaje(`Salida registrada: -${datos.cantidad} unidades`, 'exito');
        document.getElementById('form-salida').reset();
        cargarProductos();
    } catch (error) {
        console.error('Error registrando salida:', error);
    }
});

// Ajuste de stock
document.getElementById('form-ajuste').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const datos = {
        producto_id: document.getElementById('ajuste-id').value,
        nuevo_stock: parseInt(document.getElementById('ajuste-nuevo').value),
        motivo: document.getElementById('ajuste-motivo').value || 'Ajuste por auditoría'
    };
    
    try {
        await llamarAPI('POST', '/ajuste', datos);
        mostrarMensaje('Stock ajustado correctamente', 'exito');
        document.getElementById('form-ajuste').reset();
        cargarProductos();
    } catch (error) {
        console.error('Error ajustando stock:', error);
    }
});

// ============================================================
// 6. REPORTES
// ============================================================

// Botón generar reporte - se agrega una sola vez
document.getElementById('btn-generar-reporte').addEventListener('click', async () => {
    try {
        const reporte = await llamarAPI('GET', '/reporte');
        
        // Llenar datos del reporte
        document.getElementById('rep-total-prod').textContent = reporte.total_productos;
        document.getElementById('rep-total-unid').textContent = reporte.total_unidades;
        document.getElementById('rep-valor').textContent = reporte.valor_total.toFixed(2);
        document.getElementById('rep-stock-prom').textContent = reporte.stock_promedio.toFixed(1);
        document.getElementById('rep-precio-prom').textContent = reporte.precio_promedio.toFixed(2);
        
        // Obtener alertas para completar el reporte
        const alertas = await llamarAPI('GET', '/alertas');
        document.getElementById('rep-disponibles').textContent = alertas.total_productos - alertas.agotados;
        document.getElementById('rep-bajo').textContent = alertas.stock_bajo;
        document.getElementById('rep-agotados').textContent = alertas.agotados;
        
        // Mostrar el contenedor de resultados
        document.getElementById('reporte-contenedor').style.display = 'grid';
        mostrarMensaje('✅ Reporte generado exitosamente', 'exito');
    } catch (error) {
        console.error('Error generando reporte:', error);
    }
});

// ============================================================
// 7. HISTORIAL
// ============================================================

document.getElementById('btn-cargar-historial').addEventListener('click', async () => {
    try {
        const productoId = document.getElementById('filter-producto').value || null;
        let endpoint = '/historial';
        if (productoId) {
            endpoint += `?producto_id=${productoId}`;
        }
        
        const movimientos = await llamarAPI('GET', endpoint);
        const tbody = document.querySelector('#tabla-historial tbody');
        tbody.innerHTML = '';
        
        movimientos.forEach(mov => {
            const fecha = new Date(mov.fecha).toLocaleString('es-ES');
            const fila = `
                <tr>
                    <td>${fecha}</td>
                    <td>${mov.producto_id}</td>
                    <td>${mov.tipo}</td>
                    <td>${mov.cantidad}</td>
                    <td>${mov.stock_anterior}</td>
                    <td>${mov.stock_nuevo}</td>
                    <td>${mov.motivo}</td>
                </tr>
            `;
            tbody.innerHTML += fila;
        });
    } catch (error) {
        console.error('Error cargando historial:', error);
    }
});

// ============================================================
// 8. UTILIDADES
// ============================================================

function mostrarMensaje(texto, tipo) {
    const msgDiv = document.getElementById('mensaje-operacion');
    msgDiv.textContent = texto;
    msgDiv.className = `mensaje ${tipo}`;
    msgDiv.style.display = 'block';
    
    setTimeout(() => {
        msgDiv.style.display = 'none';
    }, 3000);
}

// Cargar dashboard al iniciar
window.addEventListener('load', () => {
    cargarDashboard();
    cargarProductos();
});
