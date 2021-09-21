from sys import argv
from .productivity import password_generator, compress_pdf, gpg_encrypt, gpg_decrypt
from fire import Fire

def main(func, file_path = None):

    func_mapping = {"pwd": password_generator, "compress": compress_pdf, "decrypt": gpg_decrypt, "encrypt": gpg_encrypt}
    func_to_run = func_mapping.get(func)
    _ = func() if file_path is None else func(file_path)

    return(True)

if __name__ == '__main__':
    Fire(main)
