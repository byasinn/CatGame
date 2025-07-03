def create_scene_data_1():
    return [
        {"background": ["Scene1_1Bg0", "Scene1_1Bg1"], "characters": [], "text": "Leon: Está um silêncio estranho por aqui...", "music": "Scene1.mp3"},
        {"background": ["Scene1_1Bg2"], "characters": [("Leon", "left", "fadein")], "text": "Leon: Será que Mora já chegou?"},
        {"background": ["Scene1_1Bg2"], "characters": [("Mora", "right", "fadein")], "text": "Mora: Estou aqui! Não se assuste!"},
        {"background": ["Scene1_1Bg3"], "characters": [("Leon", "left", "fadein")], "text": "Leon: Que bom!"},
        {"background": ["Scene1_1Bg4"], "characters": [("Mora", "right", "fadein")], "text": "Mora: Vamos lá!"}
    ]

def create_scene_data_2():
    return [
        # Fundo fixo da floresta com 3 camadas
        {"background": ["Scene1_2Bg0", "Scene1_2Bg1", "Scene1_2Bg2"], "characters": [], "text": "Leon: Finalmente, chegamos à floresta...", "music": "Scene2.mp3"},

        {"characters": [("Mora", "right", "fadein")], "text": "Mora: Foi difícil, mas conseguimos..."},
        {"characters": [("Leon", "left", "fadein")], "text": "Leon: Ainda não acredito no que enfrentamos."},

        {"characters": [("Luri", "right", "fadein")], "text": "Luri: Ainda bem que vocês chegaram!"},
        {"characters": [("Leon", "left", "fadein")], "text": "Leon: Luri!? Onde você estava?"},
        {"characters": [("Mora", "right", "fadein")], "text": "Mora: A gente precisava de você lá atrás!"},

        {"characters": [("Luri_rindo", "right", "fadein")], "text": "Luri: Hehe... Eu tava... ocupado... com borboletas."},
        {"characters": [("Luri_assustado", "right", "fadein")], "text": "Luri: ESPERA... vocês ouviram isso?"},

        {"characters": [("Enemy", "left", "fadein")], "text": "??? : Grrrraaahhh..."},
        {"characters": [("Leon_bravo", "left", "fadein")], "text": "Leon: VOCÊ DE NOVO?!"},
        {"characters": [("Mora_brava", "right", "fadein")], "text": "Mora: Não vamos fugir dessa vez!"},

        {"characters": [("Enemy", "left", "fadein")], "text": "??? : Acabou para vocês..."},
        {"characters": [("Luri_assustado", "right", "fadein")], "text": "Luri: Eu... eu protejo a retaguarda!"},
        {"characters": [("Leon_bravo", "left", "fadein")], "text": "Leon: Se preparem!"}
    ]


def create_scene_data_3():
    return [
        {"background": ["Scene1_3_1Bg"], "characters": [], "text": "Mora: Estamos quase lá...", "music": "Scene3.mp3"},
        {"background": ["Scene1_3_2Bg"], "characters": [("Mora", "left", "fadein"), ("Leon", "right", "fadein")], "text": "Leon: Você tem certeza que é seguro?"},
        {"background": ["Scene1_3_3Bg"], "characters": [("Mora", "left", "fadein")], "text": "Mora: Não. Mas não temos escolha."},
        {"background": ["Scene1_3_4Bg"], "characters": [("Mora", "left", "fadein"), ("Luri", "right", "fadein")], "text": "Luri: Finalmente vocês chegaram..."},
        {"background": ["Scene1_3_4Bg"], "characters": [("Leon", "left", "fadein")], "text": "Leon: Luri!? Você tá bem?"}
    ]

SCENE1_DATA = create_scene_data_1()
SCENE2_DATA = create_scene_data_2()
SCENE3_DATA = create_scene_data_3()
