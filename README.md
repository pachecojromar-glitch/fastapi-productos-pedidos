# API de Productos y Pedidos — FastAPI + AWS EC2

API RESTful construida con **FastAPI** y **SQLModel**, con operaciones CRUD completas para dos entidades relacionadas: **Productos** y **Pedidos**. Pensada para desplegarse en una instancia **AWS EC2**, accesible públicamente por un puerto personalizado.

## Estructura del proyecto

```
fastapi-ec2-project/
├── app/
│   ├── main.py              # Punto de entrada de la app FastAPI
│   ├── database.py           # Configuración del motor y la sesión de SQLModel
│   ├── models.py              # Modelos de datos: Producto y Pedido
│   └── routers/
│       ├── productos.py      # Endpoints CRUD de Productos
│       └── pedidos.py        # Endpoints CRUD de Pedidos
├── requirements.txt
├── .gitignore
└── README.md
```

## Entidades

- **Producto**: `id`, `nombre`, `descripcion`, `precio`, `stock`
- **Pedido**: `id`, `cliente`, `cantidad`, `producto_id` (FK a Producto), `fecha_pedido`

Al crear un pedido, la API valida el stock disponible del producto y lo descuenta automáticamente. Al listar/consultar pedidos, se calcula el `total` (cantidad × precio) y se incluye el nombre del producto.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Mensaje de bienvenida |
| POST | `/productos/` | Crear producto |
| GET | `/productos/` | Listar productos |
| GET | `/productos/{id}` | Obtener un producto |
| PUT | `/productos/{id}` | Actualizar un producto |
| DELETE | `/productos/{id}` | Eliminar un producto |
| POST | `/pedidos/` | Crear pedido (valida y descuenta stock) |
| GET | `/pedidos/` | Listar pedidos (con total y nombre de producto) |
| GET | `/pedidos/{id}` | Obtener un pedido |
| PUT | `/pedidos/{id}` | Actualizar un pedido |
| DELETE | `/pedidos/{id}` | Eliminar un pedido |

Documentación interactiva automática en `/docs` (Swagger) y `/redoc`.

---

## 1. Ejecutar en local

```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Prueba en el navegador: `http://localhost:8000/docs`

---

## 2. Subir a GitHub

```bash
git init
git add .
git commit -m "API FastAPI con CRUD de Productos y Pedidos"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/<tu-repo>.git
git push -u origin main
```

---

## 3. Desplegar en AWS EC2

### 3.1 Crear la instancia
1. En la consola de AWS, crea una instancia EC2 (recomendado: **Ubuntu Server 22.04 LTS**, tipo `t2.micro` — elegible para capa gratuita).
2. Genera o usa un par de llaves (`.pem`) para conectarte por SSH.
3. En el **Security Group**, agrega una regla de entrada:
   - Tipo: **Custom TCP**
   - Puerto: **8000** (o el que elijas)
   - Origen: `0.0.0.0/0` (o restringe a tu IP si prefieres mayor seguridad)
   - Además deja abierto el puerto **22** (SSH) para tu IP.

### 3.2 Conectarte a la instancia
```bash
chmod 400 tu-llave.pem
ssh -i tu-llave.pem ubuntu@<ip-publica-ec2>
```

### 3.3 Instalar dependencias en la instancia
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git

# Instalar Node.js (necesario para pm2) y pm2
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g pm2
```

### 3.4 Clonar y preparar el proyecto
```bash
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.5 Ejecutar con pm2

pm2 corre procesos de Node.js de forma nativa, pero también puede administrar cualquier proceso (como Uvicorn) usando el modo `interpreter none` / script directo. Dos formas comunes:

**Opción A — pm2 ejecutando uvicorn directamente:**
```bash
pm2 start venv/bin/uvicorn --name fastapi-app -- app.main:app --host 0.0.0.0 --port 8000
```

**Opción B — con archivo de configuración `ecosystem.config.js`** (más robusto, reinicia automáticamente):
```javascript
module.exports = {
  apps: [{
    name: "fastapi-app",
    script: "venv/bin/uvicorn",
    args: "app.main:app --host 0.0.0.0 --port 8000",
    interpreter: "none",
    autorestart: true,
  }]
}
```
```bash
pm2 start ecosystem.config.js
```

### 3.6 Dejar pm2 corriendo tras reinicios
```bash
pm2 save
pm2 startup   # ejecuta el comando que te indique con sudo
```

### 3.7 Comandos útiles de pm2
```bash
pm2 list              # ver procesos activos
pm2 logs fastapi-app  # ver logs en vivo
pm2 restart fastapi-app
pm2 stop fastapi-app
```

---

## 4. Probar la API pública

Con la instancia corriendo y el puerto abierto en el Security Group:

```
http://<ip-publica-ec2>:8000/
http://<ip-publica-ec2>:8000/docs
http://<ip-publica-ec2>:8000/productos/
```

---

## 5. Entrega

- Link del repositorio (GitHub/GitLab) con todo el código subido.
- URL pública funcionando: `http://<ip-publica-ec2>:8000`
- Video explicando el desarrollo (código, despliegue y prueba en vivo).
