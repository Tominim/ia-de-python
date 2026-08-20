import json
import os

ARCHIVO_JSON = "conocimiento_ia.json"

def reparar_base_conocimiento():
    if not os.path.exists(ARCHIVO_JSON):
        print("📭 No se encontró ningún archivo 'conocimiento_ia.json' para migrar.")
        return

    print("🔍 Leyendo base de datos local...")
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        try:
            datos = json.load(f)
        except Exception as e:
            print(f"❌ El archivo JSON está corrupto o mal formado: {e}")
            return

    datos_reparados = {}
    contador_migrados = 0

    for llave, bloque in datos.items():
        # Si el bloque es un texto plano (formato viejo), lo transformamos al formato nuevo pro
        if isinstance(bloque, str):
            datos_reparados[llave] = {
                "solucion": bloque,
                "ast": "SyntaxErrorNode",  # Valor por defecto seguro para el matching híbrido
                "meta": {
                    "creado": "Migrado por script",
                    "veces_encontrada": 0,
                    "veces_confirmada": 0,
                    "ultimo_uso": "Nunca"
                }
            }
            contador_migrados += 1
        else:
            # Si ya tenía el formato nuevo, lo dejamos exactamente como estaba
            datos_reparados[llave] = bloque

    # Guardamos los cambios de vuelta en el disco
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(datos_reparados, f, indent=4, ensure_ascii=False)

    print(f"🎉 ¡Migración completada con éxito!")
    print(f"🛠️ Se actualizaron {contador_migrados} registros viejos al nuevo formato relacional AST.")

if __name__ == "__main__":
    reparar_base_conocimiento()
