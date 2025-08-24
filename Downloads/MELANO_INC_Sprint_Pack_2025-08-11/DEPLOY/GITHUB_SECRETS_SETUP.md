# Configuración de Secretos GitHub - Melano Repository

## 🔐 Secretos Requeridos para CI/CD

### Paso 1: Acceder a GitHub Secrets
1. Ve a tu repositorio GitHub
2. Click en **Settings** (Configuración)
3. En el menú lateral, click en **Secrets and variables** > **Actions**
4. Click en **New repository secret**

### Paso 2: Configurar Secretos Docker Hub

#### DOCKERHUB_USERNAME
- **Name**: `DOCKERHUB_USERNAME`
- **Secret**: `brunomelano`

#### DOCKERHUB_TOKEN
- **Name**: `DOCKERHUB_TOKEN`
- **Secret**: `dckr_pat_sAd9T22tqTpt6m3Nhgz1KomBZOg`

### Paso 3: Secretos Opcionales (Recomendados)

#### Para Firma de Imágenes (Cosign)
Si quieres firmar las imágenes Docker para mayor seguridad:

**COSIGN_KEY** (Opcional)
- Genera una clave privada Cosign
- Guarda el contenido completo de la clave privada

**COSIGN_PASSWORD** (Opcional)
- Password para la clave privada Cosign

### Paso 4: Verificar Configuración

Una vez configurados los secretos, el workflow `.github/workflows/docker-publish.yml` automáticamente:

1. **Detectará los secretos** disponibles
2. **Construirá la imagen** Docker multi-arquitectura
3. **Publicará en Docker Hub** como `brunomelano/melano-api`
4. **Creará tags** automáticos: `latest`, hash del commit, y versión si es un tag

### 🚀 Activar el Workflow

El workflow se activa automáticamente cuando:
- Haces push a `main` o `MAIN`
- Creas un tag con formato `v*.*.*` (ej: `v1.0.0`)

### 📋 Comandos para Activar

```bash
# Crear y push un tag para activar el build
git tag v1.0.0
git push origin v1.0.0

# O usar el script automatizado
./tag_version.sh v1.0.0 "Initial production release"
```

### ✅ Verificación

Después del build exitoso, podrás:

```bash
# Descargar la imagen publicada
docker pull brunomelano/melano-api:latest
docker pull brunomelano/melano-api:v1.0.0

# Verificar en Docker Hub
# Ve a: https://hub.docker.com/r/brunomelano/melano-api
```

### 🔧 Troubleshooting

**Si el workflow falla:**
1. Verifica que los secretos estén correctamente configurados
2. Revisa los logs en GitHub Actions
3. Confirma que el token Docker Hub tenga permisos `write:packages`

**Logs del workflow:**
- Ve a tu repo > Actions > Selecciona el workflow run
- Revisa cada step para identificar errores

### 📱 Notificaciones

El workflow enviará notificaciones sobre:
- ✅ Build exitoso
- ❌ Errores en el build
- 📦 Imagen publicada en Docker Hub
- 🔒 Firma de imagen (si Cosign está configurado)

## 🎯 Próximo Paso

Una vez configurados los secretos, procede con:
```bash
./tag_version.sh v1.0.0 "Initial production release"
