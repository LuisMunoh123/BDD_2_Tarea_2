# API con Litestar y PostgreSQL

API REST para gestión de biblioteca que permite administrar usuarios, libros, préstamos, categorías y reseñas. Incluye autenticación JWT y documentación interactiva (Swagger/Scalar).

## Tarea 2 - Cambios Realizados

### Descripción de Cambios y Decisiones de Diseño

En esta segunda iteración del proyecto se implementaron mejoras significativas al sistema de gestión de biblioteca:

**1. Sistema de Reseñas (Reviews)**
- Se agregó el modelo `Review` con relación many-to-one hacia `User` y `Book`
- Validación de rating entre 1-5 implementada en el controlador
- Campos: rating (int), comment (text opcional), review_date (fecha automática)
- DTOs configurados para incluir información de usuario y libro en las respuestas

**2. Sistema de Categorías**
- Implementación de relación many-to-many entre `Book` y `Category` usando tabla intermedia `book_categories`
- Endpoints para gestionar categorías y asignar/remover libros
- Búsqueda de libros por categoría disponible en el repositorio

**3. Gestión de Inventario (Stock)**
- Nuevo campo `stock` en libros con validación (> 0 en creación, >= 0 en actualización)
- Campos adicionales: `description`, `language` (código ISO 639-1), `publisher`
- Validación flexible de idiomas permitiendo todos los códigos ISO de 2 letras
- Métodos en repositorio para consultar libros disponibles y actualizar stock

**4. Información de Contacto de Usuarios**
- Campos agregados: `email` (único, validado con regex), `phone`, `address`, `is_active`
- Validación de formato de email en creación y actualización
- El campo `is_active` no puede ser modificado por el usuario (solo desde lógica interna)

**5. Sistema Avanzado de Préstamos**
- Nuevo modelo de estados: `LoanStatus` (ACTIVE, RETURNED, OVERDUE)
- Cálculo automático de `due_date` (loan_dt + 14 días) al crear préstamo
- Sistema de multas: $500 por día de retraso calculado automáticamente
- Endpoint de devolución que actualiza stock, calcula multas y cambia estado
- Endpoints adicionales: préstamos activos, vencidos, historial por usuario

**6. Consultas Avanzadas**
- Repositorio de libros con métodos: disponibles, por categoría, más reseñados, búsqueda por autor
- Repositorio de préstamos con métodos: activos, vencidos, historial de usuario, cálculo de multas
- Actualización automática de estado a OVERDUE para préstamos vencidos

**Decisiones de Diseño:**
- Se utilizó `server_default` en migraciones para compatibilidad con registros existentes
- Los DTOs excluyen relaciones en creación/actualización para evitar datos anidados no deseados
- El campo `email` en usuarios es nullable en BD pero validado como requerido en la aplicación
- Se implementó validación en controladores para lógica de negocio compleja
- Uso de `Decimal` para montos monetarios (multas) garantizando precisión

**Uso de IA:**
Durante el desarrollo se utilizó asistencia de IA (GitHub Copilot) principalmente para:
- Entender algunas instrucciones específicas de la tarea que no eran claras inicialmente
- Debugging de errores de SQLAlchemy y Alembic cuyo origen no era evidente
- Verificación de sintaxis correcta para migraciones complejas
- El código fue revisado y entendido completamente antes de su implementación

### Tabla de Cumplimiento de Requerimientos

