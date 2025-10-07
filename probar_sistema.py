#!/usr/bin/env python3
"""
Script de Prueba del Sistema de Pasaportes
==========================================

Este script realiza pruebas básicas del sistema para verificar que todo
funcione correctamente antes de generar imágenes reales.

Pruebas realizadas:
1. Verificar archivos de configuración
2. Verificar conexión con WebUI
3. Generar configuraciones de prueba
4. Verificar modelos disponibles
5. Probar generación de una imagen de prueba

Autor: Sistema de Generación de Diversidad Étnica
Fecha: 2025-01-12
"""

import sys
import os
import json
from pathlib import Path

def verificar_archivos_configuracion():
    """Verifica que todos los archivos de configuración existan."""
    print("🔍 Verificando archivos de configuración...")
    
    archivos_requeridos = [
        "Consulta/gui_config.json",
        "Consulta/optimized_prompts.json", 
        "Consulta/intelligent_ethnic_data.json",
        "Consulta/model_descriptions.json"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not Path(archivo).exists():
            archivos_faltantes.append(archivo)
        else:
            print(f"   ✅ {archivo}")
    
    if archivos_faltantes:
        print(f"   ❌ Archivos faltantes: {archivos_faltantes}")
        return False
    
    print("   ✅ Todos los archivos de configuración están presentes")
    return True

def verificar_scripts():
    """Verifica que todos los scripts estén presentes."""
    print("\n🔍 Verificando scripts del sistema...")
    
    scripts_requeridos = [
        "generar_pasaportes.py",
        "webui_pasaportes.py", 
        "generar_pasaportes_completo.py",
        "instalar_dependencias.py"
    ]
    
    scripts_faltantes = []
    for script in scripts_requeridos:
        if not Path(script).exists():
            scripts_faltantes.append(script)
        else:
            print(f"   ✅ {script}")
    
    if scripts_faltantes:
        print(f"   ❌ Scripts faltantes: {scripts_faltantes}")
        return False
    
    print("   ✅ Todos los scripts están presentes")
    return True

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas."""
    print("\n🔍 Verificando dependencias de Python...")
    
    dependencias = ["requests", "PIL"]
    dependencias_faltantes = []
    
    for dep in dependencias:
        try:
            if dep == "PIL":
                import PIL
            else:
                __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            dependencias_faltantes.append(dep)
            print(f"   ❌ {dep}")
    
    if dependencias_faltantes:
        print(f"   ⚠️  Dependencias faltantes: {dependencias_faltantes}")
        print(f"   💡 Ejecuta: python3 instalar_dependencias.py")
        return False
    
    print("   ✅ Todas las dependencias están instaladas")
    return True

def probar_generador_configuraciones():
    """Prueba el generador de configuraciones."""
    print("\n🔍 Probando generador de configuraciones...")
    
    try:
        from generar_pasaportes import GeneradorPasaportes
        
        generador = GeneradorPasaportes()
        print("   ✅ GeneradorPasaportes inicializado correctamente")
        
        # Probar generación de características étnicas
        caracteristicas = generador.generar_caracteristicas_etnicas("venezuelan")
        print(f"   ✅ Características étnicas generadas: {len(caracteristicas)} características")
        
        # Probar generación de prompt
        prompt_pos, prompt_neg = generador.generar_prompt_completo("venezuelan", "mujer", 25, 35)
        print(f"   ✅ Prompt generado: {len(prompt_pos)} caracteres")
        
        # Probar generación de lote pequeño
        configuraciones = generador.generar_lote_imagenes(["venezuelan"], 1, "mujer", 25, 35)
        print(f"   ✅ Lote de configuraciones generado: {len(configuraciones)} configuraciones")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en generador de configuraciones: {e}")
        return False

def probar_cliente_webui():
    """Prueba el cliente de WebUI."""
    print("\n🔍 Probando cliente de WebUI...")
    
    try:
        from webui_pasaportes import WebUIPasaportes
        
        webui = WebUIPasaportes()
        print("   ✅ WebUIPasaportes inicializado correctamente")
        
        # Probar verificación de conexión
        if webui.verificar_conexion():
            print("   ✅ Conexión con WebUI establecida")
            
            # Probar obtención de modelos
            modelos = webui.obtener_modelos_disponibles()
            print(f"   ✅ Modelos disponibles: {len(modelos)} modelos")
            
            if modelos:
                print(f"   📋 Primeros 3 modelos:")
                for modelo in modelos[:3]:
                    print(f"      - {modelo}")
            
            return True
        else:
            print("   ⚠️  No se puede conectar a WebUI")
            print("   💡 Asegúrate de que WebUI esté ejecutándose: ./webui.sh")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en cliente de WebUI: {e}")
        return False

def probar_sistema_completo():
    """Prueba el sistema completo."""
    print("\n🔍 Probando sistema completo...")
    
    try:
        from generar_pasaportes_completo import SistemaPasaportesCompleto
        
        sistema = SistemaPasaportesCompleto()
        print("   ✅ SistemaPasaportesCompleto inicializado correctamente")
        
        # Probar verificación de prerequisitos
        prerequisitos_ok = sistema.verificar_prerequisitos()
        if prerequisitos_ok:
            print("   ✅ Prerequisitos verificados correctamente")
            return True
        else:
            print("   ⚠️  Algunos prerequisitos no están cumplidos")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en sistema completo: {e}")
        return False

def generar_configuracion_prueba():
    """Genera una configuración de prueba."""
    print("\n🔍 Generando configuración de prueba...")
    
    try:
        from generar_pasaportes import GeneradorPasaportes
        
        generador = GeneradorPasaportes()
        
        # Generar configuración de prueba
        configuraciones = generador.generar_lote_imagenes(
            ["venezuelan"], 1, "mujer", 25, 35
        )
        
        # Guardar configuración de prueba
        generador.guardar_configuracion_lote(configuraciones, "configuracion_prueba.json")
        
        print("   ✅ Configuración de prueba generada: configuracion_prueba.json")
        
        # Mostrar resumen de la configuración
        config = configuraciones[0]
        print(f"   📊 Resumen de configuración:")
        print(f"      - Nacionalidad: {config['nacionalidad']}")
        print(f"      - Género: {config['genero']}")
        print(f"      - Edad: {config['edad_min']}-{config['edad_max']}")
        print(f"      - Dimensiones: {config['configuracion_tecnica']['width']}x{config['configuracion_tecnica']['height']}")
        print(f"      - Modelo: {config['configuracion_tecnica']['model']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error generando configuración de prueba: {e}")
        return False

def main():
    """Función principal del script de prueba."""
    print("🧪 SCRIPT DE PRUEBA DEL SISTEMA DE PASAPORTES")
    print("=" * 50)
    
    pruebas = [
        ("Archivos de configuración", verificar_archivos_configuracion),
        ("Scripts del sistema", verificar_scripts),
        ("Dependencias de Python", verificar_dependencias),
        ("Generador de configuraciones", probar_generador_configuraciones),
        ("Cliente de WebUI", probar_cliente_webui),
        ("Sistema completo", probar_sistema_completo),
        ("Configuración de prueba", generar_configuracion_prueba)
    ]
    
    resultados = []
    
    for nombre, funcion in pruebas:
        try:
            resultado = funcion()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"   ❌ Error inesperado en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Mostrar resumen final
    print(f"\n📊 RESUMEN DE PRUEBAS")
    print("=" * 30)
    
    exitosos = 0
    for nombre, resultado in resultados:
        estado = "✅ EXITOSO" if resultado else "❌ FALLIDO"
        print(f"{estado} - {nombre}")
        if resultado:
            exitosos += 1
    
    print(f"\n📈 Resultado: {exitosos}/{len(resultados)} pruebas exitosas")
    
    if exitosos == len(resultados):
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("💡 El sistema está listo para generar imágenes de pasaportes")
        print("\n🚀 Próximos pasos:")
        print("   1. Ejecutar: python3 generar_pasaportes_completo.py --estadisticas")
        print("   2. Ejecutar: python3 generar_pasaportes_completo.py --nacionalidades venezuelan --cantidad 1")
        return 0
    else:
        print(f"\n⚠️  {len(resultados) - exitosos} pruebas fallaron")
        print("💡 Revisa los errores anteriores y corrige los problemas")
        return 1

if __name__ == "__main__":
    exit(main())
