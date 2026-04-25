# Estudio en escarlata（A Study in Scarlet）— Análisis de deducibilidad

## Información básica
- Autor：Arthur Conan Doyle
- Año：1887
- Género：Novela
- Detective：Sherlock Holmes
- Tipo de misterio central：whodunit + howdunit + whydunit

---

## Evaluación general de la deducibilidad

| Métrica | Calificación | Notas |
|---------|-------------|-------|
| Deducibilidad（Deducibility） | ⭐⭐⭐⭐ | Punto de convergencia promedio 78% — Identidad del asesino：62%；Método del crimen：75%；Motivo completo：90%；Promedio ≈ 76%，cerca del umbral de cuatro estrellas |
| Nivel de niebla（Fog Rating） | ⭐⭐⭐ | Hay una cantidad considerable de pistas falsas，pero la mayor «niebla» es en realidad de carácter estructural——el salto narrativo en la segunda parte deja al lector completamente pasivo，mientras el autor controla todo el ritmo de la revelación de información |

---

## Sinopsis

La historia se divide en dos partes completamente distintas.

**Primera parte（Inglaterra，1881）**：El médico militar retirado John H. Watson conoce a Holmes en Londres y se convierten en compañeros de piso en Baker Street 221B. En una noche de niebla，el detective de Scotland Yard Gregson solicita ayuda：en una casa vacía se ha encontrado el cadáver del ciudadano americano Enoch Drebber——sin heridas，sin robo，con la palabra alemana «RACHE» escrita en sangre en la pared，una gran cantidad de sangre en el suelo que no pertenece a la víctima，y un anillo de boda en la escena. Tras recopilar pruebas，Holmes llega rápidamente a estas conclusiones：el asesino es un hombre alto que llegó en un carruaje de cuatro ruedas，fuma cigarros de Trichinopoly，y el crimen nace de un rencor personal，no de motivos políticos. Poco después，el secretario de la víctima，Joseph Stangerson，es asesinado también en un hotel. Holmes，disfrazado de cochero，identifica al asesino——Jefferson Hope——y lo hace arrestar.

**Segunda parte（Utah，EE.UU.，1847–años 1860）**：El tiempo retrocede treinta años y Doyle narra la historia de fondo desde una perspectiva omnisciente. El explorador John Ferrier lleva consigo a su hija adoptiva Lucy para unirse a una caravana de colonos mormones que marchan hacia el oeste，y se asientan y prosperan en Utah. El joven cazador Jefferson Hope se enamora de Lucy，pero los ancianos mormones utilizan amenazas religiosas para forzar a Lucy a casarse con el hijo de Drebber. Ferrier es asesinado，Lucy muere de pena tras el matrimonio forzado. Hope quita el anillo de boda del dedo muerto de Lucy y emprende un viaje de veinte años persiguiendo a Drebber y Stangerson en busca de venganza.

El sexto capítulo regresa a Londres，donde Hope，tras ser arrestado，relata personalmente los detalles del crimen：fabricó dos píldoras de aspecto idéntico（una venenosa，una inocua），forzó a Drebber a elegir una y tragarla bajo el miedo，mientras él mismo tragaba la otra，apostando su vida. Drebber sacó la pildora envenenada y murió；Hope sufrió un sangrado nasal en su agitación y escribió «RACHE» con la sangre como distracción. Hope murió al día siguiente en prisión por la rotura de un aneurisma，antes de poder ser juzgado.

---

## Disección de la verdad

### Verdad Primera：La identidad del asesino（whodunit）

- **Punto de convergencia：aprox. 62%**
- Respuesta：Jefferson Hope，cochero de Londres，antiguo cazador estadounidense.

#### Pistas clave

