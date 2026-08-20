# 🧠 ia-de-python

> **The Zero-Data, Ultra-Lightweight Autonomous Error-Correction Ecosystem for Python.**

`ia-de-python` es un sistema experto avanzado de depuración local y entorno de ejecución controlado diseñado para interceptar, analizar y autoreparar excepciones de Python en tiempo de ejecución. 

A diferencia de las soluciones tradicionales que saturan la memoria RAM o dependen de APIs comerciales en la nube, este ecosistema implementa un **núcleo híbrido de inferencia semántica basado en Árboles de Sintaxis Abstracta (AST)**. El software tritura el ruido del código, normaliza las firmas de los errores y valida los parches en segundo plano de forma 100% aislada, offline y con **0 MB de dependencia de Internet**.

---

## ⚡ ¿Por qué destaca ia-de-python? (Ventajas Tecnológicas)

*   📴 **Privacidad Absoluta (Zero-Data Architecture)**: Diseñado para entornos corporativos estrictos o aislamiento offline. Ninguna línea de tu código fuente se envía a servidores externos.
*   🪶 **Rendimiento Micro-Core**: Ejecución nativa en milisegundos con un consumo inferior a 5MB de memoria RAM. Eficiencia algorítmica pura.
*   🔮 **Análisis Semántico por AST**: El motor extrae los identificadores del código respetando su orden de aparición física (`lineno` + `col_offset`) e ignora las variables del sistema (como `print` o `len`), permitiendo adaptar soluciones universales a cualquier variable en tiempo de ejecución.
*   📈 **Bucle de Validación Cerrado (Closed-Loop Learning)**: Cuando el cerebro propone un parche, el orquestador lo ejecuta de forma invisible. Si el script corre sin lanzar nuevas excepciones, confirma el éxito y actualiza de forma autónoma su tasa empírica de efectividad.
*   📏 **Matching Híbrido Avanzado (70/30)**: Utiliza un algoritmo nativo de Distancia Levenshtein para medir la similitud de los crashes, tolerando pequeñas variaciones en los mensajes de las librerías externas.

---

## 🛠️ Arquitectura de Ingeniería Modular

El software ha sido desacoplado siguiendo patrones limpios de diseño de software para garantizar un mantenimiento óptimo:
1.  📄 **`main.py`**: Interfaz REPL y entorno de ejecución controlado con protección defensiva de streams de consola (`stdout`).
2.  📄 **`cerebro_local.py`**: El núcleo de inteligencia, normalización léxica, métricas de efectividad y lógica analítica del AST.
3.  📄 **`motor.py`**: Capa de aislamiento encargada de la ejecución dinámica en memoria.
4.  📄 **`reparadores.py`**: Rutinas de formateo y pre-procesamiento del flujo semántico.
5.  📄 **`migrar_json.py`**: Script defensivo para la estandarización y evolución de esquemas de bases de datos JSON antiguas.

---

## 📦 Guía de Despliegue y Uso Profesional

### 1. Inicialización del Entorno
Inicia la suite interactiva ejecutando el orquestador desde tu consola:
```bash
python3 main.py
```

### 2. Flujo de Trabajo REPL
Introduce tu bloque de código (soporta múltiples líneas). Para compilar y ejecutar, escribe el comando `RUN` en una línea vacía y presiona *Enter*.

### 3. Aprendizaje Activo (RLHF Local)
Si el software detecta una excepción nueva, abrirá el canal de entrenamiento. Diseña una plantilla utilizando comodines indexados posicionalmente:
```text
<VAR1> = 0.0; <VAR2> = 100; total = <VAR1> + <VAR2>; print(total)
```
MICA memorizará la firma sintáctica e inyectará los nombres de variables correctos de forma automática la próxima vez que ocurra un error similar.

### 4. Telemetría e Historial
Escribe el comando global `HISTORIAL` en cualquier momento para desplegar la tabla analítica local. Verás el registro exacto de las veces que cada solución fue invocada, confirmada de forma real en background y su **Porcentaje de Efectividad de Reparación**. Para cerrar, usa `SALIR`.

---

## 📄 Licencia
Este ecosistema de ingeniería se distribuye bajo la licencia **MIT**, garantizando una exención total de responsabilidad legal en entornos de producción.
