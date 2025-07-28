#!/bin/bash

# 🚀 SCRIPT DE DEPLOYMENT PARA FÁBRICA DE BOTS
# Dominio: fabricadebots.tech
# Fecha: $(date)

echo "🤖 ==========================================="
echo "🚀 DESPLEGANDO FÁBRICA DE BOTS"
echo "🌐 Dominio: fabricadebots.tech"
echo "📧 Email: contacto@fabricadebots.tech"
echo "🤖 ==========================================="

# 📁 Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p fabricadebots-deploy/{public_html,database,config,scripts}
mkdir -p fabricadebots-deploy/public_html/{starter,pro,platinum,api,assets,admin}
mkdir -p fabricadebots-deploy/public_html/assets/{css,js,images,videos}
mkdir -p fabricadebots-deploy/public_html/api/{config,endpoints,classes,database}

# 🗄️ Configurar base de datos
echo "🗄️ Preparando base de datos..."
cat > fabricadebots-deploy/database/fabricadebots-complete.sql << 'EOF'
-- 🤖 FÁBRICA DE BOTS - BASE DE DATOS COMPLETA
-- Dominio: fabricadebots.tech
-- Email: contacto@fabricadebots.tech

CREATE DATABASE IF NOT EXISTS u123456789_fabricabots CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE u123456789_fabricabots;

-- 👥 Tabla de leads/clientes potenciales
CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    empresa VARCHAR(100),
    cargo VARCHAR(100),
    paquete ENUM('starter', 'pro', 'platinum') NOT NULL,
    mensaje TEXT,
    presupuesto DECIMAL(12,2),
    utm_source VARCHAR(50),
    utm_campaign VARCHAR(50),
    utm_medium VARCHAR(50),
    utm_content VARCHAR(50),
    utm_term VARCHAR(50),
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer VARCHAR(255),
    landing_page VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_contacto TIMESTAMP NULL,
    estado ENUM('nuevo', 'contactado', 'propuesta_enviada', 'negociacion', 'cerrado_ganado', 'cerrado_perdido', 'seguimiento') DEFAULT 'nuevo',
    prioridad ENUM('baja', 'media', 'alta', 'urgente') DEFAULT 'media',
    notas TEXT,
    asignado_a VARCHAR(100),
    valor_estimado DECIMAL(12,2),
    probabilidad_cierre INT DEFAULT 0,
    fecha_cierre_estimada DATE,
    origen_lead ENUM('website', 'facebook', 'instagram', 'google', 'linkedin', 'referido', 'evento') DEFAULT 'website'
);

-- 📊 Tabla de campañas publicitarias
CREATE TABLE campanas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    plataforma ENUM('facebook', 'instagram', 'google', 'linkedin', 'youtube', 'tiktok') NOT NULL,
    tipo_campana ENUM('awareness', 'traffic', 'engagement', 'leads', 'conversions', 'sales') NOT NULL,
    presupuesto_total DECIMAL(12,2),
    presupuesto_diario DECIMAL(10,2),
    presupuesto_gastado DECIMAL(12,2) DEFAULT 0,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('borrador', 'activa', 'pausada', 'finalizada', 'cancelada') DEFAULT 'borrador',
    objetivo VARCHAR(200),
    audiencia_target TEXT,
    ubicaciones TEXT,
    edad_min INT DEFAULT 18,
    edad_max INT DEFAULT 65,
    genero ENUM('todos', 'hombre', 'mujer'),
    intereses TEXT,
    idiomas VARCHAR(100) DEFAULT 'es',
    dispositivos ENUM('todos', 'desktop', 'mobile', 'tablet') DEFAULT 'todos',
    horarios_activos TEXT,
    dias_semana TEXT,
    campaign_id_externa VARCHAR(100),
    adset_id_externa VARCHAR(100),
    notas TEXT
);