| # | Pista | Ubicación（capítulo/porcentaje） | Explicación |
|---|-------|--------------------------------|-------------|
| 1 | El asesino es un hombre alto con pies grandes（zancada ancha），llegó en un carruaje de cuatro ruedas，y el carruaje no se fue hasta después del crimen | Primera parte，cap. 3–4 / aprox. 22% | Holmes declara directamente：estas son las primeras pistas clave que establecen el perfil del asesino，reduciéndolo a «un hombre alto relacionado con un carruaje» |
| 2 | Toda la sangre en la escena proviene del sangrado nasal del asesino（no de la víctima）：la dirección de las manchas de sangre coincide con las huellas del asesino；solo alguien con la cara enrojecida sangra así con tanta agitación | Primera parte，cap. 3 / aprox. 19% | Confirma que el asesino es un individuo de tez rubicunda y complexión robusta；explica también la ausencia de señales de lucha en la escena |
| 3 | Hope había sido denunciado por Drebber en Cleveland，los dos tenían una antigua enemistad：Holmes telegrafía a la policía de Cleveland y recibe la respuesta de que «Drebber había solicitado una orden de alejamiento contra el antiguo rival Jefferson Hope，quien ahora se encontraba en Europa» | Primera parte，cap. 7 / aprox. 47% | **La pista individual más importante**——aquí aparece por primera vez el nombre del asesino；la respuesta del telegrama es el punto de convergencia de la verdad sobre la «identidad del asesino» |
| 4 | La «anciana borracha» es en realidad un hombre joven disfrazado：la anciana desaparece silenciosamente de un carruaje en marcha——el disfraz de un hombre joven y ágil | Primera parte，cap. 5 / aprox. 34% | Muestra que el asesino tiene capacidad para disfrazarse y no actúa completamente solo；también sugiere que esta persona es hábil en el rastreo y el trabajo físico |
| 5 | Los Chicos de Baker Street informan de haber encontrado a un cochero llamado «Jefferson Hope» | Primera parte，cap. 7 / aprox. 51% | Punto de convergencia——identidad confirmada completamente，Holmes pone en marcha su plan de arresto |

#### Pistas de apoyo

| # | Pista | Ubicación（capítulo/porcentaje） | Explicación |
|---|-------|--------------------------------|-------------|
| 1 | La expresión de la víctima Drebber estaba llena de terror，no de dolor——reconoció a quien lo mató | Primera parte，cap. 3 / aprox. 18% | Excluye el crimen por un extraño，apunta a una enemistad personal |
| 2 | Un libro en el bolsillo de la víctima，con el nombre de Stangerson en la portadilla：muestra que los dos hombres estaban íntimamente relacionados，reduce el campo de investigación | Primera parte，cap. 3 / aprox. 20% | Presenta a Stangerson como una línea de investigación |
| 3 | En la habitación de Stangerson se encuentra un telegrama：«J. H. está en Europa»——enviado desde Cleveland un mes antes，sin remitente | Primera parte，cap. 7 / aprox. 44% | Sugiere que Stangerson sabía que alguien los seguía；«J. H.» apunta a Hope（Jefferson Hope） |
| 4 | Dos conjuntos de huellas en la escena：un par de finos zapatos de cuero（la víctima）y un par de botas con punta cuadrada（el hombre alto）——ambos entraron juntos，no en confrontación | Primera parte，cap. 4 / aprox. 22% | Excluye el robo；confirma que los dos «llegaron en el mismo carruaje»，es decir，el asesino no se encontró con la víctima por casualidad |

#### Pistas falsas

| # | Pista | Ubicación（capítulo/porcentaje） | Dirección engañosa |
|---|-------|--------------------------------|-------------------|
| 1 | «RACHE» en la pared——Lestrade cree que significa «Rachel»，sugiriendo la participación de una mujer con ese nombre | Primera parte，cap. 3 / aprox. 21% | Lleva a los lectores a pensar en un crimen pasional o en un factor femenino，desviando la atención |
| 2 | «RACHE» es la palabra alemana para «venganza»——varios periódicos lo asocian con una sociedad secreta socialista o un asesinato político | Primera parte，cap. 6 / aprox. 38% | Dirige la investigación hacia una conspiración política internacional，lo opuesto al caso real（una enemistad personal） |
| 3 | Gregson arresta al subteniente naval Arthur Charpentier——pues efectivamente persiguió a Drebber y su paradero era desconocido | Primera parte，cap. 6 / aprox. 39% | Hace creer a los lectores que el caso está resuelto y desvía la atención del verdadero asesino；desperdicia el tiempo de los lectores con un «sospechoso equivocado» |
| 4 | Lestrade sigue al secretario Stangerson，convencido de que es el cómplice | Primera parte，cap. 6 / aprox. 39% | Dos detectives oficiales se dirigen simultáneamente en la dirección equivocada，creando el efecto caótico de «detectives en desacuerdo» |
| 5 | La «anciana» que viene a recoger el anillo——parece una auténtica anciana que busca el anillo perdido de su hija | Primera parte，cap. 5 / aprox. 33% | Hace que el plan de la «trampa del anillo» de Holmes parezca temporalmente fallido，llevando a los lectores a creer que el juicio de Holmes es erróneo |

---

