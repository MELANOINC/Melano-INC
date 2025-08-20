#!/bin/bash
set -euo pipefail

# Script para crear tags de versión y activar CI/CD automático
# Uso: ./tag_version.sh v1.0.0 "Descripción del release"

VERSION=${1:-}
MESSAGE=${2:-"Release $VERSION"}

if [ -z "$VERSION" ]; then
    echo "❌ Error: Versión requerida"
    echo "Uso: $0 <version> [mensaje]"
    echo "Ejemplo: $0 v1.0.0 'Initial production release'"
    exit 1
fi

# Validar formato de versión
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "❌ Error: Formato de versión inválido"
    echo "Formato esperado: vX.Y.Z (ej: v1.0.0)"
    exit 1
fi

echo "🏷️  Creando tag de versión: $VERSION"
echo "📝 Mensaje: $MESSAGE"

# Verificar que estamos en un repo git
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "❌ Error: No estás en un repositorio Git"
    exit 1
fi

# Verificar que no hay cambios sin commit
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Advertencia: Hay cambios sin commit"
    echo "¿Quieres continuar? (y/N)"
    read -r response
    if [[ ! $response =~ ^[Yy]$ ]]; then
        echo "❌ Cancelado"
        exit 1
    fi
fi

# Verificar que el tag no existe
if git tag -l | grep -q "^$VERSION$"; then
    echo "❌ Error: El tag $VERSION ya existe"
    echo "Tags existentes:"
    git tag -l | sort -V
    exit 1
fi

# Crear el tag
echo "🔖 Creando tag..."
git tag -a "$VERSION" -m "$MESSAGE"

# Push del tag
echo "📤 Enviando tag al repositorio remoto..."
git push origin "$VERSION"

echo "✅ Tag $VERSION creado y enviado exitosamente!"
echo ""
echo "🚀 Esto activará automáticamente:"
echo "   • GitHub Actions workflow"
echo "   • Build de imagen Docker multi-arquitectura"
echo "   • Publicación en Docker Hub: brunomelano/melano-api:$VERSION"
echo "   • Publicación en Docker Hub: brunomelano/melano-api:latest"
echo ""
echo "📊 Monitorear progreso en:"
echo "   • GitHub Actions: https://github.com/tu-usuario/tu-repo/actions"
echo "   • Docker Hub: https://hub.docker.com/r/brunomelano/melano-api"
echo ""
echo "⏱️  El build tomará aproximadamente 5-10 minutos"

# Mostrar información adicional
echo ""
echo "📋 Información del release:"
echo "   Versión: $VERSION"
echo "   Commit: $(git rev-parse --short HEAD)"
echo "   Rama: $(git branch --show-current)"
echo "   Fecha: $(date)"
echo ""
echo "🔍 Para verificar cuando esté listo:"
echo "   docker pull brunomelano/melano-api:$VERSION"
echo "   docker pull brunomelano/melano-api:latest"
