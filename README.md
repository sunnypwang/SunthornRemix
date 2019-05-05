# SunthornRemix
## โมเดลแต่งกลอนสุภาพ (Thai Poem Generator)
NLP Course Project 2018/2 Chulalongkorn University

## Requirements
- Python 3
- Keras
- Tensorflow
- Flask
- Pythainlp
- Numpy

## Installation
1. git clone this repository
2. In the case you want to run backend server on remote host, change the IP Address in `static/js/app.js` to match your remote host address (Default is localhost)
3. Run flask with
```
python main.py
```
4. Go to `http://<IP_ADDRESS>:3000` on web browser
5. Enter the starting word or phrase
6. Customize generating method
7. Click the "แต่ง" button

## วิธีการติดตั้ง
1. ทำการ git clone repository นี้
2. กรณีที่ต้องการรัน backend server บน remote host ให้แก้ url ใน `static/js/app.js` เป็น IP Address ของ host ที่ต้องการ (default คือ localhost)
3. รัน flask ด้วยคำสั่ง 
```
python main.py
```
4. ไปที่ `http://<IP_ADDRESS>:3000` บน web browser
5. ใส่คำหรือวลีที่ต้องการใช้เป็นคำเริ่มต้น
6. ปรับตั้งค่าวิธีการแต่งกลอน
7. กดคำว่า "แต่ง"

## การตั้งค่าวิธีการแต่งกลอน
### ความยาว
สามารถเลือกได้ว่าจะให้โมเดลแต่งกลอน 1 วรรค หรือครบ 4 วรรค (1 บท) โดยการแต่ง 1 บทจะใช้เวลามากกว่า
### รูปแบบอัลกอริทึม
สามารถเลือกอัลกอริทึมในการเลือกคำถัดไปที่ใช้ ได้แก่ Greedy, Beam Search และ Temperature Greedy
### ลักษณะการประพันธ์
สามารถเลือกใช้โมเดลที่เรียนรู้จากบทประพันธ์ของสุนทรภู่ท่านเดียว หรือจากหลายๆท่านผสมผสานกัน โดยโมเดลที่เรียนรู้จากบทประพันธ์ของหลายๆท่านผสมผสานกัน จะมีจำนวนคำศัพท์มากกว่า