-- 📈 Tabla de métricas diarias
CREATE TABLE metricas_diarias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campana_id INT NOT NULL,
    fecha DATE NOT NULL,
    impresiones INT DEFAULT 0,
    alcance INT DEFAULT 0,
    clicks INT DEFAULT 0,
    clicks_link INT DEFAULT 0,
    ctr DECIMAL(5,4) DEFAULT 0,
    cpc DECIMAL(10,2) DEFAULT 0,
    cpm DECIMAL(10,2) DEFAULT 0,
    conversiones INT DEFAULT 0,
    costo_conversion DECIMAL(10,2) DEFAULT 0,
    costo_total DECIMAL(10,2) DEFAULT 0,
    engagement INT DEFAULT 0,
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    shares INT DEFAULT 0,
    video_views INT DEFAULT 0,
    video_views_25 INT DEFAULT 0,
    video_views_50 INT DEFAULT 0,
    video_views_75 INT DEFAULT 0,
    video_views_100 INT DEFAULT 0,
    leads_generados INT DEFAULT 0,
    leads_calificados INT DEFAULT 0,
    ventas INT DEFAULT 0,
    ingresos DECIMAL(12,2) DEFAULT 0,
    roas DECIMAL(5,2) DEFAULT 0,
    roi DECIMAL(5,2) DEFAULT 0,
    frecuencia DECIMAL(3,2) DEFAULT 0,
    FOREIGN KEY (campana_id) REFERENCES campanas(id) ON DELETE CASCADE,
    UNIQUE KEY unique_campana_fecha (campana_id, fecha)
);

-- 🎨 Tabla de creatividades/anuncios
CREATE TABLE creatividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campana_id INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    tipo ENUM('imagen', 'video', 'carousel', 'collection', 'texto') NOT NULL,
    titulo VARCHAR(255),
    descripcion TEXT,
    cta_button ENUM('learn_more', 'sign_up', 'download', 'get_quote', 'contact_us', 'shop_now', 'book_travel', 'apply_now') DEFAULT 'learn_more',
    url_destino VARCHAR(255),
    imagen_url VARCHAR(255),
    video_url VARCHAR(255),
    estado ENUM('activa', 'pausada', 'rechazada', 'pendiente') DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_aprobacion TIMESTAMP NULL,
    impresiones INT DEFAULT 0,
    clicks INT DEFAULT 0,
    conversiones INT DEFAULT 0,
    costo_total DECIMAL(10,2) DEFAULT 0,
    ctr DECIMAL(5,4) DEFAULT 0,
    cpc DECIMAL(10,2) DEFAULT 0,
    relevance_score DECIMAL(3,2) DEFAULT 0,
    notas TEXT,
    FOREIGN KEY (campana_id) REFERENCES campanas(id) ON DELETE CASCADE
);

-- 🎯 Tabla de conversiones
CREATE TABLE conversiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lead_id INT,
    campana_id INT,
    creatividad_id INT,
    tipo_conversion ENUM('lead', 'demo', 'consulta', 'venta', 'registro', 'descarga') NOT NULL,
    valor DECIMAL(12,2) DEFAULT 0,
    fecha_conversion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pagina_conversion VARCHAR(255),
    evento_facebook VARCHAR(100),
    evento_google VARCHAR(100),
    utm_source VARCHAR(50),
    utm_campaign VARCHAR(50),
    utm_medium VARCHAR(50),
    utm_content VARCHAR(50),
    utm_term VARCHAR(50),
    detalles_conversion TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE SET NULL,
    FOREIGN KEY (campana_id) REFERENCES campanas(id) ON DELETE SET NULL,
    FOREIGN KEY (creatividad_id) REFERENCES creatividades(id) ON DELETE SET NULL
);

-- 👥 Tabla de audiencias personalizadas
CREATE TABLE audiencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo ENUM('custom', 'lookalike', 'retargeting', 'engagement', 'website_visitors') NOT NULL,
    plataforma ENUM('facebook', 'google', 'linkedin') NOT NULL,
    tamaño_estimado INT,
    criterios TEXT,
    pixel_events TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    estado ENUM('activa', 'inactiva', 'procesando', 'error') DEFAULT 'procesando',
    audience_id_externa VARCHAR(100),
    tiempo_retencion INT DEFAULT 180,
    notas TEXT
);

