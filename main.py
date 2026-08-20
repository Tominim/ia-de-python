import sys
import io
import traceback
import cerebro_local

def ejecutar_y_analizar(codigo_usuario):
    """
    ENTORNO DE EJECUCIÓN CONTROLADO:
    Ejecuta el script de forma aislada en memoria. Captura las salidas de consola
    y atrapa trazas de error de forma robusta y defensiva contra alteración de streams.
    """
    # Guardamos de forma defensiva la referencia real de la consola del sistema
    stdout_original = sys.stdout
    salida_consola = io.StringIO()
    sys.stdout = salida_consola
    
    contexto_local = {}
    exito = True
    error_detallado = ""
    
    try:
        exec(codigo_usuario, {}, contexto_local)
    except Exception:
        exito = False
        error_detallado = traceback.format_exc()
    finally:
        # Restauramos apuntando exactamente a la referencia original del sistema
        sys.stdout = stdout_original
        
    return exito, salida_consola.getvalue(), error_detallado

def diagnosticar_error(codigo, error):
    print("\n💡 Análisis de Aprendizaje Local:")
    
    # 1. El cerebro busca coincidencia híbrida (Error + AST) y devuelve la propuesta y la llave del JSON
    solucion_memorizada, llave_patron = cerebro_local.buscar_solucion_aprendida(error, codigo)
    
    if solucion_memorizada:
        print("\n🤖 ¡LA IA RECONOCIÓ EL ERROR Y PROPONE ESTA SOLUCIÓN!")
        print("-" * 50)
        print(f"# Código corregido sugerido:\n{solucion_memorizada}")
        print("-" * 50)
        
        # 2. VALIDACIÓN EMPÍRICA AUTOMÁTICA EN SEGUNDO PLANO
        print("⚙️ Evaluando la efectividad del programa reparado en el entorno controlado...")
        exito_parche, _, _ = ejecutar_y_analizar(solucion_memorizada)
        
        if exito_parche:
            print("📈 ¡Validación exitosa! El programa modificado se ejecutó limpiamente de principio a fin.")
            # Si corre sin excepciones en secreto, sumamos una confirmación empírica real
            cerebro_local.registrar_exito_reparacion(llave_patron)
        else:
            print("⚠️ Alerta: El programa corregido volvió a fallar o el parche introdujo un nuevo error sintáctico.")
    else:
        # 3. Si es un patrón nuevo, activa el canal de aprendizaje manual
        cerebro_local.entrenar_ia_manualmente(error, codigo)

def ayudante_python():
    print("=" * 60)
    print("🤖 NÚCLEO AYUDANTE PYTHON: MODO CEREBRO EVOLUTIVO AST (MICA)")
    print("Escribe tu código. Ejecuta con 'RUN' en una línea vacía.")
    print("Comandos globales independientes: 'HISTORIAL' o 'SALIR'.")
    print("=" * 60)
    
    while True:
        lineas = []
        print("\n📥 Introduce tu código Python:")
        
        while True:
            linea = input()
            if linea.strip() == "RUN":
                break
            if linea.strip().upper() == "SALIR":
                print("Cerrando el asistente. ¡Buen código!")
                return
            if linea.strip().upper() == "HISTORIAL":
                cerebro_local.mostrar_historial_consola()
                lineas = []  # Limpia la cola por seguridad
                continue
            lineas.append(linea)
            
        codigo_completo = "\n".join(lineas)
        if not codigo_completo.strip():
            continue
            
        print("\n⚙️ Procesando y ejecutando localmente...")
        exito, resultado, error = ejecutar_y_analizar(codigo_completo)
        
        if exito:
            print("\n✅ ¡EJECUCIÓN EXITOSA!")
            print("-" * 50)
            print(resultado if resultado else "[El código se ejecutó correctamente pero no imprimió nada]")
            print("-" * 50)
        else:
            print("\n❌ CRASH DETECTADO:")
            print("-" * 50)
            print(error)
            print("-" * 50)
            
            # Dispara el diagnóstico inteligente adaptado al flujo de la firma del AST
            diagnosticar_error(codigo_completo, error)

if __name__ == "__main__":
    ayudante_python()
