#!/usr/bin/env python

marcos_libres = [0x0, 0x1, 0x2]
reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
segmentos = [('.text', 0x00, 0x1A),
             ('.data', 0x40, 0x28),
             ('.heap', 0x80, 0x1F),
             ('.stack', 0xC0, 0x22),
             ]


def procesar(segmentos, reqs, marcos_libres):
    PAGE_SIZE = 16
    tabla_paginas = {}  # páginas cargadas
    cola_fifo = []      # orden de asignación
    resultados = []
    free_frames = list(marcos_libres)

    for req in reqs:
        # Verificar si pertenece a algún segmento
        segmento_valido = False
        for nombre, base, limite in segmentos:
            if base <= req < base + limite:
                segmento_valido = True
                break

        if not segmento_valido:
            resultados.append((req, 0x1FF, "Segmentation Fault"))
            break

        pagina = req // PAGE_SIZE
        offset = req % PAGE_SIZE

        if pagina in tabla_paginas:
            marco = tabla_paginas[pagina]
            accion = "Marco ya estaba asignado"
        else:
            if free_frames:
                marco = free_frames.pop(0)
                tabla_paginas[pagina] = marco
                cola_fifo.append(pagina)
                accion = "Marco libre asignado"
            else:
                victima = cola_fifo.pop(0)
                marco = tabla_paginas.pop(victima)
                tabla_paginas[pagina] = marco
                cola_fifo.append(pagina)
                accion = "Marco asignado"

        direccion_fisica = marco * PAGE_SIZE + offset
        resultados.append((req, direccion_fisica, accion))

    return resultados


def print_results(results):
    for result in results:
        print(
            f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")


if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)
