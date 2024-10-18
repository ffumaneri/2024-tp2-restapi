# TUP - UTN - Trabajo práctico 2

## Objectivo

Crear una RestAPI con FastAPI para hacer un ABM de Autos en memoria.

## Métodos

`POST /auto`
`GET /auto/ALL`
`GET /auto/{ID}`
`DELETE /auto/{ID}`
`PATCH /auto/{ID}`

## Entidad Auto

```
{
"id": int
"marca": str
"modelo": str
}
```

Los datos se garabarán en una arreglo en memoria. Tendrá el siguiente formato:

```
[
{"id": 1, "marca":"Ford", "modelo": "Mondeo"},
{"id": 1, "marca":"Fiat", "modelo": "Uno"},
{"id": 1, "marca":"Renault", "modelo": "Sandero"},
]
```

