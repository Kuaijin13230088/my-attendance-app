pythonimport streamlit as st
import datetime
import requests
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="ระบบลงเวลาทำงาน", page_icon="📱", layout="centered")

st.title("📱 ระบบลงเวลาทำงานนอกสถานที่")
st.write("โปรดเปิด GPS บนมือถือของคุณก่อนกดบันทึก")

# ดึงพิกัด GPS อัตโนมัติจากมือถือพนักงาน
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
                
                # ------------------------------------------------------------------
                # ส่วนส่งข้อมูลเข้า Google Sheets ผ่านสะพาน Google Form
                # ให้แทนที่รหัส FORM_URL และตัวเลข entry ด้วยรหัสที่คุณได้จากขั้นตอนที่ 2
                # ------------------------------------------------------------------
                FORM_URL = "https://google.comี่ยนเป็นรหัสฟอร์มของคุณ/formResponse"
                
                form_data = {
                    "entry.111111111": employee_name,  # เปลี่ยนเลขให้ตรงกับช่องชื่อพนักงาน
                    "entry.222222222": status,         # เปลี่ยนเลขให้ตรงกับช่องสถานะ
                    "entry.333333333": str(lat),       # เปลี่ยนเลขให้ตรงกับช่องละติจูด
                    "entry.444444444": str(lon),       # เปลี่ยนเลขให้ตรงกับช่องลองจิจูด
                    "entry.555555555": current_time    # เปลี่ยนเลขให้ตรงกับช่องเวลาบันทึก
                }
                
                try:
                    # ยิงข้อมูลเบื้องหลังโดยที่พนักงานไม่เห็นหน้าฟอร์ม
                    response = requests.post(FORM_URL, data=form_data)
                    if response.status_code == 200:
                        st.balloons()
                        st.success(f"🎉 บันทึกสำเร็จ: {employee_name} ({status}) เรียบร้อยแล้ว!")
                    else:
                        st.error("เกิดข้อผิดพลาดในการส่งข้อมูล กรุณาลองใหม่อีกครั้ง")
                except Exception as e:
                    st.error("ไม่สามารถเชื่อมต่อระบบฐานข้อมูลได้")
else:
    st.warning("⏳ กำลังค้นหาพิกัด GPS... กรุณากด 'อนุญาต/Allow' ให้เว็บเข้าถึงสิทธิ์ตำแหน่งที่ตั้ง")