### Verdad Segunda：El método del crimen（howdunit）

- **Punto de convergencia：aprox. 75%**
- Respuesta：Hope fabricó primero dos píldoras de aspecto idéntico（una venenosa，una inocua），forzó a Drebber a elegir una y tragarla bajo el miedo，mientras él mismo tragaba la otra apostando su vida. Drebber sacó la pildora venenosa y murió；Hope，en su agitación，sufrió un sangrado nasal y escribió «RACHE» con la sangre. En el caso de Stangerson，como este se negó a cooperar，lo apuñaló directamente.

#### Pistas clave

| # | Pista | Ubicación（capítulo/porcentaje） | Explicación |
|---|-------|--------------------------------|-------------|
| 1 | Holmes olfatea los labios del cadáver en la primera escena del crimen y declara：«Envenenado.» | Primera parte，cap. 3 / aprox. 19% | Establece el veneno como el arma del crimen，descartando golpes o estrangulamiento——la víctima no tiene heridas externas pero la muerte fue violenta |
| 2 | Junto a la cama de Stangerson se encuentra «una pequeña caja de píldoras que contiene dos píldoras»——pequeñas，blancas，semitransparentes | Primera parte，cap. 7 / aprox. 45% | El objeto real aparece en escena，pero en este momento ni los lectores ni Lestrade comprenden su importancia |
| 3 | Holmes prueba las píldoras en un perro viejo y enfermo：la primera no tiene efecto，la segunda mata instantáneamente | Primera parte，cap. 7 / aprox. 48% | **La revelación completa del método**——el mecanismo de «una venenosa，una inocua，cada uno toma una» se revela completamente por primera vez aquí；este es el verdadero punto de convergencia del howdunit |
| 4 | La confesión de Hope en el capítulo 6：robó alcaloides de veneno de flecha sudamericanos mientras trabajaba como conserje en York College y fabricó las píldoras él mismo；«había llevado la caja de píldoras consigo en todo momento» antes del crimen | Segunda parte，cap. 6 / aprox. 75% | Explica completamente la fuente del veneno y el proceso de fabricación de las píldoras；la convergencia final de la capa narrativa del howdunit |

#### Pistas de apoyo

| # | Pista | Ubicación（capítulo/porcentaje） | Explicación |
|---|-------|--------------------------------|-------------|
| 1 | La sangre en la escena proviene del asesino（no de la víctima），y las manchas de sangre se superponen con las huellas del asesino | Primera parte，cap. 3 / aprox. 19% | Muestra que el asesino permaneció en la escena por un tiempo y sangró espontáneamente por agitación emocional——descarta la posibilidad de un «crimen instantáneo» |
| 2 | La expresión de la víctima en el primer caso mostraba terror extremo，no inconsciencia ni debilidad——tuvo tiempo de darse cuenta de que estaba a punto de morir | Primera parte，cap. 3 / aprox. 18% | Implica que el veneno tuvo un breve retraso antes de actuar，permitiendo a la víctima ser consciente de su destino |
| 3 | Una palangana con manchas de sangre junto a la ventana de la habitación de Stangerson：el asesino se lavó las manos tranquilamente después del acto | Primera parte，cap. 7 / aprox. 44% | En el segundo caso el asesino tuvo tiempo de lavarse las manos，lo que indica que actuó con calma——en contraste con el «sangrado nasal por agitación» del primer caso |

#### Pistas falsas

| # | Pista | Ubicación（capítulo/porcentaje） | Dirección engañosa |
|---|-------|--------------------------------|-------------------|
| 1 | Charpentier persiguió a Drebber con un garrote de roble（cudgel）——la teoría de Gregson：golpe en el abdomen，muerte repentina | Primera parte，cap. 6 / aprox. 40% | Lleva a los lectores a creer que la causa de la muerte fue un golpe contundente，descartando el envenenamiento y haciendo más difícil resolver el misterio de «sin heridas» |
| 2 | Una gran cantidad de sangre en la escena——a primera vista parece un grave incidente violento | Primera parte，cap. 3 / aprox. 18% | Los lectores tienden a imaginar una lucha o una herida de cuchillo；en realidad la sangre proviene del sangrado nasal del asesino y no tiene nada que ver con la causa de la muerte |

---

### Verdad Tercera：El motivo completo del crimen（whydunit）

