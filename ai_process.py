class Ai_analyze:
    def __init__(self):
        pass
    def analyze(self, image):
        try:
            from deepface import DeepFace
            result = DeepFace.analyze(
            img_path = image, 
            actions = ['age'])
            return result[0]['age']
        except:
            return '??? (something is wrong! make sure your face is not covered)'
            
            
def calculate_BMR(gender, height, weight, age):
    result = (10*weight) + (6.25*height) - (5*age)
    if gender=='male':
        result += 5 
    elif gender=='female':
        result -= 161 
    return result