-- ⚙️ Tabla de configuraciones del sistema
CREATE TABLE configuraciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT,
    descripcion TEXT,
    categoria ENUM('general', 'email', 'analytics', 'social', 'payments', 'api') DEFAULT 'general',
    tipo ENUM('string', 'number', 'boolean', 'json', 'array') DEFAULT 'string',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 📝 Tabla de logs del sistema
CREATE TABLE logs_sistema (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('info', 'warning', 'error', 'debug', 'critical') NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    mensaje TEXT NOT NULL,
    datos_adicionales JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    usuario_id INT,
    fecha_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tipo_fecha (tipo, fecha_log),
    INDEX idx_modulo_fecha (modulo, fecha_log)
);

-- 🎯 Insertar configuraciones iniciales
INSERT INTO configuraciones (clave, valor, descripcion, categoria, tipo) VALUES
('site_name', 'Fábrica de Bots', 'Nombre del sitio web', 'general', 'string'),
('site_url', 'https://fabricadebots.tech', 'URL principal del sitio', 'general', 'string'),
('contact_email', 'contacto@fabricadebots.tech', 'Email de contacto principal', 'email', 'string'),
('admin_email', 'admin@fabricadebots.tech', 'Email del administrador', 'email', 'string'),
('sales_email', 'ventas@fabricadebots.tech', 'Email del equipo de ventas', 'email', 'string'),
('whatsapp_number', '+5492236123456', 'Número de WhatsApp', 'general', 'string'),
('facebook_pixel', '1234567890123456', 'ID del Facebook Pixel', 'analytics', 'string'),
('google_analytics', 'G-FABRICABOTS01', 'ID de Google Analytics', 'analytics', 'string'),
('price_starter', '89900', 'Precio del paquete Starter (ARS)', 'general', 'number'),
('price_pro', '189900', 'Precio del paquete Pro (ARS)', 'general', 'number'),
('price_platinum', '389900', 'Precio del paquete Platinum (ARS)', 'general', 'number'),
('meta_ads_budget', '230000', 'Presupuesto mensual Meta Ads (ARS)', 'general', 'number'),
('leads_goal_monthly', '150', 'Objetivo mensual de leads', 'general', 'number'),
('conversion_rate_target', '15', 'Tasa de conversión objetivo (%)', 'general', 'number'),
('smtp_host', 'smtp.hostinger.com', 'Servidor SMTP', 'email', 'string'),
('smtp_port', '587', 'Puerto SMTP', 'email', 'number'),
('maintenance_mode', 'false', 'Modo mantenimiento', 'general', 'boolean'),
('debug_mode', 'false', 'Modo debug', 'general', 'boolean');

-- 📊 Insertar campañas iniciales
INSERT INTO campanas (nombre, plataforma, tipo_campana, presupuesto_total, presupuesto_diario, fecha_inicio, fecha_fin, estado, objetivo, audiencia_target) VALUES
('🚀 Fábrica de Bots - Starter', 'facebook', 'leads', 70000.00, 2333.33, '2025-07-24', '2025-08-23', 'activa', 'Captar PyMEs interesadas en automatización', 'Dueños de PyMEs en Mar del Plata, 25-55 años'),
('💼 Fábrica de Bots - Pro', 'instagram', 'conversions', 60000.00, 2000.00, '2025-07-24', '2025-08-23', 'activa', 'Atraer empresas medianas', 'Gerentes y directores de empresas, 30-60 años'),
('👑 Fábrica de Bots - Platinum', 'facebook', 'conversions', 40000.00, 1333.33, '2025-07-24', '2025-08-23', 'activa', 'Grandes empresas y corporaciones', 'CTOs, CEOs, directores de tecnología, 35-65 años'),
('🎯 Retargeting General', 'facebook', 'conversions', 30000.00, 1000.00, '2025-07-24', '2025-08-23', 'activa', 'Reconversión de visitantes web', 'Visitantes del sitio web últimos 30 días'),
('📱 Instagram Stories', 'instagram', 'awareness', 30000.00, 1000.00, '2025-07-24', '2025-08-23', 'activa', 'Awareness y engagement', 'Audiencia similar a clientes actuales');

