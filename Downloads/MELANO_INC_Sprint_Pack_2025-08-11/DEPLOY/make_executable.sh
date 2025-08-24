#!/bin/bash

# Script para hacer ejecutables todos los scripts necesarios
echo "🔧 Configurando permisos de ejecución..."

# Scripts principales
chmod +x tag_version.sh
chmod +x DEPLOY/deploy_remote.sh
chmod +x DEPLOY/rollback_remote.sh

# Verificar que los archivos existen y son ejecutables
scripts=(
    "tag_version.sh"
    "DEPLOY/deploy_remote.sh" 
    "DEPLOY/rollback_remote.sh"
)

echo "✅ Verificando permisos:"
for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo "   ✅ $script - Ejecutable"
        else
            echo "   ❌ $script - No ejecutable"
            chmod +x "$script"
            echo "   🔧 $script - Permisos corregidos"
        fi
    else
        echo "   ⚠️  $script - Archivo no encontrado"
    fi
done

echo ""
echo "🎯 Scripts listos para usar:"
echo "   ./tag_version.sh v1.0.0 'Initial release'"
echo "   bash DEPLOY/deploy_remote.sh -h 89.116.115.185 -u u846600237"
echo "   bash DEPLOY/rollback_remote.sh backup.tar.gz -h 89.116.115.185"
echo ""
echo "✅ Configuración de permisos completada!"
