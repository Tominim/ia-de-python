def formatear_solucion_sugerida(codigo_limpio):
    """Limpia y tabula la cadena de la solución sugerida antes de enviarla al REPL."""
    if not codigo_limpio:
        return "[Error: Parche vacío]"
    return codigo_limpio.strip()