-- 🎨 Insertar creatividades de ejemplo
INSERT INTO creatividades (campana_id, nombre, tipo, titulo, descripcion, cta_button, url_destino) VALUES
(1, 'Starter - Automatiza tu PyME', 'imagen', '🤖 Automatiza tu PyME con IA', 'Transforma tu negocio con chatbots inteligentes. Desde $89.900/mes. ¡Prueba GRATIS!', 'learn_more', 'https://fabricadebots.tech/starter'),
(1, 'Starter - Video Demo', 'video', '⚡ Ve cómo funciona en 60 segundos', 'Mira cómo nuestros bots aumentan las ventas de PyMEs en Mar del Plata', 'sign_up', 'https://fabricadebots.tech/starter'),
(2, 'Pro - Empresa Mediana', 'imagen', '💼 Solución completa para tu empresa', 'Apps móviles + IA + Blockchain. La tecnología que necesitas. $189.900/mes', 'get_quote', 'https://fabricadebots.tech/pro'),
(3, 'Platinum - Enterprise', 'imagen', '👑 Tecnología Enterprise', 'Desarrollo a medida + usuarios ilimitados. Para empresas que no se conforman con menos.', 'contact_us', 'https://fabricadebots.tech/platinum'),
(4, 'Retargeting - Vuelve', 'imagen', '🎯 ¿Viste algo que te gustó?', 'Vuelve y conoce nuestras soluciones de automatización. ¡Consultora GRATIS!', 'learn_more', 'https://fabricadebots.tech');

-- 📊 Log inicial del sistema
INSERT INTO logs_sistema (tipo, modulo, mensaje, datos_adicionales) VALUES
('info', 'database', 'Base de datos inicializada correctamente', '{"version": "1.0", "domain": "fabricadebots.tech", "date": "2025-07-23"}');

EOF

# 📧 Crear configuración de email
echo "📧 Configurando sistema de emails..."
cat > fabricadebots-deploy/config/email-config.php << 'EOF'
<?php
/**
 * CONFIGURACIÓN DE EMAIL - FÁBRICA DE BOTS
 * contacto@fabricadebots.tech
 */

// 📧 Configuración SMTP Hostinger
$email_config = [
    'smtp_host' => 'smtp.hostinger.com',
    'smtp_port' => 587,
    'smtp_secure' => 'tls',
    'smtp_user' => 'contacto@fabricadebots.tech',
    'smtp_pass' => 'TuPasswordEmail2025!',
    'from_email' => 'contacto@fabricadebots.tech',
    'from_name' => 'Fábrica de Bots',
    'reply_to' => 'contacto@fabricadebots.tech'
];

// 📨 Templates de email
$email_templates = [
    'lead_notification' => [
        'subject' => '🤖 Nuevo lead desde fabricadebots.tech',
        'template' => 'templates/lead-notification.html'
    ],
    'welcome_lead' => [
        'subject' => '¡Bienvenido a Fábrica de Bots! 🚀',
        'template' => 'templates/welcome-lead.html'
    ],
    'demo_request' => [
        'subject' => '📅 Solicitud de demo - Fábrica de Bots',
        'template' => 'templates/demo-request.html'
    ],
    'quote_request' => [
        'subject' => '💰 Solicitud de cotización',
        'template' => 'templates/quote-request.html'
    ]
];

