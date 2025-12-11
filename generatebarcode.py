from barcode.codex import Code128
from barcode.writer import ImageWriter
def genarate_id(nr_L: int)->str:
    return f"S{nr_L:06d}"
def generate_book_id(nr_L: int)-> str:
    return f"B{nr_L:06d}"

def genarate_barcode(book_id:str):
    return Code128(book_id,writer=ImageWriter())
def generiere_studen_barcode(student_id:int)-> str:
    return Code128(student_id, writer=ImageWriter())
    
def save_barcodebild(barcode_obj,dateifad:str):
    return barcode_obj.save(dateifad)
def validify_barcode(barcode_text:str)-> bool:
    if len(barcode_text)== 7 and barcode_text[0] in ["S","B"]:
        try: 
            int(barcode_text[1:])
            return True
        except ValueError:
            return False
    return False

if __name__== "__main__":
    student_id=genarate_id(1)
    book_code=generate_book_id(41)
                               
    student_barcode=generiere_studen_barcode(student_id)
    book_barcode=genarate_barcode(book_code)
    save_barcodebild(student_barcode,"student_barcode")
    save_barcodebild(book_barcode,"book_barcode")
    
print (validify_barcode("S000001"))
print (validify_barcode("B000001"))
print (validify_barcode("X1233456"))
print(book_barcode)
print(student_barcode)

entry=input("Barcode scan: ").strip()
if validify_barcode(entry):
    print(f"barcode identified:{entry}")
else:
    print(f"unvalid barcode!")
    
from PIL import Image

File_name=save_barcodebild(book_barcode,book_code)
img=Image.open(File_name)
img.show()



