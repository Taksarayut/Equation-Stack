import math

e = math.e
π = math.pi

def is_float(string):
   try:
      float(string)
      return True
   except ValueError:
      return False
   
def replace_trigometry(text, angle_mode): # Trigonometry conversion
   
   sin_num_brackets = {}
   cos_num_brackets = {}
   tan_num_brackets = {}
   csc_num_brackets = {} 
   sec_num_brackets = {} 
   cot_num_brackets = {}

   func_and_temp_list = {"sin(" : sin_num_brackets, "cos(" : cos_num_brackets, "tan(" : tan_num_brackets,
                     "csc(" : csc_num_brackets, "sec(" : sec_num_brackets, "cot(" : cot_num_brackets}

   def trigon_func_num_extract(list, index, func, value_list, angle_mode):

      if list[index:index+4] == func:
         stop = list.find(")", index)
         extracted_num = list[index+4: stop]
         # Assign values to their extracted numbers
         if angle_mode == "Degree":
            value_list[extracted_num] = math.radians(eval(extracted_num))
         elif angle_mode == "Radian":
            value_list[extracted_num] = eval(extracted_num) 

   for i in range(len(text)):
      for function in func_and_temp_list:
         trigon_func_num_extract(text, i, function, func_and_temp_list[function], angle_mode)
   try:
      for value in sin_num_brackets:
         text = text.replace(f"sin({value})", str(math.sin(sin_num_brackets[value])))
      for value in cos_num_brackets:
         text = text.replace(f"cos({value})", str(math.cos(cos_num_brackets[value])))
      for value in tan_num_brackets:
         sin_value = math.sin(tan_num_brackets[value])
         cos_value = math.cos(tan_num_brackets[value])
         if round(cos_value, 15) != 0:
            tan_value = sin_value * 1 / cos_value
            text = text.replace(f"tan({value})", str(tan_value))
         else:
            math.cos(tan_num_brackets[value])
            raise ZeroDivisionError
      for value in csc_num_brackets:
         if round(math.sin(csc_num_brackets[value]), 15) != 0:
            csc_result = 1/math.sin(csc_num_brackets[value])
            text = text.replace(f"csc({value})", str(csc_result))
         else:
            raise ZeroDivisionError
      for value in sec_num_brackets:
         if round(math.cos(sec_num_brackets[value]), 15) != 0:
            sec_result = 1/math.cos(sec_num_brackets[value])
            text = text.replace(f"sec({value})", str(sec_result))
         else: 
            raise ZeroDivisionError
      for value in cot_num_brackets:
         if round(math.tan(cot_num_brackets[value]), 15) != 0:
            cot_result = 1/math.tan(cot_num_brackets[value])
            text = text.replace(f"cot({value})", str(cot_result))
         else:
            raise ZeroDivisionError

   except ZeroDivisionError:
      return "ZeroDivisionError"

   result = text
   return result

def replace_polar(text, angle_mode): #Convert polar form into complex

   polar = [] # list for collecting magnitudes and phases
   magnitude = []

   # Iterate over the string
   for i in range(len(text)):
      if text[i] == '∠':

         angle_index = i # Mark the "∠" position

         #Obtain the magnitude
         for j in range(angle_index - 1, -1, -1):  # Iterate backward from "∠" position
            if is_float(text[j]) or text[j] in [".", "π", "e"]:  # Check if character is part of a float
               magnitude = text[j:i]  # Add the character to the magnitude string
            else:
               break 

         #Obtain the angle in the brackets
         stop = text.find("]", i)
         angle = text[i+2:stop]
         # Record the magnitude and angle
         polar.append((magnitude, angle)) 
         
   for magnitude, angle in polar:

      if angle_mode == "Degree":
         real_part = eval(magnitude) * math.cos(math.radians(eval(angle)))
         imaginary_part = eval(magnitude) * math.sin(math.radians(eval(angle)))

      elif angle_mode == "Radian":
         real_part = eval(magnitude) * math.cos(eval(angle))
         imaginary_part = eval(magnitude) * math.sin(eval(angle))

      value = complex(real_part, imaginary_part)
      # Replace polar form complex with its value
      text = text.replace(f"{magnitude}∠[{angle}]", str(value))

   result = text
   return result

def replace_single_j(text): # Check for single j's

   def is_empty(list, index):
      try:
         list[index]
      except IndexError:
         return True

   equation =[]
   for letter in text:
      equation.append(letter)

   for index, element in enumerate(equation):
      if element == "j": # Check j only
            #j alone
            if len(equation) == 1 and is_empty(equation, index+1):
               equation[index] = "1j"
            # j on the far left
            elif index == 0:
               equation[index] = "1j"
            # any j's with no float in front of them
            elif is_float(equation[index-1]) == False:
               equation[index] = "1j"
            # any j's with openation in front of them (e.g -j, *j)
            elif equation[index-1] in ["+" ,"-", "*", "/"]:
               equation[index] = "1j"

   result = "".join(equation)
   return result

def replace_log(text): #Replace log with their values
   log_and_base = []
   for i in range(len(text)):
      if text[i:i+4] == "log[":
         stop = text.find("]", i)
         value = text[i+4:stop]
         log_and_base.append(value)
   try:
      for set in log_and_base:
         if "," in set: # Base defined
            x, base = set.split(",")
            if eval(x) == 0 or eval(base) == 0:
               raise Exception
            else:
               log_value = math.log(eval(x), eval(base))
               text = text.replace(f"log[{set}]", str(f"{log_value}"))
         else: #Base undefined
            if eval(set) != 0:
               text = text.replace(f"log[{set}]", str(math.log(eval(set), 10)))
            else:
               raise Exception
               
      result = text
      return result
   except Exception:
      return "log_invalid"

def string_to_complex(text, angle_mode):
   try:
      if replace_trigometry(text, angle_mode) != "ZeroDivisionError":
         text = replace_trigometry(text, angle_mode)
      else:
         return "Math Error"
      if replace_log(text) != "log_invalid":
         text = replace_log(text)
      else:
         return "Math Error"
      text = replace_polar(text, angle_mode)
      text = replace_single_j(text)
      return eval(text)
   except (NameError, SyntaxError):
      return "invalid"
   except ZeroDivisionError:
      return "Math Error"