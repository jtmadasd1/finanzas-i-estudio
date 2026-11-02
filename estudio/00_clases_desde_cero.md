# Clases desde cero (Control 2)

Lo que vimos en el chat de estudio, en orden. Cada bloque tiene la idea, la fórmula, un ejemplo resuelto y un ejercicio con la respuesta escondida.

**Ruta:** ① Forwards y futuros → ② Opciones: pagos y paridad put-call → ③ Árbol binomial → ④ Black-Scholes → ⑤ Tarea → ⑥ Simulacro.

**VaR no entra en el Control 2** (lo dijo el profesor), así que no está en la ruta.

**Avance:** el bloque ① está visto completo; el ejercicio final (forward corto y dólar) está pendiente. Sigue el bloque ②.

---

## Bloque ① · Forwards (parte 1)

### Qué es

Un **forward** es un contrato que se firma hoy para comprar o vender un activo en una fecha futura **T**, a un precio **K** que se fija hoy.

- Hoy **no se paga nada**: el contrato parte valiendo cero.
- **Largo** (*long*): te comprometes a **comprar**. En T ganas **S_T − K**.
- **Corto** (*short*): te comprometes a **vender**. En T ganas **K − S_T**.

Un **futuro** es lo mismo, pero se transa en bolsa, está estandarizado y tiene **mark-to-market** (ver la parte 2).

### Precio forward sin dividendos

> F₀ = S₀ · e^(rT)

**Intuición:** tener el activo en T se puede lograr de dos maneras:

- firmar el forward y pagar F₀ en T;
- pedir prestado S₀ hoy, comprar el activo y devolver S₀·e^(rT) en T.

Como las dos terminan igual, deben costar lo mismo. Si no, hay **arbitraje**:

| Si en el mercado… | Haces (hoy) | En T |
| --- | --- | --- |
| F₀ > S₀e^(rT) (forward **caro**) | Pides prestado S₀, compras el activo y **vendes** el forward | Entregas el activo, recibes F₀, pagas S₀e^(rT) y te queda la diferencia |
| F₀ < S₀e^(rT) (forward **barato**) | Vendes corto el activo, inviertes S₀ y **compras** el forward | Recibes S₀e^(rT), pagas F₀ por el activo y lo devuelves |

La regla para no perderse: **vendes lo caro y compras lo barato.** En el control, toda pregunta de arbitraje pide tres cosas: qué haces, los flujos y cuánto ganas.

### Precio forward con dividendos

Quien tiene el forward **no recibe los dividendos**, así que el forward vale menos. A S₀ se le resta **I**, el valor presente de los dividendos:

> F₀ = (S₀ − I) · e^(rT)

> I = Σ Dᵢ · e^(−r·tᵢ)

- **Dᵢ** es el monto de cada dividendo.
- **tᵢ** es el tiempo en años desde hoy hasta ese dividendo (no hasta T).
- Solo cuentan los dividendos que se pagan **antes de T**.

| Caso | Fórmula |
| --- | --- |
| Tasa compuesta anual (no continua) | I = Σ Dᵢ / (1 + r)^tᵢ |
| Dividendo como tasa continua **q** (índices, monedas) | F₀ = S₀·e^((r − q)T); aquí no hay I |

**Ejemplo con un dividendo:** S₀ = 50, dividendo de 2 en 3 meses, r = 6% continua, forward a 6 meses.

1. I = 2·e^(−0,06·0,25) = 2 · 0,9851 = **1,970**
2. F₀ = (50 − 1,970)·e^(0,06·0,5) = 48,030 · 1,0305 = **49,49**

**Ejemplo con dos dividendos:** pagos de 1 a los 2 meses y de 1 a los 5 meses, r = 6%: I = e^(−0,06·2/12) + e^(−0,06·5/12) = 0,9900 + 0,9753 = **1,9654**.

### ✏️ Ejercicio

S₀ = 30, sin dividendos, r = 8% continua, T = 1 año. En el mercado, el forward se transa a 34. (a) ¿Cuál es el precio forward teórico? (b) ¿Hay arbitraje?

<details><summary>Ver respuesta</summary>

