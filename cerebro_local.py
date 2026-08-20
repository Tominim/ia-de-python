import json
import os
import re
import ast
from datetime import datetime

BASE_CONOCIMIENTO = "conocimiento_ia.json"

def cargar_conocimiento():
    if os.path.exists(BASE_CONOCIMIENTO):
        try:
            with open(BASE_CONOCIMIENTO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def guardar_conocimiento(datos):
    with open(BASE_CONOCIMIENTO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def unicos_en_orden(lista):
    """Elimina duplicados manteniendo estrictamente el orden original."""
    resultado = []
    for elemento in lista:
        if elemento not in resultado:
            resultado.append(elemento)
    return resultado

def analizar_estructura_ast(codigo):
    try:
        arbol = ast.parse(codigo)
        conteo_nodos = {}
        for nodo in ast.walk(arbol):
            nombre_nodo = type(nodo).__name__
            conteo_nodos[nombre_nodo] = conteo_nodos.get(nombre_nodo, 0) + 1
        componentes = [f"{k}:{v}" for k, v in sorted(conteo_nodos.items())]
        return "-".join(componentes)
    except Exception:
        return "SyntaxErrorNode"

def calcular_distancia_levenshtein(str1, str2):
    if len(str1) < len(str2):
        return calcular_distancia_levenshtein(str2, str1)
    if len(str2) == 0:
        return len(str1)
    fila_previa = range(len(str2) + 1)
    for i, c1 in enumerate(str1):
        fila_actual = [i + 1]
        for j, c2 in enumerate(str2):
            inserciones = fila_previa[j + 1] + 1
            eliminaciones = fila_actual[j] + 1
            sustituciones = fila_previa[j] + (c1 != c2)
            fila_actual.append(min(inserciones, eliminaciones, sustituciones))
        fila_previa = fila_actual
    return fila_previa[-1]

def abstraer_mensaje_error(error_sucio):
    lineas = error_sucio.strip().split("\n")
    linea_error = lineas[-1].strip()
    for linea in reversed(lineas):
        if re.search(r"^\w+Error:", linea.strip()) or re.search(r"^\w+Exception:", linea.strip()):
            linea_error = linea.strip()
            break
    linea_error = re.sub(r"'[^']+'|\"[^\"]+\"", "'<ELEMENTO>'", linea_error)
    linea_error = re.sub(r"\b\d+\b", "<NUMERO>", linea_error)
    linea_error = re.sub(r"name\s+'\w+'", "name '<VARIABLE>'", linea_error)
    linea_error = re.sub(r"module\s+'\w+'", "module '<MODULO>'", linea_error)
    return linea_error

def analizador_semantico_codigo(codigo_original, error_sucio):
    """
    ANALIZADOR SEMÁNTICO DE PRECISIÓN:
    Identifica identificadores, números y literales mediante AST, ordenándolos
    por su posición física. Filtrado progresivo libre de UnboundLocalError.
    """
    nodos_identificadores = []
    nodos_numeros = []
    nodos_strings = []
    funciones_llamadas = set()

    try:
        arbol = ast.parse(codigo_original)
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
                funciones_llamadas.add(nodo.func.id)
            if isinstance(nodo, ast.Name) and isinstance(nodo.ctx, (ast.Store, ast.Load)):
                nodos_identificadores.append(nodo)
            elif isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
                nodos_numeros.append(nodo)
            elif isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
                nodos_strings.append(nodo)
                
        nodos_identificadores.sort(key=lambda n: (getattr(n, 'lineno', 0), getattr(n, 'col_offset', 0)))
        nodos_numeros.sort(key=lambda n: (getattr(n, 'lineno', 0), getattr(n, 'col_offset', 0)))
        nodos_strings.sort(key=lambda n: (getattr(n, 'lineno', 0), getattr(n, 'col_offset', 0)))

        identificadores_limpios = []
        for n in nodos_identificadores:
            if n.id not in funciones_llamadas and n.id not in identificadores_limpios:
                identificadores_limpios.append(n.id)
                
        numeros_limpios = []
        for n in nodos_numeros:
            valor = str(n.value)
            if valor not in numeros_limpios:
                numeros_limpios.append(valor)
                
        strings_limpios = []
        for n in nodos_strings:
            valor = n.value
            if valor not in strings_limpios:
                strings_limpios.append(valor)
    except Exception:
        identificadores_limpios = unicos_en_orden(re.findall(r"\b[a-zA-Z_]\w*\b", codigo_original))
        numeros_limpios = unicos_en_orden(re.findall(r"\b\d+\b", codigo_original))
        strings_limpios = unicos_en_orden(re.findall(r"'([^']+)'|\"([^\"]+)\"", codigo_original))

    match_mod = re.search(r"No module named '([^']+)'", error_sucio)
    modulo_error = match_mod.group(1) if match_mod else None

    return {"variables": identificadores_limpios, "numeros": numeros_limpios, "strings": strings_limpios, "modulo_error": modulo_error}

def registrar_log_busqueda(patron_error):
    conocimiento = cargar_conocimiento()
    if patron_error in conocimiento:
        meta = conocimiento[patron_error].setdefault("meta", {})
        meta.setdefault("veces_encontrada", 0)
        meta.setdefault("veces_confirmada", 0)
        meta["veces_encontrada"] += 1
        meta["ultimo_uso"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        guardar_conocimiento(conocimiento)

def registrar_exito_reparacion(patron_error):
    conocimiento = cargar_conocimiento()
    if patron_error in conocimiento:
        meta = conocimiento[patron_error].setdefault("meta", {})
        meta.setdefault("veces_encontrada", 0)
        meta.setdefault("veces_confirmada", 0)
        meta["veces_confirmada"] += 1
        guardar_conocimiento(conocimiento)

def buscar_solucion_aprendida(error_detectado, codigo_original):
    conocimiento = cargar_conocimiento()
    patron_error = abstraer_mensaje_error(error_detectado)
    firma_ast = analizar_estructura_ast(codigo_original)
    
    solucion_encontrada = None
    llave_ganadora = None
    mejor_score = 0.0
    
    for llave, bloque in conocimiento.items():
        if isinstance(bloque, str):
            continue
        score_error = 1.0 - (calcular_distancia_levenshtein(patron_error, llave) / max(len(patron_error), len(llave), 1))
        score_ast = 1.0 - (calcular_distancia_levenshtein(firma_ast, bloque.get("ast", "")) / max(len(firma_ast), len(bloque.get("ast", "")), 1))
        score_total = (score_error * 0.7) + (score_ast * 0.3)
        
        if score_total > mejor_score and score_total > 0.70:
            mejor_score = score_total
            solucion_encontrada = bloque["solucion"]
            llave_ganadora = llave

    if solucion_encontrada:
        registrar_log_busqueda(llave_ganadora)
        tokens = analizador_semantico_codigo(codigo_original, error_detectado)
        
        for i, v in enumerate(tokens["variables"], 1):
            solucion_encontrada = solucion_encontrada.replace(f"<VAR{i}>", v)
        for i, n in enumerate(tokens["numeros"], 1):
            solucion_encontrada = solucion_encontrada.replace(f"<NUM{i}>", n)
        for i, s in enumerate(tokens["strings"], 1):
            solucion_encontrada = solucion_encontrada.replace(f"<ELEM{i}>", s)

        if tokens["variables"]: solucion_encontrada = solucion_encontrada.replace("<VARIABLE>", tokens["variables"][0])
        if tokens["numeros"]: solucion_encontrada = solucion_encontrada.replace("<NUMERO>", tokens["numeros"][0])
        if tokens["strings"]: solucion_encontrada = solucion_encontrada.replace("<ELEMENTO>", tokens["strings"][0])
        if tokens["modulo_error"]: solucion_encontrada = solucion_encontrada.replace("<MODULO>", tokens["modulo_error"])
            
        return solucion_encontrada, llave_ganadora
    return None, None

def entrenar_ia_manualmente(error_sucio, codigo_original):
    print("\n🚀 ANALIZADOR SEMÁNTICO ACTIVO (Identificadores por Aparición):")
    print("Comodines indexados por orden de primera aparición: <VAR1>, <VAR2>, <NUM1>...")
    print("-" * 75)
    solucion_usuario = input("👉 Introduce tu plantilla de corrección: ")
    
    if solucion_usuario.strip():
        conocimiento = cargar_conocimiento()
        patron_error = abstraer_mensaje_error(error_sucio)
        firma_ast = analizar_estructura_ast(codigo_original)
        
        conocimiento[patron_error] = {
            "solucion": solucion_usuario,
            "ast": firma_ast,
            "meta": {
                "creado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "veces_encontrada": 0,
                "veces_confirmada": 0,
                "ultimo_uso": "Nunca"
            }
        }
        guardar_conocimiento(conocimiento)
        print("✅ ¡Fórmula y metadatos indexados de manera segura!")
        return solucion_usuario
    return None

def mostrar_historial_consola():
    conocimiento = cargar_conocimiento()
    if not conocimiento:
        print("\n📭 Almacenamiento local de conocimiento sin registros.")
        return
    print("\n" + "═"*70)
    print("📊 MÉTRICAS DE DIAGNÓSTICO Y LOGS RELACIONALES DEL AST")
    print("═"*70)
    for i, (patron, datos) in enumerate(conocimiento.items(), 1):
        if isinstance(datos, str):
            continue
        meta = datos.get("meta", {})
        enc = meta.get("veces_encontrada", 0)
        conf = meta.get("veces_confirmada", 0)
        efectividad = (conf / enc * 100) if enc > 0 else 0.0
        
        print(f"{i}. Firma del Error: {patron}")
        print(f"   ↳ Código Solución: {datos['solucion']}")
        print(f"   ↳ Match/Confirmados: {enc} veces invocada | {conf} veces confirmada")
        print(f"   ↳ Efectividad de Reparación: {efectividad:.2f}%")
        print("─"*70)
