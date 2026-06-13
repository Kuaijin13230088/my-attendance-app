import streamlit as st
import pandas as pd
import datetime
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="ระบบลงเวลาทำงาน", page_icon="📱", layout="centered")

st.title("📱 ระบบลงเวลาทำงานนอกสถานที่")
st.write("โปรดเปิด GPS บนมือถือของคุณก่อนกดบันทึก")

# 1. ใส่ลิงก์ Google Sheets ของคุณที่นี่ (เปลี่ยนแทนที่ลิงก์ตัวอย่างด้านล่างนี้)
# สำคัญ: ลิงก์ต้องลงท้ายด้วย /gviz/tq?tqx=out:csv เพื่อให้ Python อ่านเป็นตารางได้
SHEET_URL = https://docs.google.com/forms/d/e/1FAIpQLSdsto7t1acM3ZpqtSJ8NFW0tKu5fTooecWaBeOfPNSxfQLIHA/formResponse?usp=pp_url&entry.1478156918=AAA&entry.1773524848=BBB&entry.2024499584=CCC&entry.203663662=DDD&entry.1339819192=EEE

# 2. ฟังก์ชันส่งข้อมูลกลับไปบันทึกที่ Google Sheets (ผ่านระบบ Google Form หรือ Webhook อัตโนมัติ)
# ในขั้นตอนแรกนี้ ระบบจะแสดงหน้าตาให้พนักงานกรอกและดึง GPS ให้คุณดูก่อน
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
                st.balloons()
                st.success(f"🎉 บันทึกสำเร็จ: {employee_name} ({status}) เมื่อเวลา {current_time}")
                st.info(f"พิกัดที่บันทึก: {lat}, {lon}")
else:
    st.warning("⏳ กำลังค้นหาพิกัด GPS... กรุณากด 'อนุญาต/Allow' ให้เว็บเข้าถึงสิทธิ์ตำแหน่งที่ตั้ง")
