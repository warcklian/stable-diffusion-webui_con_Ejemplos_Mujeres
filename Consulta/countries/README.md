# Sistema Modular de Países con Diversidad Realista

Este directorio contiene el sistema modular de datos étnicos por país, donde cada país tiene su propio archivo JSON independiente. El sistema incluye características de diversidad realista como variación de peso corporal, niveles de belleza facial, y rasgos excepcionales por herencia mixta.

## Estructura

```
countries/
├── index.json              # Índice de países disponibles
├── venezolana.json         # Datos de Venezuela
├── mexicana.json           # Datos de México
├── americana.json          # Datos de Estados Unidos
├── cubana.json             # Datos de Cuba
├── brasileña.json          # Datos de Brasil
├── add_country.py          # Utilidad para agregar países
└── README.md               # Este archivo
```

## Ventajas del Sistema Modular

### ✅ **Mantenimiento Fácil**
- Cada país en su propio archivo
- No hay conflictos entre países
- Fácil de editar y actualizar

### ✅ **Escalabilidad**
- Agregar nuevos países sin afectar existentes
- Cada desarrollador puede trabajar en países diferentes
- Control de versiones granular

### ✅ **Rendimiento**
- Solo se cargan los países necesarios
- Carga más rápida de datos específicos
- Menor uso de memoria

### ✅ **Flexibilidad**
- Diferentes estructuras por país si es necesario
- Fácil personalización de características
- Soporte para diferentes niveles de detalle

### ✅ **Diversidad Realista**
- Variación de peso corporal (delgado, normal, sobrepeso, obeso)
- Niveles de belleza facial (común, atractivo, excepcional)
- Longitud de cabello variada (muy corto a muy largo)
- Peinados específicos por género
- Rasgos excepcionales por herencia mixta (5% probabilidad)

## Cómo Agregar un Nuevo País

### Método 1: Usando la Utilidad
```bash
cd SD_Automatizador/data/countries
python add_country.py colombiana Colombia norte,centro,sur
```

### Método 2: Manual
1. Crear archivo `nuevo_pais.json` con la estructura correcta
2. Actualizar `index.json` con la información del país
3. Reiniciar la aplicación

## Estructura de un Archivo de País

```json
{
  "metadata": {
    "country_code": "venezolana",
    "country_name": "Venezuela",
    "version": "1.0",
    "description": "Descripción del país",
    "created": "2025-01-12"
  },
  "regions": {
    "region_code": {
      "name": "Nombre de la Región",
      "description": "Descripción de la región",
      "demographics": {
        "european_heritage": 0.5,
        "mestizo": 0.3,
        "indigenous": 0.2
      },
      "skin_tones": {
        "light": 0.3,
        "medium": 0.4,
        "dark": 0.3
      },
      "hair_colors": {
        "blonde": 0.1,
        "brown": 0.6,
        "black": 0.3
      },
      "hair_styles": {
        "straight": 0.4,
        "wavy": 0.4,
        "curly": 0.2
      },
      "eye_colors": {
        "blue": 0.1,
        "brown": 0.8,
        "green": 0.1
      },
      "facial_structures": {
        "oval": 0.4,
        "round": 0.3,
        "square": 0.3
      },
      "height_tendency": "average",
      "body_type": "mixed",
      "ethnic_characteristics": [
        "característica 1",
        "característica 2"
      ]
    }
  }
}
```

## Países Disponibles

### Con Datos Regionales y Diversidad Realista
- **Venezuela** (3 regiones): Caribe, Andina, Llanos
- **México** (3 regiones): Norte, Centro, Sur
- **Estados Unidos** (3 regiones): Noreste, Sur, Oeste - *Sistema multicultural avanzado*
- **Cuba** (2 regiones): Occidental, Oriental
- **Brasil** (2 regiones): Sudeste, Nordeste

### Sin Datos Regionales (Usan Sistema Anterior)
- Haitiana, Dominicana, China, Japonesa, Coreana, India, Tailandesa
- Noruega, Finlandesa, Alemana, Italiana, Francesa, Británica, Española
- Nigeriana, Etíope, Sudafricana, Australiana

## Características de Diversidad Realista

### ⚖️ **Variación de Peso Corporal**
- **5%** - Muy delgado (underweight)
- **60%** - Peso normal (normal)
- **25%** - Sobrepeso (overweight)
- **10%** - Obeso (obese)

### ✨ **Niveles de Belleza Facial**
- **70%** - Apariencia común/normal (common)
- **25%** - Atractivo (attractive)
- **5%** - Excepcionalmente atractivo (exceptional)

### **Longitud de Cabello**
- **15%** - Muy corto
- **25%** - Corto
- **30%** - Mediano
- **25%** - Largo
- **5%** - Muy largo