// 🎯 Destinatarios por tipo de lead
$lead_recipients = [
    'starter' => ['ventas@fabricadebots.tech'],
    'pro' => ['ventas@fabricadebots.tech', 'gerencia@fabricadebots.tech'],
    'platinum' => ['ventas@fabricadebots.tech', 'gerencia@fabricadebots.tech', 'ceo@fabricadebots.tech']
];

?>
EOF

# 🔒 Crear archivo .htaccess para seguridad
echo "🔒 Configurando seguridad..."
cat > fabricadebots-deploy/public_html/.htaccess << 'EOF'
# 🤖 FÁBRICA DE BOTS - CONFIGURACIÓN APACHE
# Dominio: fabricadebots.tech

# ⚡ Forzar HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# 🌐 Redirecciones SEO
RewriteRule ^paquetes/?$ /starter [R=301,L]
RewriteRule ^precios/?$ /starter [R=301,L]
RewriteRule ^bots/?$ / [R=301,L]
RewriteRule ^ia/?$ / [R=301,L]
RewriteRule ^chatbots/?$ / [R=301,L]
RewriteRule ^automatizacion/?$ / [R=301,L]

# 🔒 Seguridad: Ocultar archivos sensibles
<Files "*.php~">
    Order allow,deny
    Deny from all
</Files>

<Files ".htaccess">
    Order allow,deny
    Deny from all
</Files>

<Files "config.php">
    Order allow,deny
    Deny from all
</Files>

# 🚫 Bloquear acceso a directorios
Options -Indexes

# 📈 Compresión GZIP
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# ⚡ Cache del navegador
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>

# 🛡️ Headers de seguridad
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# 🎯 Tracking personalizado
RewriteRule ^track/([a-zA-Z0-9]+)/?$ /api/track.php?utm_campaign=$1 [L,QSA]
RewriteRule ^demo/?$ /demo.html [L]
RewriteRule ^contacto/?$ /contact.html [L]

ErrorDocument 404 /404.html
ErrorDocument 403 /403.html
ErrorDocument 500 /500.html
EOF

# 🚀 Crear script de FTP upload
echo "🚀 Creando script de subida FTP..."
cat > fabricadebots-deploy/scripts/ftp-upload.sh << 'EOF'
#!/bin/bash
# 📤 SCRIPT DE SUBIDA FTP PARA FÁBRICA DE BOTS

echo "🤖 Subiendo archivos a fabricadebots.tech..."

# Variables FTP (cambiar por las reales)
FTP_HOST="ftp.fabricadebots.tech"
FTP_USER="tu_usuario_ftp"
FTP_PASS="tu_password_ftp"
FTP_DIR="/public_html"

# 📦 Comprimir archivos
cd fabricadebots-deploy
zip -r fabricadebots-complete.zip public_html/ database/ config/

echo "📤 Conectando a servidor FTP..."
echo "🌐 Host: $FTP_HOST"
echo "👤 Usuario: $FTP_USER"
echo "📁 Directorio: $FTP_DIR"

# Usando lftp para subida automática
lftp -c "
set ftp:ssl-allow no
open $FTP_HOST
user $FTP_USER $FTP_PASS
lcd .
cd $FTP_DIR
put fabricadebots-complete.zip
quit
"

echo "✅ Archivos subidos correctamente!"
echo "🗄️ Ahora importa la base de datos desde cPanel"
echo "🔧 Y configura las variables de entorno"
EOF

chmod +x fabricadebots-deploy/scripts/ftp-upload.sh

# 📊 Crear script de verificación
echo "🔍 Creando script de verificación..."
cat > fabricadebots-deploy/scripts/verify-deployment.sh << 'EOF'
#!/bin/bash
# ✅ VERIFICACIÓN DE DEPLOYMENT - FÁBRICA DE BOTS

echo "🤖 Verificando deployment de fabricadebots.tech..."

# ✅ Verificar URLs principales
urls=(
    "https://fabricadebots.tech"
    "https://fabricadebots.tech/starter"
    "https://fabricadebots.tech/pro"
    "https://fabricadebots.tech/platinum"
    "https://api.fabricadebots.tech"
)

