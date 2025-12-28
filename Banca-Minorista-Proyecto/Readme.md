# 🏦 Pipeline de Seguimiento Minorista Bancario

## 📋 Descripción del Proyecto

Pipeline de Ingeniería de Datos diseñado para automatizar el seguimiento de métricas clave del negocio minorista bancario, desde la ingesta de datos hasta la generación de reportes ejecutivos.

**Contexto:** Proyecto orientado al rol de **Analista de Datos - Seguimiento Minorista** en BBVA, donde se requiere seguimiento de KPIs, reporting periódico y trabajo con SQL avanzado.

## 🎯 Objetivos

- ✅ Consolidar datos minoristas de múltiples fuentes
- ✅ Automatizar cálculo de KPIs bancarios
- ✅ Garantizar calidad y trazabilidad de datos
- ✅ Generar reportes automáticos para stakeholders
- ✅ Detectar desvíos y alertar proactivamente

## 🏗️ Arquitectura

[Ver diagrama interactivo completo](./img/arquitectura.png)

**Flujo general:**
```
Fuentes → n8n (ETL) → Staging → Transformación → Data Warehouse → Power BI
```

## 🧰 Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Orquestación** | n8n |
| **Base de Datos** | PostgreSQL |
| **Transformaciones** | Python (Pandas) |
| **Visualización** | Power BI |
| **Control de versiones** | Git/GitHub |

## 📊 KPIs Implementados

1. **Clientes activos** - Variación mensual
2. **Volumen operativo** - Por sucursal, canal y región
3. **Ticket promedio** - Segmentado por producto
4. **Productos por cliente** - Cross-selling
5. **Ranking de sucursales** - Performance comparativa
6. **Variación intermensual** - Tendencias y desvíos

## 🚀 Instalación y Configuración

[Instrucciones detalladas en docs/instalacion.md]

## 📈 Resultados

- ⏱️ Reducción del 80% en tiempo de preparación de reportes
- 🎯 Alertas automáticas ante desvíos críticos
- 📊 Dashboard actualizado diariamente
- ✅ Trazabilidad completa del pipeline

## 🗂️ Estructura del Repositorio
```
├── data/          # Datos simulados
├── n8n/           # Workflows
├── sql/           # Scripts SQL
├── python/        # Scripts Python
├── powerbi/       # Dashboards
└── docs/          # Documentación
```

## 📞 Contacto

[Tu nombre]  
[LinkedIn] | [Email] | [Portfolio]

---

**Nota:** Este proyecto simula un entorno bancario con datos ficticios para demostrar capacidades técnicas de Ingeniería de Datos.