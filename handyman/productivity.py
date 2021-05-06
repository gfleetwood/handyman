def compress_pdf(input_path, output_path):

  template = "gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH  -dQUIET -sOutputFile={} {}"
  os.system(template.format(output_path, input_path))

  return(1)

def password_generator(num_words = 4):

  template = 'echo $(grep "^[^\']\{3,5\}$" /usr/share/dict/words|shuf -n{})'
  os.system(template.format(num_words))

  return(1)