### 👩 **Peinados para Mujeres**
- **20%** - Largo lacio
- **15%** - Largo ondulado
- **10%** - Largo rizado
- **15%** - Mediano lacio
- **10%** - Mediano ondulado
- **5%** - Mediano rizado
- **10%** - Corto lacio
- **5%** - Corto ondulado
- **3%** - Corto rizado
- **4%** - Corte bob
- **2%** - Corte pixie
- **1%** - Cola de caballo

### 👨 **Peinados para Hombres**
- **25%** - Corto recortado
- **20%** - Corto con raya al lado
- **15%** - Corto con raya al centro
- **15%** - Corto desordenado
- **10%** - Corto con picos
- **8%** - Mediano lacio
- **4%** - Mediano ondulado
- **2%** - Largo lacio
- **1%** - Largo ondulado

### 🌟 **Rasgos Excepcionales (5% probabilidad)**

#### **Para Piel Oscura/Africana:**
- Ojos azules, verdes, avellana, marrón claro, color miel
- Cabello rubio, rojo, marrón claro, castaño rojizo, rubio fresa, marrón

#### **Para Asiáticos:**
- Ojos azules, verdes, avellana, marrón claro, ámbar
- Cabello rizado, ondulado, rojo, rubio, castaño rojizo, marrón, marrón claro

#### **Para Hispanos/Latinos:**
- Ojos azules, verdes, avellana, marrón claro, grises
- Cabello rubio, rojo, castaño rojizo, marrón claro, rubio fresa, rubio oscuro, castaño rojizo claro

#### **Rasgos Mixtos:**
- Nariz europea en persona asiática
- Ojos asiáticos en persona europea
- Labios africanos en persona europea
- Rasgos indígenas en persona mixta
- Pómulos europeos en persona asiática
- Mandíbula asiática en persona europea
- Nariz africana en persona asiática
- Ojos indígenas en persona europea

## Cómo Funciona la Selección de Regiones

1. **Si se especifica región**: Usa esa región específica
2. **Si NO se especifica región**: Selecciona una región aleatoriamente
3. **Si no hay regiones**: Usa datos generales del país

Esto garantiza máxima diversidad en las generaciones.

## Ejemplos de Generación Realista

### **Generando 10 mujeres venezolanas:**
1. **Mujer Venezolana, 28 años**
   - ⚖️ Peso: normal (60%)
   - ✨ Belleza: común (70%)
   - **Cabello**: negro, largo, largo lacio (20%)
   - 🌟 Excepcional: ninguna (95%)

2. **Mujer Venezolana, 32 años**
   - ⚖️ Peso: sobrepeso (25%)
   - ✨ Belleza: atractivo (25%)
   - **Cabello**: marrón, mediano, mediano ondulado (10%)
   - 🌟 Excepcional: `green eyes in hispanic person` (5%)

### **Generando 10 hombres japoneses:**
1. **Hombre Japonés, 30 años**
   - ⚖️ Peso: normal (60%)
   - ✨ Belleza: común (70%)
   - **Cabello**: negro, corto, corto recortado (25%)
   - 🌟 Excepcional: ninguna (95%)

2. **Hombre Japonés, 28 años**
   - ⚖️ Peso: delgado (5%)
   - ✨ Belleza: excepcional (5%)
   - **Cabello**: negro, corto, corto con raya al lado (20%)
   - 🌟 Excepcional: `blonde hair in asian person` (5%)

## Migración del Sistema Anterior

El sistema es compatible con el anterior:
1. **Prioridad 1**: Sistema modular (countries/)
2. **Prioridad 2**: Datos avanzados (advanced_ethnic_data.json)
3. **Prioridad 3**: Datos inteligentes (intelligent_ethnic_data.json)
4. **Fallback**: Datos por defecto

## Contribuir

Para agregar un nuevo país:
1. Usar `add_country.py` para crear el template
2. Personalizar las características regionales
3. Probar con la aplicación
4. Hacer commit del archivo

## Notas Técnicas

- Los archivos deben estar en UTF-8
- Las probabilidades deben sumar 1.0
- Los nombres de regiones deben ser únicos por país
- El sistema carga automáticamente todos los países disponibles
- Las características de diversidad realista se aplican automáticamente a todas las nacionalidades
- Los rasgos excepcionales se seleccionan inteligentemente basados en la etnia detectada
- El sistema de peinados respeta las diferencias de género para mayor realismo

## Logging y Debugging

El sistema incluye logging detallado para monitorear:
- Selección de regiones y grupos étnicos
- Generación de características corporales y de belleza
- Detección de rasgos excepcionales
- Información étnica específica en metadatos

### Ejemplo de Log:
```
✅ Perfil 1/10: mujer, 28 años, medium_light
   🎭 Origen étnico: Americano de Origen Europeo
   🏷️ Subgrupo: German-American
   ⚖️ Peso corporal: normal
   ✨ Nivel de belleza: común
   🌟 Características excepcionales: ['green eyes in hispanic person']
```
