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
            