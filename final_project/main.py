import os
import tkinter as tk
from PIL import Image, ImageTk
import math
import smtplib
import ssl
import pandas as pd

#Send all data to mailbox
def send_data():
    global ratio_list,global_image_order,selected_option,answers
    email = 'delboeuf.illusion@gmail.com'
    password = 'zkiossdscekuxgtt'


    dataCSV = ""
    dataCSV += ",".join(map(str, ratio_list))

    for row in global_image_order:
        dataCSV += "\n" + ",".join(map(str, row))

    dataCSV += "\n" + ",".join(map(str, selected_option))
    dataCSV += "\n" + ",".join(map(str, answers))


    message = """\
Subject: Test Data

{}""".format(dataCSV)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message)

#Save all data as CSV
def save_data_to_csv():
    global ratio_list, global_image_order, selected_option

    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, "data_test.csv")

    file_exists = os.path.exists(file_path)
    data = {
        'gender': answers[0],
        'age': answers[1],
    }

    for i, value in enumerate(ratio_list):
        data[f'Q{i + 1}'] = f"{value:.4f}"

    for i, sublist in enumerate(global_image_order):
        data[f'Q{len(ratio_list) + 1 + i}'] = f"[{' '.join(map(str, sublist))}]"

    for i, option in enumerate(selected_option):
        data[f'Q{len(ratio_list) + len(global_image_order) + 1 + i}'] = option

    df = pd.DataFrame([data])

    if file_exists:
        df.to_csv(file_path, mode='a', header=False, index=False, sep="\t")
    else:
        df.to_csv(file_path, index=False, sep="\t")

#All function about age and gender (questionnaire)
def experiment0_queries():
    global answers
    current_answer = None 

    def add_answer():
        if current_answer is not None:
            answers.append(current_answer)

    def clear_canvas(canvas):
        for widget in canvas.winfo_children():
            widget.destroy()

    def create_radio_buttons(canvas, options, command):
        nonlocal current_answer  
        for option in options:
            radio_button = tk.Radiobutton(canvas, text=option, value=option, command=lambda o=option: set_current_answer(o), highlightbackground="gray")
            radio_button.pack()

    def set_current_answer(answer):
        nonlocal current_answer
        current_answer = answer

    def show_question(canvas, index):
        nonlocal current_answer
        current_answer = None 
        clear_canvas(canvas)

        question_label = tk.Label(canvas, text=question_labels[index])
        question_label.pack()

        options = []
        if index == 0:
            options = ["Male", "Female"]
        elif index == 1:
           options = ["0-10", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]


        create_radio_buttons(canvas, options, set_current_answer)

        if index < len(question_labels) - 1:
            next_button = tk.Button(canvas, text="next", command=lambda: [add_answer(), show_question(canvas, index + 1)])
            next_button.pack()
        else:
            submit_button = tk.Button(canvas, text="submit", command=lambda: [add_answer(), finish_questionnaire()])
            submit_button.pack()

    return show_question

