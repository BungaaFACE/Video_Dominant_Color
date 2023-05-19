from PIL import Image, ImageColor, ImageOps


# image_path = "E:\\mostwanted\\low_res_pic.jpg"
image_path = "E:\\mostwanted\\1492525865183067191.jpg"
# image_path = "E:\\mostwanted\\test_object.png"

# Количество цветов-призеров
max_colors = 5
# Численное отличие значений RGB для расчета
step = 7



def get_middle_color(color_list):
    middle_color = dict()
    for color in color_list:
        middle_color[color] = round(sum(color_list[color]) / len(color_list[color]))
    return middle_color

def neighbor_color_top_rgb(color_list, step):
    
    
    def move_places(place):
        """
        Добавляем нового призера на его место и
        сдвигаем остальных на одну позицию ниже
        """
        current_place = max_colors
        
        while current_place != place:
            # сдвигаем сетку призеров вниз на 1
            top_colors["matches"][current_place] = top_colors["matches"][current_place - 1]
            top_colors["RGB"][current_place] = top_colors["RGB"][current_place - 1]
            current_place -= 1
        
        # выставляем нового призера на его место
        top_colors["matches"][place] = match_counter
        top_colors["RGB"][place] = current_color_list
            
    """
    Создаем таблицу цветов-лидеров, с кол-вом мест, указанных в начале
    Формат словаря:
        "matches":
            1 место: количество попаданий под критерии
            ...
            n место: количество попаданий под критерии
        "RGB":
            1 место: [R, G, B]
            ...
            n место: [R, G, B]
    """
    top_colors = {
        "matches": {},
        "RGB": {}
    }
    for color_place in range(max_colors):
        top_colors["matches"][color_place + 1] = 0
        """
        -step - 1 сделан для последующей проверки:
        если проверяемый цвет или похожий в диапозоне step есть, то пропускаем проверку цвета
        
        При пустой таблице лидеров
        abs(top_rgb[0] - current_color_list[0]) > step всегда выдаст True, соответственно начнет проверять этот цвет
        """
        top_colors["RGB"][color_place + 1] = [-step - 1, -step - 1, -step - 1]
        
        
    # количество пикселей на картинке
    pixel_summ = len(color_list["R"])
    # уже прошедшие проверку значения RGB в виде списка [[R, G, B], [R, G, B] ...]
    colors_done = []
    
    #Перебираем все пиксели
    for current_pixel_num in range(pixel_summ):
        
        current_color_list = [color_list["R"][current_pixel_num], color_list["G"][current_pixel_num], color_list["B"][current_pixel_num]]
        
        # Проверка, был ли такой цвет раньше
        if current_color_list not in colors_done:
            
            
            colors_done.append(current_color_list)
            match_counter = 0
            
            # Делаем список значений, подходящих под критерии
            range_r = range(color_list["R"][current_pixel_num] - step, color_list["R"][current_pixel_num] + step + 1)
            range_g = range(color_list["G"][current_pixel_num] - step, color_list["G"][current_pixel_num] + step + 1)
            range_b = range(color_list["B"][current_pixel_num] - step, color_list["B"][current_pixel_num] + step + 1)
            
            # Перебор остальных пикселей для сравнения
            for if_matches_pixel_num in range(pixel_summ):
                
                # Условия сравнения пикселей + защита от сравнения пикселя с самим собой
                if current_pixel_num != if_matches_pixel_num and \
                    current_color_list[0] in range_r and \
                    current_color_list[1] in range_g and \
                    current_color_list[2] in range_b:
                    match_counter += 1
            
            
            
            # Сравниваем совпадения с таблицей цветов-лидеров
            for check_place in top_colors["matches"].keys():
                if match_counter > top_colors["matches"][check_place]:
                    move_places(check_place)
                    break
    return top_colors
            
    # Проверяем, не было ли похожего цвета в списке лидеров
            # if all(abs(top_rgb[0] - current_color_list[0]) > step and \
            #     abs(top_rgb[1] - current_color_list[1]) > step and \
            #     abs(top_rgb[2] - current_color_list[2]) > step \
            #         for top_rgb in top_colors["RGB"].values()):

