# Proyecto de Compilador

**Integrantes:**
   Eduardo Erices,
   Benjamin Gilberto,
   Silas Vieira.
   
**Paralelo:**
 C2
   
Este proyecto consiste en un compilador diseñado para un lenguaje de programación funcional propio, desarrollado con la herramienta PLY (Python Lex-Yacc). El lenguaje permite la creación de programas mediante funciones, variables, estructuras de control y operaciones, con la posibilidad de escribir el código en inglés o español como diferenciador principal.

## Características del Lenguaje

1. **Soporte multilingüe:**
   - Las palabras clave del lenguaje (como `if/si`, `print/mostrar`, `while/mientras`, etc.) pueden usarse en inglés o español indistintamente.

2. **Funciones:**
   - Permite la definición de funciones con parámetros y valores de retorno mediante la palabra clave `func/funcion`.

3. **Asignación de variables:**
   - Soporte para diferentes tipos de datos (enteros, flotantes, cadenas, caracteres, booleanos y listas).

4. **Control de flujo:**
   - Incluye estructuras como condicionales (`if/si`, `else/sino`) y ciclos (`while/mientras`, `for/para`).

5. **Operaciones:**
   - Soporta operadores aritméticos (`+`, `-`, etc.), lógicos (`&&`, `||`, `!`) y de comparación (`<`, `>`, `==`, etc.).

6. **Manipulación de listas:**
   - Funciones avanzadas como `append` (añadir), `remove` (eliminar), `length` (longitud) y más.

7. **Entrada/Salida:**
   - Uso de `print/mostrar` para imprimir resultados y `input/entrada` para leer datos del usuario.

## Descripción del Compilador

El compilador se compone de tres fases principales:

1. **Análisis Léxico:**
   - Identifica los componentes básicos del lenguaje como palabras clave, operadores y literales.

2. **Análisis Sintáctico:**
   - Valida las estructuras del código mediante reglas gramaticales, generando un Árbol de Sintaxis Abstracta (AST).

3. **Ejecución:**
   - Interpreta el AST, permitiendo la evaluación de expresiones y la ejecución de instrucciones.

El manejo de errores es robusto, con mensajes claros para errores léxicos, sintácticos y de ejecución, facilitando la depuración por parte del usuario.

## Ejemplos de Uso de los Requerimientos

### 1. Asignación y Operaciones Aritméticas
**Entrada:**
```python
x = 10;
y = 20;
result = x + y * 2;
print("El resultado es:", result);

a = 15;
b = 5;
resultado = a / b - 2;
mostrar("The result is:", resultado);
```

**Salida:**
```
El resultado es: 50
The result is: 1.0
```

### 2. Uso de Condicionales (if/else)
**Entrada:**
```python
edad = 18;
if (edad >= 18) {
    mostrar("You are an adult");
} else {
    print("Eres menor de edad");
}

x = 30;
y = 25;
si (x > y) {
    mostrar("x es mayor que y");
} sino {
    print("y is greater or equal to x");
}
```

**Salida:**
```
You are an adult
x es mayor que y
```

### 3. Ciclos (while/for)
**Entrada:**
```python
i = 0;
mientras (i < 5) {
    print("Iteración:", i);
    i = i + 1;
}

for (j = 0; j < 3; j = j + 1) {
    mostrar("Loop iteration:", j);
}
```

**Salida:**
```
Iteración: 0
Iteración: 1
Iteración: 2
Iteración: 3
Iteración: 4
Loop iteration: 0
Loop iteration: 1
Loop iteration: 2
```

### 4. Definición y Llamada de Funciones
**Entrada:**
```python
func greet(name) {
    mostrar("Hola, " + name + "! Welcome!");
}
greet("Carlos");

funcion suma(a, b) {
    returna a + b;
}
resultado = suma(4, 6);
print("El resultado de la suma es:", resultado);
```

**Salida:**
```
Hola, Carlos! Welcome!
El resultado de la suma es: 10
```

### 5. Manipulación de Listas
**Entrada:**
```python
my_list = [1, 2, 3];
append(my_list, 4);
mostrar("La lista es ahora:", my_list);

mi_lista = [10, 20, 30];
insert(mi_lista, 1, 15);  // Inserta 15 en la posición 1
print("The updated list is:", mi_lista);

remove(mi_lista, 20);  // Elimina el 20
mostrar("Lista actualizada:", mi_lista);
```

**Salida:**
```
La lista es ahora: [1, 2, 3, 4]
The updated list is: [10, 15, 20, 30]
Lista actualizada: [10, 15, 30]
```

### 6. Entrada del Usuario
**Entrada:**
```python
nombre = entrada("What is your name?: ");
mostrar("Hola,", nombre, "! Welcome to the program.");

edad = input("¿Cuántos años tienes?: ");
print("You are", edad, "years old.");
```

Supongamos que el usuario escribe:
```
What is your name?: Juan
¿Cuántos años tienes?: 25
```

**Salida:**
```
Hola, Juan! Welcome to the program.
You are 25 years old.
```

### 7. Funciones con Retorno
**Entrada:**
```python
func multiply(a, b) {
    returna a * b;
}
resultado = multiply(5, 3);
mostrar("The result of the multiplication es:", resultado);

funcion factorial(n) {
    si (n <= 1) {
        returna 1;
    } sino {
        returna n * factorial(n - 1);
    }
}
print("El factorial de 4 es:", factorial(4));
```

**Salida:**
```
The result of the multiplication es: 15
El factorial de 4 es: 24
```

### 8. Uso Combinado (Multifuncionalidad)
**Entrada:**
```python
func fibonacci(n) {
    if (n <= 1) {
        returna n;
    } else {
        returna fibonacci(n - 1) + fibonacci(n - 2);
    }
}

x = 5;
mostrar("The Fibonacci of", x, "es:", fibonacci(x));

lista = [1, 2, 3];
append(lista, 4);
mostrar("Updated list:", lista);
```

**Salida:**
```
The Fibonacci of 5 es: 5
Updated list: [1, 2, 3, 4]
```
