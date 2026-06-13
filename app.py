pythonimport streamlit as st
import datetime
import requests
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="ระบบลงเวลาทำงาน", page_icon="📱", layout="centered")

st.title("📱 ระบบลงเวลาทำงานนอกสถานที่")
st.write("โปรดเปิด GPS บนมือถือของคุณก่อนกดบันทึก")

# ระบบค้นหาพิกัด GPS จากมือถือพนักงานอัตโนมัติ
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    st.success(f"📍 ตรวจพบพิกัดของคุณแล้ว (Lat: {lat}, Lon: {lon})")
    
    with st.form("attendance_form"):
        employee_name = st.text_input("ชื่อ-นามสกุล พนักงาน:")
        status = st.selectbox("สถานะการเข้างาน:", ["เข้างานปกติ", "ออกงาน", "สาย", "ปฏิบัติงานนอกสถานที่"])
        submit_button = st.form_submit_button(label="กดบันทึกเวลาทำงาน")
        
        if submit_button:
            if employee_name.strip() == "":
                st.error("❌ กรุณากรอกชื่อ-นามสกุลก่อนบันทึก")
            else:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # ลิงก์ส่งข้อมูลจริงของ Google Form
                FORM_URL = "https://google.com"
                
                # กำหนดข้อมูลที่จะส่ง (ส่งเฉพาะค่าหลัก 4 ค่า เพื่อลดโอกาสเกิดข้อผิดพลาดของรหัสตัวสุดท้าย)
                form_data = {
                    "entry.1478156918": employee_name,  # ช่องชื่อพนักงาน
                    "entry.1773524848": status,         # ช่องสถานะ
                    "entry.2024499584": str(lat),       # ช่องละติจูด
                    "entry.203663662": str(lon)         # ช่องลองจิจูด
                }
                
                try:
                    # คำสั่งส่งข้อมูลไปที่กูเกิลฟอร์ม
                    response = requests.post(FORM_URL, data=form_data)
                    # ตรวจสอบสถานะการส่ง (Google Form จะยอมรับค่าหากยิงสำเร็จ)
                    if response.status_code == 200 or "formResponse" in response.url:
                        st.balloons()
                        st.success(f"🎉 บันทึกสำเร็จ: {employee_name} ({status}) เรียบร้อยแล้ว!")
                    else:
                        st.error("เกิดข้อผิดพลาดในระบบจัดเก็บข้อมูล กรุณาลองใหม่อีกครั้ง")
                except Exception as e:
                    st.error("ไม่สามารถเชื่อมต่อระบบฐานข้อมูลได้")
else:
    st.warning("⏳ กำลังค้นหาพิกัด GPS... กรุณากด 'อนุญาต/Allow' ให้เว็บเข้าถึงสิทธิ์ตำแหน่งที่ตั้ง")