def get_rgb_from_image(image_path):
    """
    get RGBs for every pixel of image
    """
    frame_rgb_list = {
        "R":[], 
        "G":[], 
        "B":[]
    }
    with Image.open(image_path, 'r') as im:
        # width, height = im.size
        pixel_values = list(im.getdata())
    print("rgb", pixel_values[0])
    for pixel in pixel_values:
        frame_rgb_list["R"].append(pixel[0])
        frame_rgb_list["G"].append(pixel[1])
        frame_rgb_list["B"].append(pixel[2])
    return frame_rgb_list


def neighbor_color_top_hsv(color_list, step):
    """
    Вариантов пока два:
    1) ищем попадания H в step, затем вычисляем среднее H и V для определенного H+-step
    2) подразделяем политру H с шагов в 5, затем вычисляем среднее H и V для определенного H+-step
    варианты практически идентичны, 2 способ скорее всего ускорит процесс
    """
    
    
    def compare_to_leader(top_colors):
        """
        Функция сравниевает значения попаданий по критерию
        Если у нового значения попаданий больше, то начинается сравнения с значениями H из таблицы
        При нахождении похожего значения, если кол-во попаданий нового H > старого H, то новое заменяет старое
        Если похожего значения нет, то добавляем в таблицу лидеров, сортируем и удаляем последнее место
        """
        
        # Сравниваем совпадения с таблицей цветов-лидеров
        for place_matches in top_colors.keys():
            
            # Попадает ли цвет в таблицу лидеров
            if match_counter > place_matches:
                
                # Смотрим нет ли слишком похожих цветов в таблице призеров (H+-step*2)
                for matches, top_h_values in top_colors.items():
                    range_leader = range(round(top_h_values - step * range_leader_step), round(top_h_values + step * range_leader_step + 1))
                    if current_h_value in range_leader:
                        """
                        Верхнее и нижнее условие нельзя объединить, 
                        потому что в случае если есть похожий H, но совпадения у нового H меньше, 
                        то нужно проигнорировать его и идти дальше
                        """
                        if match_counter > matches:
                        
                            #Если есть и число попаданий больше, чем число попаданий у призера, то удаляем старое похожее число
                            top_colors[match_counter] = current_h_value
                            top_colors.pop(matches)
                            top_colors = dict(sorted(top_colors.items(), reverse=True))
                            return top_colors
                        return top_colors
                
                #Если есть новый цвет призер и нет похожих на него цветов, то добавляем новое, сортируем и удаляем последнее место
                top_colors[match_counter] = current_h_value
                top_colors = sorted(top_colors.items(), reverse=True)
                # Из sorted получаем tuple, поэтому можно удалить последний элемент следующим образом
                if len(top_colors) > max_colors:
                    top_colors = top_colors[:-1]
                top_colors = dict(top_colors)
                return top_colors
        
        return top_colors
    
    
    def find_average_sv_from_leader_h(top_colors):
        """
        Функция находит среднее значение S и V для каждого лидирующего H.
        Значения S и V удовлетворяют условиям, если H = H_leader+-step
        """

        # Поскольку дальше будут добавляться аргументы в словарь внутри итерации - заранее создаем список
        list_for_iter = list(top_colors.keys())
        
        # Перебор всех пикселей для нахождения среднего S, V значений H+-step призеров
        for current_pixel_num in range(pixel_summ):
            
            # Для каждого пикселя перебираем места призеров
            for match in list_for_iter:
                
                # Добавляем лист для последующего вычисления среднего значения
                if f"{match}_S_list" not in top_colors:
                    top_colors[f"{match}_S_list"] = []
                    top_colors[f"{match}_V_list"] = []
                
                # Если H пикселя в рендже H+-step, добавляем значения S, V в список для будущего вычисления их среднего значения
                if color_list["H"][current_pixel_num] in range(top_colors[match] - step, top_colors[match] + step + 1):
                    top_colors[f"{match}_S_list"].append(color_list["S"][current_pixel_num])
                    top_colors[f"{match}_V_list"].append(color_list["V"][current_pixel_num])
        
        # Вычисление среднего значения S и V
        for match in list_for_iter:
            top_colors[match] = [top_colors[match]]
            top_colors[match].append(round(sum(top_colors[f"{match}_S_list"]) / len(top_colors[f"{match}_S_list"])))
            top_colors[match].append(round(sum(top_colors[f"{match}_V_list"]) / len(top_colors[f"{match}_V_list"])))
            top_colors.pop(f"{match}_S_list")
            top_colors.pop(f"{match}_V_list")
        
        return top_colors
                    
    """ 
    Топ {max_colors} цветов, 
    -1 начальное значение matches для последующего сравнения
    -999 - число h. 
    Сделано для того, чтобы число H, близкое к 0 прошло проверку на одинаковость цвета
    """
    top_colors = {-1:-999}
        
    # количество пикселей на картинке
    pixel_summ = len(color_list["H"])
    # уже прошедшие проверку значения RGB в виде списка [H1, H2 ...]
    colors_done = []
    
    #Перебираем все пиксели
    for current_pixel_num in range(pixel_summ):
        
        current_h_value = color_list["H"][current_pixel_num]
        
        # Проверка, был ли такой цвет раньше
        if current_h_value not in colors_done:
            
            colors_done.append(current_h_value)
            match_counter = 0
            
            # Делаем список значений, подходящих под критерии
            range_h = range(color_list["H"][current_pixel_num] - step, color_list["H"][current_pixel_num] + step + 1)
            
            # Перебор остальных пикселей для сравнения
            for matches_pixel_num in range(pixel_summ):
                
                # Условия сравнения пикселей + защита от сравнения пикселя с самим собой
                if current_pixel_num != matches_pixel_num and color_list["H"][matches_pixel_num] in range_h:
                    match_counter += 1
            
            # Функция сравнения с лидерами и поиском похожих цветов в лидерах
            top_colors = compare_to_leader(top_colors)
    
    # Функция находит средние S и V для каждого H
    top_colors = find_average_sv_from_leader_h(top_colors)

    return top_colors
            
            
