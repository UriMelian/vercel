from fastapi import FastAPI, HTTPException, Query
from models.product import ProductCreate, Product
from database.crud import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product,
)

app = FastAPI()

@app.post("/productos", response_model=Product)
def crear_producto(product: ProductCreate):
    result = create_product(
        product.nombre,
        product.descripcion,
        product.precio,
        product.stock,
        product.categoria,
    )
if result is None:
    raise HTTPException(status_code=500, detail="Error al crear el producto")

return {
    "id": result[0],
    "nombre": result[1],
    "descripcion": result[2],
    "precio": result[3],
    "stock": result[4],
    "categoria": result[5],
 }
@app.get("/productos", response_model=list[Product])
def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    categoria: str = Query(None),
    disponible: bool = Query(None),
):
    result = get_products(
        skip=skip, limit=limit, categoria=categoria, disponible=disponible
    )
    if result is None:
        raise HTTPException(status_code=500, detail="Error al obtener productos")
    return [
    {
        "id": row[0],
        "nombre": row[1],
        "descripcion": row[2],
        "precio": row[3],
        "stock": row[4],
        "categoria": row[5],
    }
    for row in result
    ]
@app.get("/productos/{product_id}", response_model=Product)
def obtener_producto(product_id: str):
    result = get_product_by_id(product_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {
        "id": result[0],
        "nombre": result[1],
        "descripcion": result[2],
        "precio": result[3],
        "stock": result[4],
        "categoria": result[5],
    }

@app.put("/productos/{product_id}", response_model=Product)
def actualizar_producto(product_id: str, producto: ProductCreate):
    result = update_product(
        product_id,
        producto.nombre,
        producto.descripcion,
        producto.precio,
        producto.stock,
        producto.categoria,
    )

    if result is None:
        raise HTTPException(
            status_code=404, detail="Producto no encontrado o ID inválido"
        )
    return {
        "id": result[0],
        "nombre": result[1],
        "descripcion": result[2],
        "precio": result[3],
        "stock": result[4],
        "categoria": result[5],
    }

@app.delete("/productos/{product_id}")
def borrar_producto(product_id: str):
    result = delete_product(product_id)

    if result is None:
        raise HTTPException(
            status_code=404, detail="Producto no encontrado o ID inválido"
        )
    return {"message": f"Producto con ID {product_id} eliminado correctamente"}