- **Punto de convergencia：aprox. 90%**
- Respuesta：Hace veinte años，Drebber（hijo de un anciano mormón）forzó a Lucy Ferrier a casarse con él；el padre de Stangerson mató personalmente a Ferrier；Lucy murió de pena un mes después del matrimonio forzado. Hope juró venganza desde entonces. Este trasfondo se desarrolla en la segunda parte（aprox. 52%–89% del libro）a través de la narración omnisciente，y solo se confirma completamente con la confesión de Hope.

#### Pistas clave

| # | Pista | Ubicación（capítulo/porcentaje） | Explicación |
|---|-------|--------------------------------|-------------|
| 1 | La ropa de la víctima no parece de fabricación británica——identidad americana y dirección de Cleveland | Primera parte，cap. 3 / aprox. 20% | Sugiere que la raíz del crimen puede estar en América y no en Gran Bretaña |
| 2 | Holmes declara en la escena：«No es un asesinato político——es una enemistad personal；el anillo indica que esto involucra a una mujer muerta o desaparecida.» | Primera parte，cap. 3 / aprox. 21% | Convergencia temprana de la dirección del motivo——descarta la política，apunta a una venganza amorosa o familiar；pero «quién es la mujer» sigue siendo un misterio |
| 3 | Respuesta del telegrama：Drebber había solicitado una orden de alejamiento contra el «antiguo rival» Hope | Primera parte，cap. 7 / aprox. 47% | Primera evidencia documental concreta de una «disputa amorosa»，reduciendo el motivo de «enemistad personal» a «odio romántico» |
| 4 | Segunda parte（narración omnisciente）：la historia completa de la familia Ferrier y los mormones，el romance de Lucy y Hope，el matrimonio forzado y la muerte | Segunda parte，cap. 1–5 / aprox. 52%–81% | Desarrollo completo del motivo；los lectores solo conocen los eventos concretos ahora，pero el autor controla completamente la cantidad de información que se da al lector |
| 5 | La confesión de Hope：«Esa chica debía haberse casado conmigo. Fue forzada a casarse con Drebber y murió de pena. Tomé el anillo de su dedo muerto y juré que él lo vería cuando muriera.» | Segunda parte，cap. 6 / aprox. 88% | **La convergencia final del motivo**——todos los misterios（por qué el anillo estaba en la escena，por qué el asesino necesitaba que la víctima lo reconociera antes de morir）se resuelven en esta única declaración |

#### Pistas de apoyo

| # | Pista | Ubicación（capítulo/porcentaje） | Explicación |
|---|-------|--------------------------------|-------------|
| 1 | El anillo de boda en la escena y su conexión con «una mujer»——Holmes：«El asesino utilizó este anillo para recordar a la víctima sus crímenes.» | Primera parte，cap. 3 / aprox. 21% | Ya implica que el motivo es pedir cuentas a la víctima por algún acto del pasado，pero el «crimen concreto» aguarda la revelación posterior |
| 2 | Antes del crimen，Drebber había intentado propasarse con la hija de Charpentier y fue expulsado——es un hombre naturalmente licencioso que puede haber actuado de manera similar en el pasado | Primera parte，cap. 6 / aprox. 39% | Refuerza el carácter de «villano» de Drebber，da a los lectores una impresión negativa de él，y hace más razonable la inferencia de que «tuvo víctimas en el pasado» |
| 3 | El telegrama de Stangerson «J. H. está en Europa»——siempre supieron que alguien los perseguía | Primera parte，cap. 7 / aprox. 44% | Muestra que Drebber y Stangerson no son inocentes；sabían que tenían un «enemigo» pero nunca admitieron públicamente el motivo |

#### Pistas falsas

| # | Pista | Ubicación（capítulo/porcentaje） | Dirección engañosa |
|---|-------|--------------------------------|-------------------|
| 1 | «RACHE» + la teoría de la «conspiración política» de varios periódicos | Primera parte，cap. 6 / aprox. 37%–38% | Desvía el motivo de la enemistad personal hacia la persecución política o religiosa——la pista falsa de motivo más eficaz |
| 2 | La disputa entre el alojamiento de Drebber y la familia Charpentier——el subteniente persigue a Drebber por el honor familiar | Primera parte，cap. 6 / aprox. 39% | Proporciona un «motivo alternativo plausible»，haciendo que Charpentier parezca la persona con mayor motivación para cometer el crimen |

---

## Reconstrucción del camino deductivo

### Primer camino：Identificar el tipo de asesino（whodunit）