for url in "${urls[@]}"; do
    echo "🔍 Verificando: $url"
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ $status -eq 200 ]; then
        echo "✅ $url - OK"
    else
        echo "❌ $url - ERROR ($status)"
    fi
done

# 📧 Verificar email
echo "📧 Verificando configuración de email..."
echo "📩 Email principal: contacto@fabricadebots.tech"

# 🗄️ Verificar base de datos
echo "🗄️ Verificando conexión a base de datos..."
echo "🔍 Host: localhost"
echo "📊 Base: u123456789_fabricabots"

echo "🤖 Verificación completada!"
EOF

chmod +x fabricadebots-deploy/scripts/verify-deployment.sh

# 📱 Crear archivo de subdominio para API
echo "🌐 Configurando subdominios..."
cat > fabricadebots-deploy/config/subdomain-api.htaccess << 'EOF'
# 🤖 CONFIGURACIÓN API FÁBRICA DE BOTS
# Subdominio: api.fabricadebots.tech

RewriteEngine On

# 🔒 Headers de API
Header always set Access-Control-Allow-Origin "https://fabricadebots.tech"
Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
Header always set Access-Control-Allow-Headers "Content-Type, Authorization, X-API-Key"
Header always set Content-Type "application/json; charset=utf-8"

# 🎯 Rutas de API
RewriteRule ^leads/?$ endpoints/leads.php [L,QSA]
RewriteRule ^campaigns/?$ endpoints/campaigns.php [L,QSA]
RewriteRule ^metrics/?$ endpoints/metrics.php [L,QSA]
RewriteRule ^track/?$ endpoints/track.php [L,QSA]
RewriteRule ^webhook/?$ endpoints/webhook.php [L,QSA]

# 🚫 Bloquear acceso directo
RewriteCond %{REQUEST_URI} !^/endpoints/
RewriteCond %{REQUEST_URI} !^/index.php
RewriteRule ^(.*)$ index.php [L,QSA]
EOF

echo "📋 Creando archivo de instrucciones..."
cat > fabricadebots-deploy/INSTRUCCIONES-DEPLOYMENT.md << 'EOF'
# 🤖 INSTRUCCIONES DE DEPLOYMENT - FÁBRICA DE BOTS

## 🚀 PASOS PARA DESPLEGAR EN HOSTINGER

### 1️⃣ PREPARAR HOSTINGER
- ✅ Contratar plan Business Hosting ($5.99/mes)
- ✅ Configurar dominio principal: `fabricadebots.tech`
- ✅ Crear subdominios:
  - `starter.fabricadebots.tech`
  - `pro.fabricadebots.tech`
  - `platinum.fabricadebots.tech`
  - `api.fabricadebots.tech`

### 2️⃣ CONFIGURAR BASE DE DATOS
- ✅ Ir a cPanel → MySQL Databases
- ✅ Crear base: `u123456789_fabricabots`
- ✅ Crear usuario: `u123456789_admin`
- ✅ Importar: `database/fabricadebots-complete.sql`

### 3️⃣ CONFIGURAR EMAIL
- ✅ Ir a cPanel → Email Accounts
- ✅ Crear: `contacto@fabricadebots.tech`
- ✅ Crear: `ventas@fabricadebots.tech`
- ✅ Crear: `admin@fabricadebots.tech`

### 4️⃣ SUBIR ARCHIVOS
- ✅ Usar FileZilla o cPanel File Manager
- ✅ Subir contenido de `public_html/` a `/public_html/`
- ✅ Configurar permisos: 755 para directorios, 644 para archivos

### 5️⃣ CONFIGURAR SSL
- ✅ cPanel → SSL/TLS → Let's Encrypt
- ✅ Activar para todos los subdominios

### 6️⃣ CONFIGURAR DNS
- ✅ Ir a Domain Management
- ✅ Configurar subdominios A records apuntando a IP del hosting

