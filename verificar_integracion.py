#!/usr/bin/env python3
"""
Verificador Final de Integración de Pasaportes
============================================

Este script verifica que toda la integración esté funcionando correctamente
antes de usar WebUI.

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import os
import sys
from pathlib import Path

def verificar_archivos_requeridos():
    """Verifica que todos los archivos requeridos estén presentes."""
    print("🔍 Verificando archivos requeridos...")
    
    archivos_requeridos = [
        "generar_pasaportes.py",
        "webui_pasaportes.py", 
        "generar_pasaportes_completo.py",
        "instalar_dependencias.py",
        "probar_sistema.py",
        "instalar_pasaportes_txt2img.py",
        "modules/ui.py",
        "Consulta/gui_config.json",
        "Consulta/optimized_prompts.json",
        "Consulta/intelligent_ethnic_data.json"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"   ✅ {archivo}")
        else:
            archivos_faltantes.append(archivo)
            print(f"   ❌ {archivo}")
    
    return len(archivos_faltantes) == 0

def verificar_imports():
    """Verifica que los imports funcionen correctamente."""
    print("\n🔍 Verificando imports...")
    
    try:
        from generar_pasaportes import GeneradorPasaportes
        print("   ✅ generar_pasaportes.py importado correctamente")
    except Exception as e:
        print(f"   ❌ Error importando generar_pasaportes.py: {e}")
        return False
    
    try:
        from webui_pasaportes import WebUIPasaportes
        print("   ✅ webui_pasaportes.py importado correctamente")
    except Exception as e:
        print(f"   ❌ Error importando webui_pasaportes.py: {e}")
        return False
    
    return True

def verificar_generador():
    """Verifica que el generador funcione correctamente."""
    print("\n🔍 Verificando generador de pasaportes...")
    
    try:
        from generar_pasaportes import GeneradorPasaportes
        from pathlib import Path
        
        consulta_dir = Path("Consulta")
        if not consulta_dir.exists():
            print("   ❌ Carpeta Consulta no encontrada")
            return False
        
        generador = GeneradorPasaportes(str(consulta_dir))
        nacionalidades = list(generador.datos_etnicos.keys())
        
        print(f"   ✅ Generador inicializado: {len(nacionalidades)} nacionalidades")
        print(f"   📋 Nacionalidades: {', '.join(nacionalidades[:5])}...")
        
        # Probar generación de prompt
        prompt_pos, prompt_neg = generador.generar_prompt_completo('venezuelan', 'mujer', 25, 25)
        print(f"   ✅ Prompt generado: {len(prompt_pos)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en generador: {e}")
        return False

def verificar_sintaxis_ui():
    """Verifica que modules/ui.py tenga sintaxis correcta."""
    print("\n🔍 Verificando sintaxis de modules/ui.py...")
    
    try:
        import py_compile
        py_compile.compile("modules/ui.py", doraise=True)
        print("   ✅ Sintaxis de modules/ui.py correcta")
        return True
    except Exception as e:
        print(f"   ❌ Error de sintaxis en modules/ui.py: {e}")
        return False

def verificar_archivos_basura():
    """Verifica que no haya archivos basura."""
    print("\n🔍 Verificando archivos basura...")
    
    archivos_basura = [
        "configuracion_prueba.json",
        "reporte_pasaportes.json",
        "temp_configuraciones.json",
        "temp_configuraciones_pasaportes.json"
    ]
    
    archivos_encontrados = []
    for archivo in archivos_basura:
        if Path(archivo).exists():
            archivos_encontrados.append(archivo)
    
    if archivos_encontrados:
        print(f"   ⚠️  Archivos basura encontrados: {archivos_encontrados}")
        return False
    else:
        print("   ✅ No se encontraron archivos basura")
        return True

def main():
    """Función principal del verificador."""
    print("🚀 Verificador Final de Integración de Pasaportes")
    print("=" * 55)
    
    # Verificaciones
    verificaciones = [
        ("Archivos requeridos", verificar_archivos_requeridos),
        ("Imports", verificar_imports),
        ("Generador", verificar_generador),
        ("Sintaxis UI", verificar_sintaxis_ui),
        ("Archivos basura", verificar_archivos_basura)
    ]
    
    resultados = []
    for nombre, funcion in verificaciones:
        try:
            resultado = funcion()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"   ❌ Error inesperado en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print(f"\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 30)
    
    exitosos = 0
    for nombre, resultado in resultados:
        estado = "✅ EXITOSO" if resultado else "❌ FALLIDO"
        print(f"{estado} - {nombre}")
        if resultado:
            exitosos += 1
    
    print(f"\n📈 Resultado: {exitosos}/{len(resultados)} verificaciones exitosas")
    
    if exitosos == len(resultados):
        print("\n🎉 ¡Toda la integración está funcionando correctamente!")
        print("\n🚀 Próximos pasos:")
        print("1. Ejecuta WebUI: ./webui.sh")
        print("2. Ve a la pestaña 'txt2img'")
        print("3. Busca el acordeón '🇻🇪 Pasaportes Venezolanos'")
        print("4. ¡Comienza a generar imágenes de pasaportes!")
        return 0
    else:
        print(f"\n⚠️  {len(resultados) - exitosos} verificaciones fallaron")
        print("💡 Revisa los errores anteriores y corrige los problemas")
        return 1

if __name__ == "__main__":
    exit(main())