Un lector atento ya tiene suficientes pistas físicas en el tercer capítulo de la primera parte（aprox. 19%）：las huellas del carruaje de cuatro ruedas，el paso del hombre alto，el origen de la sangre que no pertenece a la víctima. En este punto debería poder deducir：**El asesino es un hombre grande y robusto relacionado con el negocio de los carruajes，y tiene alguna conexión pasada con la víctima**（porque la expresión de la víctima estaba llena de terror——reconoció al otro）.

En el cuarto capítulo（aprox. 22%），«Patent-leather（la víctima）y Square-toes（el asesino）entraron amigablemente juntos»，lo que muestra que el asesino no esperó en emboscada sino que guió a la víctima hacia adentro——un hombre con un plan premeditado.

En el quinto capítulo（aprox. 34%），la «anciana» disfrazada resulta ser un hombre joven y ágil，lo que muestra que el asesino no actúa completamente solo y tiene capacidad de disfraz.

En el séptimo capítulo（aprox. 47%），la respuesta del telegrama contiene el nombre «Jefferson Hope»——en este punto un lector con verdadera capacidad deductiva debería razonablemente sospechar que esta persona es el asesino. Cuando los Chicos de Baker Street encuentran a Hope（aprox. 51%），la identidad queda confirmada.

### Segundo camino：Descifrar el método del crimen（howdunit）

«Sin heridas，gran cantidad de sangre，expresión de terror de la víctima»——estos tres elementos aparecen simultáneamente en el tercer capítulo（19%），formando ya un poderoso misterio. Después de que Holmes huela los labios del cadáver en la escena y declare «Envenenado»，un lector que acepte este juicio debería comenzar a preguntarse：**¿Qué tipo de veneno? ¿Cómo se obliga a alguien a tomarlo?**

En el séptimo capítulo aparece la caja de píldoras（45%），pero Lestrade la considera sin importancia. Esta es una pista importante colocada a plena vista. La prueba de las píldoras de Holmes（48%）es la revelación final：el mecanismo de píldoras «una venenosa，una inocua»，el asesino diseñó que la víctima eligiera su propio destino——un método de asesinato ritual con matiz de retribución divina. El cuadro completo del método converge aquí.

### Tercer camino：Entender el motivo（whydunit）

Este es el camino que converge más tarde. Todas las pistas dadas en la primera parte（una mujer，víctimas americanas，una enemistad personal）solo son suficientes para que el lector conozca la «dirección general». La segunda parte（después del 52%）es lo que finalmente permite a los lectores conocer el cuadro completo de los eventos. Este diseño es inusual en las novelas policiacas——**el autor elige obligar a los lectores a comprender la legitimidad del motivo antes de que se resuelva el misterio**，pero el precio es que los lectores no pueden deducir este trasfondo histórico por sí mismos y solo pueden recibirlo pasivamente.

La confesión de Hope（88%）es lo que finalmente une los tres caminos：por qué el anillo estaba en la escena（porque quería que Drebber lo viera cuando muriera），por qué había tanta sangre（un sangrado nasal，causado por la agitación），qué es «RACHE»（fue una distracción improvisada——Hope mismo admite que fue un impulso del momento）.

---

## Notas adicionales

### El lugar especial de este libro en la historia de la novela policíaca

*Estudio en escarlata* es la primera novela de la serie Holmes y el primer trabajo en el que Doyle demuestra sistemáticamente la «deducción» como herramienta detectivesca. Sin embargo，desde el punto de vista del diseño del misterio，es **una obra fundacional estructuralmente contradictoria**.

**El problema estructural más fundamental：El costo de la narrativa «en dos partes»**

Esta novela consiste en dos narrativas completamente diferentes. La primera parte（Inglaterra，presente）es una novela policíaca estándar donde el lector recopila pistas junto a Holmes. La segunda parte（América，pasado）es una novela histórica del oeste que describe eventos de treinta años antes desde una perspectiva omnisciente——y esta historia era completamente desconocida para el lector en la primera parte. Esto significa：**Toda la información clave sobre el motivo es transmitida al lector por el autor como «antecedentes históricos insertados»，no deducida por el lector mismo.**

Esta es una elección especial en la literatura detectivesca. Hace que la dimensión del «whydunit» sea casi imposible de deducir con anticipación por el lector——porque las pistas simplemente no existen en el mismo espacio narrativo. El mecanismo de compensación de Doyle es hacer que los lectores simpaticen con la «legitimidad» del motivo：una vez que conocen la historia de Hope，a los lectores les resulta difícil verlo puramente como un criminal que merecía ser capturado.

