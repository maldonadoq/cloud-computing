from random import randint

dataset = ["humano","persona","gente","hombre","mujer","familia","amigo","conocido","colega","pareja","esposo","matrimonio",
			"amor","criatura","especie","ser","vida","naturaleza","campo","bosque","selva","jungla","desierto","costa","playa",
			"río","laguna","lago","mar","océano","cerro","monte","montaña", "cuerpo", "pie", "pierna", "talón", "espinilla",
			"rodilla", "muslo", "cabeza", "cara", "boca", "labios", "diente", "nariz", "bigote", "cabello", "oreja", "cerebro",
			"estómago", "brazo", "codo", "hombro", "uña", "mano", "muñeca", "palma", "dedo", "trasero", "culo", "cola", "glúteos",
			"abdomen", "hígado", "músculo", "cuello", "corazón", "mente", "alma", "cintura", "cadera", "corazón", "espalda",
			"sangre", "carne", "piel", "hueso", "pecho", "resfriado", "diarrea", "enfermedad", "abuela", "abuelo", "esposa",
			"esposo", "hermana", "hermano", "hija", "hijo", "madre", "nieta", "nieto", "padre", "prima", "primo", "tía", "tío",
			"sobrino", "sobrina", "bisabuelo", "bisabuela", "animal", "perro", "gato", "vaca", "cerdo", "caballo", "yegua", "oveja",
			"mono", "ratón", "rata", "tigre", "conejo", "dragón", "ciervo", "rana", "león", "jirafa", "elefante", "pájaro", "gallina",
			"gorrión", "cuervo", "águila", "halcón", "pez", "camarón", "langosta", "sardina", "atún", "calamar", "pulpo", "insecto",
			"bicho", "mariposa", "polilla", "saltamontes", "araña", "mosca", "mosquito", "cucaracha", "caracol", "babosa", "lombriz",
			"marisco", "molusco", "lagarto", "serpiente", "cocodrilo", "plantas", "pasto", "césped", "flor", "fruta", "semilla",
			"árbol", "hoja", "raíz", "tallo", "hongo", "ciruela", "pino", "bambú", "nuez", "almendra", "castaña", "Cosechas",
			"arroz", "avena", "cebada", "trigo", "vegetal", "verdura", "patatas", "papas", "judías", "guisantes", "porotos",
			"rábano", "zanahoria", "manzana", "naranja", "plátano", "pera", "castaño", "durazno", "tomate", "sandía", "alimento",
			"comida", "bebida", "carne", "gaseosa", "tiempo", "calendario", "edad", "época", "era", "fecha", "segundo", "minuto",
			"hora", "día", "semana", "mes", "año", "ayer", "hoy", "mañana", "amanecer", "mediodía", "tarde", "anochecer", "noche",
			"lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo", "ambiente", "espacio", "entorno", "sol", "luna",
			"estrella", "clima", "despejado", "nublado", "lluvia", "nieve", "viento", "trueno", "rayo", "tifón", "tormenta", "cielo",
			"este", "oeste", "sur", "norte", "derecha", "izquierda", "arriba", "encima", "abajo", "debajo", "adelante", "delante",
			"atrás", "detrás", "centro", "medio", "encima", "alrededor", "diagonal", "enfrente", "cerca", "lejos", "adentro", "dentro",
			"afuera", "fuera", "aquí", "acá", "ahí", "allá", "allí", "exterior", "interior", "agua", "caliente", "calor", "frío",
			"fresco", "hielo", "vapor", "fuego", "gas", "aire", "atmósfera", "tierra", "suelo", "metal", "metálico", "hierro", "cobre",
			"oro", "plata", "plomo", "sal", "barro", "lodo", "arcilla", "yeso"]

def mprint(data):
    for word in data:
    	print(word)

def mgenerate(filename, data, count):
	msize = len(data)-1
	f = open(filename,"w+")

	for i in range(count):
		r = randint(0, msize)
		f.write(data[r] + "\n")
		# print(data[r])

	f.close()

if __name__ == "__main__":
	#mprint(dataset)
	mgenerate("data/input.txt", dataset, 10)