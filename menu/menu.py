from zoneinfo import available_timezones
import pygame 

            


MENU_JSON = {
    "name" : "Menu",
    "nodeType": "Menu",
    "nodes" :[
        {   
            "name" : "Start",
            "nodeType": "button",
            "nodes" : []
        },
        {   
            "name" : "Options",
            "nodeType": "Menu",
            "nodes" : [
                {   
                    "name" : "Volume",
                    "nodeType": "Slider",
                    "maxValue" : 20,
                    "value": 10,
                    "function": lambda x: print(x)
                    # "nodes" : []
                },
                {   
                    "name" : "Music",
                    "nodeType": "Turner",
                    "value": 0,
                    "values": ["hello", "my", "friend"],
                    "function": lambda x: print(x)
                    # "nodes" : []
                },
                {   
                    "name" : "Credits",
                    "nodeType": "Menu",
                    
                    "nodes" : [
                                    {   
                                "name" : "Made by Sasha and Petya",
                                "nodeType": "Menu",
                                "nodes" : []
                            }
                    ]
                }
            ]
        },
        {   
            "name" : "Credits",
            "nodeType": "Text",
            "text" : "Hello",
            "nodes" : []
        }
    ]
}

class FreeMenu():
    def __init__(self, menu_json, DISPLAY_W, DISPLAY_H):
        self.current_path = []
        self.menu_json = menu_json
        self.current_json = self.menu_json
        self.run_display = True
        self.playing = True
        self.offset = -100
        self.state = "Start"
        self.num_item = 0
        self.font_name = "./COMIC.TTF"
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.display_w, self.display_h = DISPLAY_W, DISPLAY_H
        self.display = pygame.Surface((self.display_w, self.display_h))
        self.mid_w, self.mid_h = self.display_w // 2, self.display_h // 2 
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.BLACK, self.WHITE, self.GRAY = (0,0,0), (255,255,255), (229, 229, 229)
        self.window = pygame.display.set_mode((self.display_w, self.display_h))
        self.current_header = self.menu_json["name"]
        self.left_edge = self.display_w / 2
        self.available_height = self.display_h / 2 + 20
        self.size_between_elements = self.available_height / len(self.current_json)

    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False

    def display_menu(self):
        self.run_display = True 
        while self.run_display:
            self.check_events()
            self.check_input()
            self.display.fill(self.GRAY)
            self.draw_text(self.current_header, 20, self.display_w / 2, self.display_h / 2 - 40)
            
            for i, element in enumerate(self.current_json["nodes"]):
                if element["nodeType"] == "Turner":
                    self.draw_text(element["name"] + ":{}".format(element["values"][element["value"]]), 20, self.left_edge, self.display_h / 2 + self.size_between_elements * i)
                elif element["nodeType"] == "Slider":
                    self.draw_text(element["name"] + ":{}".format("X" * element["value"]), 20, self.left_edge, self.display_h / 2 + self.size_between_elements * i)
                else:
                    self.draw_text(element["name"], 20, self.left_edge, self.display_h / 2 + self.size_between_elements * i)
            # self.draw_text("Options", 20, self.optionsx, self.optionsy)
            # self.draw_text("Credits", 20, self.creditsx, self.creditsy)
            if len(self.current_json["nodes"])!=0:
                if (len(self.current_json["nodes"])) - 1 < self.num_item :
                    self.num_item = 0
                self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            if self.state == "Start":
                self.playing = True
            else:
                if self.current_json["nodes"][self.num_item]["nodeType"] == "Menu":
                    self.current_path.append(self.num_item)
                    self.current_json = self.current_json["nodes"][self.num_item]
                    self.current_header = self.current_json["name"]
                

        if self.BACK_KEY: 
            if len(self.current_path) != 0:
                menu_item = self.current_path.pop()
                self.current_json = self.menu_json
                for item in self.current_path:
                    self.current_json = self.current_json["nodes"][item]
                self.current_header = self.current_json["name"]
                # self.num_item = 0

        
        
            # to stop display menu
            # self.run_display = False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.BLACK)
        
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
    
    def move_cursor(self):
        # i = 0
        if (len(self.current_json["nodes"])) - 1 < self.num_item :
            self.num_item = 0
        if self.DOWN_KEY:
            self.num_item += 1 
            self.num_item = self.num_item % (len(self.current_json["nodes"]))
            i = self.num_item
            self.state = self.current_json["nodes"][self.num_item]["name"]
            self.draw_text("*", 20, self.left_edge, self.display_h / 2 + self.size_between_elements * self.num_item)
            self.cursor_rect.midtop = (self.left_edge + self.offset, self.display_h / 2 + self.size_between_elements * self.num_item)
        
        elif self.UP_KEY:
            self.num_item -= 1 
            if self.num_item < 0:
                self.num_item = (len(self.current_json["nodes"])) - 1
            i = self.num_item
            self.state = self.current_json["nodes"][self.num_item]["name"]
            self.draw_text("*", 20, self.left_edge, self.display_h / 2 + self.size_between_elements * self.num_item)
            self.cursor_rect.midtop = (self.left_edge + self.offset, self.display_h / 2 + self.size_between_elements * self.num_item)
        
        if self.LEFT_KEY: 
            if self.current_json["nodes"][self.num_item]["nodeType"] == "Slider":
                if self.current_json["nodes"][self.num_item]["value"] == 0:
                    self.current_json["nodes"][self.num_item]["value"] = self.current_json["nodes"][self.num_item]["maxValue"]
                else:
                    self.current_json["nodes"][self.num_item]["value"] -= 1
            elif self.current_json["nodes"][self.num_item]["nodeType"] == "Turner":  
                if self.current_json["nodes"][self.num_item]["value"] == 0:
                    self.current_json["nodes"][self.num_item]["value"] = len(self.current_json["nodes"][self.num_item]["values"]) - 1
                else:
                    self.current_json["nodes"][self.num_item]["value"] -= 1

        elif self.RIGHT_KEY: 
            if self.current_json["nodes"][self.num_item]["nodeType"] == "Slider":
                self.current_json["nodes"][self.num_item]["value"] += 1
                self.current_json["nodes"][self.num_item]["value"] = self.current_json["nodes"][self.num_item]["value"] % self.current_json["nodes"][self.num_item]["maxValue"]
            elif self.current_json["nodes"][self.num_item]["nodeType"] == "Turner":  
                self.current_json["nodes"][self.num_item]["value"] += 1
                self.current_json["nodes"][self.num_item]["value"] = self.current_json["nodes"][self.num_item]["value"] % len(self.current_json["nodes"][self.num_item]["values"])

    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_keys()

pygame.init()
menu = FreeMenu(MENU_JSON, 480, 270)

menu.display_menu()