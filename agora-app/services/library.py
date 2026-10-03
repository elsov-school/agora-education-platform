from database import connect, row_to_dict, transaction


MATERIAL_FIELDS = (
    "title", "material_type", "school_year", "class_name", "subject",
    "bimester", "bncc", "author_source", "content", "approval_status",
)


def list_materials(filters=None, user=None, approved_only=False, database_path=None):
    filters = filters or {}
    clauses, params = [], []
    if approved_only:
        clauses.append("approval_status = 'Aprovado'")
    for field in ("subject", "class_name", "bimester"):
        if filters.get(field):
            clauses.append(f"{field} = ?")
            params.append(filters[field])
    if filters.get("bncc"):
        clauses.append("LOWER(bncc) LIKE ?")
        params.append(f"%{filters['bncc'].lower()}%")
    if filters.get("search"):
        clauses.append("(LOWER(title) LIKE ? OR LOWER(content) LIKE ?)")
        term = f"%{filters['search'].lower()}%"
        params.extend([term, term])

    # Na visao de professor, o recorte do perfil e aplicado pela consulta Python/SQL.
    if user and user["role"] == "Professor":
        subjects = user.get("subjects", [])
        classes = user.get("classes", [])
        if not subjects or not classes:
            return []
        clauses.append(f"subject IN ({','.join('?' for _ in subjects)})")
        clauses.append(f"class_name IN ({','.join('?' for _ in classes)})")
        params.extend(subjects + classes)

    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    connection = connect(database_path)
    rows = connection.execute(f"SELECT * FROM materials{where} ORDER BY title", params).fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_material(material_id, database_path=None):
    connection = connect(database_path)
    row = connection.execute("SELECT * FROM materials WHERE id = ?", (material_id,)).fetchone()
    connection.close()
    return row_to_dict(row)


def save_material(data, material_id=None, database_path=None):
    values = {field: data[field] for field in MATERIAL_FIELDS}
    with transaction(database_path) as connection:
        if material_id:
            assignments = ", ".join(f"{field} = :{field}" for field in MATERIAL_FIELDS)
            values["id"] = material_id
            connection.execute(f"UPDATE materials SET {assignments} WHERE id = :id", values)
            return material_id
        columns = ", ".join(MATERIAL_FIELDS)
        placeholders = ", ".join(f":{field}" for field in MATERIAL_FIELDS)
        cursor = connection.execute(f"INSERT INTO materials ({columns}) VALUES ({placeholders})", values)
        return cursor.lastrowid


def delete_material(material_id, database_path=None):
    with transaction(database_path) as connection:
        connection.execute("DELETE FROM materials WHERE id = ?", (material_id,))

