import streamlit as st
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
    
    # หน้าต่างกรอกชื่อและเลือกสถานะ
    employee_name = st.text_input("ชื่อ-นามสกุล พนักงาน:")
    status = st.selectbox("สถานะการเข้างาน:", ["เข้างานปกติ", "ออกงาน", "สาย", "ปฏิบัติงานนอกสถานที่"])
    
    if employee_name.strip() != "":
        # โครงสร้างลิงก์สำหรับเปิดหน้า Google Form และกรอกข้อมูลอัตโนมัติ
        base_url = https://docs.google.com/spreadsheets/d/1UgK4BMwkMbAY7ZThP8d7NjK1l9Ye-NgZZqnlCRvmg-M/edit?usp=sharing
        
        final_link = (
            f"{base_url}?usp=pp_url"
            f"&entry.1478156918={employee_name}"
            f"&entry.1773524848={status}"
            f"&entry.2024499584={lat}"
            f"&entry.203663662={lon}"
        )
        
        st.write("---")
        st.info("กรอกข้อมูลครบถ้วนแล้ว โปรดคลิกปุ่มด้านล่างเพื่อส่งข้อมูลความปลอดภัย")
        
        # ใช้คำสั่งมาตรฐานของ Streamlit ในการเปิดลิงก์ภายนอกแบบปลอดภัย
        st.link_button(f"คลิกที่นี่เพื่อกด 'ส่ง (Submit)' บันทึกเวลาสำหรับ {employee_name}", final_link, type="primary", use_container_width=True)
    else:
        st.warning("⚠️ กรุณาพิมพ์ชื่อ-นามสกุล ของท่านเพื่อให้ปุ่มส่งข้อมูลทำงาน")
else:
    st.warning("⏳ กำลังค้นหาพิกัด GPS... กรุณากด 'อนุญาต/Allow' ให้เว็บเข้าถึงสิทธิ์ตำแหน่งที่ตั้ง")