(a) F₀ = 30·e^(0,08) = **32,50**.

(b) Sí: el forward de mercado (34) está caro. Hoy pides prestado 30, compras la acción y vendes el forward a 34. En T entregas la acción y recibes 34, devuelves 32,50 del préstamo y **ganas 1,50 por acción**.

</details>

---

## Bloque ① · Forwards (parte 2)

### 1. Valor de un forward ya firmado

Lo firmaste antes a un precio **K**. Hoy (t), el forward al mismo vencimiento se transa a **F_t**:

> f(largo) = (F_t − K) · e^(−r(T−t))          f(corto) = (K − F_t) · e^(−r(T−t))

Si no hay dividendos, el atajo es **f(largo) = S_t − K·e^(−r(T−t))**.

**Intuición:** puedes cerrar tomando la posición contraria a F_t. La diferencia entre F_t y K queda asegurada para T y la traes a valor presente.

**Ejemplo:** forward largo con K = 32,50 a 1 año. Pasan 6 meses y la acción vale 33. Entonces F_t = 33·e^(0,04) = 34,35 y f = (34,35 − 32,50)·e^(−0,04) = **1,78**: ganas.

### 2. Paridad cubierta de tasas (forward de dólar)

S está en CLP por USD y las tasas son anuales compuestas:

> F = S · (1 + r_CLP) / (1 + r_USD)

Para T distinto de 1 año, la fracción va elevada a T. Con tasas continuas: F = S·e^((r_CLP − r_USD)T).

**Intuición:** hay dos formas de tener pesos en un año: invertir en pesos, o pasarlos a dólares, invertirlos en dólares y venderlos forward. Las dos deben rendir lo mismo. Por eso **la moneda con tasa más alta vale menos en el forward.**

**Arbitraje si el forward de mercado está sobre el teórico** (vendes lo caro, o sea, vendes dólares forward):

1. Pides prestado CLP.
2. Compras USD spot.
3. Inviertes esos USD a r_USD.
4. Vendes los USD forward.

### 3. Mark-to-market (futuros)

Cada día, la cuenta de margen se ajusta por el cambio en el precio del futuro:

> Ganancia diaria (largo) = (F_hoy − F_ayer) × unidades por contrato × n° de contratos

- **Margen inicial:** lo que depositas al entrar.
- **Margen de mantención:** el piso de la cuenta. Si el saldo cae bajo el piso llega un **margin call**, y tienes que depositar hasta volver al **margen inicial**, no solo hasta el piso.

**Ejemplo:** largo en 2 contratos de 100 unidades a F = 50. El margen inicial es 2.000 y la mantención 1.500.

| Día | F | Ganancia | Saldo |
| --- | --- | --- | --- |
| 1 | 48 | (48 − 50)·200 = −400 | 1.600 (sobre el piso, sin aviso) |
| 2 | 47 | (47 − 48)·200 = −200 | 1.400 &lt; 1.500 → **margin call de 600** (para volver a 2.000) |

### ✏️ Ejercicio (pendiente en el chat)

(a) Hace 3 meses firmaste un forward **corto** a 1 año con K = 52, sobre una acción sin dividendos. Hoy S = 50 y r = 6% continua. ¿Cuánto vale tu posición?

(b) Dólar spot a 900 CLP, r_CLP = 6% y r_USD = 3% (anuales compuestas). ¿Cuál es el forward teórico a 1 año? Si el mercado lo transa a 940, ¿vendes o compras dólares forward?

<details><summary>Ver respuesta</summary>

(a) Quedan 0,75 años. f(corto) = 52·e^(−0,06·0,75) − 50 = 49,71 − 50 = **−0,29**: pierdes, porque la acción subió en relación con lo que pactaste.

(b) F = 900 · 1,06 / 1,03 = **926,21**. El mercado (940) está caro, así que **vendes dólares forward**: pides prestado 900 CLP (debes 954 en un año), compras 1 USD, lo inviertes al 3% (1,03 USD) y vendes 1,03 USD forward a 940, lo que da 968,20 CLP. Ganancia: 968,20 − 954 = **14,20 CLP**.

</details>
