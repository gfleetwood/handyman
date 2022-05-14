from google.cloud import vision

def detect_text(im):
  """Detects text."""

  # from skimage.morphology import binary_opening
  #letter = rgb2gray(letter_square)
  #letter = binary_opening(letter*(letter > .8)*(letter > .9)*(letter > .95))
  #letter_ocr = detect_text(letter).lower()

  client = vision.ImageAnnotatorClient()
  image = vision.Image(content = np_img_to_bytes(im))
  response = client.text_detection(image = image)
  texts = response.text_annotations
  result = texts[0].description.replace("\n", "").replace(" ", "")
  if response.error.message: raise Exception('{}\nError: '.format(response.error.message))

  return(result)
