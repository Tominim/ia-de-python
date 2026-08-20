import sys
import io
import traceback

def ejecutar_y_analizar(codigo_usuario):
    """
    ENTORNO DE EJECUCIÓN CONTROLADO:
    Aísla y captura las salidas o excepciones del código del usuario.
    """
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
        sys.stdout = stdout_original
        
    return exito, salida_consola.getvalue(), error_detallado
