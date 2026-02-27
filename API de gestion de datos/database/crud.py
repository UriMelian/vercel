from database.connection import get_connection
from uuid import UUID


def create_product(nombre, descripcion, precio, stock, categoria):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    query = """
    INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id, nombre, descripcion, precio, stock, categoria;
    """
    cursor.execute(query, (nombre, descripcion, precio, stock, categoria))
    product = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return product

def get_products(
    skip: int = 0, limit: int = 10, categoria: str = None, disponible: bool = None
):
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()

    query = "SELECT id, nombre, descripcion, precio, stock, categoria FROM productos"
    filters = []
    params = []

    if categoria:
        filters.append("categoria = %s")
        params.append(categoria)

    if disponible is not None:
        if disponible:
            filters.append("stock > 0")
        else:
            filters.append("stock = 0")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY id OFFSET %s LIMIT %s"
    params.extend([skip, limit])

    try:
        cur.execute(query, params)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print("Error al obtener productos:", e)
        cur.close()
        conn.close()
        return None

def get_product_by_id(product_id: str):
    try:
        product_uuid = UUID(product_id)
    except ValueError:
        return None
        
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()
    query = "SELECT id, nombre, descripcion, precio, stock, categoria FROM productos WHERE id = %s"
 
    try:
        cur.execute(query, (str(product_uuid),))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print("Error al obtener producto por ID:", e)
        cur.close()
        conn.close()
        return None


def update_product(
    product_id: str,
    nombre: str,
    descripcion: str,
    precio: float,
    stock: int,
    categoria: str,
):
    try:
        product_uuid = UUID(product_id)
    except ValueError:
        return None

    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()

    query = """
    UPDATE productos
    SET nombre = %s,
    descripcion = %s,
    precio = %s,
    stock = %s,
    categoria = %s
    WHERE id = %s
    RETURNING id, nombre, descripcion, precio, stock, categoria
    """
    try:
        cur.execute( 
            query, (nombre, descripcion, precio, stock, categoria, str(product_uuid))
        )
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        rint("Error al actualizar producto:", e)
        cur.close()
        conn.close()
        return None

def delete_product(product_id: str):
    try:
        product_uuid = UUID(product_id)
    except ValueError:
        return None

    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()
 
    query = "DELETE FROM productos WHERE id = %s RETURNING id"
 
    try:
        cur.execute(query, (str(product_uuid),))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print("Error al borrar producto:", e)
        cur.close()
        conn.close()
        return None