def finish_questionnaire():
        exp0_canvas.pack_forget()
        description1.place(x=300,y=400)
        next_button1.place(x=screen_width//2,y=screen_height-50)
        print(answers)
def nextexp1():
    exp1_complete_button.place(x=screen_width//2,y=screen_height-50)
    exp_question_number_label.place(x=20, y=20)
    exp1_label1.place(x=250, y=30)
    next_button1.place_forget()
    description1.place_forget()

    experiment1_shape(exp1_canvas, 
                      exp1_image_paths_list[exp1_current_path_index],
                      exp1_image_positions_list[exp1_current_position_index])



#exp1 all function
def experiment1_shape(canvas, image_paths,image_positions):
    current_directory = os.path.dirname(__file__)
    image1_path = os.path.join(current_directory, image_paths[0])
    image2_path = os.path.join(current_directory, image_paths[1])
    image3_path = os.path.join(current_directory, image_paths[2])
    image4_path = os.path.join(current_directory, image_paths[3])

    image1 = Image.open(image1_path)
    image1_tk = ImageTk.PhotoImage(image1)

    image2 = Image.open(image2_path)
    image2_tk = ImageTk.PhotoImage(image2)

    image3 = Image.open(image3_path)
    image3_tk = ImageTk.PhotoImage(image3)

    image4 = Image.open(image4_path)
    image4_tk = ImageTk.PhotoImage(image4)

    scale_factor = 1.0
    start_x = 0
    start_y = 0

    def exp1_show_image():
        nonlocal scale_factor, image1_tk, image2_tk
        canvas.delete("all")

        canvas.create_image(image_positions[1][0], image_positions[1][1], image=image4_tk, tags="image4")  
        canvas.tag_lower("image4")  
        canvas.create_image(image_positions[1][0], image_positions[1][1], image=image3_tk, tags="image3")

        width, height = image1.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        resized_image = image1.resize((new_width, new_height), Image.LANCZOS)
        image1_tk = ImageTk.PhotoImage(resized_image)
        canvas.create_image(image_positions[0][0], image_positions[0][1], image=image1_tk, tags="image1") 
        canvas.image = image1_tk  
        canvas.create_image(image_positions[0][0], image_positions[0][1], image=image2_tk, tags="image2")  
        canvas.tag_lower("image2")  
        
    # Experiment 1 left mouse button press event
    def exp1_on_press(event):
        nonlocal start_x, start_y
        start_x = event.x
        start_y = event.y

    # Experiment 1 left mouse button move event
    def exp1_on_motion(event):
        nonlocal scale_factor
        current_x = event.x
        current_y = event.y
        distance_x = current_x - start_x
        distance_y = current_y - start_y
        scale_factor = 1.0 + (distance_x + distance_y) * 0.002
        exp1_show_image()

    # Experiment 1 left mouse button release event
    def exp1_on_release(event):
        nonlocal scale_factor
        global ratio
        original_height3 = image3.size[1]
        original_height1 = image1.size[1]
        after=original_height1*scale_factor
        ratio = after / original_height3
        ratio=ratio
        
    

    canvas.bind("<ButtonPress-1>", exp1_on_press)
    canvas.bind("<ButtonRelease-1>", exp1_on_release)
    canvas.bind("<B1-Motion>", exp1_on_motion)

    exp1_show_image()

def exp1_on_complete():
    global exp1_current_path_index, exp1_label_counter, exp1_label1, scale_factors,exp1_current_position_index,exp1_counter,ratio,ratio_list,current_question,total_exp_questions,exp1_complete_button,exp_question_number_label
    global exp2_current_path_index
    if current_question<total_exp1_questions:
        current_question += 1

    exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
    ratio_list.append(ratio)
    print(ratio_list)
    exp1_counter += 1
    if exp1_counter >= 3:
        exp1_counter = 0
        exp1_current_path_index += 1
    exp1_current_position_index += 1
    if exp1_current_position_index >= len(exp1_image_positions_list):
        exp1_current_position_index = 0
    if exp1_current_path_index < len(exp1_image_paths_list):
        exp1_canvas.delete("all")
        experiment1_shape(exp1_canvas, exp1_image_paths_list[exp1_current_path_index],exp1_image_positions_list[exp1_current_position_index])
    if exp1_current_path_index >= len(exp1_image_paths_list):
        exp1_canvas.pack_forget()
        exp1_complete_button.place_forget()
        description2.place(x=400,y=300)
        next_button2.place(x=screen_width//2,y=screen_height-50)
        
    exp1_label_counter += 1
    if exp1_label_counter ==1:
        exp1_label1.place_forget()  
    if exp1_label_counter ==12:
        exp1_label2.place(x=400, y=30)
    if exp1_label_counter ==13:
        exp1_label2.place_forget()
    if exp1_label_counter ==24:
        exp1_label3.place(x=400, y=30)
    if exp1_label_counter ==25:
        exp1_label3.place_forget()

def nextexp2():
    global exp2_current_path_index
    exp2_button.place(x=screen_width//2,y=screen_height-50)
    exp2_label.place(x=250, y=30)
    next_button2.place_forget()
    description2.place_forget()
    experiment2_size(exp2_canvas, exp2_image_paths_list[exp2_current_path_index])





#exp2 all function
def experiment2_size(canvas, image_paths):
    global image1,image2,image3,image4,images1,images2,images3
    current_directory = os.path.dirname(__file__)

    image1_path = os.path.join(current_directory, image_paths[0])
    image2_path = os.path.join(current_directory, image_paths[1])
    image3_path = os.path.join(current_directory, image_paths[2])
    image4_path = os.path.join(current_directory, image_paths[3])

    image1 = Image.open(image1_path)
    image1 = ImageTk.PhotoImage(image1)

    image2 = Image.open(image2_path)
    image2 = ImageTk.PhotoImage(image2)

    image3 = Image.open(image3_path)
    image3 = ImageTk.PhotoImage(image3)

    image4 = Image.open(image4_path)
    image4 = ImageTk.PhotoImage(image4)

    third_width = screen_width // 3
    images1 = [canvas.create_image(third_width//2, screen_height//2, image=image1),
               canvas.create_image(third_width//2, screen_height//2, image=image4)]

    images2 = [canvas.create_image(third_width + third_width // 2, screen_height//2, image=image2),
               canvas.create_image(third_width + third_width // 2, screen_height//2, image=image4)]

    images3 = [canvas.create_image(2 * third_width + third_width // 2, screen_height//2, image=image3),
               canvas.create_image(2 * third_width + third_width // 2, screen_height//2, image=image4)]

    for image_ids in [images1, images2, images3]:
        for image_id in image_ids:
            canvas.tag_bind(image_id, "<B1-Motion>", lambda event, ids=image_ids: exp2_on_drag(event, ids))
            canvas.tag_bind(image_id, "<ButtonPress-1>", lambda event, ids=image_ids: exp2_on_press(event, ids))

    def exp2_on_drag(event, image_ids):
        x_diff = event.x - exp2_prev_x.get(image_ids[0], 0)
        y_diff = event.y - exp2_prev_y.get(image_ids[0], 0)
        for image_id in image_ids:
            canvas.tag_raise(image_id)
            canvas.move(image_id, x_diff, y_diff)
        exp2_prev_x[image_ids[0]], exp2_prev_y[image_ids[0]] = event.x, event.y

    def exp2_on_press(event, image_ids):
        exp2_prev_x[image_ids[0]], exp2_prev_y[image_ids[0]] = event.x, event.y

def exp2_update_image_order():
    global global_image_order 
    image_order = []
    for images in [images1, images2, images3]:
        x, _ = exp2_canvas.coords(images[0])  
        image_order.append((images[0], x))
    image_order.sort(key=lambda x: x[1])
    ordered_images = [image[0] for image in image_order]
    global_image_order.append(ordered_images)  

def exp2_on_submit():
    global current_question
    exp2_update_image_order()
    global exp2_current_path_index
    if exp2_current_path_index < len(exp2_image_paths_list)-1:
        exp2_canvas.delete("all")
        exp2_current_path_index +=1
        current_question += 1
        exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
    else:
        current_question += 1
        exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
        exp2_canvas.pack_forget()
        exp2_button.place_forget()
        exp2_label.place_forget()
        description3.place(x=400,y=300)
        next_button3.place(x=screen_width//2,y=screen_height-50)
    experiment2_size(exp2_canvas, exp2_image_paths_list[exp2_current_path_index])
def nextexp3():
    global exp3_paths_list,exp3_positions_list,exp3_target_size_list,exp3_num_images_list,exp3_circle_radius_list
    next_button3.place_forget()
    description3.place_forget()
    exp3_label.place(x=250, y=30)
    experiment3_var(exp3_canvas, exp3_paths_list,exp3_positions_list,exp3_target_size_list,exp3_num_images_list, exp3_circle_radius_list)




#exp3 all function
def experiment3_var(canvas, exp3_paths_list,exp3_positions,target_size,num_images, circle_radius):
    global surroundings_left,surroundings_right,center_photo,exp3_canvas_index
    current_directory = os.path.dirname(__file__)
    image1_path = os.path.join(current_directory, exp3_paths_list[exp3_canvas_index][0])
    image2_path = os.path.join(current_directory, exp3_paths_list[exp3_canvas_index][1])

    image1 = Image.open(image1_path)
    surroundings_left = ImageTk.PhotoImage(image1.resize(exp3_target_size_list[exp3_canvas_index][0], Image.LANCZOS))
    surroundings_right = ImageTk.PhotoImage(image1.resize(exp3_target_size_list[exp3_canvas_index][1], Image.LANCZOS))
    

    image2 = Image.open(image2_path)
    center_photo = ImageTk.PhotoImage(image2.resize(target_size[exp3_canvas_index][2], Image.LANCZOS))


    def show_thank_you_label(root):
        canvas.delete("all")
        send_data()
        save_data_to_csv()
        label_text = "Thanks for taking part in the test!"
        label_font = ("Helvetica", 24)  
        exp_question_number_label.place_forget()
        label = tk.Label(root, text=label_text, font=label_font,highlightbackground="gray")
        label.place(x=screen_width // 2, y=screen_height // 2, anchor="center")
    def left_center_image_click(event):
        global exp3_canvas_index,selected_option,current_question,exp3_positions_list
        selected_option.append("left")
        print(selected_option)
        if exp3_canvas_index < len(exp3_positions_list)-1:
            exp3_canvas_index += 1
            experiment3_var(canvas, exp3_paths_list,exp3_positions_list,exp3_target_size_list,exp3_num_images_list, exp3_circle_radius_list)
            current_question +=1
            exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
            
        else:
            current_question +=1
            exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
            exp3_label.place_forget()
            exp3_button.place_forget()
            show_thank_you_label(root)
            

    def right_center_image_click(event):
        global exp3_canvas_index,selected_option,current_question,exp3_positions_list
        selected_option.append("right")
        print(selected_option)
        if exp3_canvas_index < len(exp3_positions_list)-1:
            exp3_canvas_index += 1
            experiment3_var(canvas, exp3_paths_list,exp3_positions_list,exp3_target_size_list,exp3_num_images_list, exp3_circle_radius_list)
            current_question +=1
            exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
            
        else:
            current_question +=1
            exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
            exp3_label.place_forget()
            exp3_button.place_forget()
            show_thank_you_label(root)

           

    def exp3_button_click():
        global exp3_canvas_index,selected_option,current_question,exp3_positions_list
        selected_option.append("same")
        print(selected_option)
        if exp3_canvas_index < len(exp3_positions_list)-1:
            exp3_canvas_index += 1
            experiment3_var(canvas, exp3_paths_list,exp3_positions_list,exp3_target_size_list,exp3_num_images_list, exp3_circle_radius_list)
            current_question +=1
            exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
            
        else:
            current_question +=1
            exp_question_number_label.config(text=f"{current_question}/{total_exp_questions}")
            exp3_label.place_forget()
            exp3_button.place_forget()
            show_thank_you_label(root)
            
    def draw_circle_of_images(canvas, image, num_images, circle_radius,screen_width,screen_height):
        angle_increment = 360 / num_images
        for i in range(num_images):
            angle = i * angle_increment
            x = screen_width + int(circle_radius * math.cos(math.radians(angle)))
            y = screen_height + int(circle_radius * math.sin(math.radians(angle)))
            canvas.create_image(x, y, image=image)

    def create_images_with_positions(canvas, image,position1x, position1y,position2x, position2y):
        canvas.create_image(position1x,  position1y, image=image,tag='left_center')
        canvas.create_image(position2x,  position2y, image=image,tag='right_center')

        canvas.tag_bind('left_center', '<Button-1>', left_center_image_click)
        canvas.tag_bind('right_center', '<Button-1>', right_center_image_click)


    draw_circle_of_images(canvas, surroundings_left, num_images[exp3_canvas_index][0], circle_radius[exp3_canvas_index][0],exp3_positions[exp3_canvas_index][0],exp3_positions[exp3_canvas_index][1])
    draw_circle_of_images(canvas, surroundings_right, num_images[exp3_canvas_index][1], circle_radius[exp3_canvas_index][1],exp3_positions[exp3_canvas_index][2],exp3_positions[exp3_canvas_index][3])
    create_images_with_positions(canvas, center_photo,exp3_positions[exp3_canvas_index][0], exp3_positions[exp3_canvas_index][1],exp3_positions[exp3_canvas_index][2],exp3_positions[exp3_canvas_index][3])
    exp3_button = tk.Button(root, text="they are same",command=exp3_button_click,highlightbackground="gray")
    exp3_button.place(x=screen_width // 2, y=screen_height - 50)




root = tk.Tk()
root.title("Delobeuf Illusion")

# 设置窗口最大化
root.state('zoomed')

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置画布大小与屏幕一样大

exp0_canvas = tk.Canvas(root, width=screen_width, height=screen_height)
exp0_canvas.pack()

exp1_canvas = tk.Canvas(root, width=screen_width, height=screen_height, background="gray")
exp1_canvas.pack()

exp2_canvas = tk.Canvas(root, width=screen_width, height=screen_height, background="gray")
exp2_canvas.pack()

exp3_canvas = tk.Canvas(root, width=screen_width, height=screen_height, background="gray")
exp3_canvas.pack()

question_labels = [
    "What is your gender?",
    "What is your age range?"
]
# 图片路径列表
exp1_image_paths_list = [
    # circle
    ["all_images/exp1_images/right_pizza2.png", "all_images/exp1_images/right_round.png", 
     "all_images/exp1_images/left_pizza.png", "all_images/exp1_images/left_round.png"],
    # octagon
    ["all_images/exp1_images/right_pizza2.png", "all_images/exp1_images/right_octagon.png",
     "all_images/exp1_images/left_pizza.png", "all_images/exp1_images/left_octagon.png"],
    # hexagon
    ["all_images/exp1_images/right_pizza2.png", "all_images/exp1_images/right_hexagon.png",
     "all_images/exp1_images/left_pizza.png", "all_images/exp1_images/left_hexagon.png"],
    # square
    ["all_images/exp1_images/right_pizza2.png", "all_images/exp1_images/right_square.png",
     "all_images/exp1_images/left_pizza.png", "all_images/exp1_images/left_square.png"],
     #circle
     ["all_images/exp1_images/right_white_round.png", "all_images/exp1_images/right_black_round.png",
     "all_images/exp1_images/left_white_round.png", "all_images/exp1_images/left_black_round.png"],
     #octagon
     ["all_images/exp1_images/right_white_octagon.png", "all_images/exp1_images/right_black_octagon.png",
     "all_images/exp1_images/left_white_octagon.png", "all_images/exp1_images/left_black_octagon.png"],
     #hexagon
     ["all_images/exp1_images/right_white_hexagon.png", "all_images/exp1_images/right_black_hexagon.png",
     "all_images/exp1_images/left_white_hexagon.png", "all_images/exp1_images/left_black_hexagon.png"],
     #square
     ["all_images/exp1_images/right_white_square.png", "all_images/exp1_images/right_black_square.png",
     "all_images/exp1_images/left_white_square.png", "all_images/exp1_images/left_black_square.png"],
     #spoon 1
     ["all_images/exp1_images/580.png", "all_images/exp1_images/right_round.png",
     "all_images/exp1_images/285.png", "all_images/exp1_images/left_round.png"],
      #spoon 2
     ["all_images/exp1_images/soup_580.png", "all_images/exp1_images/right_round.png",
     "all_images/exp1_images/soup_285.png", "all_images/exp1_images/left_round.png"],
     #ice cream 1
     ["all_images/exp1_images/icecream_580.png", "all_images/exp1_images/right_round.png",
     "all_images/exp1_images/icecream_285.png", "all_images/exp1_images/left_round.png"],
     #ice cream 2
     ["all_images/exp1_images/ice_580.png", "all_images/exp1_images/right_round.png",
     "all_images/exp1_images/ice_285.png", "all_images/exp1_images/left_round.png"],

]

exp1_image_positions_list = [
    [
        [850, 430],  #right sdie
        [250, 430],  #lefe side

    ],
    [
        [900, 350],  
        [160, 600],  

    ],
    [
        [950, 470],  
        [250, 170],  

    ],
    
]
exp2_image_paths_list=[
    ["all_images/exp2_images/black_plate_125.png", "all_images/exp2_images/black_plate_150.png",
     "all_images/exp2_images/black_plate_200.png","all_images/exp2_images/cookies.png"],
     ["all_images/exp2_images/black_plate_150.png", "all_images/exp2_images/black_plate_250.png",
     "all_images/exp2_images/black_plate_350.png","all_images/exp2_images/cookies.png"],
      ["all_images/exp2_images/black_plate_250.png", "all_images/exp2_images/black_plate_350.png",
     "all_images/exp2_images/black_plate_450.png","all_images/exp2_images/cookies.png"],
     ["all_images/exp2_images/black_plate_350.png", "all_images/exp2_images/black_plate_450.png",
     "all_images/exp2_images/black_plate_550.png","all_images/exp2_images/cookies.png"],
    ]


exp3_paths_list=[
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
    ["all_images/exp3_images/plates.png","all_images/exp3_images/curry.png"],
]

exp3_positions_list=[
    [screen_width//3*0.75,screen_height//2,(screen_width // 3) * 2.3,screen_height//2],
    [screen_width//3*0.75,screen_height//2+150,(screen_width // 3) * 2.3,screen_height//2-120],
    [screen_width//3*0.75,screen_height//2-150,(screen_width // 3) * 2.3,screen_height//2+120],
    [screen_width//3*0.75,screen_height//2,(screen_width // 3) * 2.3,screen_height//2],
    [screen_width//3*0.75,screen_height//2+150,(screen_width // 3) * 2.3,screen_height//2-120],
    [screen_width//3*0.75,screen_height//2-150,(screen_width // 3) * 2.3,screen_height//2+120],
    [screen_width//3*0.75,screen_height//2,(screen_width // 3) * 2.3,screen_height//2],
    [screen_width//3*0.75,screen_height//2+150,(screen_width // 3) * 2.3,screen_height//2-120],
    [screen_width//3*0.75,screen_height//2-150,(screen_width // 3) * 2.3,screen_height//2+120],
]
exp3_target_size_list=[
   [(60,60),(60,60),(120,120)],
   [(60,60),(60,60),(120,120)],
   [(60,60),(60,60),(120,120)],
   [(60,60),(80,80),(120,120)],
   [(60,60),(80,80),(120,120)],
   [(60,60),(80,80),(120,120)],
   [(140,140),(140,140),(120,120)],
   [(140,140),(140,140),(120,120)],
   [(140,140),(140,140),(120,120)],
]

exp3_num_images_list=[
    [8,8],
    [8,8],
    [8,8],
    [8,8],
    [8,8],
    [8,8],
    [6,8],
    [6,8],
    [6,8],
]
exp3_circle_radius_list=[
    [100,290],
    [100,290],
    [100,290],
    [150,150],
    [150,150],
    [150,150],
    [200,200],
    [200,200],
    [200,200],
]

answers = []
intro_label = tk.Label(exp0_canvas, text="Welcome to the test\n\
This is an experiment that will test the Delboeuf illsuion.\
It will take approximately 7 to 15 minutes to complete.\n\n\
At first you will be asked for your personal information, but only your age and gender,\n\
as this will be used for research afterwards, please be assured that we will not divulge your personal information. \n\
Then, you will then be asked to complete 49 mini-experiments.\n\
All the experiments can be divided into three parts,\n\
and after each part of the experiment is completed,\n\
you can choose to take an appropriate break before clicking the button to start the next part of the experiment.\n\n\
In Experiment 1 you can perform zooming operations\n\
In Experiment 2 you can drag and drop operations\n\
In Experiment 3 you can click on the action of the image\n\n\
Thank you very much for your cooperation.\n\
Before the test begins,\n\
please ensure that you are within a properly lit environment,\n\
please make sure that the brightness of your monitor is normal for you as well.", font=('Helvetica', 16,'bold'), justify=tk.LEFT, wraplength=1050)
intro_label.place(x=200,y=100)
show_question = experiment0_queries()
accept_button = tk.Button(exp0_canvas, text="Accept", command=lambda: show_question(exp0_canvas, 0))
accept_button.place(x=600,y=500)


description1 = tk.Label(root, text="This is the experiment1\n\n\
In this experiment you can follow the instructions \n\n\
to freely zoom in and out of the image on the right.\n\n\
", font=('Helvetica', 16,'bold'), justify=tk.LEFT, wraplength=1050,bg='gray')
next_button1 = tk.Button(root, text="next", command=nextexp1,highlightbackground="gray")
total_exp1_questions = len(exp1_image_paths_list) * len(exp1_image_positions_list)
total_exp_questions = len(exp1_image_paths_list) * len(exp1_image_positions_list)+len(exp2_image_paths_list)+len(exp3_positions_list)
exp1_current_path_index = 0
exp1_current_position_index = 0
exp1_label_counter = 0
ratio_list=[]
exp1_counter = 0
current_question = 1
exp1_complete_button = tk.Button(root, text="submit", command=exp1_on_complete,highlightbackground="gray")
exp_question_number_label = tk.Label(root, text=f"{current_question}/{total_exp_questions}", font=('Helvetica', 18, 'bold'), background='gray')
exp1_label1 = tk.Label(root, text="Please adjust the right side of the pizza until you feel the left and right sides are equal in size\nThen click the submit button.",  font=('Helvetica', 18, 'bold'),background='gray')
exp1_label2 = tk.Label(root, text="Please adjust the right side of the white plate\nuntil you feel the left and right sides are equal in size.",  font=('Helvetica', 18, 'bold'),background='gray')
exp1_label3 = tk.Label(root, text="Please adjust the right side of the item\nuntil you feel the left and right sides are equal in size.",  font=('Helvetica', 18, 'bold'),background='gray')

description2 = tk.Label(root,text="This is the experiment2\n\n\
In this experiment you can freely drag the image \n\n\
You need to sort the cookies according to their size.\n\n\
The smallest cookie needs to be sorted to the far left\n\n\
the largest cookie needs to be sorted to the far right.\n\n\
", font=('Helvetica', 16,'bold'), justify=tk.LEFT, wraplength=1050,bg='gray')
exp2_label = tk.Label(root, text="Please feel free to drag.\nSort the following three groups so that the smallest biscuit is on the far left and the largest on the far right.",  font=('Helvetica', 18, 'bold'),background='gray')
next_button2 = tk.Button(root, text="next", command=nextexp2,highlightbackground="gray")
exp2_current_path_index = 0
global_image_order = []
exp2_prev_x, exp2_prev_y = {}, {}
exp2_button = tk.Button(root, text="submit", command=exp2_on_submit,highlightbackground="gray")

exp3_canvas_index=0
selected_option = []
description3 = tk.Label(root,text="This is the experiment3\n\n\
You can click on the food in the middle to indicate which food looks bigger \n\n\
If you think the size is the same, you can click the button below\n\n\
", font=('Helvetica', 16,'bold'), justify=tk.LEFT, wraplength=1050,bg='gray')
exp3_label = tk.Label(root, text="Please click on the food that you think looks bigger.\nIf you think it's the same, click the button below.",  font=('Helvetica', 18, 'bold'),background='gray')
next_button3 = tk.Button(root, text="next", command=nextexp3,highlightbackground="gray")


experiment0_queries()
root.mainloop()

