class Ai_analyze:
    def __init__(self):
        ...
    def analyze(self, image):
        try:
            from ultralytics import YOLO

            model_path = "model/yolov8n-cls.pt"
            model = YOLO(model_path)
            results = model(image)
            for result in results:
                id = result.probs.top1
                name = result.names[id]
            return name
        except:
            return ['??? - Something is wrong!']
            
            
def calculate_BMR(gender, height, weight, age):
    result = (10*weight) + (6.25*height) - (5*age)
    if gender=='male':
        result += 5 
    elif gender=='female':
        result -= 161 
    return result