| Requerimiento | Estado | Observaciones |
|--------------|--------|---------------|
| **1. Sistema de Reseñas** | Cumplido | |
| 1.1 Modelo Review con relaciones | Cumplido | Relaciones bidireccionales con User y Book |
| 1.2 Campo rating (1-5) | Cumplido | Validado en controlador |
| 1.3 Campo comment (opcional) | Cumplido | Tipo Text, nullable |
| 1.4 Fecha de reseña automática | Cumplido | Default datetime.today |
| 1.5 CRUD completo de reviews | Cumplido | GET, POST, PATCH, DELETE |
| 1.6 Validación rating en creación | Cumplido | HTTPException si fuera de rango |
| **2. Categorías y Relación M:N** | Cumplido | |
| 2.1 Modelo Category | Cumplido | name único, description opcional |
| 2.2 Relación M:N con Book | Cumplido | Tabla intermedia book_categories |
| 2.3 CRUD de categorías | Cumplido | Endpoints completos |
| 2.4 Asignar/remover libro a categoría | Cumplido | POST y DELETE implementados |
| 2.5 Listar libros por categoría | Cumplido | GET /categories/{id}/books |
| **3. Gestión de Inventario** | Cumplido | |
| 3.1 Campo stock en Book | Cumplido | Integer con default=1 |
| 3.2 Validación stock > 0 (creación) | Cumplido | Implementado en create_book |
| 3.3 Validación stock >= 0 (actualización) | Cumplido | Implementado en update_book |
| 3.4 Campos adicionales en Book | Cumplido | description, language, publisher |
| 3.5 Validación language (ISO 639-1) | Cumplido | Código de 2 letras |
| 3.6 Métodos repositorio | Cumplido | get_available_books, find_by_category |
| **4. Información de Contacto** | Cumplido | |
| 4.1 Campos en User | Cumplido | email, phone, address agregados |
| 4.2 Campo is_active | Cumplido | Boolean con default=True |
| 4.3 Validación formato email | Cumplido | Regex en controlador |
| 4.4 Protección is_active | Cumplido | Excluido de DTOs de usuario |
| **5. Sistema de Préstamos Avanzado** | Cumplido | |
| 5.1 Enum LoanStatus | Cumplido | ACTIVE, RETURNED, OVERDUE |
| 5.2 Campo due_date | Cumplido | Calculado automáticamente |
| 5.3 Campo fine_amount | Cumplido | Decimal(10,2) |
| 5.4 Cálculo de multas | Cumplido | $500 por día |
| 5.5 Endpoint devolución | Cumplido | POST /loans/{id}/return |
| 5.6 Actualización de stock | Cumplido | Incrementa en devolución |
| 5.7 Endpoint préstamos activos | Cumplido | GET /loans/active |
| 5.8 Endpoint préstamos vencidos | Cumplido | GET /loans/overdue |
| 5.9 Historial de usuario | Cumplido | GET /loans/user/{user_id} |
| 5.10 Solo actualizar status en PATCH | Cumplido | LoanUpdateDTO restrictivo |
| **6. Consultas Avanzadas** | Cumplido | |
| 6.1 Libros más reseñados | Cumplido | get_most_reviewed_books |
| 6.2 Búsqueda por autor | Cumplido | search_by_author |
| 6.3 Actualizar stock | Cumplido | update_stock con validaciones |
| **7. Migraciones** | Cumplido | |
| 7.1 Migración de reviews | Cumplido | Tabla con campos y relaciones |
| 7.2 Migración de categories | Cumplido | categories y book_categories |
| 7.3 Migración inventario | Cumplido | Campos en books con defaults |
| 7.4 Migración contacto usuarios | Cumplido | Campos en users |
| 7.5 Migración préstamos avanzados | Cumplido | Enum y campos en loans |

## Requisitos

- [uv](https://github.com/astral-sh/uv)
- PostgreSQL

## Inicio rápido

```bash
uv sync                      # Instala las dependencias
cp .env.example .env         # Configura las variables de entorno (ajusta según sea necesario)
uv run alembic upgrade head  # Aplica las migraciones de la base de datos
uv run litestar --reload     # Inicia el servidor de desarrollo
# Accede a http://localhost:8000/schema para ver la documentación de la API
```

## Variables de entorno

Crea un archivo `.env` basado en `.env.example`:

- `DEBUG`: Modo debug (True/False)
- `JWT_SECRET_KEY`: Clave secreta para tokens JWT
- `DATABASE_URL`: URL de conexión a PostgreSQL (formato: `postgresql+psycopg://usuario:contraseña@host:puerto/nombre_bd`). Recuerda crear la base de datos antes de ejecutar la aplicación con `createdb nombre_bd`.

## Estructura del proyecto

```
app/
├── controllers/     # Endpoints de la API (auth, book, loan, user)
├── dtos/            # Data Transfer Objects
├── repositories/    # Capa de acceso a datos
├── models.py        # Modelos SQLAlchemy (User, Book, Loan)
├── db.py            # Configuración de base de datos
├── config.py        # Configuración de la aplicación
└── security.py      # Autenticación y seguridad
migrations/          # Migraciones de Alembic
```

## Crear una copia privada de este repositorio

Para crear una copia privada de este repositorio en tu propia cuenta de GitHub, conservando el historial de commits, sigue estos pasos:

- Primero, crea un repositorio privado en tu cuenta de GitHub. Guarda la URL del nuevo repositorio.
- Luego, ejecuta los siguientes comandos en tu terminal, reemplazando `<URL_DE_TU_REPOSITORIO_PRIVADO>` con la URL de tu nuevo repositorio privado:

  ```bash
  git clone https://github.com/dialvarezs/learning-vue-bd2-2025 # Clona el repositorio
  cd learning-vue-bd2-2025
  git remote remove origin                                      # Elimina el origen remoto existente
  git remote add origin <URL_DE_TU_REPOSITORIO_PRIVADO>         # Agrega el nuevo origen remoto
  git push -u origin main                                       # Sube la rama principal al
  ```