def get_hsv_from_image(image_path):
    """
    get HSV from image
    """
    frame_hsv_list = {
        "H":[], 
        "S":[], 
        "V":[]
    }
    with Image.open(image_path, 'r') as im:

        # width, height = im.size
        pixel_values = list(im.convert('HSV').getdata())
    for pixel in pixel_values:
        frame_hsv_list["H"].append(pixel[0])
        frame_hsv_list["S"].append(pixel[1])
        frame_hsv_list["V"].append(pixel[2])
    return frame_hsv_list


def print_result(image_path, top_colors):
    with Image.open(image_path, 'r') as orig_image:
        one_color_width = round(orig_image.width / len(top_colors.keys()))
        one_color_height = round(orig_image.height * 0.5)
        
        result_image = Image.new(mode="HSV", size=(orig_image.width, orig_image.height + one_color_height), color=(0, 0, 0))
        result_image.paste(orig_image, (0, 0))
    
    border_size = round(result_image.width / 100)
    color_number = 0
    
    # Вставка призовых цветов
    for match in top_colors:

        # Создание картинки с призовым цветом
        new_color_image = Image.new(mode="HSV", \
            size=(one_color_width - border_size * 2, one_color_height - border_size * 2), \
            color=(top_colors[match][0], top_colors[match][1], top_colors[match][2]))
        # Добавляем границу к цвету для лучшего восприятия
        bordered_color_image = ImageOps.expand(new_color_image, border=border_size, fill=(0,0,0))
        # Вычисление начала координаты x для нового цвета
        x_ord_new_color = color_number * one_color_width
        color_number += 1
        result_image.paste(bordered_color_image, (x_ord_new_color, orig_image.height))
    
    result_image.show()
    # Image.new(mode="HSV", size=(100, 100), color=(155, 177, 137)).show()
    #[7, 64, 210] розовый
    #[27, 229, 198] оранжевый
    #160, 172, 134 синий
    # 155, 177, 137 синий
        
########### RGB ###########
# frame_rgb_list = get_rgb_from_imgage(image_path)
# print(neighbor_color_top_rgb(frame_rgb_list, step))

# print(get_middle_color(frame_rgb_list))
########### HSV ###########
range_leader_step = 1
frame_hsv_list = get_hsv_from_image(image_path)
top_colors = neighbor_color_top_hsv(frame_hsv_list, step)
print(top_colors)
print_result(image_path, top_colors)


# Image.new(mode="RGB", size=(100, 100), color=(51, 58, 113)).show()
# Image.new(mode="HSV", size=(100, 100), color=(165, 139, 113)).show()