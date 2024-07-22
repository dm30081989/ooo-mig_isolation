
# функции, определ€ющие коэф. из ѕ”Ё

# 1.9.3 автодороги в зимнее врем€
def pue_road(distance: float):
    if distance < 25:
        return 3
    elif distance < 100:
        return 2
    return 1

# 1.9.3 химические
def pue_chemistry(volume: float, distance: float, height: float):

    chemistry_table = [[1, 1, 1, 1, 1, 1, 1, 1,], 
                   [2, 1, 1, 1, 1, 1, 1, 1,], 
                   [3, 2, 1, 1, 1, 1, 1, 1,], 
                   [3, 3, 2, 1, 1, 1, 1, 1,], 
                   [4, 3, 3, 2, 2, 1, 1, 1,], 
                   [4, 4, 3, 3, 3, 2, 2, 1,],]
    
    row, column = 0, 0
    
    if 9 < volume < 500:
        row = 1
    elif 0 < volume // 500 < 7:
        row = (3 + volume // 500) // 2
    elif volume > 3499:
        row = 5

    if distance // 500 < 6:
        column = distance // 500
    elif distance < 5000:
        column = 6
    else:
        column = 7

    return chemistry_table[int(row)][int(column)]

# 1.9.6 целюлоза и бумага
def pue_paper(volume: float, distance: float, height: float):
    return 1

def pue_cellulose(volume: float, distance: float, height: float):
    
    if 74 < volume < 150 and distance < 500:
        return 2

    elif 149 < volume < 500 and distance < 500:
        return 3
        
    elif 149 < volume < 500 and distance < 1000:
        return 2

    elif 499 < volume < 1000 and distance < 500:
        return 4

    elif 499 < volume < 1000 and distance < 1000:
        return 3
        
    elif 499 < volume < 1000 and distance < 1500:
        return 2

    return 1

# 1.9.7 черна€ металлурги€
# чугун и сталь
def pue_ferrous_metallurgy_1(volume: float, distance: float, height: float):
    
    if distance < 500 and volume < 7500:
        return 2

    elif distance < 500:
        return 3

    elif distance < 1500 and volume < 1500:
        return 1

    elif distance < 1500:
        return 2

    elif 1499 < distance < 2000 and volume > 7499:
        return 2

    return 1

# горнообогатительные комбинаты
def pue_ferrous_metallurgy_2(volume: float, distance: float, height: float):

    if distance < 500 and volume > 5499:
        return 3

    elif distance < 500 and volume > 1999:
        return 2

    elif distance < 500:
        return 1

    elif distance < 1000 and volume > 5499:
        return 2

    elif distance < 1000 and volume > 9999:
        return 3

    elif 999 < distance < 1500 and volume > 9999:
        return 2

    return 1

# коксохимпроизводсвто 
def pue_ferrous_metallurgy_3(volume: float, distance: float, height: float):
    
    if distance > 2499:
        return 1

    elif 5000 < volume < 12000 and distance < 500:
        return 3
        
    return 2

# 1.9.8 цветна€ металлурги€
def pue_aluminum(volume: float, distance: float, height: float):

    if volume > 499 and distance < 1000:
        return 3

    elif 2000 > volume > 999 and 1500 > distance > 999:
        return 3

    elif 500 > volume > 99 and distance < 1000:
        return 2

    elif 1000 > volume > 499 and 2000 > distance > 999:
        return 2

    elif 2000 > volume > 999 and 2500 > distance > 1499:
        return 2

    return 1

def pue_rare_metals(volume: float, distance: float, height: float):
    if distance < 1000:
        return 4
    elif distance < 2000:
        return 3
    elif distance < 3500:
        return 2
    return 1

def pue_color_metals(volume: float, distance: float, height: float):
    if distance < 500:
        return 2
    return 1

# 1.9.9 строительные материалы
def pue_cement(volume: float, distance: float, height: float):

    cement_table = [[1, 1, 1, 1, 1, 1, 1,], 
                [2, 2, 1, 1, 1, 1, 1,], 
                [3, 3, 2, 1, 1, 1, 1,], 
                [3, 3, 3, 2, 1, 1, 1,], 
                [4, 4, 3, 3, 2, 1, 1,], 
                [4, 4, 4, 3, 3, 2, 1,],]
    
    row, column = 0, 0
    
    if 99 < volume < 500:
        row = 1
    elif 0 < volume // 500 < 7:
        row = (3 + volume // 500) // 2
    elif volume > 3499:
        row = 5

    if 249 < distance and distance // 500 < 5:
        column = 1 + distance // 500
    elif distance > 2999:
        column = 6

    return cement_table[int(row)][int(column)]

def pue_asbestos(volume: float, distance: float, height: float):
    if distance < 250:
        return 3
    elif distance < 500:
        return 2
    return 1
    
def pue_other_materials(volume: float, distance: float, height: float):
    if distance < 250:
        return 2
    return 1

# 1.9.10 машиностроительные
def pue_сar(volume: float, distance: float, height: float):
    if distance < 500:
        return 2
    return 1

# 1.9.12 добыча руд и нерудных ископаемых
def pue_iron_mining(volume: float, distance: float, height: float):
    if distance < 250:
        return 2
    return 1

def pue_coal_mining(volume: float, distance: float, height: float):
    if distance < 250:
        return 3
    elif distance < 500:
        return 2
    return 1

# 1.9.13 тэс и котельни
def pue_tes_coal(volume: float, distance: float, height: float):
    if volume > 999 and distance < 500:
        return 2
    elif volume > 999 and distance < 1000 and height < 180:
        return 2
    return 1

def pue_tes_slate(volume: float, distance: float, height: float):
    if volume < 500:
        if distance < 250:
            return 3
        elif distance < 1500:
            return 2
        return 1

    if distance > 2999:
        return 1
    elif distance > 499:
        return 2
    elif distance > 249:
        return 3
    elif height < 180:
        return 4
    
    return 3    

# 1.9.14 свалки, склады
def pue_tbo(distance: float):
    if distance < 200:
        return 3
    elif distance < 600:
        return 2
    return 1