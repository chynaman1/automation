from robocorp.tasks import task
from robocorp import browser
from robocorp import vault
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from fpdf import FPDF
import csv
import io
import requests
import os
import zipfile
import time







@task

def minimal_task():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    close_modal()
    fill()
    
    
def store_receipt_as_pdf(order_number):
  
  page=browser.goto('https://robotsparebinindustries.com/#/robot-order')
  list_file = page.locator("#robot-preview-image").screenshot()
  receipt= page.locator("#receipt").inner_html()
  s=FPDF()
  s.add_page()
  s.set_font('helvetica', size=12)
  s.write_html(receipt)
  s.image(list_file,h=100,)
  s.output("output/receipt/"+order_number+".pdf")
  y=s.output("output/receipt/"+order_number+".pdf")
  zip(order_number)
  return y

  
  

  
  #DocumentKeywords.html_to_pdf(self=DocumentKeywords,content=receipt,output_path="output/"+order_number+".pdf")
  
  


# def zip(number):
   
   
#    with zipfile.ZipFile("output/receipt/robot_files.zip", mode="w") as archive:
#     for filename in number :
#      archive.write(filename)
#      return filename
 

     
  
def get_orders(ct):
  
 
 url = 'https://robotsparebinindustries.com/orders.csv'
 r = requests.get(url)
 buff = io.StringIO(r.text)
 dr = csv.DictReader(buff )
 for n,row in enumerate(dr):
     if n == ct :
         o=row['Order number']
         l=row['Legs']
         a=row['Address']
         b=row['Body']
         h=row['Head']
         return o,h,b,l,a

       

def close_modal():
 page=browser.goto('https://robotsparebinindustries.com/#/robot-order')
 page.locator(".btn-dark").click()
 fill()
 
 
 
    
def fill():
 
 s= 0

 while True:
  t=get_orders(s)
  page=browser.goto('https://robotsparebinindustries.com/#/robot-order')
  head =t[1]
  match head:
    case 1:
      head ='Roll-a-thor head'
    case 2:
      head = 'Peanut crusher head'
    case 3:
      head ='D.A.V.E head'
    case 4:
      head ='Andy Roid head'
    case 5:
      head ='Spanner mate head'
    case 6:
      head ='Drillbit 2000 head'
      break
      
  body =t[2]
  match body:
   case 1 :
     body=1
   case 2 :
     body =2
   case 3:
     body =3
   case 4:
    body =4
   case 5:
    body=5
   case 6:
     body=6
     
  legs =t[3]
  match legs:
   case 1 :
     legs=1
   case 2 :
     legs =2
   case 3:
     legs =3
   case 4:
    legs =4
   case 5:
    legs=5
   case 6:
    legs=6
     

  s +=1
  
  if s!=20:
   page.locator("#id-body-"+body+"").click()
   page.select_option("#head",head )
   page.fill("#address", t[4].__str__())
   page.locator("xpath=//div[3]/input").fill(legs)
   page.locator("#preview").click()
   page.locator("#order").click()
   store_receipt_as_pdf(t[0])
   page.locator("#order-another").click()
   page.locator(".btn-dark").click()
   
  elif s==20:
   break
  

  
  
  
  

  
  

 
  