### La ambigüedad moral de Hope：El primer «vengador justo» de la historia de la novela policíaca

Jefferson Hope es un tipo de asesino extremadamente raro en la historia de la novela policíaca：no niega haber matado，cree ser un «ejecutor de justicia»，y muere con una sonrisa plácida en su rostro. Al final de la historia，los periódicos informan que el caso «deja saber a los extranjeros que deben resolver sus rencillas en su propio país，no traerlas a Inglaterra»——Doyle borra deliberadamente con esto la evaluación moral del caso.

La figura de Hope prefigura una tradición importante en las novelas policíacas posteriores：**el justo que se ve obligado a tomar el camino de la venganza**. Su método de asesinato（hacer que las víctimas apuesten su vida）también lleva un sabor casi veterotestamentario de juicio divino——«dejar que Dios decida quién vive y quién muere». La complejidad moral de este diseño forma un interesante contraste con la venganza obsesiva de Poe en *El tonel de amontillado*.

### La función demostrativa de la metodología de Holmes

Desde el punto de vista de la deducibilidad，lo interesante en este libro es que muchos de los procesos de razonamiento de Holmes se producen cuando él **explica los pasos a Watson（y por ende al lector）solo después de haberlos completado**. En el tercer capítulo ya declara que es «envenenamiento»，que el asesino es «alto»，que el asesino está «relacionado con un carruaje»——pero la explicación metodológica detallada no llega hasta la sección de conclusión del séptimo capítulo. Este diseño hace muy difícil que el lector «deduzca en paralelo con Holmes»——lo que observamos es una deducción ya completada，no un proceso en desarrollo.

Esto contrasta fuertemente con el diseño de la etapa madura de Agatha Christie. Christie coloca todas las pistas frente al lector，dando a los lectores la oportunidad（aunque muy difícil）de deducir la respuesta por sí mismos. El diseño temprano de Doyle se acerca más a «un espectáculo de actuación de un gran detective»——Holmes es el protagonista，el lector es el público，no un competidor en el mismo escenario de deducción.

### «RACHE»：El diseño de pista falsa más exitoso

Esta palabra escrita en sangre es uno de los elementos más ingeniosamente diseñados en *Estudio en escarlata*. En un solo movimiento logra tres cosas：

1. **Engaña a Lestrade**（lo hace buscar a una mujer llamada Rachel）
2. **Engaña a la prensa y a los lectores**（los hace pensar en una sociedad secreta política alemana）
3. **Más tarde se revela como el propio acto improvisado del asesino**——Hope admite que recordó un caso de asesinato relacionado con alemanes en Nueva York y lo usó espontáneamente para confundir a la policía

Lo interesante de «RACHE» es esto：es tanto una pista falsa como una pista real. Efectivamente apunta a la «venganza»——que es el verdadero motivo——pero leerla como alemán desvía la investigación por un camino erróneo. Solo un lector que piense sin prejuicios sobre qué significa «venganza» en sí misma tiene la posibilidad de adivinar el núcleo del motivo en la primera parte.

### Comparación con obras contemporáneas

| | Estudio en escarlata（1887） | El tonel de amontillado（1846） | Los crímenes de la calle Morgue（1841） |
|--|--|--|--|
| Rol del detective | Holmes（detective externo） | Ninguno（el asesino es el narrador） | Dupin（detective externo） |
| Preguntas fundamentales | Quién，cómo，por qué | Cómo，por qué（nunca seguro） | Quién，cómo |
| ¿Pueden los lectores deducir por sí mismos？ | Parcialmente（whodunit）；whydunit casi imposible | Casi imposible（el narrador controla todo） | Sí（todas las pistas ya presentadas） |
| Postura moral | Deliberadamente ambigua——simpatiza con el asesino | Sin juicio——los lectores deciden por sí mismos | Clara——el asesino es un monstruo |
| Innovación narrativa | Estructura en dos partes，demostración pedagógica de la metodología detectivesca | Narrador no fiable | Invención del género de la novela policíaca |

Doyle logró simultáneamente en esta obra dos objetivos：«establecer la imagen de un personaje detective» y «contar una historia completa»——pero estos dos objetivos tienen una cierta tensión en la estructura narrativa. La novela policíaca requiere que los lectores participen en el razonamiento；la narratividad requiere que el autor controle el ritmo de la liberación de información. Esta contradicción no está completamente resuelta en *Estudio en escarlata*，pero es precisamente por eso que se ha convertido en uno de los especímenes históricos más interesantes de la literatura detectivesca.