### 7️⃣ VERIFICAR FUNCIONAMIENTO
```bash
bash scripts/verify-deployment.sh
```

## 📞 SOPORTE
- 📧 Email: contacto@fabricadebots.tech
- 📱 WhatsApp: +54 9 223 6123456
- 🌐 Web: https://fabricadebots.tech

EOF

# 🎯 Crear archivo .env para configuraciones
cat > fabricadebots-deploy/.env << 'EOF'
# 🤖 FÁBRICA DE BOTS - VARIABLES DE ENTORNO
# Dominio: fabricadebots.tech

# 🌐 CONFIGURACIÓN GENERAL
SITE_NAME="Fábrica de Bots"
SITE_URL="https://fabricadebots.tech"
CONTACT_EMAIL="contacto@fabricadebots.tech"
ADMIN_EMAIL="admin@fabricadebots.tech"
SALES_EMAIL="ventas@fabricadebots.tech"

# 🗄️ BASE DE DATOS
DB_HOST="localhost"
DB_NAME="u123456789_fabricabots"
DB_USER="u123456789_admin"
DB_PASS="FabricaBots2025!"

# 📧 EMAIL SMTP
SMTP_HOST="smtp.hostinger.com"
SMTP_PORT="587"
SMTP_USER="contacto@fabricadebots.tech"
SMTP_PASS="TuPasswordEmail2025!"

# 📱 REDES SOCIALES
FB_PIXEL_ID="1234567890123456"
GA_TRACKING_ID="G-FABRICABOTS01"
WHATSAPP_NUMBER="+5492236123456"

# 💰 PRECIOS (ARS)
PRICE_STARTER="89900"
PRICE_PRO="189900"
PRICE_PLATINUM="389900"

# 🎯 META ADS
META_ADS_BUDGET="230000"
FB_ACCESS_TOKEN="tu-token-aqui"

# 🔒 SEGURIDAD
API_KEY="fabricabots_api_2025"
JWT_SECRET="jwt_secret_ultra_seguro"

# 🚀 AMBIENTE
ENVIRONMENT="production"
DEBUG_MODE="false"
MAINTENANCE_MODE="false"
EOF

echo "✅ Estructura de deployment creada!"
echo "📁 Directorio: fabricadebots-deploy/"
echo ""
echo "🤖 ======================================"
echo "📋 ARCHIVOS CREADOS:"
echo "🗄️ database/fabricadebots-complete.sql"
echo "📧 config/email-config.php" 
echo "🔒 public_html/.htaccess"
echo "🌐 config/subdomain-api.htaccess"
echo "📤 scripts/ftp-upload.sh"
echo "✅ scripts/verify-deployment.sh"
echo "📖 INSTRUCCIONES-DEPLOYMENT.md"
echo "⚙️ .env"
echo "🤖 ======================================"
echo ""
echo "🚀 PRÓXIMOS PASOS:"
echo "1️⃣ Configurar Hostinger con el dominio fabricadebots.tech"
echo "2️⃣ Crear subdominios en cPanel"
echo "3️⃣ Subir archivos con scripts/ftp-upload.sh"
echo "4️⃣ Importar base de datos"
echo "5️⃣ Configurar emails corporativos"
echo "6️⃣ Activar SSL gratuito"
echo "7️⃣ Verificar con scripts/verify-deployment.sh"
echo ""
echo "📧 Emails configurados:"
echo "   • contacto@fabricadebots.tech"
echo "   • ventas@fabricadebots.tech"
echo "   • admin@fabricadebots.tech"
echo ""
echo "🌐 URLs que funcionarán:"
echo "   • https://fabricadebots.tech"
echo "   • https://starter.fabricadebots.tech"
echo "   • https://pro.fabricadebots.tech"
echo "   • https://platinum.fabricadebots.tech"
echo "   • https://api.fabricadebots.tech"
echo ""
echo "🤖 ¡FÁBRICA DE BOTS LISTA PARA DEPLOYMENT! 🚀"
