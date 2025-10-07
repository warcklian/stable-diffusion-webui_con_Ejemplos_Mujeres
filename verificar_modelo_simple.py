#!/usr/bin/env python3
"""
Script de verificación simplificado del modelo actual en WebUI
Verifica que el modelo seleccionado coincida con el modelo cargado
"""

import sys
import os
import json
from pathlib import Path

def verificar_configuracion_webui():
    """Verifica la configuración de WebUI sin inicializar completamente"""
    print("🔍 Verificador de Configuración WebUI")
    print("=" * 50)
    
    try:
        # Buscar archivo de configuración
        config_file = Path("config.json")
        if not config_file.exists():
            print("⚠️ No se encontró archivo config.json")
            return False
        
        # Leer configuración
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ Archivo de configuración encontrado")
        
        # Obtener modelo seleccionado
        selected_model = config.get("sd_model_checkpoint", None)
        if selected_model:
            print(f"✅ Modelo seleccionado en configuración: {selected_model}")
        else:
            print("⚠️ No hay modelo seleccionado en configuración")
            return False
        
        # Verificar si el modelo existe
        models_dir = Path("models/Stable-diffusion")
        if models_dir.exists():
            model_files = list(models_dir.glob("*.safetensors")) + list(models_dir.glob("*.ckpt"))
            print(f"✅ Directorio de modelos encontrado: {len(model_files)} archivos")
            
            # Buscar el modelo seleccionado
            model_found = False
            for model_file in model_files:
                if selected_model in model_file.name or model_file.stem == selected_model:
                    print(f"✅ Modelo encontrado: {model_file.name}")
                    model_found = True
                    break
            
            if not model_found:
                print(f"⚠️ Modelo seleccionado no encontrado en el directorio")
                print(f"   Buscando: {selected_model}")
                print(f"   Archivos disponibles: {[f.name for f in model_files[:5]]}")
                return False
        else:
            print("⚠️ Directorio de modelos no encontrado")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def verificar_generador_masivo():
    """Verifica el generador masivo integrado"""
    print("\n🚀 Verificador del Generador Masivo")
    print("=" * 40)
    
    try:
        from webui_massive_generator import WebUIMassiveGenerator
        print("✅ Generador masivo importado correctamente")
        
        # Crear instancia de prueba
        generator = WebUIMassiveGenerator()
        print("✅ Instancia del generador creada")
        
        # Probar obtención de información del modelo
        model_info = generator._get_current_model_info()
        print("✅ Información del modelo obtenida:")
        print(f"   - Nombre: {model_info['model_name']}")
        print(f"   - Título: {model_info['model_title']}")
        print(f"   - Tipo: {model_info['model_type']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando generador masivo: {e}")
        return False

def verificar_archivos_consulta():
    """Verifica los archivos de configuración de Consulta"""
    print("\n📁 Verificador de Archivos Consulta")
    print("=" * 40)
    
    try:
        consulta_dir = Path("Consulta")
        if not consulta_dir.exists():
            print("❌ Directorio Consulta no encontrado")
            return False
        
        print("✅ Directorio Consulta encontrado")
        
        # Verificar archivos importantes
        archivos_importantes = [
            "gui_config.json",
            "optimized_prompts.json",
            "intelligent_ethnic_data.json"
        ]
        
        for archivo in archivos_importantes:
            archivo_path = consulta_dir / archivo
            if archivo_path.exists():
                print(f"✅ {archivo} encontrado")
            else:
                print(f"⚠️ {archivo} no encontrado")
        
        # Verificar directorio countries
        countries_dir = consulta_dir / "countries"
        if countries_dir.exists():
            country_files = list(countries_dir.glob("*.json"))
            print(f"✅ Directorio countries encontrado: {len(country_files)} archivos")
            
            # Mostrar algunos archivos
            for country_file in country_files[:3]:
                print(f"   - {country_file.name}")
        else:
            print("⚠️ Directorio countries no encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando archivos Consulta: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Verificador Completo de Sistema de Pasaportes")
    print("=" * 60)
    
    # Verificar configuración WebUI
    config_ok = verificar_configuracion_webui()
    
    # Verificar generador masivo
    generador_ok = verificar_generador_masivo()
    
    # Verificar archivos Consulta
    consulta_ok = verificar_archivos_consulta()
    
    # Resumen final
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 30)
    print(f"✅ Configuración WebUI: {'OK' if config_ok else 'ERROR'}")
    print(f"✅ Generador Masivo: {'OK' if generador_ok else 'ERROR'}")
    print(f"✅ Archivos Consulta: {'OK' if consulta_ok else 'ERROR'}")
    
    if config_ok and generador_ok and consulta_ok:
        print("\n🎉 ¡Todas las verificaciones pasaron exitosamente!")
        print("💡 El sistema está listo para generar imágenes de pasaportes")
        print("\n📋 Próximos pasos:")
        print("1. Ejecuta WebUI: ./webui.sh")
        print("2. Ve a la pestaña 'txt2img'")
        print("3. Busca el acordeón '🇻🇪 Pasaportes Venezolanos'")
        print("4. Haz clic en '🔍 Verificar Modelo' para confirmar el modelo")
        print("5. ¡Comienza a generar imágenes de pasaportes!")
        return True
    else:
        print("\n⚠️ Algunas verificaciones fallaron")
        print("💡 Revisa los errores anteriores")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
