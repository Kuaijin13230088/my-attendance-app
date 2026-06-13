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
    
    # ฟอร์มกรอกชื่อและเลือกสถานะบนหน้าเว็บ
    employee_name = st.text_input("ชื่อ-นามสกุล พนักงาน:")
    status = st.selectbox("สถานะการเข้างาน:", ["เข้างานปกติ", "ออกงาน", "สาย", "ปฏิบัติงานนอกสถานที่"])
    
    if st.button("ตกลง และส่งข้อมูลลงเวลา"):
        if employee_name.strip() == "":
            st.error("❌ กรุณากรอกชื่อ-นามสกุลก่อนทำรายการ")
        else:
            # สร้างลิงก์ด่วนส่งไปยัง Google Form พร้อมกรอกข้อมูลให้อัตโนมัติ (Pre-filled Link)
            # ดึงรหัสฟอร์มและรหัส entry จากรูปหน้าจอเดิมของคุณมาใส่ให้ถูกต้องเรียบร้อยแล้ว
            base_url = "https://google.com"
            
            final_link = (
                f"{base_url}?usp=pp_url"
                f"&entry.1478156918={employee_name}"
                f"&entry.1773524848={status}"
                f"&entry.2024499584={lat}"
                f"&entry.203663662={lon}"
            )
            
            st.info("ระบบกำลังพาท่านไปส่งข้อมูลความปลอดภัย...")
            # แสดงปุ่มให้พนักงานกดเพื่อยืนยันส่งข้อมูลเข้ากูเกิลสเปรดชีต
            st.markdown(f' <a href="{final_link}" target="_blank" style="display: inline-block; padding: 12px 24px; background-color: #00CC66; color: white; text-align: center; text-decoration: none; font-size: 18px; border-radius: 8px; font-weight: bold; width: 100%;">คลิกที่นี่เพื่อกด "ส่ง (Submit)" บันทึกเวลา</a>', unsafe_allow_html=True)
else:
    st.warning("⏳ กำลังค้นหาพิกัด GPS... กรุณากด 'อนุญาต/Allow' ให้เว็บเข้าถึงสิทธิ์ตำแหน่งที่ตั้ง")
